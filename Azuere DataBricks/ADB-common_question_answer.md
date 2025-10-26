# *Databricks Data Engineer* interview questions and answers

### **1. How does Databricks differ from a traditional Spark cluster?**

Databricks is a **managed and optimized Spark platform** that simplifies cluster management, autoscaling, and performance tuning. Unlike traditional Spark clusters that require manual setup and maintenance, Databricks provides:

* **Auto-scaling and auto-termination** of clusters
* **Optimized Spark runtime** for better performance
* **Collaborative notebooks** for development
* **Built-in integrations** with Delta Lake, MLflow, and data sources like ADLS/S3
* **Job orchestration and governance** through Databricks Workflows

---

### **2. What are the benefits of using Databricks notebooks for data engineering pipelines?**

* Interactive development and debugging
* Support for **multiple languages** (Python, SQL, Scala, R) in a single notebook
* **Version control** and collaboration features
* Easy integration with **Databricks Jobs** for scheduling
* Visualization and documentation within the same environment

---

### **3. How do you create a SparkSession in Databricks and why is it required?**

In Databricks, the SparkSession is **automatically created** as `spark`.
Example:

```python
spark = SparkSession.builder.appName("DataEngineering").getOrCreate()
```

It’s required because it serves as the **entry point** for all Spark functionalities — creating DataFrames, executing SQL queries, and accessing the SparkContext.

---

### **4. Explain the difference between SparkContext and SparkSession in Databricks.**

* **SparkContext**: Core component that connects to the cluster and manages resources for RDD operations.
* **SparkSession**: A unified entry point introduced in Spark 2.0 that encapsulates SparkContext and supports DataFrame, SQL, and Streaming APIs.
  In Databricks, you typically interact with `spark` (SparkSession), not SparkContext directly.

---

### **5. What are transformations and actions in PySpark? Give examples of each.**

* **Transformations**: Create a new DataFrame from an existing one (lazy).
  Example:

  ```python
  df_filtered = df.filter(df.age > 25)
  df_selected = df.select("name", "age")
  ```
* **Actions**: Trigger computation and return results.
  Example:

  ```python
  df.show()
  df.count()
  ```

---

### **6. Describe lazy evaluation in Spark with a practical example.**

Spark doesn’t execute transformations immediately — it builds a **logical plan** and only executes when an **action** is called.
Example:

```python
df_filtered = df.filter(df.age > 30)
df_selected = df_filtered.select("name")
df_selected.show()  # Actual computation happens here
```

This approach optimizes execution through **lineage and DAG optimization**.

---

### **7. How do you handle schema definition while creating DataFrames in Databricks?**

You can define schema **manually** for better performance and consistency:

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True)
])

df = spark.read.schema(schema).csv("/mnt/data/employees.csv")
```

Manually defining schema avoids Spark’s overhead of schema inference.

---

### **8. What are some common DataFrame transformations you have implemented in Databricks?**

* `filter()` / `where()` – filtering data
* `select()` / `withColumn()` – column selection and transformation
* `groupBy()` / `agg()` – aggregations
* `join()` – joining multiple DataFrames
* `dropDuplicates()` – removing duplicate records
* `withColumnRenamed()` – renaming columns

---

### **9. How do you use when() and otherwise() for conditional logic in PySpark?**

Used for **conditional column creation**:

```python
from pyspark.sql.functions import when

df = df.withColumn(
    "status",
    when(df.age > 18, "Adult").otherwise("Minor")
)
```

---

### **10. Explain how to create and use temporary views for SQL queries in Databricks.**

You can create a temporary view from a DataFrame:

```python
df.createOrReplaceTempView("employee_view")
spark.sql("SELECT * FROM employee_view WHERE age > 30").show()
```

This allows you to **run SQL queries** directly within Databricks.

---

### **11. What is the difference between createTempView and createOrReplaceTempView?**

* `createTempView`: Fails if the view already exists.
* `createOrReplaceTempView`: Replaces the existing view with the same name.

---

### **12. How can you optimize PySpark transformations in Databricks for large datasets?**

* Use **partitioning** and **bucketing** for parallelism
* **Cache** or **persist** reused DataFrames
* Avoid wide transformations where possible
* Use **broadcast joins** for small lookup tables
* Leverage **Databricks Runtime optimizations** and **Photon Engine**

---

### **13. What is caching and persistence in Databricks, and when should you use them?**

Caching stores a DataFrame in memory (or disk) for faster reuse:

```python
df.cache()
df.count()  # triggers caching
```

Use caching when the same DataFrame is used multiple times in a pipeline.
`persist()` provides more control over storage levels (e.g., memory-only, memory-and-disk).

---

### **14. How do you manage job scheduling and orchestration in Databricks Workflows?**

* Use **Databricks Workflows (Jobs)** to schedule notebooks, scripts, or tasks.
* Supports **task dependencies**, **alerts**, and **parameter passing**.
* Integrates with **Azure Data Factory**, **Airflow**, or **Dagster** for enterprise orchestration.

---

### **15. Explain a real-time data ingestion scenario using Auto Loader or Structured Streaming in Databricks.**

Using **Auto Loader** for incremental ingestion:

```python
df = (spark.readStream
          .format("cloudFiles")
          .option("cloudFiles.format", "json")
          .load("/mnt/raw-data/"))
df.writeStream.format("delta").option("checkpointLocation", "/mnt/checkpoints/").start("/mnt/processed/")
```

It continuously ingests new files as they arrive with **exactly-once** guarantees.

---

### **16. What is the purpose of Delta Lake in Databricks?**

Delta Lake brings **ACID transactions**, **schema enforcement**, and **time travel** to data lakes.
Benefits:

* Reliable data pipelines
* Support for **upserts and deletes**
* Efficient incremental processing

---

### **17. How do you perform incremental data updates in Delta tables?**

Using **MERGE INTO** for upserts:

```python
deltaTable.alias("t").merge(
    source_df.alias("s"),
    "t.id = s.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

This ensures only changed records are updated or inserted.

---

### **18. How can you handle schema evolution in Delta Lake?**

Enable **automatic schema evolution**:

```python
df.write.option("mergeSchema", "true").format("delta").mode("append").save("/mnt/delta/table")
```

Delta Lake allows adding new columns without recreating the table.

---

### **19. Explain a real-world project where you optimized a PySpark job using partitions or caching.**

In one project, a large sales dataset (~1TB) was processed daily.

* Initially, joins and aggregations were slow.
* Optimization steps:

  * Repartitioned data by `region` before joins
  * Cached intermediate DataFrames
  * Used **broadcast join** for small dimension tables
    Result: ~60% reduction in processing time.

---

### **20. How do you integrate Databricks with external storage systems like AWS S3 or Azure Data Lake?**

Mount external storage into Databricks:

```python
dbutils.fs.mount(
  source = "wasbs://container@storageaccount.blob.core.windows.net/",
  mount_point = "/mnt/adls",
  extra_configs = {"fs.azure.account.key.storageaccount.blob.core.windows.net": "<key>"}
)
```

Once mounted, you can read/write like:

```python
df = spark.read.parquet("/mnt/adls/data/")
```

Supports **S3, ADLS, GCS**, and others via secure connectors.

