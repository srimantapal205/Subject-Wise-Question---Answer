# Databricks Fundamentals

### 1. What is Databricks, and how does it differ from traditional big data processing frameworks?
**Answer:** Databricks is a cloud-based data analytics and machine learning platform built on Apache Spark. It provides a managed environment that simplifies big data processing, data engineering, and machine learning.

Differences from traditional big data frameworks:

|Feature|	Databricks	|Traditional Big Data Frameworks (e.g., Hadoop, On-Prem Spark)|
|-------|--------------|------------------------------------------------------------|
|Cluster Management|	Fully managed, auto-scaling	|Manual setup and scaling|
|Performance|	Optimized with Photon Engine and Delta Lake |	Performance tuning required|
|Ease of Use|	Interactive Notebooks, SQL, Python, R	|Complex configuration|
|Cost Efficiency	|Optimized cluster utilization|	Fixed infrastructure costs|
|Security & Governance |	Built-in RBAC, Unity Catalog	|Requires additional security tools|
|Integration|	Native integrations with cloud storage & services	|Needs manual integration|


---

### 2. What are the key components of the Databricks architecture?
**Answer:**
Databricks has several key components that enable efficient big data processing:

1. **Workspace** – A collaborative environment for data engineers, analysts, and scientists.
2. **Clusters** – Managed Apache Spark clusters that auto-scale based on workload.
3. **Notebooks** – Interactive notebooks supporting Python, Scala, SQL, and R.
4. **Databricks SQL** – Optimized SQL engine for running BI queries.
5. **Jobs (Workflows)** – Automates and schedules pipelines.
6. **Delta Lake** – A storage layer with ACID transactions for reliability.
7. **MLflow** – Machine learning lifecycle management.
8. **Unity Catalog** – Centralized data governance and access control.


---

### 3. Explain the differences between Databricks and Azure Synapse Analytics.
**Answer:**

| Feature|	Databricks|	Azure Synapse Analytics|
|----------------|--------------|----------------------------|
| Core Technology|	Apache Spark	| SQL-based MPP (Massively Parallel Processing)|
| Best Use Case|	Data engineering, ML, real-time processing |	Data warehousing, BI reporting |
| Performance | Optimized for large-scale transformations |	Optimized for analytical queries|
| Storage Format	| Delta Lake |	Parquet, CSV, JSON|
| Scalability	| Dynamic auto-scaling clusters	| Dedicated or serverless pools|
| Cost Model	| Pay-as-you-go, optimized clusters	| Serverless and provisioned pricing|
| SQL Support	| Databricks SQL (Spark SQL)	| T-SQL (Synapse SQL)|
| Streaming Support	| Yes, via Structured Streaming	| Limited|
| ML & AI Support	| Strong MLflow integration| 	Basic ML capabilities|


---

### 4. What is the role of Databricks Workflows (formerly Jobs) in automation?|
**Answer:**

Databricks Workflows (previously known as Jobs) enable automation and scheduling of ETL pipelines, data transformations, machine learning training, and batch processing.

**Key features:**

  ✅ **Schedule Tasks** – Automate notebooks, JAR files, and Python scripts.

  ✅ **Task Dependencies** – Define execution order and dependencies.

  ✅ **Multi-Task Workflows** – Run multiple tasks in a single job.

  ✅ **Parameterized Execution** – Pass runtime parameters dynamically.

  ✅ **Error Handling & Alerts** – Send alerts on failures.

  ✅ **Integration with CI/CD** – Connect with Azure DevOps, GitHub, and Jenkins.


Example: Running a Databricks Job using the CLI


databricks jobs run-now --job-id 1234


---

### 5. How does Databricks handle cluster management and auto-scaling?
**Answer:**

Databricks offers intelligent cluster management and auto-scaling to optimize costs and performance.

**Cluster Management Features:**

- **Auto-scaling:** Adjusts resources based on workload demand.
- **Auto-termination:** Automatically shuts down idle clusters to save costs.
- **Spot Instances (AWS) / Low-priority VMs (Azure):** Reduces costs by using preemptible instances.
- **High Concurrency Mode:** Supports multiple users running jobs simultaneously.
- **Auto-Scaling Example:** When processing high volumes of data, Databricks automatically adds more nodes to improve performance. Once the job is completed, it removes excess nodes to save costs.


---

### 6. How do you read and write data in Databricks using different formats (CSV, Parquet, Delta Lake)?
**Answer:**

Databricks supports multiple file formats for reading and writing data, including CSV, Parquet, and Delta Lake.

✅ **Reading Data:**

    # Read CSV file
    df_csv = spark.read.format("csv").option("header", "true").load("/mnt/data/sample.csv")

    # Read Parquet file
    df_parquet = spark.read.format("parquet").load("/mnt/data/sample.parquet")

    # Read Delta Lake table
    df_delta = spark.read.format("delta").load("/mnt/data/sample-delta")

