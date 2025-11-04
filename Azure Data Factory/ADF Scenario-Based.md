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

*** Answer: ***
Here’s a **complete, interview-ready answer** with a **clear architectural diagram** and detailed **step-by-step explanation** for the given **Azure Data Engineering scenario** 👇

---

## ✅ **Scenario**

You have **two datasets** in **Azure Blob Storage**:

* **Customer.csv**
* **Orders.csv**

These need to be **joined on `CustomerID`**, **aggregated**, and the **final result** should be **stored in Azure SQL Database**.

---

## 🧭 **Objective**

Build an **end-to-end data pipeline** that:

1. Reads both datasets from Blob Storage
2. Joins them on `CustomerID`
3. Performs aggregations (e.g., total order value per customer)
4. Writes the final aggregated data to Azure SQL Database

---

## 🧱 **High-Level Architecture Diagram**

```
            +--------------------------+
            |      Azure Blob Storage  |
            |--------------------------|
            |  Customer.csv  Orders.csv|
            +------------+-------------+
                         |
                         v
             +--------------------------+
             |  Azure Data Factory (ADF)|
             |--------------------------|
             |  Pipeline Orchestration  |
             |  Data Flow Activity      |
             +------------+-------------+
                          |
                          v
           +------------------------------+
           |  Mapping Data Flow in ADF     |
           |------------------------------|
           |  Source1: Customer.csv        |
           |  Source2: Orders.csv          |
           |  Join on CustomerID           |
           |  Aggregate (SUM(OrderAmount)) |
           |  Sink: Azure SQL Database     |
           +-------------------------------+
                          |
                          v
             +--------------------------+
             |   Azure SQL Database     |
             |--------------------------|
             |   Final Aggregated Table |
             +--------------------------+
```

---

## ⚙️ **Step-by-Step Implementation**

### **Step 1: Create Linked Services**

In **Azure Data Factory**:

* **Linked Service 1:** Azure Blob Storage
  → Connect to your container holding the input CSV files
* **Linked Service 2:** Azure SQL Database
  → Use connection string, username, password, and firewall settings

---

### **Step 2: Create Datasets**

* **Customer Dataset (DelimitedText)** → Points to `Customer.csv` in Blob Storage
* **Orders Dataset (DelimitedText)** → Points to `Orders.csv`
* **Azure SQL Dataset (Table)** → Destination table in Azure SQL Database (e.g., `Customer_Order_Aggregate`)

---

### **Step 3: Build Data Flow**

Inside ADF, create a **Mapping Data Flow**:

1. **Add Source transformations:**

   * Source1 → Customer dataset
   * Source2 → Orders dataset

2. **Join transformation:**

   * Join type: `Inner` (or `Left Outer`, depending on requirement)
   * Condition: `Customer.CustomerID == Orders.CustomerID`

3. **Aggregate transformation:**

   * Group by: `CustomerID`, `CustomerName`
   * Aggregates:

     * `TotalOrders = count(Orders.OrderID)`
     * `TotalAmount = sum(Orders.OrderAmount)`

4. **Sink transformation:**

   * Sink: Azure SQL Database dataset
   * Write mode: `Upsert` or `Truncate and Load` (depending on your requirement)

---

### **Step 4: Pipeline Orchestration**

In ADF:

* Create a **pipeline**
* Add **Data Flow Activity**
* Link the created **Mapping Data Flow**
* Trigger manually or set a **schedule trigger**

---

### **Step 5: Azure SQL Table Schema (Example)**

```sql
CREATE TABLE Customer_Order_Aggregate (
    CustomerID INT,
    CustomerName NVARCHAR(100),
    TotalOrders INT,
    TotalAmount DECIMAL(18,2),
    LoadDate DATETIME DEFAULT GETDATE()
);
```

---

### **Step 6: Validation and Monitoring**

* Use **ADF Monitor tab** to check pipeline execution status, data flow performance, and row counts.
* Optionally, enable **logging in Azure Log Analytics** for operational insights.

---

## 💡 **Alternative Approach (If Transformation is Complex)**

If transformations are **heavy or require custom logic**, use:

* **Azure Databricks** for joining and aggregation
* Then write the final result into **Azure SQL Database**

**Modified Flow:**
Blob Storage → Databricks (PySpark) → Azure SQL Database
→ ADF orchestrates the workflow.

---

## 🏁 **Final Answer Summary**

