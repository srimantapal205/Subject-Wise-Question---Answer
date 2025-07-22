# 𝐀𝐳𝐮𝐫𝐞 𝐃𝐚𝐭𝐚 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫 𝐈𝐧𝐭𝐞𝐫𝐯𝐢𝐞𝐰 𝐐𝐮𝐞𝐬𝐭𝐢𝐨𝐧𝐬

### 1. **What is your project architecture, and how do you get your data? How do you connect to the sources / where is your raw data stored?**

**Architecture:**
- **Data Sources:** SQL databases, REST APIs, cloud storage (Azure Blob / Data Lake).
- **Ingestion:** Azure Data Factory (ADF) pipelines.
- **Processing:** Azure Databricks using PySpark.
- **Storage:**
  - **Raw Data:** Stored in Azure Data Lake Gen2 in a "raw" container.
  - **Transformed Data:** Stored in "bronze", "silver", and "gold" layers using Delta Lake format.
- **Consumption:** Power BI connects to Gold layer for reporting.

**Connections:**
- ADF uses Linked Services to connect to sources (SQL DB, APIs, Blob, etc.).
- Databricks uses Spark connectors or mount points to access storage.

---

### 2. **Suppose there are 10 tables, I want to copy all with the same file name into a folder on cloud. Are you going to add 10 copy activities or what approach you will take and what are the activities you will use?**

**Efficient Approach:**
- Use **parameterized pipeline** with **ForEach** activity.
- Create a dataset with dynamic table name.
- Use a **Lookup** or **Get Metadata** activity to get list of tables.
- Inside the **ForEach**, use **Copy Activity** that dynamically sets source and sink file paths using parameters.

This avoids 10 separate activities and makes it scalable.

---

### 3. **What is the approach for incremental loading? How do you connect your SQL database from ADF?**

**Connection:**
- ADF connects using an **Azure SQL Database Linked Service**.
- Uses SQL authentication or managed identity.

**Incremental Loading:**
- Use a watermark column (like `LastModifiedDate` or `ID`).
- Store the last loaded value in **ADF pipeline parameters** or **Azure Table Storage**.
- In SQL source query:  
  
      SELECT * FROM Table WHERE LastModifiedDate > '@{pipeline().parameters.LastLoadedDate}'
  

---

### 4. **What approach will you follow to get the incremental data in the Delta table in Databricks?**

**Approach:**
- Maintain a **watermark value** (e.g., last updated timestamp or max ID).
- Query source for data greater than this watermark.
- Use `merge` or `upsert` logic to load into Delta table:

  python

      deltaTable.alias("target")\
      .merge(sourceDF.alias("source"), "target.id = source.id")\
      .whenMatchedUpdateAll()\
      .whenNotMatchedInsertAll().execute()
        

---

### 5. **There is a dataset in Databricks, how will you convert it to a list?**

If it's a single column:

python

      my_list = df.select("column_name").rdd.flatMap(lambda x: x).collect()


If it’s a row:

python

      my_list = df.collect()[0].asDict().values()


---

### 6. **What is repartition and coalesce? How have you implemented it in your project?**

- **repartition(n)**: Increases/decreases number of partitions by shuffling data.
- **coalesce(n)**: Decreases partitions without full shuffle (more efficient).

**Use Case:**
- After filtering/joining to reduce partitions before writing:

  python

        df.coalesce(1).write.mode("overwrite").parquet("path")
  
- Or to improve parallelism:

  python

        df.repartition(10)
  

---

### 7. **Where and how do you run your Databricks Notebooks?**

- Run via:
  - **Interactive UI** in Databricks workspace.
  - **ADF** using **Databricks Notebook activity**.
  - **Job scheduler** in Databricks for automated runs.
  - **REST API / CLI** for programmatic triggering.

---

### 8. **In the Delta table how will you check previous version data?**

Use **Delta Lake time travel**:

sql

      SELECT * FROM delta.`/path/to/table` VERSION AS OF 3

or


      SELECT * FROM delta.`/path/to/table` TIMESTAMP AS OF '2025-04-10T00:00:00Z'


---

### 9. **What approach will you take to do schema evolution?**

If using **merge** or **overwrite**:

python

      df.write.format("delta").option("mergeSchema", "true").mode("overwrite").save(path)


To enable auto schema evolution:

python

      spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")


---

### 10. **Performance Tuning Techniques in Spark**
- **Optimize shuffles**: Use `repartition()` wisely; minimize wide transformations.
- **Persist()/cache()**: Use when reusing intermediate results.
- **Broadcast joins**: Broadcast small dimension tables to avoid shuffle joins.
- **Explain plan**: Use `.explain()` to analyze the physical execution plan.

---

### 11. **Accumulator vs Broadcast Variables**
- **Accumulator**: Used for counters, sum, etc. Write-only from executors.
- **Broadcast**: Share small lookup datasets across nodes efficiently.

---

### 12. **SparkSession vs SparkContext**
| Feature        | SparkSession                         | SparkContext                     |
|----------------|--------------------------------------|----------------------------------|
| Purpose        | Unified entry point (DF, SQL, etc.)  | RDD-based operations             |
| Introduced in  | Spark 2.0                            | Spark 1.x                        |
| Example        | `SparkSession.builder.appName()`     | `SparkContext(conf)`            |

---

### 13. **Dataset vs DataFrame**
- **Dataset** (Scala/Java): Type-safe, compile-time checks.
- **DataFrame**: Untyped, row-based with schema.

---