✅ **Writing Data:**


    # Write as CSV
    df.write.format("csv").option("header", "true").save("/mnt/output/sample.csv")

    # Write as Parquet
    df.write.format("parquet").save("/mnt/output/sample.parquet")

    # Write as Delta Lake
    df.write.format("delta").mode("overwrite").save("/mnt/output/sample-delta")

---

### 7. What is Delta Lake, and how does it enhance data reliability in Databricks?
**Answer:**
Delta Lake is an open-source storage layer that enhances data lakes by adding ACID transactions, schema enforcement, and time travel.

✅ Key Features of Delta Lake:

* ACID Transactions – Ensures data consistency even with concurrent writes.
* Schema Enforcement & Evolution – Prevents corrupt data from being inserted.
* Time Travel – Allows rollback to previous versions of data.
* Data Compaction – Merges small files to improve read performance.
* Scalability – Works on cloud storage (Azure, AWS, GCP).

✅ Delta Lake vs. Parquet Comparison:

| Feature	|Delta Lake	|Parquet|
|----------|-------------|--------|
| ACID Transactions|	✅ Yes	|❌ No|
| Schema Evolution|	✅ Yes|	❌ No|
| Time Travel|	✅ Yes|	❌ No|
| Data Compaction|	✅ Yes|	❌ No|
| Performance	|🚀 Faster (Optimized reads/writes)|	⚡ Slower|

---

### 8. Explain ACID transactions in Delta Lake.

**Answer:**
Delta Lake ensures data reliability with ACID transactions (Atomicity, Consistency, Isolation, Durability).

**🔹 Atomicity** – A transaction is either fully completed or fully rolled back.

**🔹 Consistency** – Ensures that data adheres to predefined constraints.

**🔹 Isolation** – Concurrent transactions do not interfere with each other.

**🔹 Durability** – Once committed, the changes are permanent.


✅ Example: Writing data with ACID transactions in Delta Lake


      from pyspark.sql.functions import *
      from delta.tables import DeltaTable

      delta_table = DeltaTable.forPath(spark, "/mnt/output/sample-delta")

      # Upsert new records (Merge Operation)
      delta_table.alias("old") \
        .merge(df_new.alias("new"), "old.id = new.id") \
        .whenMatchedUpdate(set={"old.value": "new.value"}) \
        .whenNotMatchedInsert(values={"id": "new.id", "value": "new.value"}) \
        .execute()

---

### 9. How does Databricks handle schema evolution in Delta Lake?
**Answer:**
Delta Lake supports schema evolution, allowing changes in table structure without breaking existing data.

✅ Handling Schema Evolution Automatically:

    df_new.write.format("delta").mode("append").option("mergeSchema", "true").save("/mnt/output/sample-delta")

The mergeSchema option ensures new columns in incoming data are added to the existing schema.

✅ Example: Schema Evolution with ALTER TABLE:
    
    ALTER TABLE delta.`/mnt/output/sample-delta` ADD COLUMNS (new_column STRING);

---

### 10. What are the different ways to perform ETL in Databricks?
**Answer:**
Databricks provides multiple approaches to extract, transform, and load (ETL) data.

| ETL Method|	Description|
|-----------|---------------|
| Databricks Notebooks|	Interactive development using Python, SQL, Scala.|
| Databricks Workflows (Jobs)|	Schedule and automate ETL pipelines.|
| Delta Live Tables (DLT)|	Declarative ETL framework that ensures reliability.|
| Apache Spark Structured Streaming|	Real-time data processing from Kafka, Event Hubs, etc.|
| Auto Loader|	Efficient ingestion of new files from cloud storage.|
| Databricks SQL|	Perform ETL transformations using SQL queries.|

✅ Example: Using Auto Loader for Streaming ETL


    df = spark.readStream \
        .format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .load("/mnt/raw-data")

    df.writeStream \
        .format("delta") \
        .option("checkpointLocation", "/mnt/checkpoints") \
        .start("/mnt/processed-data")

---

### 11. How do you optimize Spark jobs in Databricks?
**Answer:**
Optimizing Spark jobs in Databricks involves multiple techniques to reduce execution time and improve resource utilization.

✅ Best Practices for Spark Job Optimization:

* **Use Delta Lake** – Faster reads/writes compared to Parquet/CSV.
* **Enable Adaptive Query Execution (AQE)** – Dynamically optimizes queries at runtime.
* **Broadcast Smaller Tables in Joins** – Avoids expensive shuffle joins.
* **Optimize Data Partitioning** – Ensures balanced workload distribution.
* **Use Caching & Persistence** – Avoids recomputation of expensive transformations.
* **Optimize File Size** – Aim for 100–250 MB file sizes for efficient reads.
* **Use Columnar Formats** – Parquet and Delta improve compression and read speed.
* **Use Photon Engine (Databricks-specific)** – Vectorized execution engine for faster performance.
* **Reduce Shuffle Operations** – Minimize groupBy(), distinct(), and repartition().
* **Optimize Garbage Collection (GC)** – Use Executor Memory Tuning (spark.memory.fraction).

