# 📋 ADF Scenario-Based Questions

### 1. **How would you design a pipeline to ingest incremental data from an on-prem SQL Server to Azure Data Lake every hour?**

   * Follow-up: How will you handle late-arriving data?



✅ Great question — this is a **common real-world scenario** and a typical interview topic for Data Engineers working with Azure.

Let’s walk through both parts step by step:

---

# 🚀 **Pipeline to ingest incremental data from on-prem SQL Server to Azure Data Lake every hour**

#### 🔷 **Requirements**

* Source: On-premises **SQL Server**
* Destination: **Azure Data Lake (ADLS Gen2)**
* Frequency: **Hourly**
* Only **incremental data** (changes since last load)
* Must also handle **late-arriving data**

---

# 🎯 **Design Steps**

---

#### 1️⃣ **Connectivity**

* Use **Self-hosted Integration Runtime (SHIR)** to connect securely to your on-prem SQL Server from Azure.

  * Install SHIR on a VM or server in your network.
  * Register it with Azure Data Factory (ADF).

---

#### 2️⃣ **Detect Incremental Data**

There are several ways to identify incremental changes:

* If the source table has a column like:

  * `LastModifiedDateTime` (preferred)
  * `CreatedDateTime`
  * or a **change tracking / CDC mechanism**

#### Options:

| Method                        | Notes                                                                                                                                               |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Timestamp column**          | If a column like `LastModifiedDateTime` exists, store the **max timestamp** loaded in each run. Query: `WHERE LastModifiedDateTime > @LastMaxTime`. |
| **Change Tracking (CT)**      | SQL Server feature — lightweight, tracks changes since a version. Use the **version token** for next run.                                           |
| **Change Data Capture (CDC)** | SQL Server feature — more detailed than CT. Reads from CDC tables to get inserts/updates/deletes.                                                   |

For most scenarios:
✅ simplest: `LastModifiedDateTime`
✅ better for updates & deletes: CT or CDC.

---

#### 3️⃣ **Build the ADF Pipeline**

##### Components:

* **Lookup** activity → fetch last watermark from a control table / blob file.
* **Source Dataset** → SQL Server table, with query:

  ```sql
  SELECT * FROM Table WHERE LastModifiedDateTime > @last_watermark
  ```
* **Copy Activity** → write to ADLS in Parquet/CSV with folder structure:

  ```
  /raw_data/TableName/YYYY/MM/DD/HH/
  ```
* After successful load → update the watermark for next run.

---

#### 4️⃣ **Schedule**

* Use **ADF Trigger** (time-based) → run **every hour on the hour**.

---

#### 5️⃣ **Schema & Partitioning**

* Store data in ADLS partitioned by date/hour:

  ```
  adls://datalake/container/table_name/year=2025/month=07/day=05/hour=18/
  ```
* Choose **Parquet** for efficient storage & analytics.

---

---

## 📦 **Handling Late-Arriving Data**

Late-arriving data means records that belong to an earlier period (e.g., a transaction for 10 AM arrives at 2 PM).

### Strategies:

---

### 🌟 1. **Do Nothing (if acceptable)**

If your downstream processing tolerates late data, and consumers always query the **latest snapshot**, you may not need to correct history.

---

### 🌟 2. **Reprocess Window**

* Keep a **rolling window of N hours/days** in your ingestion pipeline.
* Every hour:

  * Load data modified in the **last 2–3 hours** (instead of just 1).
  * This catches late updates.
  * Example query:

    ```sql
    WHERE LastModifiedDateTime > @last_watermark - 2 hours
    ```
* In ADLS:

  * Overwrite the partitions corresponding to those hours/days to ensure accuracy.

---

### 🌟 3. **Delta Lake / Upserts**

* Store data in **Delta Lake** format on ADLS.
* With Delta tables, you can **merge/upsert** late-arriving records into existing partitions.
* This is more sophisticated & ensures correctness over time.

---

### 🌟 4. **Audit & Alerts**

* Optionally track how much late data is arriving.
* Trigger alerts if lateness > threshold → so the source system can be improved.

---

# ✨ **Summary Table**

