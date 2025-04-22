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

### **2. Performance Tuning Techniques in Spark**
- **Optimize shuffles**: Use `repartition()` wisely; minimize wide transformations.
- **Persist()/cache()**: Use when reusing intermediate results.
- **Broadcast joins**: Broadcast small dimension tables to avoid shuffle joins.
- **Explain plan**: Use `.explain()` to analyze the physical execution plan.

---

### **3. Accumulator vs Broadcast Variables**
- **Accumulator**: Used for counters, sum, etc. Write-only from executors.
- **Broadcast**: Share small lookup datasets across nodes efficiently.

---

### **4. SparkSession vs SparkContext**
| Feature        | SparkSession                         | SparkContext                     |
|----------------|--------------------------------------|----------------------------------|
| Purpose        | Unified entry point (DF, SQL, etc.)  | RDD-based operations             |
| Introduced in  | Spark 2.0                            | Spark 1.x                        |
| Example        | `SparkSession.builder.appName()`     | `SparkContext(conf)`            |

---

### **5. Dataset vs DataFrame**
- **Dataset** (Scala/Java): Type-safe, compile-time checks.
- **DataFrame**: Untyped, row-based with schema.

---

### **6. Spark Session Command**
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()
```

---

### **7. Command to Read JSON Data**
```python
df = spark.read.option("multiline", "true").json("path/to/file.json")
```

---

### **8. CSV Without Column Names/Schema**
```python
df = spark.read.option("header", "false").csv("path.csv")
```

---

### **9. Find 3rd Highest Salary**
```sql
SELECT DISTINCT salary FROM employee ORDER BY salary DESC LIMIT 3

--OR

SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC OFFSET 2 ROWS FETCH NEXT 1 ROW ONLY;
```
---

### **10. Employees Earning More Than Manager**
```sql
SELECT e.name FROM employee e JOIN employee m ON e.manager_id = m.id WHERE e.salary > m.salary

```

---

### **11. Palindrome Check (PySpark UDF Example)**
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

def is_palindrome(s):
    return s == s[::-1]

is_palindrome_udf = udf(is_palindrome, BooleanType())
df = df.withColumn("is_palindrome", is_palindrome_udf(df["column"]))
```

---

### **12. Spark Submit Command**
```bash
spark-submit --class com.example.Main --master yarn /path/to/app.jar
```

---

### **13. Memory Tuning**
- `--executor-memory 4G`
- Use `StorageLevel.MEMORY_AND_DISK`
- Tune GC with `spark.executor.extraJavaOptions`

---

### **14. Created JARs**
> I created JARs using Maven for my Scala Spark jobs. Used `pom.xml` to manage dependencies and `spark-submit` to deploy.

---

### **15. Worked with UDFs**
> Yes, I used UDFs in Python for data transformation like converting date formats, validating emails, or checking for palindromes.

---

### **16. Dynamic Resource Allocation**
```bash
--conf spark.dynamicAllocation.enabled=true
--conf spark.dynamicAllocation.minExecutors=2
--conf spark.dynamicAllocation.maxExecutors=10
```

---

### **17. Daily Data Volume**
> We processed ~1TB/day from various sources including system logs, e-commerce transactions, and IoT device data.

---

### **18. DataFrame vs Dataset**
Covered above.  
> DataFrame is untyped (runtime schema checks), Dataset is typed (compile-time checks, only in Scala/Java).

---

### **19. Load CSV from HDFS**
```python
df = spark.read.csv("hdfs://namenode/path/file.csv", header=True, inferSchema=True)
```

---

### **20. What is Multiline?**
> The `multiline` option is used when JSON records span multiple lines.

```python
spark.read.option("multiline", "true").json("path")
```

---

### **21. No Column Names in CSV**
```python
df = spark.read.option("header", "false").csv("path.csv")
```

---

#### **22. Case Class and StructType Syntax**
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

### **23. Partitioning vs Bucketing**
| Technique    | Partitioning                      | Bucketing                            |
|--------------|-----------------------------------|--------------------------------------|
| Based on     | Directory structure               | Hashing function                     |
| Performance  | Good for filtering                | Good for join optimization           |
| Use case     | Date-based queries                | Joining large datasets efficiently   |

---

### **24. Closure Function**
> A closure captures variables from its outer scope. Spark sends the closure to executors, so variables must be serializable.

---

### **25. Count of Alphabets in String (Python)**
```python
from collections import Counter

def count_alpha(s):
    return dict(Counter(filter(str.isalpha, s)))
```

---

### **26. List vs Tuple**
| Feature      | List                          | Tuple                        |
|--------------|-------------------------------|------------------------------|
| Mutability   | Mutable                        | Immutable                    |
| Performance  | Slightly slower                | Faster                       |
| Syntax       | `[1, 2, 3]`                    | `(1, 2, 3)`                  |

---

### **27 In ADF, what is the other way to get the incremental load without Watermark Columns:

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