✅ Example: Enabling AQE for Auto-Optimization


    spark.conf.set("spark.sql.adaptive.enabled", "true")

---

### 12. Explain caching and persist operations in Spark.
**Answer:**

Caching and persistence store frequently accessed RDDs or DataFrames in memory/disk to speed up computations.

✅ Cache (df.cache())

* Stores data only in memory (RAM).
* Best for small-to-medium-sized datasets.

✅ Persist (df.persist(StorageLevel))

* Provides more control over storage levels (memory, disk, or both).
* Useful for large datasets where memory is limited.

✅ Storage Levels in persist()

* Storage Level	Description
* MEMORY_ONLY	Fastest, stores in RAM, recomputes if lost.
* MEMORY_AND_DISK	Stores in RAM, writes to disk if needed.
* DISK_ONLY	Stores data only on disk (slower).
* MEMORY_AND_DISK_SER	Serialized storage, saves memory but increases CPU usage.

✅ Example: Using Cache and Persist


      df.cache()  # Stores DataFrame in memory for faster access
      df.count()  # Triggers cache

      from pyspark import StorageLevel
      df.persist(StorageLevel.MEMORY_AND_DISK)  # Stores in both memory and disk

### 13. What is Adaptive Query Execution (AQE) in Spark, and how does it help?
**Answer:**
Adaptive Query Execution (AQE) dynamically optimizes query plans at runtime based on data characteristics.

✅ Key Features of AQE:

* **Dynamic Partition Pruning** – Reduces unnecessary data scans.
* **Optimized Join Strategies** – Converts shuffle joins into broadcast joins when possible.
* **Skew Join Handling** – Reduces data skew by splitting large partitions.
* **Coalescing Shuffle Partitions** – Reduces shuffle overhead for better performance.

✅ Example: Enabling AQE

      spark.conf.set("spark.sql.adaptive.enabled", "true")

✅ Example: Dynamic Partition Pruning


      SELECT * FROM sales
      JOIN customers
      ON sales.customer_id = customers.customer_id
      WHERE customers.region = 'North America';

AQE automatically prunes unnecessary partitions, reducing the amount of data scanned.


---

### 14. How can you improve the performance of joins in Spark?
**Answer:**

Joins can be expensive in Spark due to shuffle operations. The following techniques help optimize joins:

#### ✅ 1. Use Broadcast Joins for Small Tables

Avoids shuffle operations by copying small tables to each executor.

    from pyspark.sql.functions import broadcast
    df_large.join(broadcast(df_small), "id")

#### ✅ 2. Enable AQE for Auto-Optimization

    spark.conf.set("spark.sql.adaptive.enabled", "true")

#### ✅ 3. Use Bucketed and Sorted Joins

Pre-partition and sort tables before joining to reduce shuffle.

    df.write.format("parquet").bucketBy(10, "id").sortBy("id").saveAsTable("bucketed_table")

#### ✅ 4. Optimize Data Skew Handling

+ Identify skewed keys using:

    df.groupBy("id").count().orderBy("count", ascending=False).show()

+ If skew exists, use salting:

      df = df.withColumn("salt", (rand() * 10).cast("int"))
      df_large = df_large.withColumn("salt", (rand() * 10).cast("int"))
      df_large.join(df_small, ["id", "salt"])

#### ✅ 5. Reduce Number of Shuffle Partitions

    spark.conf.set("spark.sql.shuffle.partitions", "200")
    (Default is 200, can be adjusted based on dataset size.)


---

### 15. What are some best practices for partitioning data in Databricks?
**Answer:**
Partitioning helps improve query performance by allowing Spark to scan only relevant partitions.

✅ Best Practices for Partitioning:

**Choose the Right Partition Column:**

* Select a high-cardinality column to balance partition sizes.

Example: Good (date, region), Bad (gender, boolean fields).

**Avoid Too Many Small Partitions**

Ideal partition size: 100–250 MB (large enough for efficient reads).

Use **coalesce()** or **repartition()** to optimize partitions.

    df.repartition(10, "region")  # Creates 10 partitions based on 'region'
    df.coalesce(5)  # Reduces to 5 partitions

Optimize File Size for Performance

**Use Delta Lake’s OPTIMIZE command for compaction:**

  OPTIMIZE my_table ZORDER BY (customer_id)

**Use Dynamic Partition Pruning (DPP) for Faster Queries**

**Enabled by default in AQE (reduces unnecessary scans):** Partition Pruning for Faster Reads

    SELECT * FROM sales WHERE date >= '2024-01-01';

