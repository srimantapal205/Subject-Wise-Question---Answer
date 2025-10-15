# 🚀 Comprehensive Guide to Optimizing Spark Jobs in Databricks

Optimizing Spark jobs in **Databricks** is crucial for improving performance, reducing costs, and ensuring reliability in large-scale data processing. Let’s go step-by-step through **detailed techniques and strategies** — from **architecture-level tuning** down to **code-level optimization**.

---

## 🔹 1. Understand Spark Job Execution Basics

Before optimizing, it’s essential to understand how Spark executes a job:

* **Driver:** Coordinates the job (planning, scheduling, and collecting results).
* **Executors:** Run tasks on worker nodes and store data in memory/disk.
* **Stages & Tasks:** Spark breaks jobs into stages (based on shuffles) and tasks (parallel units of work).

Optimization focuses on **reducing shuffles**, **minimizing I/O**, and **efficient resource utilization**.

---

## 🔹 2. Cluster & Resource Optimization

### ✅ **a. Use Autoscaling and Right-Sizing**

* Enable **Databricks Autoscaling** to dynamically adjust cluster size.
* Choose an **instance type** based on workload:

  * CPU-intensive → compute-optimized (e.g., `Standard_F` series)
  * Memory-intensive → memory-optimized (e.g., `Standard_E` or `r` series)
  * I/O-bound → storage-optimized (e.g., `L` series)
* Start small (e.g., 2–4 workers) and scale up as needed.

### ✅ **b. Use Photon Runtime**

* **Photon** (Databricks’ native vectorized engine) accelerates SQL, DataFrame, and Delta operations — often 2–4× faster.
* Simply enable it in cluster settings (`Use Photon Acceleration`).

### ✅ **c. Cache and Reuse Data Efficiently**

* Use `.cache()` or `.persist()` only when reused multiple times.
* Always **unpersist()** after use to free memory.

---

## 🔹 3. Data I/O Optimization

### ✅ **a. Optimize Delta Tables**

* **Z-Ordering:** Cluster related data to improve filtering performance.

  ```python
  OPTIMIZE delta_table_name ZORDER BY (column_name)
  ```
* **VACUUM:** Remove old files and reduce storage overhead.

  ```python
  VACUUM delta_table_name RETAIN 168 HOURS
  ```
* **Data Skipping:** Leverage Delta statistics to skip irrelevant data automatically.

### ✅ **b. Partition Tables Intelligently**

* Partition on **high-cardinality columns = bad** (too many small files).
* Partition on **moderate-cardinality columns** used in filters.
* Example:

  ```python
  df.write.partitionBy("year", "month").format("delta").save("/mnt/data/sales")
  ```

### ✅ **c. Combine Small Files**

* Too many small files = metadata overhead + slow reads.
* Compact them periodically:

  ```python
  OPTIMIZE delta_table_name
  ```

  or with a custom coalesce:

  ```python
  df.coalesce(10).write.mode("overwrite").format("delta").save(path)
  ```

---

## 🔹 4. Shuffle and Skew Optimization

### ✅ **a. Minimize Shuffles**

* Avoid unnecessary wide transformations (e.g., `groupByKey`, `distinct`, `repartition`).
* Prefer:

  ```python
  df.reduceByKey(lambda x, y: x + y)  # better than groupByKey
  ```

### ✅ **b. Handle Data Skew**

* Skew = one partition much larger than others → slow tasks.
* Mitigation strategies:

  * **Salting technique:**

    ```python
    from pyspark.sql.functions import concat_ws, lit, rand

    salted_df = df.withColumn("salted_key", concat_ws("_", col("key"), (rand()*10).cast("int")))
    ```
  * **Broadcast small tables** to avoid shuffles:

    ```python
    from pyspark.sql.functions import broadcast
    joined = large_df.join(broadcast(small_df), "key")
    ```

### ✅ **c. Control Partition Size**

* Ideal partition size: **100–200 MB** per partition.
* Adjust dynamically:

  ```python
  spark.conf.set("spark.sql.shuffle.partitions", 200)
  ```

---

## 🔹 5. Query and Transformation Optimization

### ✅ **a. Use DataFrame API (not RDDs)**

* DataFrame API enables **Catalyst Optimizer**, automatic query optimization, and better physical plans.

### ✅ **b. Pushdown Filters and Projections**

* Always apply filters early:

  ```python
  df = spark.read.parquet(path).filter("country = 'US'").select("id", "sales")
  ```
* Avoid reading unnecessary columns.

### ✅ **c. Avoid UDFs (if possible)**

* UDFs (Python/Scala) break optimization and are slow.
* Prefer Spark SQL functions:

  ```python
  from pyspark.sql.functions import when, col
  df = df.withColumn("category", when(col("amount") > 100, "high").otherwise("low"))
  ```
