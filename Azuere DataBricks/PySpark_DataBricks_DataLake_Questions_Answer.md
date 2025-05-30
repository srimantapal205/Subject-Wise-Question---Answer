# The PySpark Interview questions & answers


### **1. Explain how the Catalyst Optimizer works. How can you take advantage of it when writing Spark SQL?**

**Answer:**
The Catalyst Optimizer is a key component of Spark SQL that transforms logical plans into optimized physical execution plans using rule-based and cost-based optimization techniques. It applies multiple optimization rules like predicate pushdown, constant folding, and projection pruning.

**How to take advantage:**

* Write transformations using **Spark SQL** or **DataFrame APIs** instead of RDDs to allow Catalyst to optimize your queries.
* Avoid UDFs when possible, as Catalyst can’t optimize them.
* Use **filter()** and **select()** early to prune unnecessary data.
* Leverage **broadcast joins**, **partition pruning**, and **statistics collection** to help Catalyst make better decisions.

---

### **2. What is the difference between narrow and wide transformations in PySpark? Give real examples.**

**Answer:**

* **Narrow transformations**: Data is processed within a single partition. No shuffling is required.

  * Examples: `map()`, `filter()`, `union()`
* **Wide transformations**: Data needs to be shuffled across partitions because output depends on multiple input partitions.

  * Examples: `groupByKey()`, `reduceByKey()`, `join()`

**Real Example:**

* `df.filter("age > 30")` is a narrow transformation.
* `df.groupBy("country").count()` is a wide transformation because it involves a shuffle across partitions.

---

### **3. How does PySpark handle skewed data during joins? How have you mitigated skew in your projects?**

**Answer:**
PySpark can struggle with skewed joins because a large key may send most data to one task, causing stragglers.

**Techniques I’ve used to mitigate skew:**

* **Salting**: Add a random prefix to skewed keys and replicate smaller datasets accordingly to spread the load.
* **Broadcast joins**: When one dataset is small, broadcasting avoids shuffles altogether.
* **Skew hints** in Spark 3.x+: e.g., `df.hint("skew")` to help Spark manage skewed joins.
* **Filter or split** skewed keys for separate processing.

---

### **4. Explain the internals of how PySpark handles shuffling. What are the best practices to reduce shuffle operations?**

**Answer:**
Shuffling in PySpark involves redistributing data across partitions, writing intermediate data to disk, and transferring it over the network. It occurs during wide transformations like `groupBy`, `join`, or `distinct`.

**Best practices to reduce shuffle:**

* Use **broadcast joins** for small tables.
* Replace `groupBy()` with **reduceByKey()** or **aggregateByKey()** for RDDs.
* Avoid **repartition()** unless necessary; use **coalesce()** when reducing partitions.
* Reuse partitioned data using **persist()** after expensive shuffle operations.
* Use **salting** or **custom partitioning** for skewed data.

---

### **5. When would you prefer using persist() vs cache() vs broadcasting variables?**

**Answer:**

* **cache()**: Persists the DataFrame in memory only with default storage level (MEMORY\_AND\_DISK). Good for iterative operations when data fits in memory.
* **persist()**: Gives more control over storage levels (e.g., MEMORY\_ONLY, MEMORY\_AND\_DISK\_SER). Use when data doesn’t fit entirely in memory.
* **broadcast()**: Distributes a small dataset to all nodes to avoid shuffling during joins. Use for joining large and small datasets.

**Example:**
I used `broadcast()` to optimize dimension table joins in a star schema model and `persist(MEMORY_AND_DISK)` to reuse a transformed large DataFrame across multiple actions.

---

### **6. What is the role of the Tungsten engine in PySpark’s performance optimization?**

**Answer:**
Tungsten is Spark’s execution engine that focuses on CPU and memory efficiency.

**Key contributions:**

* **Whole-stage code generation**: Compiles query plans into optimized bytecode for the JVM.
* **Off-heap memory management**: Reduces GC overhead by managing memory manually.
* **Cache-aware computation**: Uses CPU registers and avoids virtual function calls for faster execution.