| Step | Component          | Purpose                            |
| ---- | ------------------ | ---------------------------------- |
| 1    | Azure Blob Storage | Store raw Customer and Orders CSVs |
| 2    | Azure Data Factory | Orchestrate and transform data     |
| 3    | Mapping Data Flow  | Join on CustomerID, aggregate      |
| 4    | Azure SQL Database | Store final aggregated result      |
| 5    | Trigger/Monitor    | Schedule and observe pipeline runs |

---


## 7. **How would you implement Slowly Changing Dimension (SCD) Type 2 logic in ADF Data Flows?**
*** Answer: ***
Here’s a **complete, interview-ready answer** — explaining **how to implement Slowly Changing Dimension (SCD) Type 2** in **Azure Data Factory (ADF) Mapping Data Flows**, with a **diagram**, **step-by-step explanation**, and **key interview talking points** 👇

---

## 🎯 **Scenario**

You have a **dimension table (e.g., Customer Dimension)** in **Azure SQL Database**, and a **daily incremental file** (e.g., from Azure Blob Storage) with **updated customer data**.
You need to track **historical changes** (Type 2 SCD), meaning:

* When a record changes, you must **insert a new row** with updated details,
* and **mark the old row as inactive**.

---

## 💡 **Goal**

Implement **SCD Type 2** logic in **ADF Mapping Data Flow** so that:

* Historical versions are preserved,
* Only one record per business key is **current**,
* Changes are captured efficiently.

---

## 🧱 **Architecture Diagram**

```
          +---------------------------+
          | Azure Blob Storage        |
          |---------------------------|
          | customer_incremental.csv  |
          +------------+--------------+
                       |
                       v
            +---------------------------+
            | Azure Data Factory (ADF)  |
            | Mapping Data Flow         |
            |---------------------------|
            | Source (New Data)         |
            | Lookup (Existing Data)    |
            | Conditional Split         |
            | AlterRow + Sink           |
            +------------+--------------+
                       |
                       v
          +----------------------------+
          | Azure SQL Database          |
          | Customer_Dimension Table    |
          +----------------------------+
```

---

## ⚙️ **Step-by-Step Implementation**

### **Step 1: Prepare Target Table (Azure SQL)**

Create a **Customer_Dimension** table with SCD tracking columns:

```sql
CREATE TABLE Customer_Dimension (
    CustomerID INT,
    CustomerName NVARCHAR(100),
    Address NVARCHAR(200),
    City NVARCHAR(100),
    EffectiveStartDate DATETIME,
    EffectiveEndDate DATETIME,
    IsCurrent BIT,
    CONSTRAINT PK_Customer PRIMARY KEY (CustomerID, EffectiveStartDate)
);
```

---

### **Step 2: Create Linked Services and Datasets**

* **Linked Services:**

  * Azure Blob Storage (source)
  * Azure SQL Database (target)
* **Datasets:**

  * `Customer_New` → source CSV
  * `Customer_Dim` → SQL table

---

### **Step 3: Build the Mapping Data Flow**

#### 🔹 1. **Source Transformation**

* Source → New incoming data (`Customer_New`)

#### 🔹 2. **Lookup Transformation**

* Lookup against the **existing dimension table (`Customer_Dim`)**
* Join on **`CustomerID`**
* Retrieve columns: `CustomerName`, `Address`, `City`, `EffectiveStartDate`, `EffectiveEndDate`, `IsCurrent`

#### 🔹 3. **Derived Column (Optional)**

Add `CurrentDate = currentUTC()` to mark load date dynamically.

#### 🔹 4. **Conditional Split**

Use this to separate rows into three categories:

| Condition                    | Meaning          | Action                             |
| ---------------------------- | ---------------- | ---------------------------------- |
| No match in Lookup           | New Customer     | **Insert as new record**           |
| Match but attributes changed | Updated Customer | **Expire old + insert new record** |
| Match and no change          | Unchanged        | **Skip (no action)**               |

Example expression:

```text
iif(isNull(lookup.CustomerID), 'New',
    iif(CustomerName != lookup.CustomerName || Address != lookup.Address || City != lookup.City, 'Changed', 'Unchanged'))
```

#### 🔹 5. **Alter Row Transformation**

Define actions for each condition:

| Row Type | Rule                            | Action                                                                            |
| -------- | ------------------------------- | --------------------------------------------------------------------------------- |
| New      | `conditionalSplit == 'New'`     | **Insert**                                                                        |
| Changed  | `conditionalSplit == 'Changed'` | **Insert** new record (with new EffectiveStartDate)                               |
| Changed  | Expire old record               | **Update** existing record (set `IsCurrent=0` and `EffectiveEndDate=CurrentDate`) |

You’ll need **two sinks**:

* One for inserting **new/changed records**
* One for **updating** old records (to expire them)

#### 🔹 6. **Sink Transformations**

* **Sink 1 (Insert new rows):**

  * Target: Customer_Dimension
  * Insert mode
  * Columns: set `EffectiveStartDate = currentUTC()`, `EffectiveEndDate = NULL`, `IsCurrent = 1`
* **Sink 2 (Update old rows):**

  * Target: Customer_Dimension
  * Update mode
  * Match on `CustomerID` and `IsCurrent = 1`
  * Set `EffectiveEndDate = currentUTC()`, `IsCurrent = 0`

---

## 🧩 **Data Flow Logic Summary**

| Transformation        | Purpose                                      |
| --------------------- | -------------------------------------------- |
| **Source**            | Load new customer data                       |
| **Lookup**            | Get existing data from dimension table       |
| **Conditional Split** | Detect new, changed, or unchanged records    |
| **Alter Row**         | Define insert/update actions                 |
| **Sink (Insert)**     | Add new or changed customers as new versions |
| **Sink (Update)**     | Expire old versions (set IsCurrent=0)        |

---

## 📊 **Example**

| CustomerID | Name  | City     | IsCurrent | StartDate  | EndDate    |
| ---------- | ----- | -------- | --------- | ---------- | ---------- |
| 1          | Alice | New York | 1         | 2023-01-01 | NULL       |
| 1          | Alice | London   | 0         | 2021-06-01 | 2022-12-31 |

When Alice moves to a new city, old record is marked inactive, and new record is inserted with updated data.

---

## 🧠 **Interview Tip: Key Talking Points**

✅ Explain **why Type 2** → preserves history
✅ Mention **Effective Dates and IsCurrent flags**
✅ Explain **ADF’s “Alter Row” transformation** for upserts
✅ Mention **Lookup + Conditional Split** pattern
✅ Optionally, say **Data Flows scale well for SCD** vs manual SQL merges

---

## 🚀 **Bonus: Optimization Tips**

* Use **Surrogate Keys** (Identity in SQL) for dimension records
* Filter only **IsCurrent = 1** records in lookup for efficiency
* Use **staging tables** if data volume is large
* Enable **data flow debug mode** for validation before deployment

---


## 8. **If the source file contains invalid/malformed rows, how would you handle and log them?**
*** Answer: ****
Excellent question — this is a **very common scenario** asked in **Azure Data Factory (ADF)** or **Data Engineering interviews** to check how you handle **bad data quality** and ensure **data reliability**.

Here’s a **complete, scenario-based answer** with **ADF best practices, data flow design, and logging strategy** 👇

---

## 🎯 **Scenario**

You are ingesting data from a **source file (e.g., CSV in Azure Blob Storage)** into a **target database (Azure SQL)** using **Azure Data Factory**.
However, some rows in the file are **invalid or malformed** — for example:

* Missing required fields
* Incorrect data types
* Extra delimiters or corrupted values
* Date parsing errors

You need to **detect**, **handle**, and **log** these bad rows without failing the entire pipeline.

---

## 🧱 **High-Level Architecture Diagram**

```
+----------------------------+
| Azure Blob Storage         |
|----------------------------|
| Source File (CSV)          |
|                            |
|  ├── Valid rows            |
|  └── Invalid rows          |
+-------------+--------------+
              |
              v
  +---------------------------+
  | Azure Data Factory (ADF)  |
  | Mapping Data Flow         |
  |---------------------------|
  |  1. Source                |
  |  2. Derived Column        |
  |  3. Conditional Split     |
  |  4. Sink (Valid -> DB)    |
  |  5. Sink (Invalid -> Blob)|
  +-------------+-------------+
              |
              v
  +-----------------------------+
  | Azure SQL Database (Valid)  |
  | Azure Blob Storage (Invalid)|
  +-----------------------------+
```

---

## ⚙️ **Step-by-Step Implementation**

### **Step 1: Source Transformation**

* Connect your **source CSV** file from Azure Blob Storage.
* Enable **"Fault tolerance"** options in data flow settings:

  * `Skip error rows` → Yes
  * `Report rows with errors` → Enables bad data tracking

✅ **Tip:** ADF will automatically log parsing errors like mismatched columns or bad data types.

---

### **Step 2: Derived Column Transformation (Optional)**

Use this to perform **data cleansing or validation logic**.

Example:

```text
isValidEmail = iif(isMatch(Email, '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'), true(), false())
```

Or check nulls:

```text
isValidRecord = iif(!isNull(CustomerID) && !isNull(OrderDate), true(), false())
```