| Feature            | Implementation                                        |
| ------------------ | ----------------------------------------------------- |
| Incremental Data   | Use `LastModifiedDateTime`, CT, or CDC                |
| Pipeline           | ADF pipeline → SHIR → SQL → ADLS                      |
| Schedule           | Hourly trigger                                        |
| Watermark          | Store in SQL table / Blob metadata                    |
| Data Format        | Parquet or Delta, partitioned by date/hour            |
| Late Data Handling | Reprocess rolling window OR use Delta Lake with MERGE |

---

# 📋 Example Architecture:

```
On-prem SQL Server
    ⬇️ (via SHIR)
ADF Pipeline
    ⬇️ (Copy Activity)
ADLS Gen2 → partitioned folders or Delta table
    ⬇️
(Downstream processing: Databricks, Synapse, Power BI)
```

---




## 2. **You need to copy files from an SFTP server to Azure Blob Storage and send an email to the manager if any file is missing. How would you implement this?**
✅ Good scenario — let me walk you through a **design** for this use case step by step:

> 📄 **Goal**: Copy files from SFTP → Azure Blob Storage, and if any expected file(s) are missing, send an email to the manager.

---

### 🔷 **High-level steps**

1️⃣ **Define the list of expected files**

* This could come from:

  * A static list configured in your pipeline (e.g., parameter or config file).
  * A dynamic list fetched from a database or metadata store.

---

2️⃣ **Pipeline implementation:**

We’ll use **Azure Data Factory (ADF)** or **Synapse Pipelines** since they support SFTP, Blob Storage, and email notification.

---

### 📐 **ADF Pipeline Design**

#### 📂 1. Get the list of actual files from SFTP

* Use a **Get Metadata activity** to list files in the SFTP folder.

  * Configure a Linked Service to connect to the SFTP server.
  * Use a Dataset pointing to the folder on SFTP.
  * The output will be an array of file names.

---

#### 📜 2. Compare actual vs expected

* Pass the list of expected files as a pipeline parameter or retrieve it from a Lookup activity.
* Use a **Set Variable** or a **Stored Procedure** / **Mapping Data Flow** / custom **Azure Function** / **Until activity** with an **If Condition** to compare the expected list and the actual list.

  * Identify which files are missing.

---

#### 📤 3. Copy files

* For each file in the actual list:

  * Use a **ForEach activity** to loop over the files.
  * Inside the ForEach, use a **Copy activity**:

    * Source: SFTP file.
    * Sink: Azure Blob Storage container.

---

#### 📧 4. Notify manager if files are missing

* If any expected file is not present on the SFTP, trigger a **Web activity** to call:

  * Logic App
  * Power Automate
  * Or directly use the ADF **Send Email (Preview)** activity (if available in your region)
  * The email body can include which files were missing.

---

### 📄 Example flow in ADF:

```
[Lookup: Expected file list]
          |
     [Get Metadata: SFTP folder file list]
          |
  [Compare lists: identify missing files]
          |
        /   \
[If no missing] [If missing]
   |               |
[ForEach: Copy]   [Send Email]
```

---

### 🔷 Notes:

✅ Make sure the SFTP Linked Service has proper credentials (key or password).
✅ Use a dynamic dataset in the Copy activity to handle different file names.
✅ For comparison logic, you can use:

* Data Flow (with Left Anti Join between expected & actual).
* Stored Procedure in SQL.
* Custom Azure Function for complex logic.
  ✅ For the email, if ADF native email isn’t available, a Logic App or Function is the usual choice.

---

### Sample tools:

| Step          | Tool/Activity                |
| ------------- | ---------------------------- |
| Expected list | Lookup or Pipeline parameter |
| Actual list   | Get Metadata                 |
| Compare lists | Data Flow or pipeline logic  |
| Copy files    | Copy activity in ForEach     |
| Send email    | Web activity → Logic App     |

---

### 💡 Example Email:

```
Subject: Missing files detected on SFTP

Hello Manager,

The following expected files were not found on the SFTP server during today’s run:
- file1.csv
- file2.csv

Please investigate.

Thanks,
Data Engineering Team
```

---


## 3. **You’re asked to ingest data from 50 different REST APIs with different authentication mechanisms. How would you make the pipeline reusable and dynamic?**

✅ This is a **classic scenario** in data engineering where you need to ingest data from many REST APIs — each with **different authentication mechanisms** — and you want to build a **reusable & dynamic pipeline** rather than 50 hard-coded pipelines.

Here’s how you can design and implement it, step by step:

---

## 🎯 Goals:

* Handle multiple APIs (50+).
* Support different authentication types (API key, OAuth2, Basic auth, etc.).
* Make the pipeline reusable — no code changes when adding a new API.
* Make it dynamic — parameters driven by configuration.

---

## 🚀 Solution Design

### 1️⃣ **Use a Metadata/Configuration-driven Approach**

Create a **configuration store** (in a database table, JSON, or YAML file) that contains all the details for each API.

Example schema for the config table:

| api\_name   | endpoint\_url                 | auth\_type  | auth\_details          | params | headers | schedule |
| ----------- | ----------------------------- | ----------- | ---------------------- | ------ | ------- | -------- |
| WeatherAPI  | `https://api.weather.com/...` | API\_KEY    | `{ "key": "abc123" }`  | `{…}`  | `{…}`   | daily    |
| TwitterAPI  | `https://api.twitter.com/...` | OAUTH2      | `{ "client_id": … }`   | `{…}`  | `{…}`   | hourly   |
| InternalAPI | `https://myapp.local/...`     | BASIC\_AUTH | `{ "user":…, "pwd":…}` | `{…}`  | `{…}`   | weekly   |

---

### 2️⃣ **Design the Pipeline**

You can build the pipeline in **Azure Data Factory**, **Databricks**, or any orchestration tool (Airflow, Prefect).
The key is:

* Read the configuration.
* Loop over each API config.
* Call the REST API with appropriate auth and params.
* Store the response.

---

### 3️⃣ **Implement Authentication Handlers**

Write reusable functions or modules to handle different `auth_type`:

* If `auth_type = API_KEY`: Inject the key into header or query string.
* If `auth_type = BASIC_AUTH`: Base64 encode user\:password.
* If `auth_type = OAUTH2`: Obtain token, refresh if expired, and attach to header.
* If `auth_type = NONE`: Just call.

You can implement these as Python functions, or ADF Web Activity dynamic expressions.

---

### 4️⃣ **Dynamic Pipeline in ADF (example)**

In **ADF**:

* Use a **Lookup activity** to read the configuration (from SQL table, Blob JSON, etc.)
* Use a **ForEach activity** to iterate over each API.
* Inside ForEach:

  * Use a **Web activity** (or Azure Function) to call the API.
  * Pass dynamic `url`, `headers`, `body`, etc. from the config.
  * Handle the response and save it (Blob, ADLS, SQL, etc.)
  * Optionally log the status.

---

### 5️⃣ **Dynamic Pipeline in Databricks (example)**

In **Databricks (PySpark)**:

* Read the config table into a DataFrame.
* Loop through rows:

  ```python
  import requests
  import base64

  for row in config_df.collect():
      url = row['endpoint_url']
      auth_type = row['auth_type']
      auth_details = json.loads(row['auth_details'])
      headers = json.loads(row['headers']) or {}
      params = json.loads(row['params']) or {}

      if auth_type == 'API_KEY':
          headers['Authorization'] = f"Bearer {auth_details['key']}"
      elif auth_type == 'BASIC_AUTH':
          token = base64.b64encode(f"{auth_details['user']}:{auth_details['pwd']}".encode()).decode()
          headers['Authorization'] = f"Basic {token}"
      elif auth_type == 'OAUTH2':
          # implement token retrieval & attach
          pass
      
      response = requests.get(url, headers=headers, params=params)
      # save response to storage
  ```

---

### 6️⃣ **Logging & Monitoring**

* Log success/failure for each API call.
* Capture response status & any error messages.
* You can store logs in a table or monitoring tool.

---

### 7️⃣ **Adding New APIs**

Once this framework is in place:

* To add a new API, just add a new record to the config table/file.
* No code or pipeline change required.

---

## 📝 Benefits

✅ Scalable: Easily supports >50 APIs.
✅ Reusable: Single pipeline for all APIs.
✅ Configurable: Changes driven by metadata.
✅ Auditable: Logs everything centrally.

---

## Example Tech Stack:

| Task          | Tools                              |
| ------------- | ---------------------------------- |
| Orchestration | ADF, Airflow, Databricks workflows |
| Config Store  | Azure SQL DB, Cosmos DB, Blob JSON |
| API Calls     | ADF Web Activity / Python requests |
| Storage       | ADLS Gen2, Blob, SQL               |
| Monitoring    | Azure Monitor, Log Analytics       |