### 14. **Spark Session Command**
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()
```

---

### 15. **Command to Read JSON Data**
```python
df = spark.read.option("multiline", "true").json("path/to/file.json")
```

---

### 16. **CSV Without Column Names/Schema**
```python
df = spark.read.option("header", "false").csv("path.csv")
```

---

### 17. **Find 3rd Highest Salary**
```sql
SELECT DISTINCT salary FROM employee ORDER BY salary DESC LIMIT 3

--OR

SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC OFFSET 2 ROWS FETCH NEXT 1 ROW ONLY;
```
---

### 18. **Employees Earning More Than Manager**
```sql
SELECT e.name FROM employee e JOIN employee m ON e.manager_id = m.id WHERE e.salary > m.salary

```

---

### 19. **Palindrome Check (PySpark UDF Example)**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

def is_palindrome(s):
    return s == s[::-1]

is_palindrome_udf = udf(is_palindrome, BooleanType())
df = df.withColumn("is_palindrome", is_palindrome_udf(df["column"]))
```

---

### 20. **Spark Submit Command**
```bash
spark-submit --class com.example.Main --master yarn /path/to/app.jar
```

---

### 21. **Memory Tuning**
- `--executor-memory 4G`
- Use `StorageLevel.MEMORY_AND_DISK`
- Tune GC with `spark.executor.extraJavaOptions`

---

### 22. **Created JARs**
> I created JARs using Maven for my Scala Spark jobs. Used `pom.xml` to manage dependencies and `spark-submit` to deploy.

---

### 23. **Worked with UDFs**
> Yes, I used UDFs in Python for data transformation like converting date formats, validating emails, or checking for palindromes.

---

### 24. **Dynamic Resource Allocation**
```bash
--conf spark.dynamicAllocation.enabled=true
--conf spark.dynamicAllocation.minExecutors=2
--conf spark.dynamicAllocation.maxExecutors=10
```

---

### 25. **Daily Data Volume**
> We processed ~1TB/day from various sources including system logs, e-commerce transactions, and IoT device data.

---

### 26. **DataFrame vs Dataset**

> DataFrame is untyped (runtime schema checks), Dataset is typed (compile-time checks, only in Scala/Java).

---

### 27. **Load CSV from HDFS**
```python
df = spark.read.csv("hdfs://namenode/path/file.csv", header=True, inferSchema=True)
```

---

### 28. **What is Multiline?**
> The `multiline` option is used when JSON records span multiple lines.

```python
spark.read.option("multiline", "true").json("path")
```

---

### 29. **No Column Names in CSV**
```python
df = spark.read.option("header", "false").csv("path.csv")
```

---

### 30. **Case Class and StructType Syntax**
**Scala:**
```scala
case class Person(name: String, age: Int)
val df = spark.read.as[Person]
```

**Python:**
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])
df = spark.read.schema(schema).csv("path")
```

---

### 31. **Partitioning vs Bucketing**
| Technique    | Partitioning                      | Bucketing                            |
|--------------|-----------------------------------|--------------------------------------|
| Based on     | Directory structure               | Hashing function                     |
| Performance  | Good for filtering                | Good for join optimization           |
| Use case     | Date-based queries                | Joining large datasets efficiently   |

---

### 32. **Closure Function**
> A closure captures variables from its outer scope. Spark sends the closure to executors, so variables must be serializable.

---

### 33. **Count of Alphabets in String (Python)**
```python
from collections import Counter

def count_alpha(s):
    return dict(Counter(filter(str.isalpha, s)))
```

---

### 34. **List vs Tuple**
| Feature      | List                          | Tuple                        |
|--------------|-------------------------------|------------------------------|
| Mutability   | Mutable                        | Immutable                    |
| Performance  | Slightly slower                | Faster                       |
| Syntax       | `[1, 2, 3]`                    | `(1, 2, 3)`                  |

---


### 35. **In ADF, what is the other way to get the incremental load without Watermark Columns?**

In **Azure Data Factory (ADF)**, if you want to implement **incremental load** without using **watermark columns** (like `LastModifiedDate` or `UpdatedDate`), there are **several alternative strategies**, depending on the data source and structure:

#### 🔁 1. **Change Data Capture (CDC)**
- **Applicable to**: Azure SQL DB, SQL Server, Synapse, Oracle (with log-based CDC), etc.
- ADF now **supports CDC natively**, enabling you to load **only the changed data** by tracking changes at the database engine level.
- Setup involves:
  - Enabling CDC on the source table.
  - Using the **"Change Data Capture" connector** in ADF.
- No need for watermark columns.

#### 🗃️ 2. **Delta Files / Partitioned Files in Blob/Data Lake**
- **Applicable to**: File-based sources like Azure Blob Storage, Data Lake, S3.
- If incoming files are **partitioned by date/time** (e.g., folder names like `/year=2025/month=04/day=23/`), you can use ADF to:
  - Read **only the new folders/files**.
  - Track previously processed partitions via **metadata table** or pipeline variables.
- This avoids scanning the entire dataset every time.

#### 🧾 3. **Using File Name/Metadata Tracking**
- **Track the file name** or **file properties** (e.g., creation timestamp) in a **lookup table**.
- Before each load:
  - Compare incoming files to the tracked ones.
  - Only ingest **new or updated** files.
- Update the tracking table after processing.

#### 🔄 4. **Hash Comparison or Checksum**
- Compute a **hash or checksum** (e.g., MD5) of each row or record.
- Compare current hash with stored hash (in staging or target).
- Only insert/update rows that have changed.
- Used when no timestamp is available and data volume is manageable.

#### 🧠 5. **Source-System Triggers or Flags**
- Some systems add a **status flag** (e.g., `IsProcessed`, `IsNew`, `SyncFlag`) to identify rows ready for load.
- ADF filters for `IsProcessed = false`, then updates the flag after successful load.


### 36. **How to run more than 100 pipelines at a time sequentially, with dependencies (one by one)?**

If you have **more than 100 pipelines** that need to be executed **sequentially** (i.e., one after another, in a specific order, with dependencies), you can **orchestrate them efficiently in Azure Data Factory** (ADF) using the following methods:

---

### ✅ **Recommended Approach: Use Master Pipeline with Execute Pipeline Activities**

You can create a **Master Pipeline** that calls other pipelines in sequence using the **"Execute Pipeline"** activity. Here's how to manage more than 100:



### 🛠️ **Step-by-Step Strategy**

#### 🔁 1. **Group Pipelines into Batches**
- Since ADF has a UI performance limit of ~40–50 activities per pipeline, **don’t put all 100+ pipelines in one single pipeline.**
- Group them into **batches of 20–30 pipelines per group**.
- Create **Batch Pipelines** like:
  - `BatchPipeline1` (calls `Pipeline001` to `Pipeline030`)
  - `BatchPipeline2` (calls `Pipeline031` to `Pipeline060`)
  - ... and so on.

#### 🧠 2. **Create a Master Orchestration Pipeline**
- This pipeline calls each **Batch Pipeline** one after another using **Execute Pipeline** activities.
- Ensure each `Execute Pipeline` activity is **chained via success dependency** (green arrow).

```plaintext
MasterPipeline
  └── ExecutePipeline (BatchPipeline1)
        └── ExecutePipeline (BatchPipeline2)
              └── ExecutePipeline (BatchPipeline3)
                    ...