---

### **Step 3: Conditional Split Transformation**

Split the data into **valid** and **invalid** streams.

Example expression:

```text
iif(isValidRecord == true(), 'Valid', 'Invalid')
```

This gives you:

* ✅ **Valid stream** — clean rows ready for loading
* ❌ **Invalid stream** — malformed rows to be logged

---

### **Step 4: Sink 1 — Valid Data Sink**

* Target: **Azure SQL Database** (or Data Lake “Processed” zone)
* Operation: **Insert**
* Configure schema mapping properly

---

### **Step 5: Sink 2 — Invalid Data Sink**

* Target: **Azure Blob Storage (or Azure Data Lake)**
* File format: **DelimitedText or JSON**
* File name: include timestamp for traceability (e.g., `bad_records_2025_11_05.csv`)
* Include additional fields for debugging:

  * FileName
  * RowNumber
  * ErrorDescription
  * PipelineRunID

You can add these using a **Derived Column** before the sink:

```text
ErrorDescription = 'Invalid Email or Null CustomerID'
LoadDate = currentUTC()
```

---

### **Step 6: Pipeline-Level Logging (Optional)**

Add a **Stored Procedure Activity** or **Web Activity** after data flow to log summary metrics into a **logging table**, e.g.:

```sql
CREATE TABLE Pipeline_Run_Log (
    PipelineRunID NVARCHAR(50),
    SourceFile NVARCHAR(100),
    TotalRows INT,
    ValidRows INT,
    InvalidRows INT,
    StartTime DATETIME,
    EndTime DATETIME,
    Status NVARCHAR(20)
);
```

ADF can pass the **row counts** using data flow output parameters into the logging table.

---

## 🧩 **ADF Fault Tolerance Settings (Alternative)**

ADF Mapping Data Flow has a **"Fault tolerance"** tab where you can:

* **Skip malformed rows**
* **Redirect rows to error stream**
* **Collect error messages and file locations**

This approach is often used for simple file format issues like extra columns or bad delimiters.

---

## 💡 **Example Outcome**

| CustomerID | Email                                   | OrderDate  | isValidRecord | ErrorDescription        |
| ---------- | --------------------------------------- | ---------- | ------------- | ----------------------- |
| 1001       | [john@gmail.com](mailto:john@gmail.com) | 2025-11-05 | TRUE          | NULL                    |
| NULL       | [jane@xyz.com](mailto:jane@xyz.com)     | NULL       | FALSE         | Missing CustomerID/Date |
| 1003       | invalid-email                           | 2025-11-04 | FALSE         | Invalid Email Format    |

✅ Valid records go to SQL
❌ Invalid records are logged in Blob under `/bad_records/`

---

## 🧠 **Interview Key Points to Mention**

| Concept             | Talking Point                                                           |
| ------------------- | ----------------------------------------------------------------------- |
| **Error Handling**  | Use Conditional Split to route invalid records                          |
| **Logging**         | Store invalid records with context (error reason, file name, timestamp) |
| **Fault Tolerance** | Use Data Flow fault tolerance to skip/redirect malformed rows           |
| **Automation**      | Use Stored Procedure or Web Activity for run summary logging            |
| **Best Practice**   | Never drop bad data silently — always log for audit                     |

---

## 🚀 **Bonus: Advanced Enhancements**

* Integrate with **Azure Log Analytics** for centralized monitoring
* Trigger **Azure Function** or **Logic App** to send alerts if bad record % exceeds threshold
* Use **ADF Expressions** to dynamically name output error files
* Optionally use **Azure Data Quality Services (DQS)** for complex validation

---
Perfect — this is a **classic real-world and interview scenario** that tests your ability to design **efficient, production-grade data pipelines** in **Azure Data Factory (ADF)** using **Mapping Data Flows** for file format conversion and partitioning.

Below is a **complete, structured, and interview-ready answer** with a **diagram**, **step-by-step explanation**, and **key talking points** 👇

---

## 🎯 **Scenario**

You have **raw CSV files** landing in **Azure Blob Storage or ADLS “Raw Zone”**.
You need to:

1. Convert these files from **CSV → Parquet** (optimized columnar format)
2. **Partition the output** by **date** (e.g., `Year/Month/Day`)
3. Store them in **Azure Data Lake Storage (ADLS)** — in a **Processed or Curated Zone**

---

## 🧱 **High-Level Architecture Diagram**