---


## 4. **If your source table doesn’t have a column that indicates updated/inserted records, how can you implement incremental load?**

✅ Great question — and a very common challenge in data engineering & ETL design!

If your **source table doesn’t have a column to indicate which records were inserted/updated (like a timestamp, last\_modified, or change\_flag)**, then you **cannot do a simple incremental load based on a watermark.**

But you *can still implement incremental loading* using one of the following strategies:

---

## 🚀 Options to Implement Incremental Load Without a Change Column

---

### 1️⃣ **Full Extract + Change Data Capture (CDC) Logic**

* Load the **entire source table** into a staging area (usually in your data lake or staging database).
* Compare the staging data with the target table to identify:

  * **New records** → Not present in the target.
  * **Updated records** → Present in the target but with different values.
  * **Unchanged records** → Already in the target & identical.

You typically implement this using:

* A **hash or checksum** of each row to detect changes efficiently.
* Or by comparing all relevant columns directly.

**Steps:**

```sql
-- Step 1: Compute a hash of each record in source & target
SELECT id, md5(concat(col1, col2, col3, …)) AS row_hash FROM source_table;
SELECT id, md5(concat(col1, col2, col3, …)) AS row_hash FROM target_table;

-- Step 2: Join on `id` and compare hashes
-- If `id` not in target → insert
-- If `id` in target & hash != → update
-- If `id` in target & hash = → skip
```

---

### 2️⃣ **Change Data Capture at the Database Level**

* Some databases (SQL Server, Oracle, MySQL, PostgreSQL) support CDC features or write-ahead logs (WAL) you can tap into.
* Tools like:

  * **SQL Server CDC/CT (Change Tracking)**
  * **Debezium**
  * **GoldenGate**
  * **Azure Data Factory with CDC in Mapping Data Flows**
    can capture changes at the transaction/log level — even if your table itself doesn’t store `last_updated`.

---

### 3️⃣ **Triggers in Source Database**

If allowed, you can create a trigger on the source table to populate an auxiliary log table whenever rows are inserted/updated/deleted.
Your pipeline can then read from this log table to get the deltas.

---

### 4️⃣ **Snapshots + SCD (Slowly Changing Dimension) Type 2**

* Take regular **snapshots** of the table (daily, hourly, etc.).
* Compare today’s snapshot to the previous snapshot.
* Insert changes or maintain history (like SCD Type 2).

---

### 5️⃣ **External Tools**

If you’re using cloud tools like:

* **Azure Data Factory**,
* **Databricks**,
* **Fivetran**,
* **Snowflake streams**,
  you can often configure them to detect & load changes by comparing snapshots or using built-in CDC features.

---

## 📌 Key Techniques Used

| Technique                      | Pros                        | Cons                         |
| ------------------------------ | --------------------------- | ---------------------------- |
| Full extract + hash comparison | Simple, no DB changes       | High data transfer & compute |
| CDC / Log-based                | Efficient, minimal overhead | Requires DB support & setup  |
| Triggers                       | Works on any DB             | Adds write overhead          |
| Snapshots + diff               | No DB change, keeps history | Storage intensive            |

---

## 👷 Best Practice

✅ If the source DB supports CDC → use it.
✅ If not, but data size is small → use full extract + hash comparison.
✅ If large & no CDC → consider designing a lightweight trigger-based log.
✅ Always try to push the responsibility for tracking changes to the **source system** if possible (add a `last_modified` column if feasible).

---



## 5. **Your pipeline needs to fetch yesterday’s sales data automatically. How would you parameterize and set up the pipeline for that?**


✅ This is a very common **date-driven pipeline design question**, and a good answer shows you know how to make it **dynamic and reusable**.

Here is a clear explanation with **steps and an example** (using Azure Data Factory or Databricks, but the principles apply to any ETL tool):

---

### 🎯 Goal:

Fetch **yesterday’s sales data** automatically every day — for example, process sales where `sales_date = yesterday`.

---

## 🚀 Approach

### 1️⃣ **Parameterize the date**

* Define a **pipeline parameter** called `ProcessingDate`.
* You don’t hard-code it; instead, calculate it dynamically.

In Azure Data Factory (ADF), you can use the expression:

```sql
@formatDateTime(addDays(utcnow(), -1), 'yyyy-MM-dd')
```