```

#### ⛓️ 3. **Control Flow with Dependency Conditions**
- Each `Execute Pipeline` can be followed by success/failure paths if needed.
- You can also add error handling using **Try-Catch logic** with `If Condition` and `Until` activities for retries.



### ⚙️ Alternative Approaches

#### 🧾 1. **Use Metadata-Driven Execution**
- Store pipeline names in a **SQL Table** or **JSON config file**.
- Use a `ForEach` activity to loop through and call each pipeline one by one using a dynamic `Execute Pipeline` activity.

```json
[
  {"PipelineName": "Pipeline001"},
  {"PipelineName": "Pipeline002"},
  ...
]
```

- Inside `ForEach`, set **batch count = 1** to ensure **sequential execution**.


### 🧩 2. **Use Azure Data Factory REST API or Azure Functions**
- If you want external control, create an orchestration logic using **Azure Functions**, **PowerShell**, or **Logic Apps** to:
  - Call each pipeline using ADF REST API.
  - Wait for one pipeline to finish before calling the next.


### ✅ Best Practices

- **Limit pipeline nesting** to reduce complexity.
- Use **logging** and **error-handling pipelines** for production reliability.
- **Monitor** via ADF monitoring tab or **Log Analytics** if connected.

---

Great questions! Here's a comprehensive breakdown of each one:

---

### 37. **Explain the differences between RDDs, DataFrames, and Datasets in PySpark. When would you use each?**

| Feature         | RDD                            | DataFrame                            | Dataset (Scala/Java only)        |
|----------------|---------------------------------|--------------------------------------|----------------------------------|
| Abstraction     | Low-level                      | High-level (structured)              | High-level + Strongly typed      |
| Compile-time type safety | Yes                     | No                                   | Yes                              |
| Optimization   | No (manual optimization)        | Yes (Catalyst & Tungsten)            | Yes                              |
| Ease of use    | Less (more boilerplate)         | More (SQL-like API)                  | Medium (better than RDDs)        |
| Language Support | Python, Scala, Java           | Python, Scala, Java, R               | Scala and Java only              |

**Use cases:**
- **RDD**: Complex transformations, unstructured data.
- **DataFrame**: Structured data, ETL pipelines, SQL queries.
- **Dataset**: Strong typing + compile-time safety (Scala/Java only).

---

### 38. **How does PySpark handle lazy evaluation? Can you provide an example demonstrating this concept?**

PySpark transformations are lazy, meaning they’re not executed until an action is called.

**Example:**
```python
rdd = sc.textFile("data.txt")
words = rdd.flatMap(lambda x: x.split(" "))
wordPairs = words.map(lambda x: (x, 1))  # Lazy
counts = wordPairs.reduceByKey(lambda a, b: a + b)  # Still lazy
counts.collect()  # Triggers execution
```

Only when `collect()` is called does Spark build and execute the DAG.

---

### 39. **Describe the role of the Catalyst optimizer in PySpark. How does it enhance query execution?**

Catalyst is Spark SQL’s query optimizer. It improves performance by:
- Analyzing and optimizing logical and physical query plans.
- Applying rule-based transformations (e.g., constant folding, predicate pushdown).
- Reordering operations for optimal execution.

**Benefit:** Makes DataFrame and SQL operations significantly faster than RDDs.

---

### 40. **What are the various types of joins supported in PySpark? How do they differ in terms of performance and use cases?**

- **Inner Join**: Only matching keys.
- **Left/Right Outer Join**: Keeps all rows from one side, nulls for no matches.
- **Full Outer Join**: All records from both sides.
- **Left Semi Join**: Rows from left where matches exist on right.
- **Left Anti Join**: Rows from left where no match on right.
- **Cross Join**: Cartesian product (use with caution).

**Performance Tips**:
- Broadcast small tables for faster joins.
- Avoid shuffles when possible.

---

### 41. **How can you handle missing or null values in a PySpark DataFrame? What strategies are available?**

Common strategies:
```python
    df.dropna()                   # Drop rows with nulls
    df.fillna(0)                  # Replace nulls
    df.na.replace(...)            # Replace specific values