This query automatically prunes unnecessary partitions.



 ## Databricks Notebooks and Workflows

---

### 16. How do you schedule a Databricks notebook as a job?
**Answer:**
You can schedule a Databricks notebook as a job using Databricks Workflows (formerly Jobs).

✅ Steps to Schedule a Databricks Notebook as a Job:

* Go to Databricks UI → Workflows (Jobs) → Create Job.
* Click Add Task and select Notebook.
* Choose the notebook to run.
* Select the cluster for execution.
* Configure the schedule (daily, hourly, etc.).
* Click Create and enable email notifications if needed.


✅ Using Databricks CLI to Schedule a Job:

    databricks jobs create --json '{
      "name": "Daily Notebook Job",
      "tasks": [{
        "task_key": "run_notebook",
        "notebook_task": {
          "notebook_path": "/Users/myuser/ETL_notebook"
        },
        "new_cluster": {
          "spark_version": "12.2.x-scala2.12",
          "node_type_id": "Standard_DS3_v2",
          "num_workers": 2
        }
      }]
    }'


✅ Using REST API to Schedule a Job:


    curl -X POST https://<databricks-instance>/api/2.1/jobs/create \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Scheduled_ETL",
      "tasks": [{
        "task_key": "my_task",
        "notebook_task": { "notebook_path": "/Users/myuser/ETL_notebook" },
        "new_cluster": { "num_workers": 2, "spark_version": "12.2.x-scala2.12" }
      }]
    }'


---

### 17. What are widgets in Databricks, and how can they be used?
**Answer:**
Widgets allow users to pass parameters dynamically into notebooks for interactive execution.

✅ Types of Widgets:

* text – Accepts a single string input.
* dropdown – Allows selection from a predefined list.
* combobox – Similar to a dropdown but allows user input.
* multiselect – Allows multiple values to be selected.

✅ Example: Creating Widgets in Databricks Notebooks

    # Create a text widget for dynamic input
    dbutils.widgets.text("input_param", "default_value", "Enter a Parameter")

    # Create a dropdown widget
    dbutils.widgets.dropdown("job_type", "ETL", ["ETL", "ML", "Analytics"], "Select Job Type")

    # Retrieve widget values
    param_value = dbutils.widgets.get("input_param")
    job_type = dbutils.widgets.get("job_type")
    print(f"Input Parameter: {param_value}, Job Type: {job_type}")

✅ Use Case: Passing Parameters in Scheduled Jobs

Widgets allow passing dynamic values from Azure Data Factory or REST API when running notebooks.

---

### 18. How do you integrate Databricks with Azure Data Factory (ADF)?
**Answer:**
Azure Data Factory (ADF) can orchestrate Databricks by executing notebooks, JARs, or Python scripts.

✅ Steps to Integrate Databricks with ADF:

* Create an Azure Databricks Linked Service in ADF.
* Use "Databricks Notebook" or "Databricks Python" activity.
* Pass parameters to the notebook using ADF pipeline variables.
* Trigger Databricks jobs via ADF pipelines.

✅ Example: Running a Databricks Notebook in ADF

* Create a Linked Service in ADF to Databricks using:
* Access Token or Managed Identity authentication.
* Add a Databricks Notebook Activity in an ADF pipeline.
* Pass parameters dynamically:
* Define parameters in ADF pipeline → Notebook Activity → Parameters.

✅ Example: Passing Parameters from ADF to Databricks Notebook
    # Retrieve parameters passed from ADF
    
    param1 = dbutils.widgets.get("param1")
    param2 = dbutils.widgets.get("param2")
    print(f"Received params: {param1}, {param2}")

✅ Example: Calling Databricks Job from ADF Using REST API

    curl -X POST https://<databricks-instance>/api/2.1/jobs/run-now \
    -H "Authorization: Bearer <token>" \
    -d '{
      "job_id": 123,
      "notebook_params": { "input_file": "data.csv", "table_name": "sales" }
    }'

---

### 19. What are the different cluster types in Databricks?
**Answer:**
Databricks provides four main cluster types depending on workload needs.

#### Cluster Type	Description	Use Case
* Single Node	Runs on one machine (no workers)	ML models, small ETL jobs
* Standard	Supports multiple workers, auto-scaling	General-purpose workloads
* High Concurrency	Optimized for multi-user shared workloads	BI dashboards, SQL queries
* Job Clusters	Created per-job basis, auto-terminates	Scheduled jobs, ADF pipelines

✅ Example: Creating a Cluster Using REST API

    curl -X POST https://<databricks-instance>/api/2.0/clusters/create \
    -H "Authorization: Bearer <token>" \
    -d '{
      "cluster_name": "ETL-Cluster",
      "spark_version": "12.2.x-scala2.12",
      "node_type_id": "Standard_DS3_v2",
      "num_workers": 2
    }'

