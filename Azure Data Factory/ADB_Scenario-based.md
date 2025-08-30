# Databricks Scenario-Based Interview Questions & Answers

---

## 🔹 Beginner-Level (1–10)

### 1. **Scenario:** Your team just got access to Azure Databricks. You need to explain to a junior teammate what Databricks is and why we use it.

**Answer:**
Azure Databricks is a **cloud-based unified analytics platform** built on Apache Spark, integrated with Azure services. It’s used for **big data processing, ETL, machine learning, and analytics**.

* Key benefits:

  * **Scalability**: Auto-scaling clusters handle massive data volumes.
  * **Collaboration**: Notebooks allow data scientists, engineers, and analysts to work together.
  * **Azure Integration**: Native integration with ADLS, Synapse, ADF, Key Vault, Event Hubs, etc.
* Use cases: ETL pipelines, ML model training, streaming analytics, data lakehouse implementation.

---

### 2. **Scenario:** Your manager asks why Databricks notebooks are preferred over just running Spark locally.

**Answer:**

* Databricks manages **cluster setup, scaling, and Spark configuration** automatically, removing DevOps overhead.
* Offers **collaboration** and **version control** within notebooks.
* Provides **enterprise security** (RBAC, VNet injection, Azure AD integration).
* Built-in **integrations** with Delta Lake, MLflow, and Azure ecosystem make development faster and more secure.

---

### 3. **Scenario:** You are onboarding new data engineers. How would you explain Databricks clusters to them?

**Answer:**
A Databricks cluster is a **set of compute resources (VMs)** for running Spark jobs:

* **Driver node**: Orchestrates tasks.
* **Worker nodes**: Execute Spark tasks.
* **Cluster types**:

  * **Interactive**: Used for notebooks and exploration.
  * **Job clusters**: Spin up for scheduled jobs, terminate after.
  * **High-Concurrency**: Multi-user workloads.
* Clusters auto-scale based on load.

---

### 4. **Scenario:** The team wants to move from a traditional SQL server to Databricks. How would you justify the migration?

**Answer:**

* Databricks scales horizontally for **big data workloads**.
* Supports **structured, semi-structured, and unstructured** data.
* Enables **data lakehouse** design, combining data lake scalability with warehouse performance.
* Integrates easily with BI tools and Azure Synapse for reporting.
* Offers ML & AI capabilities natively.

---

### 5. **Scenario:** You are asked to ingest data from an Azure Blob Storage container. How would you do it?

**Answer:**

```python
spark.conf.set("fs.azure.account.key.<storage_account>.blob.core.windows.net", "<access_key>")

df = spark.read.format("csv") \
    .option("header", "true") \
    .load("wasbs://<container>@<storage_account>.blob.core.windows.net/path/to/file.csv")

df.display()
```

Alternatively, use **Azure Data Lake Storage Gen2** and **Azure Service Principal** for secure access.

---

### 6. **Scenario:** Your pipeline keeps failing because of a schema change in the source data. What would you do?

**Answer:**

* Use **Delta Lake’s schema evolution**:

```python
df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("overwrite") \
    .save("/mnt/delta/table")
```

* Implement **schema validation** and **data contracts** to proactively detect changes.
* Create **quarantine tables** for unexpected columns.

---

### 7. **Scenario:** You’re asked to connect Databricks to Azure Key Vault for secrets. How would you achieve this?

**Answer:**

1. Store credentials in **Azure Key Vault**.
2. Create a **Databricks Secret Scope** linked to Key Vault:

```bash
databricks secrets create-scope --scope myScope --scope-backend-type AZURE_KEYVAULT \
--resource-id <KeyVaultResourceId> --dns-name <KeyVaultDNS>
```

3. Access secrets in Spark:

```python
dbutils.secrets.get(scope="myScope", key="storageKey")
```

---

### 8. **Scenario:** A teammate wants to query data using SQL, but your pipeline uses PySpark. How do you help them?

**Answer:**
Databricks supports **SQL, Python, R, Scala** interchangeably. You can create a **SQL cell** in the notebook using:

```sql
%sql
SELECT COUNT(*) FROM delta.`/mnt/delta/table`
```

Or register a temporary view in PySpark:

```python
df.createOrReplaceTempView("table_name")
```

---

### 9. **Scenario:** You want to optimize reading large JSON data. How would you do it?

**Answer:**

* Use **multi-line JSON option**:

```python
df = spark.read.option("multiline", "true").json("path")
```

* **Infer schema once** and cache for performance.
* Store parsed data as **Delta tables** for future queries.

---

### 10. **Scenario:** The team wants a “single source of truth” for analytics. How would Databricks help?

**Answer:**
Use the **Lakehouse architecture** with:

* Raw data in **Bronze layer**.
* Cleansed data in **Silver layer**.
* Aggregated data in **Gold layer** for BI tools.
  This enables **governance, scalability, and high-performance querying**.

---

## 🔹 Intermediate-Level (11–25)

### 11. **Scenario:** You need to implement incremental data loading. What’s your approach?

**Answer:**
Use **Delta Lake MERGE** for incremental updates:

```python
deltaTable.alias("t").merge(
    sourceDF.alias("s"),
    "t.id = s.id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

Track **watermarks** or use **Change Data Capture (CDC)** from source systems.

---

### 12. **Scenario:** Your pipeline is failing due to skewed data. How would you fix it?

**Answer:**

* Use **salting** (adding random keys to distribute skewed keys).
* **Repartition** or **coalesce** data to balance partitions.
* Use `spark.sql.adaptive.enabled=true` to enable **Adaptive Query Execution**.

---

### 13. **Scenario:** Your job cluster takes a long time to start. What would you recommend?

**Answer:**

* Enable **Cluster Pools** to pre-warm VMs.
* Use **smaller clusters** for dev, larger clusters for production.
* Use **Autoscaling** to reduce idle time.

---

### 14. **Scenario:** A data analyst needs Power BI access to Databricks. How do you enable it?

**Answer:**

* Configure **Databricks SQL Endpoint** and generate a **JDBC/ODBC connection string**.
* Use **Azure Active Directory (AAD) authentication**.
* Analysts can connect using **Power BI Databricks Connector**.

---

### 15. **Scenario:** Your team needs to implement CI/CD for Databricks notebooks.

**Answer:**

* Use **Databricks Repos** with GitHub/Azure DevOps integration.
* Store notebooks as `.py` files in Git.
* Deploy using **Databricks CLI or Terraform**.
* Use **Databricks Jobs API** for automated deployment.

---

### 16. **Scenario:** A Spark job fails with an “Out of Memory” error. What’s your strategy?

**Answer:**

* Optimize data partitioning (`repartition`, `coalesce`).
* Cache only necessary data.
* Increase **executor memory** in cluster configuration.
* Consider **data pruning** and `filter pushdown`.

---

### 17. **Scenario:** You need to schedule ETL jobs in Databricks.

**Answer:**
Use **Databricks Jobs** to schedule notebooks or JAR tasks.

* Define **clusters, libraries, retry policies, email alerts**.
* Integrate with **Azure Data Factory** or **Airflow** for orchestration.

---

### 18. **Scenario:** The client requires data lineage. How do you implement it?

**Answer:**

* Use **Unity Catalog** to track **table-level and column-level lineage**.
* Enable **table auditing and logging** with Delta.
* Integrate with **Purview** for end-to-end lineage.

---

### 19. **Scenario:** You need to process real-time streaming data from Event Hubs.

**Answer:**

```python
eventHubConfig = {
  "eventhubs.connectionString": "<conn_str>"
}

df = spark.readStream.format("eventhubs").options(**eventHubConfig).load()
df.writeStream.format("delta").outputMode("append").start("/mnt/delta/stream")
```

---

### 20. **Scenario:** You have multiple environments (dev, test, prod). How would you handle configurations?

**Answer:**

* Store environment variables in **Key Vault**.
* Use **databricks-cli** with environment-specific workspaces.
* Parameterize notebooks using **widgets**.
* Deploy via **Terraform or ARM templates**.

---

### 21. **Scenario:** Your job writes duplicate data. How would you fix it?

**Answer:**

* Use **Delta MERGE** or **dropDuplicates()**.
* Enforce **primary keys** using Delta constraints:

```sql
ALTER TABLE my_table ADD CONSTRAINT pk PRIMARY KEY (id);
```

---

### 22. **Scenario:** How do you optimize Delta table performance?

**Answer:**

* Use **OPTIMIZE** with Z-ORDER for query acceleration:

```sql
OPTIMIZE my_table ZORDER BY (customer_id)
```

* **VACUUM** old files.
* Use **Delta caching** and partition pruning.

---

### 23. **Scenario:** You need to mask sensitive data. How would you do it?

**Answer:**

* Use **Unity Catalog column-level security**.
* Apply **dynamic views** to hide PII.
* Implement **hashing or encryption** for sensitive fields.

---

### 24. **Scenario:** You’re asked to create a Lakehouse in Databricks. What’s your approach?

**Answer:**

* Store raw data in **Bronze** (raw), curated data in **Silver** (cleaned), aggregated metrics in **Gold**.
* Use **Delta Lake** for reliability.
* Govern access using **Unity Catalog**.
* Expose Gold tables via **Databricks SQL endpoints**.

---

### 25. **Scenario:** Your notebooks are unorganized. How do you structure a production-ready project?

**Answer:**

* Separate **ETL code into modular notebooks**.
* Use a **medallion architecture** folder structure:

  ```
  /notebooks/bronze
  /notebooks/silver
  /notebooks/gold
  ```
* Parameterize paths and secrets.
* Store reusable functions in **Python modules** or **Databricks Repos**.

---

## 🔹 Advanced-Level (26–40)

### 26. **Scenario:** Your Delta table is very large. How do you handle performance degradation?

**Answer:**

* Run **OPTIMIZE** with Z-ORDER regularly.
* Use **data skipping** indexes.
* Compact small files with **auto-optimize**.
* Implement **partitioning** based on query patterns.

---

### 27. **Scenario:** A compliance audit requires detailed access logs. How do you achieve this?

**Answer:**

* Enable **Unity Catalog audit logs**.
* Capture cluster logs in **Azure Monitor / Log Analytics**.
* Enable **table access auditing** with Databricks SQL.

---

### 28. **Scenario:** You need to implement ML training in Databricks. How would you design it?

**Answer:**

* Use **MLflow** for experiment tracking and model registry.
* Train ML models in **PySpark or TensorFlow on Databricks**.
* Use **Feature Store** to reuse engineered features.
* Deploy models as **MLflow endpoints**.

---

### 29. **Scenario:** How would you handle data sharing with external partners?

**Answer:**

* Use **Delta Sharing** to securely share tables.
* Provide read-only access via **secure endpoints**.
* Audit and revoke access as needed.

---

### 30. **Scenario:** A new data source sends nested JSON. How do you flatten it?

**Answer:**

```python
from pyspark.sql.functions import col, explode