```

Approach depends on context—sometimes mean/median imputation is better than dropping.

---

### 42. **Explain the significance of partitioning in PySpark. How does it impact performance, and how do you implement it?**

Partitioning affects **parallelism** and **shuffling**.

**Benefits:**
- Reduces data movement.
- Improves task scheduling.

**Implementation:**
```python
df.repartition(10, "column")
df.coalesce(5)
```

Use `repartition()` when increasing partitions; `coalesce()` to reduce them efficiently.

---

### 43. **What is the difference between the `cache()` and `persist()` methods in PySpark? When would you use each?**

- `cache()` = shorthand for `persist(StorageLevel.MEMORY_AND_DISK)`
- `persist()` = allows other storage levels (e.g., disk-only)

Use `cache()` for small-to-medium datasets accessed repeatedly. Use `persist()` for large datasets or specific storage needs.

---

### 44. **How do you create and register a user-defined function (UDF) in PySpark? What are the performance considerations?**

```python
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType

    def upper_case(name):
        return name.upper()

    upper_udf = udf(upper_case, StringType())
    df.withColumn("upper_name", upper_udf(df["name"]))
```

**Performance Warning**: UDFs are black-box to Catalyst—avoid if possible. Use built-in functions or Pandas UDFs.

---

### 45. **Discuss the concept of shuffling in PySpark. How does it affect performance, and how can it be minimized?**

Shuffling = redistributing data across partitions, triggered by:
- Wide transformations (`groupByKey`, `reduceByKey`, `join`)
- Repartitioning

**Impact**: Slows down performance, increases network I/O.

**Minimize by**:
- Using `reduceByKey` instead of `groupByKey`
- Broadcasting smaller datasets
- Pre-partitioning data

---

### 46. **Describe a scenario where you had to optimize a PySpark job for performance. What steps did you take?**

**Example**: Job was slow due to large shuffle in join.

**Steps Taken**:
1. Used `broadcast()` for small dimension table.
2. Repartitioned large table by join key.
3. Cached intermediate result reused in multiple stages.
4. Used DataFrames instead of RDDs for Catalyst optimization.

Result: Reduced execution time by 70%.

---

### 47. **How do you read data from and write data to various file formats (e.g., CSV, Parquet, JSON) in PySpark?**

```python
    # CSV
    df = spark.read.csv("file.csv", header=True, inferSchema=True)
    df.write.csv("out.csv")

    # Parquet
    df = spark.read.parquet("file.parquet")
    df.write.parquet("out.parquet")

    # JSON
    df = spark.read.json("file.json")
    df.write.json("out.json")
```

Parquet is preferred for performance (columnar, compressed).

---
### 48. **Explain how you would perform aggregations in PySpark. What functions and methods are commonly used?**

```python
    from pyspark.sql.functions import count, avg, sum

    df.groupBy("category").agg(
        count("*").alias("cnt"),
        avg("price").alias("avg_price"),
        sum("sales").alias("total_sales")
    )
```

Also use `window()` for time-based aggregations.

---

### 49. **What are broadcast variables in PySpark? How do they help in improving the performance of join operations?**

Used to cache small lookup tables on all worker nodes to avoid data shuffling during joins.

```python
    from pyspark.sql.functions import broadcast
    df.join(broadcast(dim_table), "id")
```

Greatly improves performance for joins with small datasets.

---

### 50. **Describe the process of handling schema evolution in PySpark when dealing with changing data structures.**

For evolving schemas:
- Use Parquet/Avro—they support schema evolution.
- Enable schema merge:
```python
    spark.read.option("mergeSchema", "true").parquet("path")