```
+-----------------------------------+
|  Azure Blob Storage / ADLS (Raw)  |
|-----------------------------------|
|  sales_2025-11-05.csv             |
|  sales_2025-11-06.csv             |
+-------------------+---------------+
                    |
                    v
        +----------------------------+
        | Azure Data Factory (ADF)   |
        | Mapping Data Flow          |
        |----------------------------|
        | 1. Source (CSV)            |
        | 2. Derived Column (Date)   |
        | 3. Sink (Parquet + Partition) |
        +----------------------------+
                    |
                    v
+----------------------------------------------+
|  Azure Data Lake Storage (Processed Zone)    |
|----------------------------------------------|
| /year=2025/month=11/day=05/sales.parquet     |
| /year=2025/month=11/day=06/sales.parquet     |
+----------------------------------------------+
```

---

## ⚙️ **Step-by-Step Implementation**

### **Step 1: Create Linked Services**

* **Source Linked Service:** Azure Blob Storage (Raw Zone)
* **Sink Linked Service:** Azure Data Lake Storage Gen2 (Processed Zone)

---

### **Step 2: Create Datasets**

* **Source Dataset:**

  * Type: **DelimitedText (CSV)**
  * Points to the raw CSV folder
  * Schema: Import from a sample file
  * Enable “First row as header”
* **Sink Dataset:**

  * Type: **Parquet**
  * Points to ADLS processed zone
  * Do **not** hardcode file names; use dynamic expressions

---

### **Step 3: Build Mapping Data Flow**

#### 🔹 1. **Source Transformation**

* Load the CSV dataset.
* Optionally enable **wildcard paths** to pick up multiple files (`sales_*.csv`).

Example path:

```
@dataset().path
```

---

#### 🔹 2. **Derived Column Transformation**

Add columns for **partitioning** based on file name or a date column within data.

If the file has a column like `TransactionDate`, derive partition values:

```text
Year = year(toDate(TransactionDate))
Month = month(toDate(TransactionDate))
Day = day(toDate(TransactionDate))
```

Or, if the date is in the file name (like `sales_2025-11-05.csv`), use ADF system variable `@item().name` and extract date using string functions.

---

#### 🔹 3. **Sink Transformation**

Configure Sink to write **Parquet** files partitioned by date.

In **Sink Settings:**

* Dataset: Parquet dataset (pointing to ADLS folder)

* File format: Parquet

* File path:

  ```
  /year=$Year/month=$Month/day=$Day/
  ```

  (You can use dynamic content or derived column values.)

* **Partition Options:**

  * Enable **“Partition by column”**
  * Choose: `Year`, `Month`, `Day`

* Set “File name option” → “Output to single file” (if desired)

* Compression → Snappy (default Parquet compression)

---

### **Step 4: Pipeline Configuration**

* Add **Get Metadata** or **ForEach** activity to loop over all source CSV files.
* Inside ForEach → call the **Data Flow Activity**.
* Pass **file name** dynamically to the data flow for processing.

Example dynamic expression for parameter:

```
@item().name
```

---

### **Step 5: Schedule and Monitor**

* Schedule the pipeline (daily/trigger-based)
* Monitor pipeline runs in **ADF Monitor tab**
* Verify ADLS output folder structure:

  ```
  /processed/year=2025/month=11/day=05/sales.parquet
  ```

---

## 📊 **Example Folder Structure (Final Output)**

```
adls://sales-data/processed/
 ├── year=2025/
 │    ├── month=11/
 │    │     ├── day=05/
 │    │     │     └── sales.parquet
 │    │     ├── day=06/
 │    │     │     └── sales.parquet
```

Each folder corresponds to a logical partition.

---

## 💡 **Why Convert CSV to Parquet?**

| Feature            | CSV                  | Parquet                                  |
| ------------------ | -------------------- | ---------------------------------------- |
| Storage efficiency | Large (uncompressed) | Highly compressed                        |
| Query performance  | Slow (row-based)     | Fast (columnar)                          |
| Schema             | Text-based           | Self-describing (includes schema)        |
| Analytics tools    | Limited              | Optimized for Spark, Synapse, Databricks |

---

## 🧠 **Interview Key Points to Mention**

| Concept                     | Talking Point                                      |
| --------------------------- | -------------------------------------------------- |
| **ADF Mapping Data Flow**   | Best suited for format conversion and partitioning |
| **Partitioning Strategy**   | Improves query and read performance                |
| **Derived Column**          | Used to extract or compute partition values        |
| **Dynamic Sink Path**       | Enables automation for multiple dates/files        |
| **Monitoring & Validation** | Use debug mode and logs in ADF Monitor             |

---

## 🚀 **Bonus: Optimization Tips**