**Impact:**
Tungsten drastically improves performance for Spark SQL and DataFrames, especially in complex pipelines.

---

### **7. Explain partitioning strategies in PySpark. How do you choose the number of partitions for a DataFrame?**

**Answer:**
Partitioning determines how data is distributed across executors.

**Strategies:**

* **Default hash partitioning** for operations like `groupBy` or `join`.
* **Range partitioning** can be useful for sorted data.
* **Custom partitioning** via `partitionBy()` during writes or RDD transformations.

**Choosing number of partitions:**

* Rule of thumb: **2–4 partitions per CPU core**.
* Use `df.rdd.getNumPartitions()` to inspect and `repartition()` or `coalesce()` to adjust.
* For large shuffles or joins, increase partitions to avoid data skew and OOM errors.

---

### **8. What are some common causes of OutOfMemory errors in PySpark, and how do you handle them?**

**Answer:**
**Common causes:**

* Large shuffle operations.
* Insufficient memory per executor.
* Using `collect()` on large datasets.
* Storing large objects in driver memory.

**How I handle them:**

* Tune Spark configs: `spark.executor.memory`, `spark.memory.fraction`, `spark.sql.shuffle.partitions`.
* Avoid `collect()`; use `take()` or `limit()` for samples.
* Use **persist()** or **cache()** carefully; unpersist when done.
* Optimize joins using **broadcast** where applicable.
* Repartition large DataFrames to better distribute memory usage.

---

### **9. How does schema evolution work in PySpark with different file formats like Parquet and Delta Lake?**

**Answer:**

* **Parquet**: Supports **schema evolution** by merging schemas during read. Must enable `mergeSchema=true`, but this can impact performance.
* **Delta Lake**: Provides better schema enforcement and evolution.

  * Use `MERGE SCHEMA` to evolve columns safely.
  * Supports column addition (but not deletion or type change by default).
  * Tracks schema versions in the transaction log.

**In my projects**, I prefer Delta Lake for evolving schemas because of its ACID guarantees and better schema compatibility controls.

---


### **10. What are the performance implications of using Python UDFs in PySpark?**

**Answer:**
Python UDFs (User-Defined Functions) introduce a performance bottleneck because they:

* **Bypass the Catalyst Optimizer**, meaning no query optimization can be applied to the UDF logic.
* Require **data to be serialized and transferred** from the JVM to the Python process (and back), leading to high overhead.
* Are not vectorized, so they operate **row-by-row**, making them slower than native functions.

**Summary:** Use Python UDFs only when absolutely necessary—prefer built-in Spark SQL functions or SQL expressions when possible.

---

### **11. Describe a scenario where a UDF was the only solution. How did you implement and optimize it?**

**Answer:**
**Scenario:** In one of my projects, IoT devices were sending nested JSON strings in a single column. The JSON structure varied slightly based on device type, and we had to normalize and extract specific sensor values with fallback logic.

**Why UDF was needed:** Spark SQL functions couldn’t handle the complex conditional parsing and schema irregularities.

**Implementation:**

```python
import json
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def parse_sensor(json_str):
    try:
        data = json.loads(json_str)
        return data.get("sensorValue", None)
    except Exception:
        return None

sensor_udf = udf(parse_sensor, StringType())
df = df.withColumn("sensor_value", sensor_udf(df["payload"]))
```

**Optimization:**

* Used **`@udf`** annotation instead of lambda for better serialization.
* Filtered out nulls and invalid JSON before applying the UDF.
* Isolated UDF logic in a dedicated script and unit-tested it for correctness.

---

### **12. Have you used Pandas UDFs (vectorized UDFs)? How do they differ from regular UDFs in terms of performance?**

**Answer:**
Yes, I’ve used **Pandas UDFs** (aka vectorized UDFs) to significantly improve performance when applying complex transformations.

**Differences from regular UDFs:**

* Pandas UDFs operate on **batches of data** (Pandas Series), enabling **vectorized operations**.
* They minimize JVM-Python serialization overhead using **Apache Arrow**.
* Are generally **10–100x faster** than regular UDFs for numeric or text-based batch processing.