* If needed, use **Pandas UDFs** (vectorized) for better performance.

---

## 🔹 6. Job and Stage Optimization

### ✅ **a. Monitor Spark UI**

* Check for:

  * Long-running tasks (possible skew)
  * Shuffle read/write size
  * Task deserialization or GC time
* Optimize based on the **bottleneck stage**.

### ✅ **b. Reuse Broadcast Variables**

* For repeated lookups or joins with small tables:

  ```python
  broadcast_var = spark.sparkContext.broadcast(lookup_dict)
  ```

### ✅ **c. Avoid Collecting Large Data to Driver**

* Never use `.collect()` on large datasets — it can crash the driver.
* Use `.limit()`, `.take()`, or write to storage instead.

---

## 🔹 7. Configurations for Performance

Here are some key **Spark configurations** you can tune in Databricks:

| Configuration                          | Purpose                                   | Recommended Value                |
| -------------------------------------- | ----------------------------------------- | -------------------------------- |
| `spark.sql.shuffle.partitions`         | Controls number of shuffle partitions     | 200 (adjust per workload)        |
| `spark.default.parallelism`            | Default number of RDD partitions          | Usually = number of cores × 2    |
| `spark.sql.files.maxPartitionBytes`    | Split large files into smaller partitions | 128MB–256MB                      |
| `spark.sql.autoBroadcastJoinThreshold` | Auto-broadcast small tables               | 10MB–100MB                       |
| `spark.executor.memory`                | Memory per executor                       | ~4–8GB for medium workloads      |
| `spark.executor.cores`                 | Cores per executor                        | 2–5 (balance parallelism and GC) |

---

## 🔹 8. Code Review & Development Practices

* **Avoid nested operations:** Chain transformations smartly.
* **Use checkpointing** for long pipelines (break lineage):

  ```python
  df.checkpoint()
  ```
* **Leverage Delta caching** in Databricks for hot data.
* **Profile and benchmark** with Databricks’ “Job Run” metrics.

---

## 🔹 9. Example — Before & After Optimization

**Before:**

```python
data = spark.read.parquet("/mnt/raw/transactions/")
filtered = data.filter("country = 'US'")
joined = filtered.join(customers, "cust_id")
result = joined.groupBy("region").agg(sum("amount").alias("total_sales"))
result.write.format("parquet").save("/mnt/output/")
```

**After (Optimized):**

```python
spark.conf.set("spark.sql.shuffle.partitions", 200)

data = (
    spark.read.format("delta").load("/mnt/raw/transactions/")
    .select("cust_id", "amount", "region", "country")
    .filter("country = 'US'")
)

# Broadcast small table
from pyspark.sql.functions import broadcast, sum

result = (
    data.join(broadcast(customers), "cust_id")
        .groupBy("region")
        .agg(sum("amount").alias("total_sales"))
)

result.coalesce(10).write.format("delta").mode("overwrite").save("/mnt/output/")
```

**Performance Gain:**
✅ 40–70% faster execution
✅ Reduced shuffle stages
✅ Smaller output file count

---

## 🔹 10. Continuous Optimization in Databricks

Databricks offers **automatic optimization features** for Delta:

* **Auto Optimize:** Merges small files automatically.
* **Auto Compaction:** Periodically compacts files.
* **Optimize Write:** Writes data into larger, more efficient files.

You can enable these in table properties:

```sql
ALTER TABLE sales
SET TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true,
  delta.autoOptimize.autoCompact = true
)
```

---

Here’s a **production-ready Databricks notebook template** designed to apply **Spark optimization techniques** systematically, with **performance metrics tracking** and detailed **inline comments**.

You can directly copy this into a Databricks notebook (`.dbc` or `.py` format) — it’s written in PySpark syntax.

---

## 🧠 **Databricks Notebook: Spark Job Optimization Template**