```
- Plan schema carefully and use versioning for backward compatibility.

---

### 51. **Can you provide an example of a complex PySpark transformation pipeline you've implemented? What challenges did you face, and how did you overcome them?**

**Scenario**:
- Merged IoT device data from multiple sources
- Cleaned, joined with metadata, and aggregated for daily metrics
- Stored in Delta Lake with partitioning

**Challenges**:
- Handling out-of-order data
- Optimizing joins
- Schema evolution over time

**Solutions**:
- Used watermarking and window functions
- Applied broadcast joins
- Enabled merge schema in Delta writes

---

### 52. **Explain the difference between RDD, DataFrame, and Dataset in PySpark.**

| Aspect        | RDD                                  | DataFrame                          | Dataset (not in PySpark)           |
|---------------|--------------------------------------|------------------------------------|------------------------------------|
| Level         | Low-level API                        | High-level API (with schema)       | Typed high-level API (Scala/Java only) |
| Optimization  | No automatic optimization            | Catalyst & Tungsten optimization  | Catalyst & Tungsten optimization  |
| Ease of use   | Complex, verbose                     | Easy, SQL-like operations         | Type-safe but verbose (not in PySpark) |
| Schema        | No schema                            | Has schema (columns & types)      | Strongly typed schema             |

🔵 **Note**: Dataset API doesn’t exist in PySpark, only in Scala/Java. PySpark combines DataFrame and Dataset concept internally.

---

### 53. **What is the difference between `cache()` and `persist()` in PySpark?**

| Aspect   | `cache()`                         | `persist()`                         |
|----------|-----------------------------------|-------------------------------------|
| Storage  | Stores in memory only             | Stores in memory or disk (user-defined) |
| Default  | MEMORY_AND_DISK (memory first)    | You can specify storage levels     |
| Usage    | Simpler when you need in-memory   | Flexible for different storage strategies |

---

### 54. **How does Lazy Evaluation work in PySpark?**

- Transformations (like `map`, `filter`) are **lazy** — they are **not executed immediately**.
- Actions (like `collect`, `count`) **trigger** the computation.
- Benefits:
  - Optimizes execution plans (via Catalyst Optimizer).
  - Reduces unnecessary computations.

---

### 55. **What are wide and narrow transformations in PySpark?**

| Type         | Narrow Transformation          | Wide Transformation               |
|--------------|---------------------------------|------------------------------------|
| Definition   | Data moved within a partition   | Data shuffled across partitions   |
| Examples     | `map`, `filter`                 | `groupByKey`, `reduceByKey`, `join` |
| Performance  | Faster (no shuffle)             | Slower (shuffle involved)          |

---

### 56. **Explain shuffle operations in PySpark and their impact on performance.**

- **Shuffle** = data movement across nodes for operations like `groupBy`, `reduceByKey`, `join`.
- Impact:
  - Costly in terms of time and memory.
  - Can cause network IO and disk spills.
- PySpark tries to **minimize shuffles** during optimization.

---

### 57. **What are the different persistence levels available in PySpark?**

- `MEMORY_ONLY`
- `MEMORY_AND_DISK`
- `MEMORY_ONLY_SER`
- `MEMORY_AND_DISK_SER`
- `DISK_ONLY`
- `OFF_HEAP` (rare)
  
Each one balances memory vs. disk based on resource availability.

---

### 58. **How does PySpark handle schema evolution in DataFrames?**

- PySpark supports **schema merging** when reading Parquet/ORC formats.
- For example, different files can have different schemas, and PySpark can merge them using:
  ```python
      spark.read.option("mergeSchema", "true").parquet("path")
  ```
- Not fully automatic with all formats; mostly works well with Parquet/Delta.

---

### 59. **What is broadcast join, and when should we use it?**

- Used when **one dataset is small** enough to fit into memory.
- PySpark broadcasts the small dataset to all nodes.
- Avoids shuffle, making joins much faster.

```python
    from pyspark.sql.functions import broadcast
    df_large.join(broadcast(df_small), "key")
```

---

### 60. **Explain the difference between `groupBy()` and `reduceByKey()` in PySpark.**

| Aspect        | groupBy()                         | reduceByKey()                     |
|---------------|------------------------------------|-----------------------------------|
| Input         | DataFrame / RDD                    | (key, value) RDD                  |
| Shuffle       | Always shuffles                    | Does local aggregation before shuffling |
| Efficiency    | Less efficient                     | More efficient for (key, value) aggregations |

---

### 61. **What is the use of `explode()` function in PySpark?**

- Used to **flatten arrays or maps** into multiple rows.
  
Example:
```python
    from pyspark.sql.functions import explode
    df.select("name", explode("hobbies"))
```
If a person has multiple hobbies, `explode()` will create one row per hobby.

---

## Coding Questions 🎯

---

### 62. **Find the top 3 highest-paid employees from each department**

```python
    from pyspark.sql import SparkSession
    from pyspark.sql.window import Window
    from pyspark.sql.functions import col, row_number

    spark = SparkSession.builder.getOrCreate()

    data = [
        (1, "Amit", "IT", 90000),
        (2, "Neha", "HR", 50000),
        (3, "Raj", "IT", 85000),
        (4, "Priya", "HR", 60000),
        (5, "Suresh", "Finance", 75000),
        (6, "Anjali", "Finance", 80000),
        (7, "Vikas", "IT", 92000),
        (8, "Rohan", "HR", 58000),
        (9, "Meera", "Finance", 82000)
    ]

    columns = ["id", "name", "dept", "salary"]

    df = spark.createDataFrame(data, columns)

    windowSpec = Window.partitionBy("dept").orderBy(col("salary").desc())

    top3 = df.withColumn("rank", row_number().over(windowSpec)).filter(col("rank") <= 3)
    top3.show()
```

---

### 63. **Count the number of null values in each column**

```python
    from pyspark.sql.functions import col, sum as _sum, when

    null_counts = df.select([_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns])
    null_counts.show()
```

---

### 64. **Remove duplicate records based on a specific column**

(Say, remove based on `id`)

```python
    data = [
        (101, "Mumbai", "Maharashtra"),
        (102, "Delhi", "Delhi"),
        (103, "Bangalore", "Karnataka"),
        (101, "Mumbai", "Maharashtra"),
        (104, "Pune", "Maharashtra")
    ]

    columns = ["id", "city", "state"]

    df = spark.createDataFrame(data, columns)

    df_unique = df.dropDuplicates(["id"])
    df_unique.show()
```

---

### 65. **Replace null values with previous non-null value**

(Use **window function** with `last()`)

```python
    from pyspark.sql.window import Window
    from pyspark.sql.functions import last

    windowSpec = Window.orderBy("id").rowsBetween(Window.unboundedPreceding, 0)

    df_filled = df.withColumn("city_filled", last("city", True).over(windowSpec))
    df_filled.show()
```

---

### 66. **Moving average of sales over last 3 months**

Assuming we have data like:

```python
    sales_data = [
        ("2024-01", 100),
        ("2024-02", 150),
        ("2024-03", 200),
        ("2024-04", 300),
        ("2024-05", 250)
    ]

    columns = ["month", "sales"]

    df = spark.createDataFrame(sales_data, columns)

    from pyspark.sql.functions import avg
    from pyspark.sql.window import Window

    windowSpec = Window.orderBy("month").rowsBetween(-2, 0)

    df_moving_avg = df.withColumn("moving_avg", avg("sales").over(windowSpec))
    df_moving_avg.show()