✅ Best Practices for Cluster Selection:

* Use High Concurrency Clusters for SQL analytics to reduce startup times.
* Use Job Clusters for ETL workflows to minimize costs.
* Enable Auto-Termination to prevent idle clusters from incurring charges.

---

### 20. How do you handle dependencies in a Databricks workflow?
**Answer:**
In Databricks Workflows, dependencies can be managed using:

* Library Management (pip install, Maven, DBFS storage).
* Task Dependencies in Workflows (define execution order).
* Databricks Repos (integrate with Git for version control).

✅ 1. Handling Python Dependencies in Notebooks


    # Install required packages
    %pip install pandas numpy

    # Verify installation
    import pandas as pd
    import numpy as np
    print(pd.__version__, np.__version__)

✅ 2. Using Databricks Repos for Version Control


    #Clone a GitHub repo in Databricks

    databricks repos create --path /Repos/my_project --url https://github.com/user/repo.git

✅ 3. Setting Dependencies in Workflows

Task A → Task B (dependent execution).
Example: Load data before running transformations.

    {
      "name": "ETL Workflow",
      "tasks": [
        {
          "task_key": "load_data",
          "notebook_task": { "notebook_path": "/Users/load_data" }
        },
        {
          "task_key": "transform_data",
          "depends_on": [ { "task_key": "load_data" } ],
          "notebook_task": { "notebook_path": "/Users/transform_data" }
        }
      ]
    }

✅ 4. Uploading External JARs for Scala/PySpark Dependencies


---

## Security & Access Control

---

### 21. What are the different ways to manage access control in Databricks?
**Answer:**
Databricks provides multiple access control mechanisms to secure data, notebooks, and clusters.

#### ✅ 1. Identity & Access Management (IAM)

+ Uses Azure Active Directory (AAD) or AWS IAM for authentication.
+ Supports Single Sign-On (SSO) via SAML, OAuth, and SCIM.
+ Role-Based Access Control (RBAC) allows fine-grained permission management.

#### ✅ 2. Databricks Access Control Lists (ACLs)

+ Controls workspace permissions (read/write/execute).
+ Manages cluster access (who can attach, restart, or manage clusters).
+ Defines notebook permissions (view/edit/run/manage).

#### ✅ 3. Table & Data Access Controls (Unity Catalog)

+ Provides centralized data governance for Databricks.
+ Uses catalog-level, schema-level, and table-level permissions.
+ Enforces row-level and column-level security.

#### ✅ 4. Network Security

+ Supports Private Link for secure connections between Databricks and Azure/AWS services.
+ Restricts IP-based access via Cluster Policies & Network Security Groups (NSGs).
+ Uses VPC/VNet peering for secure internal networking.
#### ✅ 5. Cluster Policies for Governance

+ Defines who can create clusters and what configurations they can use.
+ Enforces resource limits (number of nodes, instance types).

#### ✅ 6. Data Masking & Tokenization

+ Uses Dynamic Views in Unity Catalog to mask sensitive data.
+ Supports tokenization to replace PII with pseudonyms.

---

### 22. How does Databricks handle data encryption and security?
**Answer:**
Databricks encrypts data at rest and in transit using industry-standard security.

#### ✅ 1. Encryption at Rest

Uses AES-256 encryption for DBFS (Databricks File System), Delta Lake, and metadata.
Allows Customer-Managed Keys (CMK) for additional security in Azure Key Vault or AWS KMS.
#### ✅ 2. Encryption in Transit

All data transfers use TLS 1.2+ encryption.
Supports encrypted connections for JDBC/ODBC, APIs, and notebooks.
#### ✅ 3. Secure Data Sharing

Unity Catalog enables secure data sharing across workspaces and accounts.
Supports fine-grained access control (row-level, column-level security).
#### ✅ 4. Secret Management

Uses Databricks Secrets to securely store credentials, API keys, and connection strings.
Secrets can be fetched using environment variables in notebooks.
✅ Example: Using Databricks Secrets for Secure Authentication

**Retrieve secret value from Databricks Secrets**
    db_password = dbutils.secrets.get(scope="my_scope", key="db_password")

**Use the secret in a database connection**
    jdbc_url = f"jdbc:mysql://mydbserver.com:3306/mydb?user=admin&password={db_password}"

#### ✅ 5. Data Masking & Anonymization

Uses Dynamic Views to enforce masking on sensitive data.
✅ Example: Data Masking with Unity Catalog

    CREATE VIEW masked_view AS
    SELECT 
      user_id, 
      CASE WHEN current_user() = 'admin' THEN ssn ELSE 'XXX-XX-XXXX' END AS masked_ssn
    FROM customers;

---

### 23. What is Unity Catalog and its benefits in Databricks?

**Answer:**
Unity Catalog is Databricks' unified governance layer for managing data access, security, and lineage.

