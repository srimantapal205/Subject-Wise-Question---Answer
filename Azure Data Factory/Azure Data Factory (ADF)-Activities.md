# Azure Data Factory (ADF) - Activities

In **Azure Data Factory (ADF)**, **activities** are the building blocks of a pipeline. They define the actions you want to perform on your data — such as copying, transforming, controlling flow, or executing external processes.

Here is a detailed explanation of **all key activity types**, their **functionality**, and **real-world use cases/scenarios**.

---

### 🔹 1. **Data Movement Activities**

#### **Copy Data Activity**

* **Function:** Copies data from source to sink (destination).
* **Common Sources/Sinks:** Blob Storage, SQL DB, Data Lake, REST API, S3, etc.
* **Scenario:**

  > Copy sales data from Amazon S3 to Azure SQL Database daily for reporting.

---

### 🔹 2. **Data Transformation Activities (Mapping Data Flows)**

#### **Data Flow Activity**

* **Function:** Performs complex transformations using a visual interface.
* **Features:** Joins, Aggregates, Derived Columns, Conditional Splits, etc.
* **Scenario:**

  > Clean IoT sensor data, remove nulls, calculate average temperature, and load to Azure Data Lake.

---

### 🔹 3. **Control Flow Activities**

These manage pipeline execution flow.

#### **Wait**

* **Function:** Delays pipeline for specified time.
* **Scenario:**

  > Wait 10 minutes after a file copy to ensure downstream system has picked it up.

#### **If Condition**

* **Function:** Executes activities based on a condition.
* **Scenario:**

  > If a file exists in Blob Storage, then proceed to copy and transform, else send alert.

#### **Switch**

* **Function:** Branches logic based on multiple possible values.
* **Scenario:**

  > Process data differently for each `Region` (e.g., US, EU, APAC).

#### **ForEach**

* **Function:** Iterates over a collection (e.g., list of files or tables).
* **Scenario:**

  > Loop over a list of table names and copy each to a destination SQL DB.

#### **Until**

* **Function:** Repeats activities until a condition is met.
* **Scenario:**

  > Check every 5 minutes if a specific file has landed; continue only after the file arrives.

---

### 🔹 4. **External Execution Activities**

#### **Stored Procedure**

* **Function:** Executes a stored procedure in SQL DB.
* **Scenario:**

  > Call a stored procedure after data load to update summary tables.

#### **Lookup**

* **Function:** Executes a query and retrieves data (scalar or result set).
* **Scenario:**

  > Lookup last successful load date to perform incremental load.

#### **Web Activity**

* **Function:** Call a REST endpoint.
* **Scenario:**

  > Trigger a Logic App or send a Teams/Slack notification.

#### **Webhook Activity**

* **Function:** Waits for a callback from external system after triggering a web request.
* **Scenario:**

  > Trigger a third-party data enrichment service and wait for its completion.

#### **Azure Function Activity**

* **Function:** Call a custom Azure Function for complex logic.
* **Scenario:**

  > Validate file format before ingestion using custom function logic.

#### **Databricks Notebook / Python / Jar Activity**

* **Function:** Runs notebooks or scripts in Azure Databricks.
* **Scenario:**

  > Run a machine learning model to predict customer churn.

#### **HDInsight Activity**

* **Function:** Execute Hive, Pig, MapReduce, Spark jobs on HDInsight.
* **Scenario:**

  > Run a Spark job on a Hadoop cluster for log processing.

#### **Azure Batch Service**

* **Function:** Run parallel compute-intensive jobs.
* **Scenario:**

  > Process millions of images in batches using custom code.

#### **Execute Pipeline**

* **Function:** Call another pipeline as a child process.
* **Scenario:**

  > Master pipeline calls daily data load pipelines for each department.

---

### 🔹 5. **Iteration & Branching Activities (Extended)**

#### **Append Variable**

* **Function:** Adds a value to an array variable.
* **Scenario:**

  > Store list of successfully processed files for logging.

#### **Set Variable**

* **Function:** Assigns value to a variable.
* **Scenario:**

  > Set status = “Completed” after file processing ends.

#### **Get Metadata**

* **Function:** Retrieves metadata from a dataset (e.g., file name, size).
* **Scenario:**

  > Check if today's data file exists in blob by reading file metadata.

---

### 🔹 6. **Validation & Monitoring Activities**

#### **Validation Activity**

* **Function:** Checks for existence of files, folders, tables, etc.
* **Scenario:**

  > Validate that file exists before initiating transformation.

#### **Fail Activity**

* **Function:** Forces pipeline to fail intentionally.
* **Scenario:**

  > If a required file is missing or validation fails, stop pipeline with error.

#### **Until with Web Activity (Polling Pattern)**

* **Scenario:**

  > Use `Until` with `Web` to poll API every 10 seconds until `status=completed`.

---

## ✅ Example Real-World Use Case

### **Scenario:** Daily Sales Data Ingestion and Reporting

#### Steps:

1. **Get Metadata** – Check if daily sales CSV exists in Blob.
2. **If Condition** – If exists, proceed. Else, send alert via Web Activity.
3. **Copy Data** – Load raw CSV data to Azure Data Lake.
4. **Data Flow Activity** – Clean and transform sales data (remove duplicates, derive fields).
5. **Stored Procedure** – Run SP to update reporting tables.
6. **Execute Pipeline** – Call pipeline to refresh Power BI dataset.
7. **Web Activity** – Notify business users of completion.

---

Would you like a **visual diagram** or **ADF JSON template** of such a use case?