📌 This computes yesterday’s date at runtime.

If you’re in Databricks:

```python
from datetime import datetime, timedelta
processing_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
```

---

### 2️⃣ **Use this parameter in your source query/path**

* If you’re querying a database:

```sql
SELECT * 
FROM sales 
WHERE sales_date = '@{pipeline().parameters.ProcessingDate}'
```

* If you’re reading from files (like `sales_YYYY-MM-DD.csv`):
  you can build the path dynamically:

```
/data/sales/sales_@{pipeline().parameters.ProcessingDate}.csv
```

---

### 3️⃣ **Schedule the pipeline**

* Use a trigger to **run daily at a set time**, e.g., 2 AM.
* No manual intervention is needed since the date is calculated dynamically.

---

## 🔷 Optional Enhancements

✅ Add a fallback: If the parameter is supplied manually, use it; else default to yesterday.
ADF example:

```sql
@if(equals(pipeline().parameters.ProcessingDate, ''), 
    formatDateTime(addDays(utcnow(), -1), 'yyyy-MM-dd'), 
    pipeline().parameters.ProcessingDate)
```

✅ Add validation to ensure data for the date exists before processing.

---

### 📋 Example Summary Table

| Step                           | What you do                                            |
| ------------------------------ | ------------------------------------------------------ |
| Define parameter               | `ProcessingDate`                                       |
| Default value (ADF expression) | `@formatDateTime(addDays(utcnow(), -1), 'yyyy-MM-dd')` |
| Use parameter in query/path    | `WHERE sales_date = '@ProcessingDate'` or file path    |
| Schedule pipeline              | Daily trigger (e.g., at 2 AM)                          |


---

### 🔷 Data Transformation & Data Flow Scenarios

## 6. **You have two datasets (customer & orders) in Blob Storage that need to be joined on `CustomerID`, aggregated, and written into Azure SQL Database. How would you build this?**

## 7. **How would you implement Slowly Changing Dimension (SCD) Type 2 logic in ADF Data Flows?**

## 8. **If the source file contains invalid/malformed rows, how would you handle and log them?**

## 9. **Your pipeline needs to convert files from CSV to Parquet and partition them by date before storing in ADLS. How would you achieve this?**

---

### 🔷 Orchestration & Monitoring Scenarios

## 10. **How would you design a pipeline that runs every day at 2AM, but only if the upstream system has deposited a new file in Blob Storage?**

## 11. **How would you retry a failed activity only 3 times and send a Teams notification if it still fails?**

## 12. **You need to execute pipelines in a specific order — Pipeline A → Pipeline B → Pipeline C, but only if A & B are successful. How would you design this?**

## 13. **How would you implement a mechanism to log every pipeline run status, start & end time, and activity outcomes into a SQL table for auditing?**

---

### 🔷 Performance & Optimization Scenarios

## 14. **What techniques would you use to optimize the performance of a copy activity transferring millions of rows?**

## 15. **How would you design your pipeline to scale when processing 1TB of daily data without failing?**

---

### 🔷 Dynamic & Parameterized Pipelines

## 16. **You have to load data from 100 tables of a database into their respective folders in ADLS. How would you build a single dynamic pipeline to handle this?**

## 17. **Your pipeline needs to read the schema of incoming files dynamically and load them to a staging table. How would you handle schema drift?**

---

### 🔷 Security & Access Scenarios

## 18. **If you need to securely connect to an on-prem SQL Server via Self-Hosted Integration Runtime, what steps would you take?**

## 19. **How would you ensure that sensitive information (like passwords or API keys) are not exposed in your pipelines?**

---

### 🔷 Advanced/Real-Time Scenarios

## 20. **You’re asked to implement a pipeline that triggers on arrival of a file, transforms it, and updates Power BI datasets in near real-time. How would you design it?**

## 21. **You have to process and validate thousands of small files arriving every hour and merge them into a single Parquet file. How would you build this?**

---

## 📌 Bonus — Troubleshooting & Best Practices

## 22. **A pipeline that was running fine yesterday is now failing with a timeout error when writing to SQL Database. How would you debug it?**

## 23. **What are some best practices you follow for naming conventions, folder structure, and reusability in ADF?**

## 24. **How would you test your pipelines before moving them to production?**

## 25. **What would you do if the dataset schema at the source changed suddenly and broke your pipeline?**

---