#### ✅ Key Benefits of Unity Catalog:

**1. Centralized Access Control:** Manages permissions across workspaces, tables, schemas, and catalogs.

**2. Fine-Grained Permissions:** Supports row-level & column-level security with Attribute-Based Access Control (ABAC).

**3. Data Lineage Tracking:** Tracks how data is created, transformed, and consumed across Databricks.

**4. Secure Data Sharing (Delta Sharing):** Allows cross-account sharing of Delta tables without copying data.

**5. Multi-Cloud Support:** Works across Azure, AWS, and GCP, providing unified governance.


✅ Example: Creating a Table in Unity Catalog

    CREATE TABLE catalog_name.schema_name.sales_data (
      order_id STRING,
      customer_name STRING,
      amount DECIMAL(10,2)
    );


✅ Example: Granting Table-Level Permissions in Unity Catalog

    GRANT SELECT ON TABLE catalog_name.schema_name.sales_data TO user1;

✅ Example: Enabling Row-Level Security in Unity Catalog

    CREATE VIEW sales_data_filtered AS
    SELECT * FROM sales_data WHERE region = current_user();

---

### 24. How do you implement row-level and column-level security in Databricks?
**Answer:**
Row-level and column-level security (RLS & CLS) can be implemented using Unity Catalog Dynamic Views.

#### ✅ 1. Implementing Row-Level Security (RLS)

Uses Dynamic Views to restrict access based on user identity.

    CREATE VIEW sales_filtered AS
    SELECT *
    FROM sales_data
    WHERE region = current_user();

Example Use Case: Only users belonging to a region can see their own data.

#### ✅ 2. Implementing Column-Level Security (CLS)

Uses Dynamic Views to hide/mask sensitive columns.

    CREATE VIEW masked_customers AS
    SELECT 
      customer_id, 
      name, 
      CASE WHEN current_user() IN ('admin', 'finance') THEN ssn ELSE 'XXX-XX-XXXX' END AS masked_ssn
    FROM customers;
  
Example Use Case: Only admins and finance teams can see SSNs.

#### ✅ 3. Combining RLS & CLS

    CREATE VIEW sales_secured AS
    SELECT 
      order_id, 
      amount, 
      CASE 
        WHEN current_user() = 'finance_manager' THEN customer_name 
        ELSE 'Hidden' 
      END AS customer_name
    FROM sales_data
    WHERE region = current_user();
**Example Use Case:**
+ Finance Managers can see customer names.
+ Regular users only see their region's data.

#### ✅ 4. Using Attribute-Based Access Control (ABAC)

ABAC allows fine-grained control based on user attributes (e.g., job title, department).

    GRANT SELECT ON TABLE sales_data TO user WHERE department = 'finance';

---


## Integrations & Connectivity

---

###  25. How do you connect Databricks to Azure Blob Storage?
**Answer:**
Databricks can connect to Azure Blob Storage using:

+ ABFS (Azure Blob File System) via Azure Data Lake Storage Gen2
+ SAS tokens, Access Keys, or Service Principal Authentication
+ Mounting Blob Storage as a DBFS volume

✅ Method 1: Using ABFS (Recommended for ADLS Gen2)

    spark.conf.set(
        "fs.azure.account.key.<storage-account-name>.dfs.core.windows.net",
        "<your-storage-access-key>"
    )

    df = spark.read.csv("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<file-path>")
    df.show()

✅ Method 2: Using SAS Token

    spark.conf.set(
        "fs.azure.sas.<container-name>.<storage-account-name>.blob.core.windows.net",
        "<sas-token>"
    )

    df = spark.read.parquet("wasbs://<container-name>@<storage-account-name>.blob.core.windows.net/<file-path>")
    df.show()

✅ Method 3: Mounting Blob Storage to DBFS

    dbutils.fs.mount(
        source="wasbs://<container-name>@<storage-account-name>.blob.core.windows.net/",
        mount_point="/mnt/myblob",
        extra_configs={"fs.azure.account.key.<storage-account-name>.blob.core.windows.net": "<your-storage-access-key>"}
    )

**Read a file from the mounted storage:**

    df = spark.read.csv("/mnt/myblob/<file-path>")
    df.show()

Mounted storage is persistent across sessions but only accessible within the workspace.

ABFS is preferred for higher performance and scalability.

---

### 26. How can Databricks be integrated with external databases like Azure SQL Database?

**Answer:**
Databricks connects to Azure SQL Database using:

* JDBC Driver
* Azure Data Factory (ADF) for ETL
* Databricks Autoloader with Azure Event Grid

✅ Method 1: Connecting via JDBC (Recommended)

    jdbc_url = "jdbc:sqlserver://<server-name>.database.windows.net:1433;database=<database-name>;user=<username>@<server-name>;password=<password>;encrypt=true;trustServerCertificate=false"

    df = spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "dbo.customers").load()
    df.show()