df_flat = df.select(
    col("id"),
    col("name"),
    explode(col("items")).alias("item")
)
```

* Use `pyspark.sql.functions` to handle deeply nested structures.

---

### 31. **Scenario:** Your Spark job is slow. How do you troubleshoot?

**Answer:**

* Check **Spark UI** for stage bottlenecks.
* Look for **wide transformations** (shuffles).
* Optimize joins using **broadcast joins**.
* Enable **Adaptive Query Execution**.

---

### 32. **Scenario:** You must ensure data is ACID compliant. How does Delta Lake help?

**Answer:**

* Delta provides **ACID transactions** with commit logs.
* Supports **time travel** for rollback.
* Eliminates **data corruption** from concurrent writes.

---

### 33. **Scenario:** How do you secure Databricks at an enterprise scale?

**Answer:**

* Use **VNet injection** and **Private Link**.
* Integrate with **Azure AD** for RBAC.
* Enable **Unity Catalog** for data governance.
* Use **credential passthrough** for data access.

---

### 34. **Scenario:** Your team wants a fully automated data platform. What would you propose?

**Answer:**

* Use **ADF or Azure Synapse pipelines** for orchestration.
* Automate cluster lifecycle with **Databricks REST API or Terraform**.
* Implement **event-driven architecture** with Event Grid.
* Apply CI/CD with **Azure DevOps**.

---

### 35. **Scenario:** You need to migrate an on-prem Hadoop cluster to Databricks.

**Answer:**

* Migrate data to **ADLS Gen2**.
* Convert Hive tables to **Delta Lake**.
* Rewrite HiveQL to **Spark SQL**.
* Use **Databricks migration tools** for automation.

---

### 36. **Scenario:** How would you optimize storage costs in Databricks?

**Answer:**

* Use **Delta caching** to reduce redundant reads.
* Store raw data in **Parquet** or Delta.
* Enable **table retention policies**.
* Delete unused clusters and use **spot VMs**.

---

### 37. **Scenario:** A pipeline must handle 100 TB of data daily. What would you recommend?

**Answer:**

* Use **auto-scaling clusters** with **Photon** execution engine.
* Partition data effectively.
* Use **streaming ingestion** to avoid batch bottlenecks.
* Optimize tables with **Delta Lake**.

---

### 38. **Scenario:** How would you manage multiple teams’ data access?

**Answer:**

* Implement **Unity Catalog with data lineage**.
* Assign permissions at **catalog, schema, table, and column** levels.
* Use **Azure AD Groups** for RBAC.

---

### 39. **Scenario:** How do you test Databricks notebooks?

**Answer:**

* Write reusable functions in `.py` modules.
* Use **pytest** for unit tests.
* Run tests in **CI/CD pipelines** before deployment.
* Use **databricks-connect** to run tests locally.

---

### 40. **Scenario:** You must ensure high availability in Databricks. What’s your strategy?

**Answer:**

* Use **Job Clusters** for critical workloads (auto-restart).
* Deploy across **multiple availability zones**.
* Enable **checkpointing** in streaming jobs.
* Use **Delta Lake** for data reliability.

---
