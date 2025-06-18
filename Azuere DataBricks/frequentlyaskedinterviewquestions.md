Here are **20 frequently asked interview questions and answers on Databricks** tailored for a **Data Engineer** role. These questions cover practical scenarios, architecture, Spark optimizations, integrations, and real-world usage in a production environment.

---

### ✅ **Databricks Interview Questions & Answers for Data Engineers**

---

### **1. What is Databricks? How is it different from Apache Spark?**

**Answer:**
Databricks is a unified data analytics platform built on top of Apache Spark. It provides collaborative notebooks, optimized Spark engine, ML lifecycle management (MLflow), Delta Lake support, and native integrations with Azure, AWS, and GCP.
Unlike raw Spark, Databricks offers simplified cluster management, version control, security, and performance enhancements.

---

### **2. How do you ingest data into Databricks from various sources?**

**Answer:**
Databricks supports ingestion via:

* Mounting Azure Data Lake (ADLS Gen2) or S3
* Using Auto Loader for continuous ingestion
* REST APIs
* Structured streaming
* JDBC connectors
* Databricks connectors for Snowflake, Kafka, Event Hubs, etc.

---

### **3. What is Delta Lake and how does it enhance data reliability in Databricks?**

**Answer:**
Delta Lake is an open-source storage layer that brings **ACID transactions**, **schema enforcement**, **time travel**, and **data versioning** to data lakes. In Databricks, it helps maintain consistency, enables rollbacks, and supports efficient upserts and deletes using `MERGE INTO`.

---

### **4. How would you implement Slowly Changing Dimensions (SCD) Type 1/2 in Databricks?**

**Answer:**
Use **Delta Lake’s `MERGE INTO`** for SCD implementation:

* **Type 1**: Overwrite existing records using `UPDATE`.
* **Type 2**: Use `MERGE` with `INSERT` for new rows and `UPDATE` to mark existing rows as historical (`IsCurrent = false`, `EndDate` set).

---

### **5. Explain the differences between Databricks Jobs, Notebooks, and Workflows.**

**Answer:**

* **Notebooks**: Interactive development interface (supports Python, SQL, Scala).
* **Jobs**: Scheduled or triggered tasks that run Notebooks or JARs.
* **Workflows**: Orchestration feature (like Airflow) to chain multiple jobs with dependencies, parameters, and retries.

---

### **6. What are the benefits of using Databricks Auto Loader?**

**Answer:**

* Efficient incremental ingestion from cloud storage.
* Automatically detects and processes new files.
* Supports schema evolution and error handling.
* Scalable and fault-tolerant (uses checkpointing and file notification APIs).

---

### **7. How do you handle schema evolution in Delta Lake?**

**Answer:**
Use `MERGE` or `WRITE` options with:

```python
.option("mergeSchema", "true")
```

Or use `ALTER TABLE` to explicitly evolve schema. Delta ensures consistency and tracks changes.

---

### **8. What is Z-Ordering in Databricks Delta?**

**Answer:**
Z-Ordering is a multi-dimensional clustering technique that optimizes file layout to improve **query performance** by colocating related information in the same set of files. Use `OPTIMIZE ... ZORDER BY (col1, col2)`.

---

### **9. What are best practices for partitioning in Databricks?**

**Answer:**

* Partition by columns with **high cardinality but limited range** (e.g., `year`, `month`, `region`).
* Avoid too many small files (over-partitioning).
* Use `OPTIMIZE` and `VACUUM` for file management.

---

### **10. How do you tune Spark performance in Databricks?**

**Answer:**

* Use **Delta Lake** to reduce shuffling and optimize file sizes.
* Apply **caching** with `.cache()` or `.persist()`.
* Tune `spark.sql.shuffle.partitions` and `spark.executor.memory`.
* Use **broadcast joins** for small dimension tables.
* Monitor jobs in **Spark UI**.

---

### **11. What is the difference between a managed and unmanaged table in Databricks?**

**Answer:**

* **Managed table**: Databricks manages both data and metadata.
* **Unmanaged table**: Only metadata is managed; data stays at specified location (like ADLS or S3).

---

### **12. How do you perform streaming ETL in Databricks?**

**Answer:**
Use `readStream` and `writeStream` APIs with sources like Kafka, Event Hub, or Auto Loader, and sinks like Delta, Kafka, or SQL DB. Leverage watermarking, checkpointing, and structured streaming.

---

### **13. How does Databricks handle security and access control?**

**Answer:**

* Integration with **Azure Active Directory (AAD)**.
* Fine-grained **access control** on notebooks, clusters, tables.
* **Unity Catalog** for centralized data governance (RBAC, lineage).
* Token-based or OAuth 2.0 for secure API access.

---

### **14. What is Unity Catalog in Databricks?**

**Answer:**
Unity Catalog is a unified governance solution for all data and AI assets in Databricks. It enables centralized access control, data lineage, audit logging, and cross-workspace sharing.

---

### **15. How do you handle error logging and monitoring in Databricks jobs?**

**Answer:**

* Use `try-except` blocks in notebooks.
* Enable job-level **alerts** and **email notifications**.
* Monitor via **Databricks job logs**, **Spark UI**, and **Azure Monitor**.
* Push logs to **Log Analytics** or **Splunk**.

---

### **16. How can you schedule and orchestrate data pipelines in Databricks?**

**Answer:**

* Use **Databricks Jobs + Workflows**.
* Trigger from **Azure Data Factory**, **Airflow**, or **Event Grid**.
* Implement dependencies, retries, and parameter passing.

---

### **17. How do you join two large datasets in Spark efficiently?**

**Answer:**

* Use **broadcast join** when one dataset is small.
* Repartition on join keys to avoid shuffling.
* Filter early, cache intermediate results.
* Consider **bucketing** or **Z-ordering**.

---

### **18. What is the function of the `%run` command in Databricks?**

**Answer:**
`%run ./path/to/notebook` is used to **import and execute another notebook**, sharing variables and context across notebooks in the same job.

---

### **19. Explain how checkpointing works in streaming pipelines.**

**Answer:**
Checkpointing stores metadata and progress (offsets) of streaming jobs in a persistent location (e.g., DBFS or ADLS), enabling fault tolerance and recovery after failure.

---

### **20. How do you handle late-arriving data in streaming jobs?**

**Answer:**
Use **watermarks** to set event-time thresholds:

```python
.withWatermark("eventTime", "15 minutes")
```

Allows handling of late data up to defined time without unbounded state growth.

---

Let me know if you’d like:

* Scenario-based questions
* More questions on ML or SQL in Databricks
* An Excel or PDF export for interview prep