✅ Method 2: Writing Data to Azure SQL Database

    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "dbo.sales_data") \
        .option("user", "<username>") \
        .option("password", "<password>") \
        .mode("append") \
        .save()

✅ Method 3: Using Azure Data Factory (ADF)

ADF orchestrates ETL pipelines from Databricks to Azure SQL.

Uses Copy Activity or Databricks Notebook Activity.

---

### 27. What is the difference between mounting storage in Databricks and using direct access?
**Answer:**

+ Feature	Mounting Storage (DBFS)	Direct Access (ABFS, WASBS)
+ Performance	Slower (involves DBFS layer)	Faster (direct connection)
+ Security	Not recommended for sensitive data	More secure (uses service principal/SAS)
+ Persistence	Persistent across sessions	Requires authentication every session
+ Use Case	Good for interactive analysis	Best for big data processing

✅ Recommendation: Use ABFS for production and DBFS mount for ad-hoc analysis.

---

### 28. How can you use Databricks connectors for Snowflake, AWS Redshift, or Google BigQuery?
**Answer:**
Databricks provides built-in connectors for cloud data warehouses.

✅ Connecting Databricks to Snowflake

Requires the Databricks-Snowflake Connector.

    options = {
        "sfURL": "https://<account>.snowflakecomputing.com",
        "sfDatabase": "<database>",
        "sfSchema": "<schema>",
        "sfWarehouse": "<warehouse>",
        "sfRole": "<role>",
        "user": "<username>",
        "password": "<password>"
    }

    df = spark.read.format("snowflake").options(**options).option("dbtable", "orders").load()
    df.show()

Uses Snowflake's pushdown query execution for efficiency.

✅ Connecting Databricks to AWS Redshift

Uses the JDBC Redshift Connector.


    jdbc_url = "jdbc:redshift://<redshift-cluster>.redshift.amazonaws.com:5439/<database>?user=<username>&password=<password>"

    df = spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "public.sales").load()
    df.show()
✅ Connecting Databricks to Google BigQuery

Uses the Databricks BigQuery Connector.


    df = spark.read.format("bigquery").option("project", "<gcp-project-id>").option("dataset", "<dataset-name>").option("table", "<table-name>").load()
    df.show()

✅ Key Takeaways:

Snowflake Connector supports query pushdown, making it highly optimized.

Redshift & BigQuery use JDBC, requiring manual optimizations.




## Troubleshooting & Debugging

---

### 29. How do you debug performance issues in Databricks?
**Answer:**
Debugging performance issues in Databricks involves identifying bottlenecks in data processing, execution plans, cluster configuration, and memory usage.

✅ Step 1: Check Spark UI for Job Execution Details

+ Databricks Spark UI provides job, stage, and task breakdowns.
+ Look at shuffle read/write, task duration, and DAG visualization.
+ Identify skewed partitions, excessive shuffling, and slow stages.


✅ Step 2: Use Query Execution Plan (explain() & explain(True))

    df.explain(True)  # Shows physical and logical execution plan

Look for "Exchange" (Shuffle) and "SortMergeJoin" (Expensive Joins).

Convert SortMergeJoin to Broadcast Join if one dataset is small.

    df_large.join(broadcast(df_small), "id", "inner")

✅ Step 3: Optimize Spark Configurations

    spark.conf.set("spark.sql.shuffle.partitions", "200")  # Adjust partitions dynamically
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10MB")  # Optimize broadcast joins

✅ Step 4: Monitor Cluster Metrics

Use Ganglia Metrics UI (/driver-profiles/) to check CPU, memory, and garbage collection.

Enable adaptive query execution (AQE) to optimize partitions dynamically.


    spark.conf.set("spark.sql.adaptive.enabled", "true")

✅ Step 5: Cache Intermediate DataFrames

+ Recompute cost can be high; use cache() or persist() for reused DataFrames.

    df.persist()  # Default: StorageLevel.MEMORY_AND_DISK

+ Drop cache after use to free memory:

    df.unpersist()

✅ Step 6: Use Delta Lake for Faster Queries

+ Convert CSV/Parquet to Delta for better performance.

    df.write.format("delta").mode("overwrite").save("/mnt/delta/sales")

+ Enable Delta Caching

    spark.conf.set("spark.databricks.io.cache.enabled", "true")

---

### 30. What are some common errors in Spark and their resolutions?
**Answer:**

##### Error	Cause	Resolution:
* OutOfMemoryError (OOM) in Driver	Large data collected using .collect()	Use .show(), .limit(), or .take() instead of .collect()
* Job Aborted due to Stage Failure	Skewed partitions, too many shuffles	Enable Adaptive Query Execution (AQE), repartition skewed data
* GC Overhead Limit Exceeded	Too many small partitions causing excessive garbage collection	Increase executor memory, optimize shuffle partitions
* Task Not Serializable Exception	UDF or lambda function is not serializable	Avoid passing class objects in UDFs, use built-in functions
* FileNotFoundException (for Delta tables)	Delta transaction log corrupted	Run VACUUM and FSCK commands to clean up Delta files