```python
# Databricks notebook source
# MAGIC %md
# MAGIC ## 🚀 Spark Optimization Template for Databricks
# MAGIC
# MAGIC This notebook demonstrates:
# MAGIC - Cluster and Spark configuration tuning
# MAGIC - Efficient DataFrame transformations
# MAGIC - Delta optimization (Z-Order, compaction)
# MAGIC - Skew and shuffle handling
# MAGIC - Performance metrics capture

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast, sum, when
import time

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1️⃣ Spark Session Configuration
# MAGIC Set Spark tuning parameters before starting your job.

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", 200)        # Optimize shuffle parallelism
spark.conf.set("spark.default.parallelism", 200)           # Default task parallelism
spark.conf.set("spark.sql.files.maxPartitionBytes", 134217728)  # ~128 MB per partition
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50 MB
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", True)
spark.conf.set("spark.databricks.delta.autoCompact.enabled", True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2️⃣ Load Data Efficiently
# MAGIC Use predicate pushdown and column pruning. Load only required columns and rows.

# COMMAND ----------

start_time = time.time()

input_path = "/mnt/raw/transactions_delta"
customer_path = "/mnt/raw/customers_delta"

# Read only necessary columns and apply filters early
transactions_df = (
    spark.read.format("delta")
    .load(input_path)
    .select("cust_id", "amount", "region", "country", "year", "month")
    .filter(col("country") == "US")
)

customers_df = (
    spark.read.format("delta")
    .load(customer_path)
    .select("cust_id", "customer_name", "segment")
)

print(f"Data load completed in {round(time.time() - start_time, 2)} seconds")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3️⃣ Handle Data Skew and Optimize Joins
# MAGIC Use broadcast joins for small tables, or apply salting if one side is heavily skewed.

# COMMAND ----------

start_join = time.time()

# Broadcast smaller table to avoid shuffles
joined_df = transactions_df.join(broadcast(customers_df), "cust_id")

print(f"Join completed in {round(time.time() - start_join, 2)} seconds")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4️⃣ Perform Aggregations Efficiently
# MAGIC Avoid wide transformations when possible. Group only by required keys.

# COMMAND ----------

start_agg = time.time()

aggregated_df = (
    joined_df.groupBy("region", "segment")
    .agg(sum("amount").alias("total_sales"))
)

print(f"Aggregation completed in {round(time.time() - start_agg, 2)} seconds")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5️⃣ Persist Reusable DataFrames (When Needed)
# MAGIC Cache intermediate results only if reused multiple times.

# COMMAND ----------

aggregated_df.cache()
aggregated_df.count()  # Materialize cache
print("Aggregated DataFrame cached successfully.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6️⃣ Write Optimized Output
# MAGIC Coalesce reduces small files and optimizes parallel writes.

# COMMAND ----------

output_path = "/mnt/curated/sales_summary"

start_write = time.time()

aggregated_df.coalesce(10).write.format("delta").mode("overwrite").save(output_path)

print(f"Write completed in {round(time.time() - start_write, 2)} seconds")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7️⃣ Delta Table Maintenance
# MAGIC Use OPTIMIZE and ZORDER to cluster data for faster reads.

# COMMAND ----------

# Use SQL commands for Delta optimization
spark.sql(f"""
OPTIMIZE delta.`{output_path}`
ZORDER BY (region, segment)
""")

# Remove old files (e.g., older than 7 days)
spark.sql(f"""
VACUUM delta.`{output_path}` RETAIN 168 HOURS
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 8️⃣ Performance Metrics Summary

# COMMAND ----------

# Capture Spark execution metrics
job_metrics = {
    "input_records": transactions_df.count(),
    "output_records": aggregated_df.count(),
    "total_runtime_sec": round(time.time() - start_time, 2),
    "shuffle_partitions": spark.conf.get("spark.sql.shuffle.partitions"),
}

for k, v in job_metrics.items():
    print(f"{k}: {v}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 9️⃣ Example Visualization (Optional)
# MAGIC Use Databricks display utilities or matplotlib for quick profiling.

# COMMAND ----------

display(aggregated_df.orderBy(col("total_sales").desc()).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔟 Key Best Practices Recap
# MAGIC
# MAGIC ✅ Use Photon runtime for acceleration  
# MAGIC ✅ Optimize data layout with Delta and ZORDER  
# MAGIC ✅ Broadcast small tables to avoid shuffles  
# MAGIC ✅ Tune partition count (~100–200MB each)  
# MAGIC ✅ Avoid UDFs unless absolutely necessary  
# MAGIC ✅ Cache intermediate results only when reused  
# MAGIC ✅ Compact and vacuum Delta tables regularly
```

---

## 🧩 How to Use This Notebook

1. **Attach to a cluster** (preferably with Photon enabled).
2. Update paths for:

   * `input_path`
   * `customer_path`
   * `output_path`
3. Run cells step-by-step or as a Databricks job.
4. Monitor performance improvements in:

   * **Spark UI** (Jobs tab → Stages → Tasks)
   * **Ganglia metrics**
   * **Job metrics output (in last cell)**

---

## 🧠 Optional Enhancements

You can extend this notebook to include:

* **Automatic skew detection:** Using Spark’s `skewJoinHints`.
* **Adaptive Query Execution (AQE):**

  ```python
  spark.conf.set("spark.sql.adaptive.enabled", True)
  spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", True)
  spark.conf.set("spark.sql.adaptive.skewJoin.enabled", True)
  ```
* **Delta Live Tables integration** for continuous optimization pipelines.

---