* Enable **Data Flow Debug Mode** to test output partitions.
* Use **parameterized pipelines** to dynamically handle multiple source paths.
* Leverage **Auto-scaling Integration Runtimes** for large file conversions.
* Store metadata (input/output paths, file counts) in a **logging table** for audit.

---

## 🧩 **Alternative Option**

If you need **complex transformation** or **large-scale data conversion**, use:

* **Azure Databricks**

  * Read CSV → `spark.read.csv()`
  * Write Parquet → `df.write.partitionBy("Year","Month","Day").parquet()`
  * Orchestrate using **ADF Notebook activity**

---



## 9. **Your pipeline needs to convert files from CSV to Parquet and partition them by date before storing in ADLS. How would you achieve this?**

*** Answer: ****

Perfect — this is a **classic real-world and interview scenario** that tests your ability to design **efficient, production-grade data pipelines** in **Azure Data Factory (ADF)** using **Mapping Data Flows** for file format conversion and partitioning.

Below is a **complete, structured, and interview-ready answer** with a **diagram**, **step-by-step explanation**, and **key talking points** 👇

---

## 🎯 **Scenario**

You have **raw CSV files** landing in **Azure Blob Storage or ADLS “Raw Zone”**.
You need to:

1. Convert these files from **CSV → Parquet** (optimized columnar format)
2. **Partition the output** by **date** (e.g., `Year/Month/Day`)
3. Store them in **Azure Data Lake Storage (ADLS)** — in a **Processed or Curated Zone**

---

## 🧱 **High-Level Architecture Diagram**

```
+-----------------------------------+
|  Azure Blob Storage / ADLS (Raw)  |
|-----------------------------------|
|  sales_2025-11-05.csv             |
|  sales_2025-11-06.csv             |
+-------------------+---------------+
                    |
                    v
        +----------------------------+
        | Azure Data Factory (ADF)   |
        | Mapping Data Flow          |
        |----------------------------|
        | 1. Source (CSV)            |
        | 2. Derived Column (Date)   |
        | 3. Sink (Parquet + Partition) |
        +----------------------------+
                    |
                    v
+----------------------------------------------+
|  Azure Data Lake Storage (Processed Zone)    |
|----------------------------------------------|
| /year=2025/month=11/day=05/sales.parquet     |
| /year=2025/month=11/day=06/sales.parquet     |
+----------------------------------------------+
```

---

## ⚙️ **Step-by-Step Implementation**

### **Step 1: Create Linked Services**

* **Source Linked Service:** Azure Blob Storage (Raw Zone)
* **Sink Linked Service:** Azure Data Lake Storage Gen2 (Processed Zone)

---

### **Step 2: Create Datasets**

* **Source Dataset:**

  * Type: **DelimitedText (CSV)**
  * Points to the raw CSV folder
  * Schema: Import from a sample file
  * Enable “First row as header”
* **Sink Dataset:**

  * Type: **Parquet**
  * Points to ADLS processed zone
  * Do **not** hardcode file names; use dynamic expressions

---

### **Step 3: Build Mapping Data Flow**

#### 🔹 1. **Source Transformation**

* Load the CSV dataset.
* Optionally enable **wildcard paths** to pick up multiple files (`sales_*.csv`).

Example path:

```
@dataset().path
```

---

#### 🔹 2. **Derived Column Transformation**

Add columns for **partitioning** based on file name or a date column within data.

If the file has a column like `TransactionDate`, derive partition values:

```text
Year = year(toDate(TransactionDate))
Month = month(toDate(TransactionDate))
Day = day(toDate(TransactionDate))
```

Or, if the date is in the file name (like `sales_2025-11-05.csv`), use ADF system variable `@item().name` and extract date using string functions.

---

#### 🔹 3. **Sink Transformation**

Configure Sink to write **Parquet** files partitioned by date.

In **Sink Settings:**

* Dataset: Parquet dataset (pointing to ADLS folder)

* File format: Parquet

* File path:

  ```
  /year=$Year/month=$Month/day=$Day/
  ```

  (You can use dynamic content or derived column values.)

* **Partition Options:**

  * Enable **“Partition by column”**
  * Choose: `Year`, `Month`, `Day`

* Set “File name option” → “Output to single file” (if desired)

* Compression → Snappy (default Parquet compression)

---

### **Step 4: Pipeline Configuration**

* Add **Get Metadata** or **ForEach** activity to loop over all source CSV files.
* Inside ForEach → call the **Data Flow Activity**.
* Pass **file name** dynamically to the data flow for processing.

