# 🧠 50 Real-World PySpark Scenario-Based Questions & Answers

---

### **1. How do you handle schema drift while reading multiple CSV files in a folder?**

**Scenario:** Some files contain extra or missing columns.

**Answer:**
Use `mergeSchema=True` while reading in Spark 3.x:

```python
df = spark.read.option("mergeSchema", "true").csv("path/to/folder", header=True, inferSchema=True)
```

Alternatively, define a **master schema** and cast columns manually to maintain consistency.

---

### **2. You’re reading JSON files from IoT devices where schema changes dynamically. How do you handle it?**

**Answer:**

* Use `schema_of_json` + `from_json()` to infer structure dynamically.
* Apply a **bronze-silver-gold** Delta architecture: store raw JSON in Bronze and parse incrementally in Silver.

```python
schema = spark.read.json(df.rdd.map(lambda r: r.value)).schema
parsed_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")
```

---

### **3. How to identify and remove duplicate records from a DataFrame based on multiple columns?**

**Answer:**

```python
deduped_df = df.dropDuplicates(["CustomerID", "TransactionDate"])
```

If you want the latest record:

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, desc

windowSpec = Window.partitionBy("CustomerID").orderBy(desc("TransactionDate"))
latest = df.withColumn("rn", row_number().over(windowSpec)).filter("rn = 1").drop("rn")
```

---

### **4. You have large input files (100 GB+). How do you optimize PySpark read performance?**

**Answer:**

* Use `spark.sql.files.maxPartitionBytes` to control partition size (e.g., 128MB).
* Repartition using `repartition()` or `coalesce()` wisely.
* Use **predicate pushdown** and **column pruning** with Parquet/Delta.
* Cache intermediate results when reused.

---

### **5. You need to join two very large DataFrames causing shuffling issues. How do you optimize?**

**Answer:**

* Use **broadcast joins** if one table is small enough:

```python
from pyspark.sql.functions import broadcast
df = large_df.join(broadcast(small_df), "key")
```

* Repartition both on join keys before joining.
* Avoid skew by salting keys (see next).

---

### **6. How to handle skewed data in joins?**

**Answer:**
Add random salts to join keys:

```python
from pyspark.sql.functions import rand, ceil
skewed = df1.withColumn("salt", ceil(rand() * 10))
df2_salted = df2.crossJoin(spark.range(1, 11).withColumnRenamed("id", "salt"))
joined = skewed.join(df2_salted, ["key", "salt"])
```

Then remove salt post-join.

---

### **7. How to detect anomalies (e.g., outliers) in transaction data using PySpark?**

**Answer:**
Use statistical thresholding:

```python
from pyspark.sql.functions import mean, stddev, col

stats = df.select(mean("amount").alias("mean"), stddev("amount").alias("std")).collect()[0]
outliers = df.filter((col("amount") > stats['mean'] + 3*stats['std']) | (col("amount") < stats['mean'] - 3*stats['std']))
```

---

### **8. You want to pivot monthly sales data with dynamic months. How?**

**Answer:**

```python
pivot_df = df.groupBy("ProductID").pivot("Month").agg(sum("Sales"))
```

If months vary dynamically, Spark handles it automatically at runtime.

---

### **9. How to perform incremental load from a source folder (only new files)?**

**Answer:**
Track processed files in a Delta table or checkpoint location:

```python
processed_files = spark.read.table("metadata.processed_files")
new_files = [f for f in all_files if f not in processed_files]
```

Alternatively, use **Auto Loader** in Databricks:

```python
spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv").load("path")
```

---

### **10. How do you write DataFrame to partitioned Parquet efficiently?**

**Answer:**

```python
df.write.mode("overwrite").partitionBy("year", "month").parquet("/mnt/data/sales/")
```

Use dynamic partition overwrite mode:

```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
```

---

### **11. How to find top N records per group (e.g., top 3 sales per region)?**

**Answer:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, desc

windowSpec = Window.partitionBy("region").orderBy(desc("sales"))
top3 = df.withColumn("rank", rank().over(windowSpec)).filter("rank <= 3")
```

---

### **12. You have nested JSON columns. How do you flatten them?**

**Answer:**
Use `selectExpr` or `explode`:

```python
df.select("id", "user.name", "user.email", "user.location.city")
```

For arrays:

```python
df.withColumn("user", explode("users")).select("user.*")
```

---