```

---
Alright, let’s break it down very simply:

---
### 67. **What is Logical Plan in PySpark?**

- In PySpark, **Logical Plan** is **how Spark understands your query internally**, step-by-step, **before** actually running it.
- It is a **blueprint** that shows **what** operations you want to do (like select, join, filter) — but **not yet** concerned about **how** to do them.

Think of it like:
> 📝 "You describe *what* you want, and Spark figures out *how* to do it best."

```python
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("LogicalPlanExample").getOrCreate()

    data = [(1, "cat"), (2, "dog"), (3, "rabbit")]
    df = spark.createDataFrame(data, ["id", "animal"])

    result = df.filter("id > 1").select("animal")
    result.explain()
```

**Output:**
```
    == Physical Plan ==
    *(1) Project [animal#x]
    +- *(1) Filter (id#x > 1)
      +- Scan ExistingRDD[id#x, animal#x]
```

**Logical plan is hidden inside** this `explain()` — before optimization.

#### Stages inside the Logical Plan:
1. **Unresolved Logical Plan**  
   - Spark just reads your query.
   - Columns, tables, etc. are **not validated yet**.
2. **Analyzed Logical Plan**  
   - Spark checks your DataFrame:  
     ✅ Do the columns exist?  
     ✅ Is the syntax correct?
3. **Optimized Logical Plan**  
   - Spark tries to **optimize**:  
     - Push filters earlier  
     - Simplify expressions  
     - Remove unnecessary steps

 Only **after** this optimization, Spark builds a **Physical Plan** (how to actually run it on executors).


#### In super simple words:

| Concept             | Meaning                                           |
|---------------------|----------------------------------------------------|
| **Unresolved Plan**  | "User said something, not sure if it's correct."    |
| **Analyzed Plan**    | "I checked — the columns exist, everything is fine." |
| **Optimized Plan**   | "Let me reorganize to make it faster."             |

```
+--------------------------+
| Your PySpark Code        |
+--------------------------+
             ↓
+--------------------------+
| Unresolved Logical Plan  |
| - No validation          |
| - Columns not verified   |
+--------------------------+
             ↓
+--------------------------+
| Analyzed Logical Plan    |
| - Columns checked        |
| - Syntax validated       |
+--------------------------+
             ↓
+--------------------------+
| Optimized Logical Plan   |
| - Reorders operations    |
| - Removes redundancy     |
+--------------------------+
             ↓
+--------------------------+
| Physical Plan            |
| - Execution strategy     |
| - Which node does what   |
+--------------------------+
```


---

### 68. **What is `collect()` in Spark (PySpark)?**
- `.collect()` **brings all the data** from your **Spark DataFrame or RDD** **into the driver** (your local Python program).
- It **gathers** all the distributed data spread across worker nodes and **returns it as a Python list** (for RDD) or list of Row objects (for DataFrame).

Example:

```python
    df = spark.createDataFrame([(1, "cat"), (2, "dog")], ["id", "animal"])

    # This will bring all data to your local program
    data = df.collect()

    for row in data:
        print(row)
```

**Output:**
```
    Row(id=1, animal='cat')
    Row(id=2, animal='dog')
```


#### So in short:
| Concept         | Meaning                                      |
|-----------------|----------------------------------------------|
| Where           | Driver program (your local code)             |
| What            | All rows as Python objects (or dicts)         |
| Why             | To process or print data locally             |



#### Warning: Be careful!
- `.collect()` can cause **memory overflow** if the dataset is **very large**.
- Because **all** the data is pulled **at once** into **driver memory**.
- **Spark is designed for distributed processing**, so `.collect()` should only be used on **small datasets**.


#### Real-world Tip:
- Use `.show()`, `.take()`, or `.limit()` if you just want to **peek** at some rows instead of pulling everything.

Example:

```python
    df.show(5)  # shows 5 rows without collecting
```


#### 🔥 In short:
> `.collect()` = "Give me everything from the cluster to my Python program."

---

## Here's a well-structured **L2 Technical Interview Q\&A** set for a Data Engineering role focused on **Apache Spark, Azure Data Factory, and related data systems**:

---

### 69. **Explain the architecture of Apache Spark. What are the key components and how do they interact?**

**Answer:**
Apache Spark follows a master-slave architecture. The **Driver Program** runs the main function and manages SparkContext, which coordinates all tasks. The **Cluster Manager** (e.g., YARN, Kubernetes, or Standalone) allocates resources. **Executors** run on worker nodes to execute tasks and store data. A job is split into **stages**, and stages into **tasks**, which are scheduled by the Driver and executed by Executors. The **DAG Scheduler** builds the execution plan from RDD lineage and manages stage dependencies.

---

### 70. **What is the Catalyst Optimizer in Spark? How does it help improve query performance?**

**Answer:**
Catalyst is Spark SQL’s query optimization framework. It transforms SQL queries into an optimized logical plan, applies rule-based and cost-based optimizations (like constant folding, predicate pushdown), and finally converts it to a physical plan. This improves performance by selecting efficient join strategies, reordering filters, and eliminating unnecessary computations.

---

### 71. **What are the differences between Data Lake and Delta Lake? Why was Delta Lake introduced?**

**Answer:**

* **Data Lake** is a storage repository that holds raw, unstructured/structured data, often in formats like Parquet or CSV. It lacks ACID transaction support.
* **Delta Lake** is a storage layer built on top of Data Lake that brings ACID transactions, schema enforcement, time travel, and efficient upserts using **Delta format**.

**Delta Lake was introduced** to handle reliability, data consistency, and performance issues in data lakes, especially for streaming + batch workloads.

---

### 72. **Explain the internal working of the Spark SQL engine, from query parsing to execution.**

**Answer:**

1. **Parsing:** SQL is parsed into an unresolved logical plan.
2. **Analysis:** The plan is resolved against the catalog to identify tables, columns.
3. **Optimization:** Catalyst applies logical optimization rules.
4. **Physical Planning:** The logical plan is converted to multiple physical plans.
5. **Cost Model:** The most efficient physical plan is selected.
6. **Code Generation:** Tungsten generates Java bytecode for optimized execution.

---

### 73. **Describe different join strategies in Spark. What happens under the hood during each?**

**Answer:**

* **Broadcast Join:** One side (usually small) is broadcast to all executors to avoid shuffle.
* **Shuffle Hash Join:** Both datasets are shuffled, hashed, and joined; suitable for medium-sized data.
* **Sort-Merge Join:** Datasets are sorted and merged on join keys; preferred for large sorted datasets.
* **Skew Join Handling:** Spark can use techniques like salting or AQE’s skew join optimization.

---

### 74. **ADF Scenario: Describe real-world pipeline use cases. Why and when would you use various activities and connectors in Azure Data Factory?**

**Answer:**
**Use Case:** Ingest data from REST APIs and Oracle into ADLS, transform in Databricks, and load into Azure SQL.

* **Copy Activity**: For ingestion.
* **Lookup & If Condition**: For dynamic control flow.
* **Stored Procedure**: For post-load processing.
* **Web Activity**: For triggering external APIs.
  **Connectors:** Use built-in connectors for S3, Snowflake, Oracle, etc., to integrate diverse data sources.

---

### 75. **What is Adaptive Query Execution (AQE) in Spark? How does it improve runtime performance?**

**Answer:**
AQE dynamically optimizes query execution at runtime using actual statistics:

* Switch join strategy (e.g., to Broadcast)
* Optimize skewed joins
* Coalesce partitions dynamically
  It helps in handling data skew, misestimated statistics, and improves performance in unpredictable data scenarios.

---

### 76. **How would you implement Slowly Changing Dimension Type 2 (SCD Type 2) logic in a data pipeline?**

**Answer:**
In a Spark/Databricks pipeline:

1. Compare source vs target using surrogate keys.
2. Identify new, changed, and unchanged records.
3. For changed records: expire old (set `IsCurrent=False`, `EndDate=CurrentDate`) and insert new with `IsCurrent=True`.
4. Merge using Delta Lake's `MERGE INTO` for atomic SCD2 updates.

---

### 77. **What are the key differences between Azure Blob Storage and Azure Data Lake Storage Gen2?**

**Answer:**

| Feature                | Blob Storage            | ADLS Gen2                         |
| ---------------------- | ----------------------- | --------------------------------- |
| Hierarchical Namespace | No                      | Yes                               |
| Performance            | Basic                   | Optimized for big data            |
| Access Control         | Basic ACLs              | POSIX-compliant fine-grained ACLs |
| Use Case               | General-purpose storage | Big data analytics, Hadoop-like   |

---

### 78. **Why is Spark lazily evaluated? What are the benefits of lazy evaluation in practice?**

**Answer:**
Spark defers execution until an **action** is called. This allows:

* Optimizing the DAG before execution
* Reducing unnecessary computation
* Efficient pipeline execution through task fusion
  It leads to better performance and resource management.

---

### 79. **Compare Kryo serialization vs Java serialization in Spark. When should you use Kryo?**

**Answer:**

* **Java Serialization**: Default in Spark, flexible but slow and verbose.
* **Kryo Serialization**: Faster, more compact.
  **Use Kryo** when:
* Performance is critical.
* You're dealing with large data or custom classes.
* You register classes upfront to avoid overhead.

Use:

```python
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

---


### 80. **Explain the difference between clustering and partitioning in data warehousing.**

**Answer:**

* **Partitioning** divides a table **physically into separate segments** based on column values.
  
  Example:
  ```sql
  PARTITION BY RANGE(sale_date)
  ```
  This will store January data in one partition, February in another.

* **Clustering** organizes the data **logically within a partition** to keep similar rows together (does not create separate physical files but improves I/O).
  
  Example (in Snowflake):
  ```sql
  CLUSTER BY (customer_id)
  ```
  Keeps rows of the same customer close together.

📌 **Use Case:**

* Partitioning is better for queries that filter on the partition column (e.g., by month).
* Clustering improves performance for queries scanning large partitions with filters on non-partition keys.

---

📌 **Use Case:**

* Partitioning is better for queries that filter on the partition column (e.g., by month).
* Clustering improves performance for queries scanning large partitions with filters on non-partition keys.
### 81. **How do you optimize SQL queries for performance?**

**Answer:**

* Use proper indexes.
  
  *E.g.: Create index on frequently-filtered columns:*
  ```sql
  CREATE INDEX idx_customer ON orders(customer_id);
  ```
* Avoid `SELECT *`, specify columns.
* Use **EXPLAIN PLAN** to check the query execution path.
* Minimize nested subqueries.
* Use joins appropriately (use inner join if outer join isn’t required).
* Use partition pruning where possible.
* Use CTEs to simplify repeated logic.

---
### 82. **Design a schema/address mapping for a swipe-payment API.**

**Answer:**

For a swipe-payment system:

* Table: `transactions`
  ```sql
  id (PK), user_id, card_id, merchant_id, amount, currency, timestamp, status
  ```
* Table: `users`
  ```sql
  id (PK), name, email, phone, address_id
  ```
* Table: `address`
  ```sql
  id (PK), street, city, state, zip, country
  ```

📌 **Description:**

* Normalize addresses to avoid duplication.
* Link transactions to user and merchant.
* Use indexed `timestamp` & `user_id` for analytics.

---
### 83. **Implement the "Next Greater Element" algorithm for an array.**

**Answer:**

Find for each element the next element greater than it.

```python
def next_greater(arr):
    stack = []
    res = [-1] * len(arr)
    for i in range(len(arr)):
        while stack and arr[i] > arr[stack[-1]]:
            idx = stack.pop()
            res[idx] = arr[i]
        stack.append(i)
    return res

print(next_greater([4, 5, 2, 25]))  # Output: [5, 25, 25, -1]
```
---
### 84. **Search in a rotated sorted array.**

**Answer:**

```python
def search(nums, target):
    l, r = 0, len(nums)-1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid-1
            else:
                l = mid+1
        else:
            if nums[mid] < target <= nums[r]:
                l = mid+1
            else:
                r = mid-1
    return -1

search([4,5,6,7,0,1,2], 0)  # Output: 4
```
---

### 85. **Find the K-th element across two sorted arrays.**

**Answer:**

Use a binary-search approach:

```python
def find_kth(arr1, arr2, k):
    i, j = 0, 0
    while True:
        if i == len(arr1): return arr2[j + k - 1]
        if j == len(arr2): return arr1[i + k - 1]
        if k == 1: return min(arr1[i], arr2[j])

        mid_k = k // 2
        new_i = min(i + mid_k, len(arr1)) - 1
        new_j = min(j + mid_k, len(arr2)) - 1
        if arr1[new_i] <= arr2[new_j]:
            k -= (new_i - i + 1)
            i = new_i + 1
        else:
            k -= (new_j - j + 1)
            j = new_j + 1

find_kth([1,3,5], [2,4,6], 4)  # Output: 4
```

---

### 86. **Traverse a binary tree in zigzag (spiral) order.**

**Answer:**

```python
from collections import deque

def zigzag(root):
    if not root: return []
    res, q, left_to_right = [], deque([root]), True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
    return res
```

### 87. **Explain Slowly Changing Dimensions (SCD) types and their use cases.**

**Answer:**

* **Type 1:** Overwrite old data.  
  *E.g., Correcting an address error.*
* **Type 2:** Add a new row with validity period (tracks history).  
  *E.g., Customer moved to a new city.*
* **Type 3:** Add a new column to hold previous value.  
  *E.g., Store current & previous manager.*
* **Type 4:** Historical table to keep all changes separately.
* **Type 6/Hybrid:** Combination of Type 1,2,3.

---

### 88. **Describe the ETL process end-to-end.**

**Answer:**

* **Extract:** Retrieve data from sources (databases, APIs, files).  
  *E.g., Read sales CSVs daily.*
* **Transform:** Clean, join, aggregate, validate.  
  *E.g., Convert currencies, remove nulls, join with customer.*
* **Load:** Insert into target warehouse/table.  
  *E.g., Load into Snowflake fact tables.*

**Tools:** ADF, Talend, Informatica.

---

### 89. **Compare data lakes vs. data warehouses.**

| Feature      | Data Lake                       | Data Warehouse                |
| ------------ | ------------------------------- | ----------------------------- |
| Data type    | Raw (structured + unstructured) | Structured & cleaned          |
| Storage cost | Cheaper (cloud object storage)  | Expensive (compute optimized) |
| Schema       | Schema-on-read                  | Schema-on-write               |
| Use case     | ML, data discovery              | BI, reporting                 |

---

### 90. **How does Hadoop MapReduce work?**

**Answer:**

* Splits input into **blocks** processed in parallel.
* **Map phase:** Processes each block → (key, value) pairs.
* **Shuffle & Sort:** Groups by key.
* **Reduce phase:** Aggregates results.

*E.g., Word count: Map emits (word, 1), Reduce sums counts per word.*

---

### 91. **Describe Apache Spark and its advantages over Hadoop MapReduce.**

**Answer:**

* Spark processes in-memory → much faster.
* Supports SQL, ML, Streaming.
* Supports iterative algorithms (Graph, ML) efficiently.
* Fault-tolerant via lineage (RDDs).

*E.g., Spark SQL for aggregating logs 100× faster than MapReduce.*

---

### 92. **Explain Apache Kafka and its role in real-time streaming pipelines.**

**Answer:**

Kafka is a distributed, fault-tolerant publish-subscribe system:

* **Producers** send events (e.g., payments, logs).
* **Brokers** store events in topics.
* **Consumers** read events.

📌 *Use case:* Capture IoT sensor data in real time → process → store in a database.

---
### 93. **Walk through designing a data pipeline and schema to support address lookup or payment flow.**

**Answer:**

📌 Payment Flow Pipeline:

* **Ingest:** API → Kafka → Stream.
* **Validate & transform:** Mask card details, validate amount.
* **Store:** Transactions fact table; address dimension table.

**Schema:**

* `transaction_id, user_id, merchant_id, amount, timestamp, status`
* `address_id, street, city, state, zip`

---

### 94. **Given a real-world case study (e.g., loading pricing options), break it down into ingestion, transformations, storage, and data serving.**

**Answer:**

📌 Case: Airline pricing options

* **Ingestion:** Fetch JSON from partner APIs → land in blob storage.
* **Transformation:** Parse JSON, normalize prices & currencies.
* **Storage:** Load into `pricing_options` fact table with dimensions: route, date, airline.
* **Serving:** Power BI dashboard querying the warehouse for cheapest/best flights.

---