**Example:**

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def normalize_column(col: pd.Series) -> pd.Series:
    return (col - col.mean()) / col.std()

df = df.withColumn("normalized", normalize_column(df["metric"]))
```

---

### **13. How do you handle null-safe operations inside a UDF?**

**Answer:**
Nulls can break UDFs if not handled explicitly because PySpark passes `None` values to the UDF, which can cause errors during processing.

**Approach:**

* Add `if x is not None` or use `try/except` blocks in the UDF.
* Use **Spark SQL filters** to exclude nulls before applying the UDF when appropriate.

**Example:**

```python
@udf("string")
def safe_transform(val):
    if val is None:
        return "Unknown"
    return val.upper()
```

Alternatively, use **`when()` and `otherwise()`** before applying a UDF if logic can be expressed using native functions.

---

### **14. Can you write a UDF to validate and transform a complex JSON field in a DataFrame?**

**Answer:**
Yes. Here’s an example of a UDF that validates a nested JSON field and extracts required fields with default values:

```python
import json
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define schema for the output
schema = StructType([
    StructField("device_id", StringType()),
    StructField("temperature", DoubleType()),
    StructField("status", StringType())
])

@udf(schema)
def parse_json(json_str):
    try:
        data = json.loads(json_str)
        return {
            "device_id": data.get("device", {}).get("id", "unknown"),
            "temperature": float(data.get("metrics", {}).get("temp", 0.0)),
            "status": data.get("status", "inactive")
        }
    except Exception:
        return {"device_id": "error", "temperature": 0.0, "status": "error"}