### **13. You need to calculate running totals per customer.**

**Answer:**

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import sum

windowSpec = Window.partitionBy("CustomerID").orderBy("TransactionDate").rowsBetween(Window.unboundedPreceding, 0)
df.withColumn("running_total", sum("amount").over(windowSpec))
```

---

### **14. How to handle null or corrupt records when reading files?**

**Answer:**

```python
df = spark.read.option("mode", "DROPMALFORMED").json("path")
```

Other modes: `PERMISSIVE`, `FAILFAST`.

---

### **15. How to handle small files problem in PySpark?**

**Answer:**

* Use `repartition()` before writing.
* Combine files periodically.

```python
df.coalesce(1).write.parquet("path")
```

* Use **Auto Loader** with `trigger(once=True)` for continuous merging.

---

### **16. How to perform data validation (e.g., negative sales, missing ID)?**

**Answer:**

```python
invalid = df.filter("sales < 0 OR id IS NULL")
valid = df.subtract(invalid)
```

Or use Delta **EXPECTATIONS** in Databricks (Delta 3.0+).

---

### **17. How to generate surrogate keys in PySpark?**

**Answer:**

```python
from pyspark.sql.functions import monotonically_increasing_id
df = df.withColumn("surrogate_key", monotonically_increasing_id())
```

---

### **18. How to implement Slowly Changing Dimension (SCD Type 2)?**

**Answer:**
Join current data with historical table, compare columns, and insert new records with updated `EffectiveDate` and `IsCurrent`.
Delta merge example:

```python
target.alias("t").merge(
  source.alias("s"),
  "t.id = s.id"
).whenMatchedUpdate(set={"t.IsCurrent": "false"})\
 .whenNotMatchedInsert(values={"id": "s.id", "IsCurrent": "true"})\
 .execute()
```

---

### **19. How to read and transform large zipped files (e.g., CSV inside .zip)?**

**Answer:**
Use Python’s `zipfile` with Spark parallelism:

```python
import zipfile, io
from pyspark.sql import SparkSession

with zipfile.ZipFile("/mnt/data/file.zip") as z:
    with z.open("data.csv") as f:
        df = spark.read.csv(io.TextIOWrapper(f), header=True)
```

---

### **20. How do you perform audit logging in PySpark pipelines?**

**Answer:**
Maintain a metadata table:

```python
audit_df = spark.createDataFrame([(batch_id, datetime.now(), status)], ["batch_id", "timestamp", "status"])
audit_df.write.mode("append").saveAsTable("etl.audit_log")
```

---

### **21. How to detect duplicate file loads (same content but different name)?**

**Answer:**
Compute hash of file contents:

```python
from pyspark.sql.functions import sha2, concat_ws
df = df.withColumn("hash", sha2(concat_ws("", *df.columns), 256))
duplicates = df.groupBy("hash").count().filter("count > 1")
```

---

### **22. You want to dynamically rename all columns to lowercase.**

**Answer:**

```python
df = df.toDF(*[c.lower() for c in df.columns])
```

---

### **23. How to perform date difference between timestamp columns?**

**Answer:**

```python
from pyspark.sql.functions import datediff
df.withColumn("days_diff", datediff("end_date", "start_date"))
```

---

### **24. How to explode arrays and maintain parent-child relationship?**

**Answer:**

```python
df.withColumn("exploded", explode("items")).select("order_id", "exploded.*")
```

---

### **25. How do you debug slow PySpark jobs?**

**Answer:**

* Check **Spark UI** for shuffle size, skewed stages.
* Increase `spark.sql.shuffle.partitions`.
* Use `.explain(True)` to check query plan.
* Cache and persist heavy transformations.

---

### **26. You have 10 TB of logs; need to extract only lines containing “ERROR.”**

**Answer:**
Use RDD or DataFrame filter:

```python
logs = spark.read.text("path")
errors = logs.filter(logs.value.contains("ERROR"))
```

---

### **27. How to implement upsert (merge) in Delta Lake?**

**Answer:**

```python
from delta.tables import DeltaTable
deltaTable.alias("t").merge(source.alias("s"), "t.id = s.id")\
    .whenMatchedUpdateAll()\
    .whenNotMatchedInsertAll()\
    .execute()
```

---

### **28. How to read a file list from metadata and process each file dynamically?**

**Answer:**

```python
for f in file_list:
    df = spark.read.csv(f)
    process(df)