Example dynamic expression for parameter:

```
@item().name
```

---

### **Step 5: Schedule and Monitor**

* Schedule the pipeline (daily/trigger-based)
* Monitor pipeline runs in **ADF Monitor tab**
* Verify ADLS output folder structure:

  ```
  /processed/year=2025/month=11/day=05/sales.parquet
  ```

---

## 📊 **Example Folder Structure (Final Output)**

```
adls://sales-data/processed/
 ├── year=2025/
 │    ├── month=11/
 │    │     ├── day=05/
 │    │     │     └── sales.parquet
 │    │     ├── day=06/
 │    │     │     └── sales.parquet
```

Each folder corresponds to a logical partition.

---

## 💡 **Why Convert CSV to Parquet?**

| Feature            | CSV                  | Parquet                                  |
| ------------------ | -------------------- | ---------------------------------------- |
| Storage efficiency | Large (uncompressed) | Highly compressed                        |
| Query performance  | Slow (row-based)     | Fast (columnar)                          |
| Schema             | Text-based           | Self-describing (includes schema)        |
| Analytics tools    | Limited              | Optimized for Spark, Synapse, Databricks |

---

## 🧠 **Interview Key Points to Mention**

| Concept                     | Talking Point                                      |
| --------------------------- | -------------------------------------------------- |
| **ADF Mapping Data Flow**   | Best suited for format conversion and partitioning |
| **Partitioning Strategy**   | Improves query and read performance                |
| **Derived Column**          | Used to extract or compute partition values        |
| **Dynamic Sink Path**       | Enables automation for multiple dates/files        |
| **Monitoring & Validation** | Use debug mode and logs in ADF Monitor             |

---

## 🚀 **Bonus: Optimization Tips**

* Enable **Data Flow Debug Mode** to test output partitions.
* Use **parameterized pipelines** to dynamically handle multiple source paths.
* Leverage **Auto-scaling Integration Runtimes** for large file conversions.
* Store metadata (input/output paths, file counts) in a **logging table** for audit.

---

## 🧩 **Alternative Option**

If you need **complex transformation** or **large-scale data conversion**, use:

* **Azure Databricks**

  * Read CSV → `spark.read.csv()`
  * Write Parquet → `df.write.partitionBy("Year","Month","Day").parquet()`
  * Orchestrate using **ADF Notebook activity**

---

### 🔷 Orchestration & Monitoring Scenarios

## 10. **How would you design a pipeline that runs every day at 2AM, but only if the upstream system has deposited a new file in Blob Storage?**

*** Answer: ****
Excellent — this is a **very practical and frequently asked scenario** in **Azure Data Factory (ADF)** interviews. It checks your ability to handle **event-based and schedule-based triggers together**, ensuring **automation with dependency awareness**.

Here’s a **complete, interview-quality answer** with a **diagram**, **step-by-step explanation**, and **best practices** 👇

---

## 🎯 **Scenario**

You need to design an **ADF pipeline** that:

* Runs **every day at 2 AM**
* But only **if a new file** has been **deposited in Azure Blob Storage** by an upstream system
* If no new file is available, **the pipeline should not run** (to avoid reprocessing old data)

---

## 🧱 **High-Level Architecture Diagram**

```
                   ┌───────────────────────────────┐
                   │   Upstream System              │
                   │ (Drops file in Blob Storage)   │
                   └──────────────┬────────────────┘
                                  │
                                  ▼
              +-------------------------------------+
              |  Azure Blob Storage (Landing Zone)  |
              |-------------------------------------|
              |  /incoming/sales_2025-11-05.csv     |
              +-----------------┬-------------------+
                                │
                                ▼
             +--------------------------------------+
             | Azure Data Factory (ADF) Pipeline    |
             |--------------------------------------|
             | 1. Trigger Check for New File        |
             | 2. If New File Found → Run Pipeline  |
             | 3. Else → Exit Gracefully            |
             +-----------------┬--------------------+
                               │
                               ▼
               +------------------------------------+
               |  Azure SQL / ADLS / Power BI       |
               | (Target System)                    |
               +------------------------------------+
```

---

## ⚙️ **Two Common Approaches (You Can Mention Either or Both)**

### **Approach 1: Event-Based Trigger (Recommended for Real-Time Scenarios)**

Use an **Event-Based Trigger** that fires **as soon as a new file is added** to Blob Storage.

#### ✅ Steps:

1. **Configure Event-Based Trigger** in ADF:

   * Type: **Blob Event Trigger**
   * Event: **Blob Created**
   * Storage Type: **Azure Blob Storage or ADLS Gen2**
   * Container: e.g., `/incoming`
   * File path filter: e.g., `sales_*.csv`