✅ Example: Avoiding OOM with DataFrame Operations

❌ Bad Practice: Collecting large DataFrame into driver memory


    data = df.collect()  # Might cause OutOfMemoryError

✅ Best Practice: Using .show() or .take()
    df.show(10)
    small_data = df.limit(100).collect()

✅ Example: Fixing "Job Aborted due to Stage Failure"

    spark.conf.set("spark.sql.adaptive.enabled", "true")  # Enable AQE
    df = df.repartition(100)  # Reduce shuffle partitions

---

### 31. How do you monitor Databricks jobs and logs?
**Answer:**
Databricks provides multiple ways to monitor jobs and logs.

✅ 1. Databricks Job UI (Jobs > Run Output)

Shows Job execution history, logs, and error messages.

Provides timing details for each stage and task.

✅ 2. Spark UI (Clusters > Spark UI)

Provides execution plan visualization (DAG).

Shows Shuffle Read/Write, Task execution time, and failed tasks.

✅ 3. Logging in Notebooks (stdout and stderr)

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Processing started...")

✅ 4. Enable Cluster Event Logs

Databricks logs cluster events under "Event Log" (includes auto-scaling, node failures).

+ Logs can be accessed using dbutils.fs:
    dbutils.fs.head("dbfs:/cluster-logs/<cluster-id>/driver.log", 100)

✅ 5. Monitor Jobs via REST API

    import requests
    token = "<databricks-token>"
    workspace_url = "https://<databricks-instance>"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{workspace_url}/api/2.0/jobs/runs/list", headers=headers)
    print(response.json())


✅ 6. Use Databricks Metrics for Auto-Scaling Monitoring

  spark.conf.set("spark.databricks.cluster.metrics.enabled", "true")

Monitors CPU, Memory, and Disk Usage dynamically.

---

### 32. Explain What is the different read mode in spark?
**Answer:**

In **Spark**, when you **read files** (like CSV, JSON, etc.), you can specify a **mode** to tell Spark how to handle **corrupt** or **bad records**.  

Here are the main **modes** you can use during reading:


### 🔥 Different Modes in Spark Read

| Mode          | Behavior                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------ |
| **PERMISSIVE** (default) | Puts corrupt records in a special column (e.g., `_corrupt_record`). Loads the rest normally. |
| **DROPMALFORMED**        | Drops any records that are corrupted or don’t match the schema.                        |
| **FAILFAST**             | Immediately throws an error if any malformed record is found.                          |


### 🛠️ How to Set Mode in Code

```python
        # Example for reading a CSV with different modes
        df = spark.read.option("mode", "PERMISSIVE").csv("path/to/data.csv", schema=schema)

        df = spark.read.option("mode", "DROPMALFORMED").csv("path/to/data.csv", schema=schema)

        df = spark.read.option("mode", "FAILFAST").csv("path/to/data.csv", schema=schema)
```



### 🔎 Short Summary:
- **PERMISSIVE** = Save bad records separately.
- **DROPMALFORMED** = Ignore bad records.
- **FAILFAST** = Crash immediately on bad records.


### 33. Explain What is the different Write mode in spark?

When you **write** data (save DataFrames) in Spark, you can control **what happens if the target location already exists** by using different **write modes**.

Here’s the full breakdown:



### 🔥 Different Write Modes in Spark

| Mode         | Behavior |
| ------------ | -------- |
| **append**   | Adds new data to the existing data (does not delete old data). |
| **overwrite**| Deletes the existing data at the path and writes new data. |
| **ignore**   | If data already exists at the path, Spark does nothing (no error, no overwrite). |
| **error** (or **errorifexists**) | Default. If data already exists at the path, Spark throws an error and stops writing. |



### 🛠️ How to Set Write Mode in Code

```python
        # Example of different write modes
        df.write.mode("append").csv("path/to/folder")

        df.write.mode("overwrite").parquet("path/to/folder")

        df.write.mode("ignore").json("path/to/folder")

        df.write.mode("error").saveAsTable("table_name")
```



### ✨ Quick Behavior Summary:

- **append** ➔ Keep old + Add new.
- **overwrite** ➔ Delete old ➔ Write new.
- **ignore** ➔ If exists, skip writing.
- **error** ➔ If exists, throw an error.



**Important Note:**  
- In **overwrite**, if you're writing to a table (not just files), you can control **how partition overwrite** happens using extra options like:
  ```python
  df.write.mode("overwrite").option("partitionOverwriteMode", "dynamic").saveAsTable("table_name")
  ```
  (This is super important for big tables!)

---