```

---

### **29. How to compute 7-day moving average per user?**

**Answer:**

```python
window = Window.partitionBy("user").orderBy("date").rowsBetween(-6, 0)
df.withColumn("moving_avg", avg("value").over(window))
```

---

### **30. How to mask PII data (email, phone)?**

**Answer:**

```python
from pyspark.sql.functions import regexp_replace
df = df.withColumn("email", regexp_replace("email", r"(^.).*(@.*)", r"\1*****\2"))
```

---

### **31. How to merge multiple DataFrames with same schema dynamically?**

**Answer:**

```python
from functools import reduce
df_merged = reduce(DataFrame.unionByName, df_list)
```

---

### **32. How to load data incrementally based on last modified timestamp?**

**Answer:**

```python
last_load = datetime.strptime(get_last_timestamp(), "%Y-%m-%d %H:%M:%S")
df = spark.read.option("modifiedAfter", last_load.isoformat()).parquet("path")
```

---

### **33. How to handle corrupted Parquet files?**

**Answer:**
Try reading with `ignoreCorruptFiles=true`:

```python
spark.read.option("ignoreCorruptFiles", "true").parquet("path")
```

---

### **34. How to calculate percent rank per group?**

**Answer:**

```python
from pyspark.sql.functions import percent_rank
df.withColumn("percent_rank", percent_rank().over(Window.partitionBy("dept").orderBy("salary")))
```

---

### **35. How to detect missing sequence numbers in time-series data?**

**Answer:**

```python
from pyspark.sql.functions import lag
window = Window.partitionBy("id").orderBy("timestamp")
df.withColumn("gap", col("timestamp") - lag("timestamp", 1).over(window))
```

---

### **36. How to union two DataFrames with different column sets?**

**Answer:**
Use `unionByName(allowMissingColumns=True)`.

---

### **37. How to validate column data types and auto-correct mismatches?**

**Answer:**
Compare with a reference schema and cast mismatched columns dynamically.

---

### **38. How to calculate data volume growth over time?**

**Answer:**
Aggregate record counts by `ingest_date`, then compare with previous using lag.

---

### **39. How to detect column drift between two DataFrames?**

**Answer:**

```python
set(df1.columns).symmetric_difference(set(df2.columns))
```

---

### **40. How to optimize wide transformations like groupBy and join?**

**Answer:**

* Use bucketing on join keys.
* Pre-partition on keys before wide transformations.
* Cache reused datasets.

---

### **41. How to compress Parquet output efficiently?**

**Answer:**

```python
spark.conf.set("spark.sql.parquet.compression.codec", "snappy")
```

---

### **42. How to capture rejected records (e.g., schema mismatch)?**

**Answer:**
Read as `PERMISSIVE` mode and access `_corrupt_record` column.

---

### **43. How to profile DataFrame columns (count, null %, distinct)?**

**Answer:**

```python
for col_name in df.columns:
    df.agg(count("*"), countDistinct(col_name), count(when(col(col_name).isNull(), col_name)))
```

---

### **44. How to detect changes between two datasets (delta comparison)?**

**Answer:**
Perform `exceptAll` or use `Delta Merge` to identify inserts/updates/deletes.

---

### **45. How to cache and uncache DataFrames efficiently?**

**Answer:**

```python
df.cache()
df.count()  # materialize
df.unpersist()
```

---

### **46. How to measure job execution time in PySpark?**

**Answer:**

```python
import time
start = time.time()
df.collect()
print("Duration:", time.time() - start)
```

---

### **47. How to manage broadcast timeout errors?**

**Answer:**
Increase:

```python
spark.conf.set("spark.sql.broadcastTimeout", 600)
```

Or disable broadcast with hint:

```python
df.join(other_df.hint("NO_BROADCAST"), "key")
```

---

### **48. How to checkpoint intermediate results in a long pipeline?**

**Answer:**

```python
spark.sparkContext.setCheckpointDir("/mnt/checkpoints")
df.checkpoint()
```

---

### **49. How to convert semi-structured logs to structured DataFrame efficiently?**

**Answer:**
Use regex or `from_json()` with inferred schema.

---

### **50. How to integrate PySpark with ADF or Databricks pipelines?**

**Answer:**

* Trigger PySpark notebooks using ADF Web Activity or Notebook Activity.
* Pass parameters via `dbutils.widgets`.
* Return success/failure status using notebook exit code.

---