2. **Trigger → ADF Pipeline**

   * The pipeline will **automatically run whenever a new file arrives**.
   * You can also add a **filter activity** to ensure it only processes specific files (by date or pattern).

3. **Optional Scheduling Constraint**

   * If the business rule says *only after 2 AM*, you can use:

     * A **Wait activity** (until 2 AM)
     * Or **time window validation** before processing.

#### ⚙️ Example Flow:

```
Blob Upload → Event Grid → ADF Event Trigger → Pipeline Executes
```

---

### **Approach 2: Scheduled Trigger + File Check Logic (Controlled 2 AM Runs)**

Use a **Time-Based (Schedule) Trigger** that runs **every day at 2 AM**, but add logic inside the pipeline to **check for file presence** before proceeding.

#### ✅ Steps:

1. **ADF Trigger:**

   * Type: **Schedule Trigger**
   * Time: **2:00 AM IST**
   * Recurrence: **Daily**

2. **Pipeline Activities:**

   ```
   ADF Pipeline: CheckAndProcessFile
   ├── Get Metadata Activity → check file in Blob
   ├── If Condition Activity
   │     ├── [True] → Execute Data Flow / Copy Activity
   │     └── [False] → Log & End Pipeline
   ```

#### 🔹 **Step 1: Get Metadata Activity**

* Linked Service: Azure Blob Storage
* Point to the folder `/incoming/`
* Configure: “Field list → Child Items”

#### 🔹 **Step 2: If Condition Activity**

Expression example:

```text
@greater(length(activity('Get Metadata').output.childItems), 0)
```

➡ **True branch:**
Run Copy or Data Flow activity (process the file)

➡ **False branch:**
Log “No new file found” into SQL/Log Analytics or simply end pipeline.

#### 🔹 **Step 3: Optional Enhancements**

* Track the **last processed file name** in a metadata table, and compare to detect **only new files**.
* Delete or move processed files to `/archive/` after completion.

---

## 🧩 **Sample Folder Flow**

```
/incoming/sales_2025-11-05.csv    → New file detected at 1:45 AM
/scheduled pipeline runs @ 2:00AM
 → File found → Process → Move to /archive/
/incoming/ empty → Next run waits for next file
```

---

## 🧠 **Interview Key Points to Mention**

| Concept                 | Explanation                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| **Event-Based Trigger** | Best when you need real-time response to file arrival            |
| **Scheduled Trigger**   | Best when pipeline must run at a specific time (e.g., 2 AM)      |
| **File Presence Check** | Use *Get Metadata + If Condition*                                |
| **Idempotency**         | Always check last processed file to avoid duplicates             |
| **Logging**             | Log file names, timestamps, and status for audit trail           |
| **Scalability**         | You can extend logic for multiple file types using ForEach loops |

---

## 🚀 **Best Practice Hybrid Approach**

Use **Event-Based Trigger + Validation Window**:

* Event trigger starts pipeline immediately when file lands.
* Pipeline includes a **Wait or Time Check activity**:

  * If file lands early (say at midnight), it waits until **2 AM** to process.
* Combines **event-driven automation** with **schedule enforcement**.

---

## ✅ **Example Pseudocode Logic (in ADF Expressions)**

**If Condition Expression:**

```text
@and(
    greater(length(activity('Get Metadata').output.childItems), 0),
    equals(formatDateTime(utcNow(),'HH:mm'), '02:00')
)
```

---

## 📊 **Logging Table Example**

| RunDate    | FileName             | Status  | Remarks              |
| ---------- | -------------------- | ------- | -------------------- |
| 2025-11-05 | sales_2025-11-05.csv | Success | Processed at 2:03 AM |
| 2025-11-06 | (none)               | Skipped | No new file found    |

---

## 💬 **Final Summary (Answer for Interview)**

> “I would design this using a **daily schedule trigger at 2 AM** combined with a **file existence check** inside the pipeline.
> The pipeline uses a **Get Metadata** activity to check if a new file has been deposited in Blob Storage.
> If found, it proceeds with transformation or loading; otherwise, it exits gracefully.
>
> Alternatively, for real-time scenarios, I can use an **event-based trigger** that automatically starts the pipeline as soon as a new file is uploaded.
> Both methods ensure that the pipeline only runs when valid new data is available, preventing unnecessary executions.”

---



## 11. **How would you retry a failed activity only 3 times and send a Teams notification if it still fails?**

*** Answer: ****



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