df = df.withColumn("parsed", parse_json(df["json_column"]))
df = df.select("parsed.*")
```

---

### **15. Explain when you would replace a UDF with Spark SQL expressions or built-in functions.**

**Answer:**
I replace UDFs with Spark SQL expressions or built-in functions when:

* The logic can be expressed using functions like `when()`, `regexp_extract()`, `split()`, `coalesce()`, etc.
* Performance is critical, especially on large datasets or repeated transformations.
* The transformation is **stateless** and can be vectorized or optimized by Catalyst.

**Real example:**
I replaced a UDF that extracted domain names from URLs with:

```python
from pyspark.sql.functions import regexp_extract
df = df.withColumn("domain", regexp_extract("url", "https?://(www\\.)?([^/]+)", 2))
```

This improved performance and enabled better query planning.

---


### **16. How do you manage and schedule jobs in Azure Databricks?**

**Answer:**
In Azure Databricks, I manage and schedule jobs using the **Databricks Jobs UI** or via **Jobs API** and **Terraform** for infrastructure-as-code. Each job consists of:

* **Tasks**: Notebooks, JARs, Python scripts, or Delta Live Tables.
* **Dependencies**: I use task dependencies to create multi-step workflows.
* **Schedules**: Configured using **cron expressions** for time-based triggers or **event-driven** via the REST API or Azure Data Factory.

**Best Practices I follow:**

* Use **job clusters** for cost-efficiency.
* Enable **retry policies** and **email/alert notifications**.
* Use **parameterization** to pass dynamic values to notebooks.
* Monitor job runs via **Job Run history** and **Azure Log Analytics**.

---

### **17. What is the difference between interactive clusters and job clusters in Databricks?**

**Answer:**

| Feature         | **Interactive Cluster**                | **Job Cluster**                                |
| --------------- | -------------------------------------- | ---------------------------------------------- |
| Purpose         | Used for development, ad hoc analysis  | Used for scheduled jobs or workflows           |
| Lifecycle       | Manually started/stopped by users      | Auto-created for each job run, auto-terminates |
| Sharing         | Shared by multiple users or notebooks  | Dedicated to a single job run                  |
| Cost Efficiency | Can remain idle if not auto-terminated | More cost-effective due to ephemeral nature    |

**When I use each:**

* Interactive: During development or testing phases.
* Job: For production jobs with **automated scheduling**, for better isolation and scalability.

---

### **18. Explain Unity Catalog and how it enhances security and governance in Databricks.**

**Answer:**
**Unity Catalog** is Databricks' unified data governance layer that provides **centralized access control**, **data lineage**, and **auditability** across workspaces.

**Key Features:**

* **Fine-grained access control**: Down to tables, columns, and rows using ANSI SQL `GRANT` syntax.
* **Centralized metastore**: Replaces per-workspace Hive metastores.
* **Data lineage**: Tracks where data comes from and how it is transformed.
* **Integration with Azure AD**: Uses identity federation and supports service principals and groups.

**Impact:**
Unity Catalog simplifies **RBAC**, enables **secure data sharing** (e.g., Delta Sharing), and enforces **data ownership boundaries** across teams or departments.

---

### **19. How do you implement CI/CD in a Databricks environment using notebooks and Git integration?**

**Answer:**
My CI/CD approach in Databricks involves:

1. **Git Integration**:

   * Connect notebooks to **Git repos** (e.g., Azure DevOps, GitHub).
   * Use Git branches for development, QA, and production environments.

2. **CI/CD Tools**:

   * Use **Azure DevOps Pipelines** or **GitHub Actions** to automate:

     * Unit testing (e.g., with `pytest`)
     * Linting (e.g., `flake8`)
     * Deployment of notebooks/jobs using **Databricks CLI** or **Databricks Terraform provider**.

3. **Deployment Strategy**:

   * Use **notebook exports** (`.dbc` or `.py` files).
   * Maintain **job definitions and cluster configs** as code (YAML/JSON).
   * Separate **dev**, **test**, and **prod** workspaces or use **multi-branch** pipelines for environment-specific deployments.

---

### **20. Describe your approach to debugging a failing notebook in a Databricks job.**

**Answer:**
My debugging process typically includes:

1. **Examine Job Run Output**:

   * Check **stdout**, **stderr**, and **error tracebacks** in the job run UI.
   * Identify the failing task and cell.

2. **Reproduce the issue**:

   * Run the notebook **interactively** with the same input parameters and cluster configuration.

3. **Check dependencies**:

   * Ensure **external libraries** are available (PyPI/JAR/whl).
   * Validate file paths and table names, especially when accessing ADLS or Delta tables.

4. **Use logging and assertions**:

   * Add **`print()`**, **`display()`**, or **custom logs** to narrow down issues.
   * Use **assertions** to validate inputs or preconditions early.

5. **Version Control**:

   * Compare with previous working versions via Git for regression issues.

---

### **21. How do you manage secrets and credentials securely within Databricks?**

**Answer:**
I use **Databricks Secrets** stored in **Secret Scopes** to manage sensitive data securely.

**Practices I follow:**

* Store credentials (e.g., Azure Storage keys, API tokens) in **secret scopes** (either backed by **Databricks** or **Azure Key Vault**).
* Access secrets in notebooks using:

  ```python
  dbutils.secrets.get(scope="my-scope", key="my-key")
  ```
* Avoid hardcoding secrets in notebooks or configs.
* Use **Key Vault-backed scopes** for centralized secret management.
* Enforce **RBAC** for scope access using Unity Catalog and workspace permissions.

---


### **22. What are the key features that Delta Lake provides over traditional Parquet formats?**

**Answer:**
Delta Lake builds on top of Parquet and provides key **ACID transactional** features that are missing in traditional data lakes. The major improvements include:

| Feature                        | Delta Lake                                  | Traditional Parquet          |
| ------------------------------ | ------------------------------------------- | ---------------------------- |
| ACID Transactions              | ✅ Yes (via transaction log)                 | ❌ No                         |
| Schema Evolution & Enforcement | ✅ Yes                                       | ❌ Partial (only reader-side) |
| Time Travel                    | ✅ Yes (`VERSION AS OF` / `TIMESTAMP AS OF`) | ❌ No                         |
| Upserts & Deletes              | ✅ Yes (`MERGE`, `UPDATE`, `DELETE`)         | ❌ No                         |
| File Compaction                | ✅ `OPTIMIZE` command                        | ❌ Manual                     |
| Performance Tuning             | ✅ ZORDER, Data skipping, Caching            | ❌ Limited                    |

**Summary:** Delta Lake brings data lake **reliability, governance, and performance** to open-format storage.

---

### **23. Explain the Delta Lake transaction log (`_delta_log`). How does it ensure ACID compliance?**

**Answer:**
The `_delta_log` is a **JSON-based transaction log** stored alongside Delta tables. It records every change (add, remove, metadata, commit) in a **serializable, append-only format**, ensuring **ACID properties**:

* **Atomicity**: All operations in a transaction either succeed together or are rolled back.
* **Consistency**: Each write produces a valid Delta state.
* **Isolation**: Writes use optimistic concurrency; read operations see a consistent snapshot.
* **Durability**: Once committed, logs are persisted on storage (like ADLS or S3).

Each log file is named incrementally (`00000000000000000010.json`), and readers build a snapshot by reading the latest version.

---

### **24. How does time travel work in Delta Lake? Give a use case where you applied it.**

**Answer:**
Delta Lake supports **time travel** via `VERSION AS OF` or `TIMESTAMP AS OF`, allowing queries to access historical snapshots.

**Example:**

```sql
SELECT * FROM my_table VERSION AS OF 15;
-- or
SELECT * FROM my_table TIMESTAMP AS OF '2024-06-15 00:00:00';
```

**Use Case (Real-world):**
In a project involving daily ingested sales data, an accidental overwrite corrupted the data. We used:

```sql
CREATE OR REPLACE TABLE sales AS
SELECT * FROM sales VERSION AS OF 120;
```

This helped **roll back** to a consistent state within seconds, avoiding downtime.

---

### **25. What is the difference between MERGE, UPDATE, and UPSERT operations in Delta Lake?**

**Answer:**

| Operation | Description                                            | Use Case                               |
| --------- | ------------------------------------------------------ | -------------------------------------- |
| `UPDATE`  | Modifies rows matching a condition                     | Fixing records with wrong status codes |
| `MERGE`   | Conditional `INSERT`, `UPDATE`, and `DELETE` (Upsert)  | Change data capture (CDC) pipelines    |
| `UPSERT`  | Informal term for a `MERGE` that handles insert/update | Same as MERGE (technically the same)   |

**Example of `MERGE` (Upsert):**

```sql
MERGE INTO target_table t
USING updates u
ON t.id = u.id
WHEN MATCHED THEN UPDATE SET t.name = u.name
WHEN NOT MATCHED THEN INSERT (id, name) VALUES (u.id, u.name)
```

---

### **26. How do you optimize Delta tables for read and write performance? (e.g., ZORDER, OPTIMIZE, VACUUM)**

**Answer:**
**Performance Tuning Techniques:**

* **OPTIMIZE**: Compacts small files into larger ones for faster scans.

  ```sql
  OPTIMIZE sales;
  ```

* **ZORDER BY**: Co-locates related data for better skipping during reads (especially with filters).

  ```sql
  OPTIMIZE sales ZORDER BY (region, product_id);
  ```

* **VACUUM**: Removes old files no longer in the current snapshot (default retention is 7 days).

  ```sql
  VACUUM sales RETAIN 168 HOURS;
  ```

* **Partitioning**: Choose partition columns with low cardinality (e.g., `date`, `region`).

* **Auto Optimize & Auto Compaction**: Enable table properties to automate file management.

  ```sql
  ALTER TABLE my_table SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
  );
  ```

---

### **27. What are the challenges you faced while enabling schema evolution and enforcement in Delta Lake?**

**Answer:**

**Challenges:**

* **Unexpected schema drift** from inconsistent upstream sources (e.g., missing fields or extra nested columns).
* Schema changes in nested structures are **not automatically handled** unless `MERGE`-based.
* Enabling **column addition** is easy, but **column renaming or data type changes** can break pipelines.

**How I addressed them:**

* Enabled **schema evolution** explicitly:

  ```python
  df.write.option("mergeSchema", "true").format("delta").mode("append").save(path)
  ```
* Used **Delta table constraints and enforcement** to reject incompatible data.
* Established **data contracts and validations** at ingestion layer to avoid uncontrolled schema evolution.
* Used **schema merging** in ETL pipelines cautiously and documented schema expectations.

---
