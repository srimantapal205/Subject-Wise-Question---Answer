# Azure Data Factory

### 1. How to copy data from REST API multiple page response using ADF
#### Answer:To **copy data from a REST API with multiple pages** using **Azure Data Factory (ADF)**, you can follow these steps. ADF supports pagination rules when calling REST APIs, allowing you to retrieve data across multiple pages and copy it into your target storage.

---

## ✅ Step-by-Step Guide: Copy Paginated REST API Data in ADF

### **1. Create Linked Services**

* **REST API Linked Service**

  * Go to **Manage > Linked services > New > REST**.
  * Set the **Base URL** (e.g., `https://api.example.com/data`).
  * Configure authentication (if needed).

* **Sink Linked Service** (e.g., Azure Blob, Azure SQL Database, etc.)

---

### **2. Create Dataset for REST Source**

* Go to **Author > Datasets > New dataset > REST**.
* Choose the REST linked service.
* Set the relative URL (e.g., `/data?page=1` or just `/data`).
* Set request method: `GET`.
* If the response is JSON, point to the correct `JSONPath` (e.g., `$.items`).

---

### **3. Define Pagination Rules**

In the **Source** settings of your Copy Activity:

#### ADF supports several pagination methods:

| Pagination Type        | Description                                   |
| ---------------------- | --------------------------------------------- |
| **Absolute URL**       | If the API response gives a `nextPageUrl`.    |
| **Next Page Number**   | If the API uses `?page=2`, `?page=3`, etc.    |
| **Continuation Token** | If the response has a token like `nextToken`. |

You set this in the **Copy Activity > Source > Pagination rules**.

---

### **Example: Page Number Pagination**

Suppose your API supports this URL pattern:

```
https://api.example.com/data?page=1
```

And the response includes metadata like:

```json
{
  "items": [...],
  "page": 1,
  "pageSize": 100,
  "totalPages": 5
}
```

#### In ADF Copy Activity:

* Go to **Source > Pagination rules**:

  * **Pagination rule type**: *"By page number"*
  * **Start page**: `1`
  * **Page size**: `100` (optional)
  * **Maximum number of pages**: `5` (or use dynamic expression)
* Define the pagination logic using **dynamic content** if `totalPages` is dynamic.

> ⚠️ If the total number of pages is not known in advance, you'll need to create a loop using **Until activity** in a pipeline.

---

### **4. Optional: Use Until Loop for Dynamic Pagination**

If the API doesn't tell you how many pages exist in advance:

#### Use this pattern:

1. **Web Activity**: Call the first page of the API.
2. **Set Variable Activity**: Store next page number or token.
3. **Until Activity**:

   * Inside: Call REST API with dynamic page/token.
   * Use Copy Activity to load data.
   * Use `If` + `Set Variable` to control when to stop (e.g., if next page is null).

---

### **5. Sink Settings**

* Set up your **sink dataset** (Azure SQL/Blob/Parquet/Delta/etc.).
* Configure schema mapping if needed.

---

## 🧪 Example JSON Response with "next" URL

```json
{
  "data": [...],
  "next": "https://api.example.com/data?page=2"
}
```

In this case, set:

* **Pagination rule type**: *Absolute URL*.
* **Absolute URL path**: `$.next`

ADF will follow the `next` link until it is null or not returned.

---

## ✅ Best Practices

* Test the API manually using Postman first.
* Ensure the API supports a reasonable rate limit.
* Use **retry policies** in Copy Activity.
* Handle API errors gracefully with **Try-Catch** (e.g., `If Condition` and `Web Activity`).

---


### 2. How to convert Timezone using Dataflow in ADF
#### Answer:In **Azure Data Factory (ADF) Data Flow**, converting time from one **timezone to another** can be done using the **`toUTC()`**, **`toLocal()`**, or **`convertTimeZone()`** functions in **Derived Column** transformation.

---

## ✅ Use Case

You have a datetime column in one timezone (e.g., UTC), and you want to convert it to another timezone (e.g., `India Standard Time` or `Pacific Standard Time`).

---

## 🔧 Step-by-Step: Timezone Conversion in ADF Data Flow

### **1. Add a Data Flow to Your Pipeline**

* Go to **Author > Data Flows > New Data Flow**.

### **2. Source**

* Add a **source dataset** that contains the datetime column (e.g., `event_time`).

### **3. Derived Column**

* Add a **Derived Column** transformation.
* Create a new column (or replace existing) with timezone-converted datetime.

---

### ✅ Option 1: Convert from UTC to Local Timezone

```plaintext
toLocal(event_time, 'India Standard Time')
```

This converts from UTC to **IST**.

### ✅ Option 2: Convert from Local to UTC

```plaintext
toUTC(event_time, 'Pacific Standard Time')
```

This assumes `event_time` is in PST and converts to UTC.

### ✅ Option 3: Convert Between Any Two Timezones

```plaintext
convertTimeZone(event_time, 'UTC', 'India Standard Time')
```

This converts from **UTC → IST** explicitly.

---

## 🕐 Supported Timezone Names

Use full **Windows timezone IDs** like:

* `UTC`
* `India Standard Time`
* `Pacific Standard Time`
* `Eastern Standard Time`
* `W. Europe Standard Time`

> ⚠️ **IANA timezone names** (like `Asia/Kolkata`, `America/Los_Angeles`) are **not supported**. Stick to **Windows timezone IDs**.

---

## 📌 Example

If your `event_time` is `"2025-06-06T10:00:00Z"` (UTC), and you want to convert to IST:

### Expression:

```plaintext
convertTimeZone(event_time, 'UTC', 'India Standard Time')
```

### Result:

`2025-06-06T15:30:00` (IST is UTC +5:30)

---

## ✅ Final Step: Sink

* Add the **sink** dataset (Azure SQL, Parquet, Blob, etc.).
* Map the derived column to the destination field.

---

## 🧪 Bonus Tip

You can chain timezone conversion with formatting:

```plaintext
formatDateTime(convertTimeZone(event_time, 'UTC', 'India Standard Time'), 'yyyy-MM-dd HH:mm:ss')
```

---


### 3. How to round off decimal number in pipeline expression using ADF
#### Answer:In **Azure Data Factory (ADF)**, you can round off decimal numbers directly in **pipeline expressions** using the built-in **`round()`** function.

---

## ✅ Syntax of `round()` in ADF Expression Language

```plaintext
round(value, digits)
```

* `value`: The decimal number you want to round.
* `digits`: The number of decimal places to keep (can be 0 or more).

---

## 🔧 Examples

### 🔹 Round to 2 decimal places:

```plaintext
round(3.14159, 2)
```

✅ Output: `3.14`

### 🔹 Round to nearest integer:

```plaintext
round(5.67, 0)
```

✅ Output: `6`

### 🔹 Round down with a negative number of digits (e.g., to nearest ten):

```plaintext
round(123.45, -1)
```

✅ Output: `120`

---

## 🛠️ Where to Use This in ADF

### 1. **Set Variable Activity**

You can use the `round()` function like this:

```plaintext
@round(variables('price'), 2)
```

### 2. **Derived Column in Data Flow**

If you're working in **Data Flow**, use expression language (no `@`) like:

```plaintext
round(amount, 2)
```

### 3. **Mapping Data Flows > Conditional Split or Sink Mapping**

* Use `round(columnName, 0)` to clean or normalize numeric data.

---

## ⚠️ Notes

* `round()` in **pipeline expressions** uses `@` notation.
* In **Data Flows**, use without `@`.

---


### 4. How to download zip file from API and load into sink path after unzip using ADF
#### Answer:To **download a ZIP file from a REST API**, **unzip it**, and **load its content into a sink path** (like Azure Blob Storage or Data Lake) using **Azure Data Factory (ADF)**, you need to combine **Web Activity**, **Azure Function or Azure Batch**, and **Copy Activity**.

---

## ✅ High-Level Architecture

```plaintext
[Web Activity] → [Azure Function / Batch (Unzip)] → [Copy Activity to Sink]
```

---

## 🔧 Step-by-Step Guide

### ### 1. **Use Web Activity to Download ZIP File**

ADF cannot **natively download and save a binary file**, so:

* **Web Activity** calls the **API** that returns the **ZIP file**.
* You must handle the file **in code** (via Azure Function or Azure Batch) because ADF can't save binary HTTP response directly.

---

### 2. **Create an Azure Function to Handle the Download + Unzip**

This function should:

* Call the REST API using `requests` or `http.client`.
* Read the binary `.zip` file from the response.
* Extract the contents to a temporary location or directly to Azure Blob/ADLS using `azure-storage-blob` SDK.

#### ✅ Sample Python Code for Azure Function

```python
import os, zipfile, io, requests
from azure.storage.blob import BlobServiceClient
import logging

def main(req):
    zip_url = "https://example.com/download/file.zip"
    response = requests.get(zip_url)
    if response.status_code == 200:
        blob_service_client = BlobServiceClient.from_connection_string("Your_Connection_String")
        container_name = "unzipped-files"
        zipfile_obj = zipfile.ZipFile(io.BytesIO(response.content))
        
        for file_name in zipfile_obj.namelist():
            file_data = zipfile_obj.read(file_name)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob_client.upload_blob(file_data, overwrite=True)

        return "Success"
    else:
        return f"Failed to download zip: {response.status_code}"
```

---

### 3. **Call Azure Function from ADF**

* Use **Web Activity** to trigger the Azure Function.
* Method: `POST` or `GET` depending on your function setup.
* Pass API endpoint, blob container, and storage credentials via parameters (secured via Azure Key Vault ideally).

---

### 4. **Use Copy Activity to Load Unzipped Data to Final Sink**

* Now that files are in Blob/ADLS (e.g., CSVs inside the zip), use a **Copy Activity** to move them to the final destination.
* You can apply transformations or mappings if needed.

---

## 🧪 Optional: Use Data Flow for Further Processing

Once files are unzipped and saved, use **Data Flow** to:

* Transform
* Filter
* Aggregate
* Load into SQL, Synapse, etc.

---

## 🛑 Why You Can’t Do This with Just Copy Activity

* **Copy Activity doesn’t support unzipping archives or parsing binary HTTP response**.
* You need Azure Function, Azure Batch, or Azure Logic Apps to handle binary + unzip.

---

## ✅ Alternative with Azure Logic Apps

If you prefer **low-code**, Logic Apps can:

1. Call REST API.
2. Save ZIP to Blob.
3. Unzip using Azure Storage actions.
4. Trigger ADF pipeline or Copy Activity.

---

## 💡 Best Practice

* Use **Azure Function** for flexibility and performance.
* Store credentials in **Azure Key Vault**.
* Monitor each step with **ADF activity logs**.

---

### 5. How to download files from API and load into sink path using Azure Data Factory
#### Answer:To **download files from a REST API** and **load them into a sink path** (like Azure Blob Storage, ADLS, etc.) using **Azure Data Factory (ADF)**, follow this pattern:

---

## ✅ Scenario

You want to:

1. Call an API that returns file content (e.g., PDF, CSV, JSON, etc.).
2. Save the file to Azure Blob Storage / ADLS Gen2.

---

## ✅ ADF Doesn’t Support Binary Response Handling Directly

### ❌ Limitation:

ADF’s **Copy Activity** and **Web Activity** can **call APIs** but **cannot handle binary responses like files** directly (e.g., `.pdf`, `.csv`, `.zip`, etc.).

### ✅ Solution:

You need to use **Azure Function** or **Azure Logic App** to:

* Call the API,
* Get the binary content,
* Write it to Blob Storage,
* Then optionally trigger further ADF activities.

---

## ✅ Step-by-Step Guide

### 🔹 Step 1: Create an Azure Function to Download the File

#### Sample Python Code (HTTP Trigger):

```python
import requests
from azure.storage.blob import BlobServiceClient
import os

def main(req):
    # API endpoint
    file_url = "https://example.com/api/file/download"
    
    # Call API
    response = requests.get(file_url)
    
    if response.status_code == 200:
        file_bytes = response.content
        file_name = "downloaded_file.csv"  # dynamic if needed

        # Upload to Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string("Your_Connection_String")
        container_client = blob_service_client.get_container_client("your-container")
        blob_client = container_client.get_blob_client(file_name)

        blob_client.upload_blob(file_bytes, overwrite=True)
        return "Success"
    else:
        return f"Failed to download file: {response.status_code}"
```

> You can enhance the function to:
>
> * Take file name from query params,
> * Loop through a list of files,
> * Accept authentication headers.

---

### 🔹 Step 2: Deploy the Azure Function

1. Deploy to Azure.
2. Secure with Azure AD, Key, or allow anonymous for test.
3. Note the Function URL.

---

### 🔹 Step 3: Call Azure Function from ADF

* Add a **Web Activity** in your pipeline.
* Set **URL** to your Azure Function URL.
* Method: `POST` or `GET` (as per your function).
* Body (optional): pass parameters like `fileUrl`, `filename`, `containerName`.

---

### 🔹 Step 4: Load Into Sink (Optional Copy Activity)

If you need to:

* Transform or move the file to another format/location,
* Add a **Copy Activity** after the Web Activity.

Use Blob Storage as the **source** and define the **sink** path as needed (e.g., Azure SQL, another container, etc.).

---

## ✅ Optional Enhancements

| Requirement                       | Add This                                           |
| --------------------------------- | -------------------------------------------------- |
| Download multiple files           | Use **ForEach** loop in ADF with dynamic file list |
| Authenticated API                 | Pass headers via Web Activity or Function          |
| Monitor logs                      | Enable **Application Insights** in Azure Function  |
| Unzip after download              | Add unzip logic in Azure Function                  |
| Trigger function only when needed | Use **If Condition** before Web Activity           |

---

## 🧪 Example Use Cases

* Download daily sales reports (`.csv`) from an API and store in ADLS.
* Pull customer invoice PDFs and save to Blob.
* Get JSON logs from a monitoring API and archive them.

---

### 6. How to split single rows data into multiple rows using Mapping Data Flows in Azure Data Factory
#### Answer:To **split a single row of data into multiple rows** using **Mapping Data Flows in Azure Data Factory (ADF)**, you typically use the **`Flatten`** or **`Derived Column + Explode-like logic`**, depending on the structure of your data.

---

## ✅ Common Scenarios

### 1. **Splitting a Delimited String (e.g., CSV inside a column)**

You have a column like:

| ID | Items        |
| -- | ------------ |
| 1  | Apple,Banana |

You want to split it into:

| ID | Item   |
| -- | ------ |
| 1  | Apple  |
| 1  | Banana |

---

## 🔧 Step-by-Step: Split Row into Multiple Rows (Delimited String)

### ✅ Step 1: Source

Load the dataset where one of the columns contains delimited data (e.g., `"Apple,Banana,Orange"`).

### ✅ Step 2: Add **Derived Column**

Add a new column that **splits the string into an array**.

Example:

```plaintext
split(Items, ',')
```

This gives you an array: `["Apple", "Banana", "Orange"]`

Let’s say you name the new column: `ItemsArray`.

### ✅ Step 3: Add **Flatten Transformation**

* Flatten the new array column: `ItemsArray`
* It will unroll each element of the array into a separate row.

Set:

* **Unroll by**: `ItemsArray`

### ✅ Step 4: Rename the Flattened Column

* The new column will be named like `ItemsArray` or `ItemsArray.Item`.
* Use **Select** or another **Derived Column** to rename it to something like `Item`.

### ✅ Step 5: Sink

Write the output to your destination (Blob, SQL DB, ADLS, etc.).

---

## 📌 Final Flow Example

```plaintext
Source
  ↓
Derived Column: split(Items, ',') → ItemsArray
  ↓
Flatten: unroll ItemsArray
  ↓
Select: rename ItemsArray → Item
  ↓
Sink
```

---

## 🧪 Sample Input/Output

### Input (Single Row):

| ID | Items              |
| -- | ------------------ |
| 1  | Apple,Banana,Mango |

### Output (Multiple Rows):

| ID | Item   |
| -- | ------ |
| 1  | Apple  |
| 1  | Banana |
| 1  | Mango  |

---

## ✅ Bonus: JSON Arrays or Nested Arrays

If your input is JSON and the field is already an **array**, you can directly use **Flatten** without a split.

---

## ❗ Notes

* `split()` only works on strings, not arrays.
* `Flatten` only works on **array columns**.
* If you need to flatten **nested JSON**, use **Parse + Flatten**.

---


### 7. How to send email alert on pipeline failure using ADF
#### Answer: To **send an email alert on pipeline failure in Azure Data Factory (ADF)**, you can use one of these recommended methods:

---

## ✅ Recommended Methods

### **Option 1: Send Email via Azure Logic App (Best Practice)**

Use a **Logic App** to send the email, and trigger it from the ADF pipeline failure.

---

### 🔧 Step-by-Step: Logic App + ADF Failure

#### **1. Create a Logic App to Send Email**

* Go to **Azure Portal > Logic Apps > Create**
* Use **"When an HTTP request is received"** as trigger
* Add **"Send an Email (V2)"** from Outlook or Gmail connector
* Add dynamic content like:

  * Subject: `"ADF Pipeline Failed: @{triggerBody().pipelineName}"`
  * Body: Include failure reason, pipeline name, etc.

Example output body:

```json
{
  "pipelineName": "@{triggerBody().pipelineName}",
  "errorMessage": "@{triggerBody().errorMessage}",
  "runId": "@{triggerBody().runId}"
}
```

* Save the Logic App and copy the **HTTP POST URL**

---

#### **2. Call the Logic App from ADF on Failure**

* In ADF Pipeline, add a **Web Activity**
* Place it inside the **Failure path** (use red failure arrow)
* Configure:

  * **URL**: Paste Logic App POST URL
  * **Method**: POST
  * **Headers**: `{ "Content-Type": "application/json" }`
  * **Body** (example):

    ```json
    {
      "pipelineName": "@pipeline().Pipeline",
      "runId": "@pipeline().RunId",
      "errorMessage": "Pipeline failed"
    }
    ```

---

### 📌 Use `@pipeline()` Expressions:

* `@pipeline().Pipeline`: Current pipeline name
* `@pipeline().RunId`: Unique run ID

---

### ✅ Option 2: Alert via Azure Monitor (Basic Notification)

If you're using **Azure Monitor**, you can:

1. Go to **Azure Portal > Alerts > Create Alert**
2. Set **Target** as your ADF pipeline
3. Condition: `"Pipeline failed"`
4. Action: Email, SMS, webhook, or Logic App

➡️ This is useful for **email alerts without changing pipeline**.

---

## ✅ Best Practice

| Task                           | Recommendation                                         |
| ------------------------------ | ------------------------------------------------------ |
| Custom email body / formatting | Use **Logic Apps**                                     |
| Secure email integration       | Use **Managed Identity** or OAuth                      |
| Multiple recipients            | Use distribution list                                  |
| Logs and diagnostics           | Enable **ADF diagnostic settings** + **Log Analytics** |

---

## 🧪 Bonus: Retry Logic

Combine alerts with **retry policies** to avoid alerting on transient issues.

---

### 8. Merge multiple rows value into single row using dataflow
#### Answer: To **merge multiple rows into a single row** in **Mapping Data Flows** in **Azure Data Factory (ADF)** — also known as **row aggregation or pivoting** — you typically use a combination of **`Aggregate`** and optionally **`Derived Column`** transformations.

---

## ✅ Scenario Example

### **Input: Multiple Rows**

| ID | Item   |
| -- | ------ |
| 1  | Apple  |
| 1  | Banana |
| 1  | Mango  |

### **Goal: Single Row (Merged Column)**

| ID | Items              |
| -- | ------------------ |
| 1  | Apple,Banana,Mango |

---

## 🔧 Step-by-Step: Merge Rows into Single Row Using Mapping Data Flow

### ✅ Step 1: **Source**

* Load your input data (from SQL, Blob, ADLS, etc.)

### ✅ Step 2: **Aggregate**

* Add an **Aggregate** transformation.

#### Group By:

* `ID` (or the field you want to group by)

#### Aggregates:

* Create a new column (e.g., `MergedItems`)
* Use expression:

```plaintext
collect(Item)
```

This creates an **array** of all `Item` values grouped by `ID`.

---

### ✅ Step 3: **Derived Column**

* Add a **Derived Column** transformation to convert the array into a string.

#### Example:

```plaintext
arrayToString(MergedItems, ',')
```

This converts the array `["Apple", "Banana", "Mango"]` → `"Apple,Banana,Mango"`

You can name this column `Items`.

---

### ✅ Step 4: **Sink**

* Output to your target sink (SQL, Blob, ADLS, etc.)

---

## 🧪 Example Input → Output

**Input:**

| ID | Item   |
| -- | ------ |
| 1  | Apple  |
| 1  | Banana |
| 1  | Mango  |

**Output:**

| ID | Items              |
| -- | ------------------ |
| 1  | Apple,Banana,Mango |

---

## ✅ Full Data Flow Overview

```plaintext
[Source]
   ↓
[Aggregate]
   Group by: ID
   Aggregates: collect(Item) → MergedItems (array)
   ↓
[Derived Column]
   Items = arrayToString(MergedItems, ',')
   ↓
[Sink]
```

---

## 📝 Notes

* `collect()` turns a column into an array of values for that group.
* `arrayToString()` joins array elements using a delimiter.
* This works for **text, numbers**, etc., but not for complex types like structs or maps.

---

### 9. Dynamic sink based on file format in Azure Data Factory Azure Data Factory
#### Answer:In Azure Data Factory (ADF), to implement a **dynamic sink based on file format** (e.g., writing output to CSV, JSON, Parquet dynamically), you can use **Mapping Data Flows** or **Copy Activity with dynamic dataset parameters**.

---

## ✅ How to Configure Dynamic Sink Based on File Format in ADF

---

### Option 1: **Dynamic Sink in Mapping Data Flow**

---

#### 🔧 Steps:

1. **Create Source Dataset**

   * Connect to your source (Blob, SQL, etc.)

2. **Add Sink Transformation**

   * In the sink settings, you can parameterize:

     * File format (CSV, JSON, Parquet)
     * File name, folder path, compression, etc.

3. **Parameterize Sink Dataset**

   * Create a **dataset parameter** called `fileFormat` (string).
   * Set dataset's **format** dynamically using that parameter.

4. **Configure Sink Dataset Format Using Parameters**

   * Unfortunately, dataset format (e.g., CSV vs Parquet) **cannot be changed dynamically inside one dataset**.
   * Instead, **create multiple datasets** with different formats (one for CSV, one for JSON, one for Parquet), each with parameters for path, filename, etc.

5. **In Data Flow Sink, Use Expression to Choose Dataset**

   * Use a **parameter** in the pipeline (e.g., `sinkFormat`).
   * Pass the parameter to the Data Flow.

6. **Use Data Flow Parameters or Pipeline Logic**

   * In **pipeline**, use **If Condition** or **Switch** activity to call Data Flow with specific sink dataset based on `sinkFormat`.
   * Alternatively, in Data Flow, use **Sink** with dataset parameterized for path, and inside pipeline, switch the dataset dynamically by setting the dataset parameter or calling different Data Flows.

---

### Option 2: **Dynamic Sink in Copy Activity**

---

#### 🔧 Steps:

1. **Create Multiple Sink Datasets**

   * Create one dataset for each file format (CSV, JSON, Parquet).
   * Each dataset parameterized for folder path and file name.

2. **In Pipeline, Use Parameter `sinkFormat`**

   * Use **If Condition** or **Switch Activity** based on `sinkFormat`.

3. **Based on SinkFormat, Choose Copy Activity Dataset**

   * Have different Copy Activities or one Copy Activity with dynamic dataset using `@pipeline().parameters.sinkFormat`.

4. **Use Dataset Parameter for File Path and Name**

---

### Sample Pipeline Parameter:

```json
{
  "name": "sinkFormat",
  "type": "String",
  "defaultValue": "csv"
}
```

### Sample Switch Activity on `sinkFormat`:

| Case    | Activity                      |
| ------- | ----------------------------- |
| csv     | CopyActivity using CSV DS     |
| json    | CopyActivity using JSON DS    |
| parquet | CopyActivity using Parquet DS |

---

## ✅ Summary Table

| Feature                              | Possible | Notes                                                                 |
| ------------------------------------ | -------- | --------------------------------------------------------------------- |
| Single dataset format dynamic change | ❌        | Dataset format is fixed                                               |
| Use multiple datasets dynamically    | ✅        | Use Switch or If in pipeline                                          |
| Parameterize path & file name        | ✅        | Works well for dynamic naming                                         |
| Dynamic sink inside Data Flow        | Partial  | Parameterize path, but format switch needs multiple datasets or flows |

---

## 🤔 Additional Tips

* Use **parameters** for path, filename, partition folders.
* For big pipelines, keep dataset count manageable by using parameters for paths.
* For many formats, use **Switch** or **If Condition** to select Copy Activity or Data Flow.

---


### 10. Dynamic column mapping in Azure Data Factory
#### Answer: In **Azure Data Factory (ADF)**, **dynamic column mapping** lets you flexibly map source columns to sink columns at runtime instead of hardcoding them. This is useful when:

* Source schemas change,
* You want to load multiple tables with different columns,
* Or want to avoid re-publishing for minor mapping changes.

---

## ✅ How to Implement Dynamic Column Mapping in ADF

---

### Option 1: **Copy Activity with Mapping as JSON Expression**

* In **Copy Activity**, you can specify the **`mapping` property** dynamically using **pipeline parameters** and **expressions**.

* The mapping looks like this (JSON array):

```json
[
  { "source": { "name": "srcCol1" }, "sink": { "name": "destCol1" } },
  { "source": { "name": "srcCol2" }, "sink": { "name": "destCol2" } }
]
```

---

### 🔧 Step-by-step for Copy Activity Dynamic Mapping

1. **Define a Pipeline Parameter**
   Example: `columnMapping` (string type)

2. **Pass JSON Mapping as String**
   Example parameter value:

   ```json
   [
     { "source": { "name": "Name" }, "sink": { "name": "FullName" } },
     { "source": { "name": "Age" }, "sink": { "name": "PersonAge" } }
   ]
   ```

3. **In Copy Activity, Set Mapping Property**
   Use the expression editor to parse JSON parameter:

   ```expression
   @json(pipeline().parameters.columnMapping)
   ```

4. **Result**: Copy Activity dynamically applies the column mapping.

---

### Option 2: **Mapping Data Flow with Schema Drift**

---

* In **Mapping Data Flow**, you can enable **schema drift** (allowing columns not explicitly defined to pass through).
* Use **Auto Mapping** or **Map drifted columns** feature:

  * Go to **Source** and enable **Allow schema drift**
  * In **Sink**, enable **Auto Mapping** or manually map columns using expressions
* You can also use **Derived Column** or **Select** transformations with expressions to rename or manipulate columns dynamically.

---

### Option 3: **Use Stored Procedure or Script to Handle Dynamic Columns**

* For databases, you can use **stored procedures** or **dynamic SQL** to handle schema changes.
* ADF can execute them via **Stored Procedure Activity** or **Script Activity**.

---

## ✅ Tips for Dynamic Column Mapping

| Aspect                                      | Recommendation                                    |
| ------------------------------------------- | ------------------------------------------------- |
| When columns change frequently              | Use **Copy Activity with JSON mapping** parameter |
| When complex transformations needed         | Use **Mapping Data Flow** with schema drift       |
| When source and sink column names differ    | Use explicit mapping in JSON                      |
| When multiple tables with different schemas | Use parameterized pipeline with dynamic mapping   |

---

## 🧪 Example Pipeline Parameter: `columnMapping`

```json
[
  { "source": { "name": "FirstName" }, "sink": { "name": "FName" } },
  { "source": { "name": "LastName" }, "sink": { "name": "LName" } }
]
```

---


### 11. How to execute Store Procedure with Output Parameter using ADF
#### Answer: To **execute a stored procedure with output parameters** in **Azure Data Factory (ADF)**, you use the **Stored Procedure Activity** and configure it to handle output parameters.

---

## Step-by-Step: Execute Stored Procedure with Output Parameter in ADF

---

### 1. **Create Stored Procedure with Output Parameter**

Example in SQL Server:

```sql
CREATE PROCEDURE dbo.GetEmployeeCount
    @DepartmentId INT,
    @EmployeeCount INT OUTPUT
AS
BEGIN
    SELECT @EmployeeCount = COUNT(*) 
    FROM Employees 
    WHERE DepartmentId = @DepartmentId;
END
```

---

### 2. **Create Linked Service**

* Create a linked service to your SQL database in ADF.

---

### 3. **Add Stored Procedure Activity**

* Add **Stored Procedure Activity** in your pipeline.
* Set the linked service to your database.

---

### 4. **Configure Stored Procedure and Parameters**

* Choose the stored procedure (e.g., `dbo.GetEmployeeCount`).
* Add parameters:

  * Input parameter: `@DepartmentId` (e.g., value 10)
  * Output parameter: `@EmployeeCount`

---

### 5. **Define Parameters in Stored Procedure Activity**

* For the input parameter, set the value directly or via pipeline parameters.
* For the output parameter:

  * Mark the parameter as **Output** by checking the box next to it.

---

### 6. **Access Output Parameter in Subsequent Activities**

* The stored procedure activity outputs the output parameters in the activity output JSON.

You can access it using:

```expression
@activity('StoredProcedureActivityName').output.firstRow.EmployeeCount
```

---

### 7. **Use Output Parameter**

* For example, use it in a **Set Variable Activity**, or in **If Condition** for branching.

---

## Example Expression to Read Output Parameter

If your stored procedure returns output parameter `@EmployeeCount`, then:

```json
{
  "output": {
    "firstRow": {
      "EmployeeCount": 42
    }
  }
}
```

Use in pipeline expression:

```expression
@activity('SPActivity').output.firstRow.EmployeeCount
```

---

## Summary

| Step                      | Details                                   |
| ------------------------- | ----------------------------------------- |
| Create SP with output     | Define OUTPUT parameter in SP             |
| Linked Service            | SQL DB linked service                     |
| Stored Procedure Activity | Select SP, set input & output params      |
| Access output             | Use `@activity().output.firstRow.<param>` |

---


### 12. How to copy multiple tables data using ADF
#### Answer: Copying data from **multiple tables** in Azure Data Factory (ADF) can be done efficiently using **parameterized pipelines** and **ForEach activities**. This approach lets you avoid creating separate pipelines or copy activities for each table.

---

## ✅ How to Copy Multiple Tables Data Using ADF

---

### Overview:

1. **Maintain a list of table names** (could be an array parameter or a lookup from metadata table).
2. **Use ForEach activity** to loop through each table.
3. Inside the loop, use a **Copy Activity** with parameterized source and sink datasets.
4. Pass the current table name dynamically to datasets.

---

### Step-by-Step:

---

### 1. Create Pipeline Parameter

* Create a pipeline parameter, e.g., `TableList` (Array type).
* Example value:

  ```json
  ["Customers", "Orders", "Products"]
  ```

---

### 2. Create Parameterized Source Dataset

* Create a source dataset (e.g., Azure SQL, Azure Blob, etc.).
* Add a **parameter** to the dataset: `TableName` (String).
* Use this parameter in the dataset’s table or file path property.

**Example for Azure SQL Source dataset:**

* Set the **Table** property as:
  `@dataset().TableName`

---

### 3. Create Parameterized Sink Dataset

* Similarly, create a sink dataset.
* Add parameters like `TableName` or `FolderPath` for dynamic sink locations.

---

### 4. Add **ForEach** Activity in Pipeline

* Add **ForEach** activity.
* Set **Items** as the pipeline parameter: `@pipeline().parameters.TableList`

---

### 5. Inside ForEach, Add **Copy Activity**

* In Copy Activity, select the parameterized source and sink datasets.
* Pass the current item from ForEach as dataset parameter:

  * Source dataset parameter `TableName`: `@item()`
  * Sink dataset parameter (e.g., file name or folder path): `@item()`

---

### 6. Run Pipeline

* When you trigger the pipeline, it will loop over all tables and copy data accordingly.

---

## 📌 Bonus: Get Table List Dynamically

* Instead of hardcoding the list, you can use **Lookup Activity** to read table names from a metadata table or a file.
* Pass the output of Lookup to ForEach activity.

---

## Summary Table

| Component          | Configuration                                |
| ------------------ | -------------------------------------------- |
| Pipeline Parameter | `TableList` (Array of table names)           |
| Source Dataset     | Parameterized with `TableName`               |
| Sink Dataset       | Parameterized with `TableName` or path       |
| ForEach Activity   | Loop over `@pipeline().parameters.TableList` |
| Copy Activity      | Pass `@item()` to dataset parameters         |

---


### 13. Slowly Changing Dimension(SCD)Type2 using Data Flow in ADF
#### Answer: Implementing **Slowly Changing Dimension (SCD) Type 2** in **Azure Data Factory (ADF) Mapping Data Flow** involves capturing historical changes by preserving old records and inserting new versions with updated data. Here's a step-by-step guide:

---

## What is SCD Type 2?

* Tracks historical changes by adding new rows when data changes.
* Keeps previous records with an **end date** or a flag indicating they're no longer current.
* New records get a new **effective date** and are marked as current.

---

## How to Implement SCD Type 2 in ADF Data Flow

---

### Step 1: Prepare Your Source & Sink

* **Source:** Your incoming data (e.g., updates or full dataset).
* **Sink:** Dimension table with historical data having columns like:

  * `NaturalKey` (business key)
  * `Attributes` (columns that can change)
  * `StartDate` (when record became effective)
  * `EndDate` (when record expired, e.g., `9999-12-31` for active record)
  * `IsCurrent` flag (1 = current record, 0 = historical)

---

### Step 2: Data Flow Components Overview

| Transformation    | Purpose                           |
| ----------------- | --------------------------------- |
| Source            | Read incoming data                |
| Lookup            | Lookup existing records in sink   |
| Conditional Split | Separate inserts vs updates       |
| Derived Column    | Set date flags and status flags   |
| Alter Row         | Insert new rows / update old rows |
| Sink              | Write back to dimension table     |

---

### Step 3: Detailed Steps

#### 1. **Source**

* Read the incoming (staging) data with latest records.

#### 2. **Lookup**

* Lookup existing dimension data by the business key (natural key).
* Enable **"Allow lookup on multiple rows"** if needed.

#### 3. **Conditional Split**

* Compare incoming data with existing records to detect:

  * **New records:** No match found in lookup
  * **Unchanged records:** Match found and attributes are same
  * **Changed records:** Match found but attributes differ

Example condition expressions:

* New records:

  ```plaintext
  isNull(lookupColumn)
  ```
* Changed records:

  ```plaintext
  !isNull(lookupColumn) && (incomingAttr != lookupAttr || ...)
  ```

---

#### 4. **Insert New Records**

* For new records, set:

  * `StartDate = current date`
  * `EndDate = '9999-12-31'` (or NULL)
  * `IsCurrent = 1`

#### 5. **Update Old Records**

* For changed records, mark existing record as expired:

  * `EndDate = current date - 1`
  * `IsCurrent = 0`

* Insert a new record with updated attribute values:

  * `StartDate = current date`
  * `EndDate = '9999-12-31'`
  * `IsCurrent = 1`

---

#### 6. **Alter Row**

* Use **Alter Row** transformation to define row-level insert/update:

  * Insert: for new records and new versions
  * Update: for expiring old versions

---

#### 7. **Sink**

* Use **upsert** or **allow insert/update** to write data back to dimension table.

---

## Example Expression Snippets

* Current date (to set `StartDate` / `EndDate`):

```plaintext
currentTimestamp()
```

* Mark as expired record:

```plaintext
EndDate = currentTimestamp()
IsCurrent = 0
```

---

## Summary Flow

```plaintext
Source --> Lookup --> Conditional Split --> 
    (Insert New) --> Derived Column (set flags) --> Alter Row (insert) --> Sink
    (Update Old) --> Derived Column (set flags) --> Alter Row (update) --> Sink
```

---

## Tips

* Always keep a unique business key + version key or surrogate key.
* Test with sample data thoroughly to ensure historic data integrity.
* Use **debug mode** in Data Flow to check row transformations.

---

If you want, I can help create a **sample Data Flow JSON** or detailed expressions for your use case!

### 14. How to store pipeline execution log in SQL table using ADF
#### Answer: Storing **pipeline execution logs** in a SQL table using Azure Data Factory (ADF) is a common pattern to track pipeline runs, status, and metadata for auditing or troubleshooting.

---

## How to Store Pipeline Execution Logs in SQL Table Using ADF

---

### 1. **Create a SQL Table for Logs**

Create a table to store the logs, e.g.:

```sql
CREATE TABLE PipelineExecutionLog (
    PipelineName VARCHAR(100),
    RunId UNIQUEIDENTIFIER,
    RunStartTime DATETIME,
    RunEndTime DATETIME,
    Status VARCHAR(50),
    ErrorMessage NVARCHAR(MAX),
    InsertedOn DATETIME DEFAULT GETDATE()
);
```

---

### 2. **Use Pipeline Variables or System Variables**

ADF provides system variables for pipeline run details:

| Variable                  | Description           |
| ------------------------- | --------------------- |
| `@pipeline().Pipeline`    | Pipeline name         |
| `@pipeline().RunId`       | Pipeline run ID       |
| `@pipeline().RunStart`    | Pipeline start time   |
| `@pipeline().TriggerTime` | Pipeline trigger time |

You can also get **Activity run outputs** for status and error messages.

---

### 3. **Add Web or Stored Procedure Activity to Insert Logs**

* **Option A: Use Stored Procedure Activity**

  * Create a stored procedure in SQL to insert the log entry.

  ```sql
  CREATE PROCEDURE InsertPipelineLog
      @PipelineName VARCHAR(100),
      @RunId UNIQUEIDENTIFIER,
      @RunStartTime DATETIME,
      @RunEndTime DATETIME,
      @Status VARCHAR(50),
      @ErrorMessage NVARCHAR(MAX)
  AS
  BEGIN
      INSERT INTO PipelineExecutionLog
      (PipelineName, RunId, RunStartTime, RunEndTime, Status, ErrorMessage)
      VALUES (@PipelineName, @RunId, @RunStartTime, @RunEndTime, @Status, @ErrorMessage)
  END
  ```

* Add a **Stored Procedure Activity** at the end of the pipeline.

* Pass parameters with system variables and status.

---

### 4. **Get Pipeline Status**

* Use **pipeline failure and success paths** or **try-catch pattern**:

  * On success path, status = 'Succeeded'
  * On failure path, status = 'Failed' and pass error message from `@activity('ActivityName').Error.Message`

---

### 5. **Example Parameter Mapping in Stored Procedure Activity**

| Parameter    | Value                                           |
| ------------ | ----------------------------------------------- |
| PipelineName | `@pipeline().Pipeline`                          |
| RunId        | `@pipeline().RunId`                             |
| RunStartTime | `@pipeline().RunStart`                          |
| RunEndTime   | `@utcnow()` or from last activity's end time    |
| Status       | Set dynamically as 'Succeeded' or 'Failed'      |
| ErrorMessage | `@activity('YourActivity').Error.Message` or '' |

---

### 6. **Sample Implementation Pattern**

```plaintext
Start --> Your Activities --> If Condition on success/failure -->
    Stored Procedure Activity to log (with params) -->
End
```

---

### 7. **Alternative: Use Azure Monitor Logs (Optional)**

* You can enable **diagnostic logs** for ADF and export to Log Analytics or SQL.
* But custom logging gives you more control inside the pipeline.

---

## Summary

| Step                                    | Details                                   |
| --------------------------------------- | ----------------------------------------- |
| Create SQL Log Table                    | Store pipeline name, run id, status, etc. |
| Use Stored Procedure or Insert Activity | To insert log entries                     |
| Pass Pipeline/System Variables          | For runtime info and status               |
| Use Success/Failure Pathways            | To track status and errors                |

---


### 15. How to validate file schema before processing in ADF
#### Answer: Validating a file’s schema before processing in **Azure Data Factory (ADF)** is important to ensure data quality and prevent pipeline failures. Here’s how you can do it effectively:

---

## How to Validate File Schema Before Processing in ADF

---

### Approach 1: Use **Mapping Data Flow** with Schema Validation

* **Read the file in a Data Flow source** with **"Validate schema"** enabled.
* If the schema of the incoming file doesn’t match the expected schema, the Data Flow will fail.
* You can catch this failure using pipeline error handling and route accordingly.

**Steps:**

1. Create a **Mapping Data Flow**.
2. Add a **Source** transformation pointing to your file.
3. In Source options, enable **"Validate schema"**.
4. Define the expected schema explicitly in the source.
5. If schema validation fails, the Data Flow errors out.
6. Use **Try-Catch** or **Failure path** in your pipeline to handle the error.

---

### Approach 2: Use **Get Metadata Activity + If Condition**

1. Use **Get Metadata** activity on the file or folder.
2. Retrieve **structure** (for Parquet/JSON) or **column names** if supported.
3. Compare the retrieved schema info with expected schema stored in a variable or database.
4. Use **If Condition** activity to:

   * Proceed if schema matches.
   * Fail or notify if schema differs.

*Note:* This works best with structured formats like Parquet or JSON. CSV needs extra steps.

---

### Approach 3: Use **Custom Validation Logic with Data Flow**

* In Data Flow, after source, use **Derived Column** or **Conditional Split** to check:

  * Number of columns
  * Column data types (to some extent)
  * Column names (if passed as parameters)
* Use a **Filter or Conditional Split** to separate valid vs invalid schema rows.
* Use **Assert** transformation to fail pipeline if schema check fails.

---

### Approach 4: Use **Azure Function or Custom Activity**

* Trigger an **Azure Function** or **Databricks notebook** to read file schema programmatically.
* Return success/failure to ADF pipeline.
* Based on result, decide whether to proceed or fail.

---

### Summary Table

| Method                              | Best For                        | Pros                           | Cons                          |
| ----------------------------------- | ------------------------------- | ------------------------------ | ----------------------------- |
| Mapping Data Flow "Validate schema" | Structured files (CSV, Parquet) | Built-in validation, no coding | Fails pipeline on mismatch    |
| Get Metadata + If Condition         | Parquet, JSON, limited CSV      | Simple, no code                | Limited schema detail for CSV |
| Data Flow Conditional Split         | Complex validation              | Flexible, detailed checks      | Requires building logic       |
| Azure Function / Custom Code        | Complex or custom formats       | Very flexible                  | Requires extra components     |

---


### 16. How to add new column with source file name using ADF
#### Answer: To add a new column containing the **source file name** in Azure Data Factory (ADF), you can do this easily in **Mapping Data Flow** or with Copy Activity using dataset parameters.

Here’s how:

---

## Method 1: Using **Mapping Data Flow**

### Steps:

1. **Create a Source Dataset** (e.g., Azure Blob Storage, ADLS)

   * Ensure your source dataset has **"Enable partitioning"** enabled or you are reading from a folder so you can get file metadata.

2. **In Data Flow Source settings**

   * Enable **"Enable file name column"** — this adds a new column called `FileName` (or similar) with the source file name for each row.

3. **Add a Derived Column transformation** (optional)

   * To customize or rename the filename column, or extract just the file name from the full path.
   * Example expression to extract filename only:

     ```
     last(split(FileName, '/'))
     ```

     or for Windows-style paths:

     ```
     last(split(FileName, '\\'))
     ```

4. Use this new column downstream as needed.

---

## Method 2: Using Copy Activity with Dataset Parameter

* In the **source dataset**, define a **parameter** for folder or file path.
* When triggering the pipeline or Copy Activity, pass the file name/path as a **pipeline parameter**.
* In the Copy Activity, use the **Mapping** tab to add a new column with the value of the file name (passed as a parameter).

---

## Summary

| Approach               | How to Add File Name Column                                       | Use Case                                  |
| ---------------------- | ----------------------------------------------------------------- | ----------------------------------------- |
| Mapping Data Flow      | Enable **"File name column"** in source settings + Derived Column | When transforming data in Data Flow       |
| Copy Activity + Params | Pass file name as param, map as new column in Copy Mapping        | When copying files without transformation |

---


### 17. How to get count of files in a folder using ADF
#### Answer: To get the **count of files in a folder** using Azure Data Factory (ADF), you can use the **Get Metadata** activity, which supports retrieving the list of child items (files and folders). Then you can get the count from that list.

---

## Steps to Get File Count in a Folder Using ADF

---

### 1. Add **Get Metadata** Activity

* Set the dataset to point to the **folder path** (Azure Blob Storage, ADLS, etc.).
* In the **Field list**, select **"Child Items"** — this retrieves an array of files and folders inside the folder.

---

### 2. Add **Set Variable** Activity (Optional)

* If you want to store the file count in a variable:

  * Add a pipeline variable of type **int**, e.g., `FileCount`.
  * Use **Set Variable** activity.
  * Set the value to the length of the child items array:

```
@length(activity('Get Metadata1').output.childItems)
```

---

### 3. Use the Count

* You can use this count value to make decisions (via If Condition activity) or for logging.

---

## Notes:

* **Child Items** returns both files and folders. If you want only files, you may need to filter them out by checking the file extensions or by adding additional logic (e.g., in a ForEach with filter).
* For flat folder structures, this works perfectly.
* For nested folders, you'd need recursive logic (which is more complex).

---

## Summary

| Step         | Description                                                         |
| ------------ | ------------------------------------------------------------------- |
| Get Metadata | Set folder path, get **childItems**                                 |
| Set Variable | Count files: `@length(activity('Get Metadata1').output.childItems)` |
| Use Count    | Use in conditions, logging, etc.                                    |

---


### 18. Slowly Changing Dimension(SCD)Type1 using Data Flow in ADF
#### Answer: Implementing **Slowly Changing Dimension (SCD) Type 1** using **Mapping Data Flow** in Azure Data Factory (ADF) means you want to **overwrite existing records** with the latest data (no history kept).

---

## What is SCD Type 1?

* Updates existing records in the dimension with new values.
* No history is kept.
* Simple overwrite based on matching business keys.

---

## How to Implement SCD Type 1 in ADF Data Flow

---

### Step 1: Setup Source & Sink

* **Source:** Incoming dataset with updated records.
* **Sink:** Dimension table in your database.

---

### Step 2: Data Flow Components Overview

| Transformation    | Purpose                            |
| ----------------- | ---------------------------------- |
| Source            | Read incoming updated data         |
| Lookup            | Lookup existing dimension data     |
| Conditional Split | Split new vs existing records      |
| Sink              | Insert new rows or update existing |

---

### Step 3: Detailed Steps

#### 1. **Source**

* Read your incoming updated data (e.g., from CSV, SQL table, etc.).

#### 2. **Lookup**

* Lookup existing dimension table by **business key** (natural key).

#### 3. **Conditional Split**

* Compare incoming and existing data.
* Conditions:

  * **New rows:** Records with no match in lookup.
  * **Updated rows:** Records with match but different attribute values.
  * **Unchanged rows:** Records with match and same attribute values (can be ignored).

Example expressions:

* New rows:

  ```plaintext
  isNull(lookup.BusinessKey)
  ```

* Updated rows:

  ```plaintext
  !isNull(lookup.BusinessKey) && (incoming.Attribute1 != lookup.Attribute1 || incoming.Attribute2 != lookup.Attribute2)
  ```

---

#### 4. **Sink**

* For **new rows**: Insert into dimension.
* For **updated rows**: Use **Update** method in Sink to overwrite existing records.
* Ignore unchanged rows.

---

### Step 4: Sink Configuration

* Set Sink **Update method** to **Update** based on business key.
* For new rows, set Sink to **Insert**.

---

### Summary Flow

```plaintext
Source --> Lookup --> Conditional Split --> 
    Insert new rows --> Sink (Insert)
    Update existing rows --> Sink (Update)
```

---

### Notes

* SCD Type 1 does **not** maintain history.
* The dimension table contains only current values.
* Make sure the Sink supports update operation (e.g., SQL DB, Synapse).

---


### 19. How to create running total using Data Flow in ADF
#### Answer: Creating a **running total** in Azure Data Factory's **Mapping Data Flow** can be done using the **Window transformation**. The Window transformation lets you perform cumulative aggregations like running totals.

---

## How to Create Running Total Using Data Flow in ADF

---

### Step-by-Step Guide

#### 1. Add **Source**

* Load your source data (e.g., sales data with columns like `Date` and `Amount`).

#### 2. Add **Window Transformation**

* Add a **Window** transformation after the source.

#### 3. Configure Window Transformation

* **Partition By:**
  Partition the data if you want running totals per group (e.g., per `CustomerID` or `Category`). If no partitioning needed, leave blank.

* **Order By:**
  Order rows by the column that defines the sequence (e.g., `Date` or `TransactionID`).

* **Aggregate:**

  * Add a new column, e.g., `RunningTotal`.
  * Use **Aggregation function:** `sum`.
  * **Column:** The numeric column to sum (e.g., `Amount`).
  * **Window frame:**
    Set to
    `From start of partition` to `current row`
    (This is the default frame for running total).

#### 4. Use Output

* The output will have a new column with the running total.

---

### Example:

| Date       | Amount | RunningTotal |
| ---------- | ------ | ------------ |
| 2025-01-01 | 100    | 100          |
| 2025-01-02 | 200    | 300          |
| 2025-01-03 | 150    | 450          |

---

### Notes:

* If you want running totals **across the entire dataset** without partition, just leave **Partition By** empty.
* If you want per group running totals, specify the group column in **Partition By**.
* Make sure to sort your data correctly in **Order By** for proper cumulative calculation.

---


### 20. How to create incremental key using Data Flow in ADF
#### Answer: Creating an **incremental key (surrogate key)** in Azure Data Factory (ADF) **Mapping Data Flow** usually means generating a unique, sequential number for each row, often used as a primary key or to track row versions.

---

## How to Create Incremental Key (Surrogate Key) Using Data Flow in ADF

---

### Method 1: Use **Window Transformation with Row Number**

The most common way to generate an incremental key is to use the **Row Number** function in the **Window** transformation.

---

### Step-by-Step:

#### 1. Add **Source**

Load your source dataset.

#### 2. Add **Window Transformation**

* Open the Window transformation.
* Set **Partition By** if you want row numbers per group (optional). Leave empty if you want row numbers globally.
* Set **Order By** to define the order of numbering (e.g., by date or natural key).
* Add an **Aggregate column**, e.g., `IncrementalKey`.
* Use **Row number()** as the aggregate function.

Example expression for row number column:

```
rowNumber()
```

This will assign sequential numbers starting from 1, according to the ordering.

---

### Method 2: Use **Surrogate Key Transformation**

ADF Data Flow has a built-in **Surrogate Key** transformation designed exactly for this:

#### Steps:

1. After your source or any transformation, add **Surrogate Key** transformation.
2. Configure:

   * Specify **Output Column Name** (e.g., `IncrementalKey`).
   * Configure **Key start value** (default 1).
   * Configure **Increment step** (default 1).
3. This automatically adds a unique sequential key column to each row.

---

### Important Notes:

* **Surrogate Key transformation** is easier and recommended if you just need a simple sequential key.
* **Window + rowNumber()** offers more flexibility if you need partitioning or specific ordering.
* Generated keys are per pipeline run, not global across runs unless you merge with existing keys.

---

### Summary

| Method                  | Use Case                                 | Pros               | Cons                                |
| ----------------------- | ---------------------------------------- | ------------------ | ----------------------------------- |
| Surrogate Key Transform | Simple sequential key generation         | Easy and built-in  | No partitioning or ordering control |
| Window + rowNumber()    | Advanced control with ordering/partition | Flexible, powerful | Slightly complex setup              |

---


### 21. How to remove duplicate rows using dataflow in ADF
#### Answer: To **remove duplicate rows** using **Mapping Data Flow** in Azure Data Factory (ADF), you can use the **Aggregate** or **Window** transformation. Here's how to do it step-by-step:

---

## Method 1: Using **Aggregate Transformation** (most common for deduplication)

### Steps:

1. **Add Source**
   Load your dataset.

2. **Add Aggregate Transformation**

   * Group by the columns that define uniqueness (e.g., all columns or a subset of columns that determine duplicates).
   * For other columns, use aggregation functions like `first()`, `last()`, `max()`, or `min()` to select which row's values you want to keep.

3. **Result**
   The output will contain unique rows based on your group-by columns, effectively removing duplicates.

---

## Method 2: Using **Window Transformation**

If you want to keep the **first or last occurrence** of duplicates based on some ordering:

### Steps:

1. **Add Source**

2. **Add Window Transformation**

   * Partition by the columns that define duplicates.
   * Order by a column to decide which duplicate to keep (e.g., timestamp).
   * Add a new column, say `row_num`, with expression:

     ```
     rowNumber()
     ```

3. **Add Filter Transformation**

   * Filter rows where `row_num == 1` to keep only the first occurrence.

---

## Summary Table

| Method          | When to Use                              | Pros                                 | Cons                                    |
| --------------- | ---------------------------------------- | ------------------------------------ | --------------------------------------- |
| Aggregate       | Remove duplicates by grouping columns    | Simple and efficient                 | Needs aggregation for non-group columns |
| Window + Filter | Keep first/last duplicate based on order | Control over which duplicate to keep | Slightly more complex                   |

---


### 22. How to process fixed length text file using ADF DataFlow
#### Answer: Processing **fixed-length text files** in **Azure Data Factory (ADF) Mapping Data Flow** requires some custom handling because ADF doesn’t have built-in fixed-width parser support like it does for delimited files.

Here’s how you can process fixed-length files using Data Flow:

---

## How to Process Fixed Length Text File in ADF Data Flow

---

### Step 1: Ingest the file as **single-column text**

* Define your **source dataset** as a **single-column delimited text file** using a delimiter that does not exist in your data (e.g., a pipe `|` or some unusual character), or treat the entire row as one column.
* Or better, set the dataset to treat the whole line as a single string column. You can do this by:

  * Setting **Column delimiter** to **None** or a character not present.
  * Define only one column (e.g., `LineText`).

---

### Step 2: Use **Derived Column** or **Select** transformation to extract fields

* Add a **Derived Column** transformation in Data Flow.
* Use string functions like `substring()` to extract fixed-width fields from the single string column.

Example:

Assuming your fixed-width file format is:

| Field1 (5 chars) | Field2 (10 chars) | Field3 (3 chars) |
| ---------------- | ----------------- | ---------------- |

You can create new columns with expressions like:

```
substring(LineText, 0, 5)      // Extract Field1 (characters 0 to 4)
substring(LineText, 5, 10)     // Extract Field2 (characters 5 to 14)
substring(LineText, 15, 3)     // Extract Field3 (characters 15 to 17)
```

---

### Step 3: Data type conversion

* Use additional **Derived Column** transformations or **Data Type** casting in **Select** transformation to convert extracted string fields to proper data types (int, date, decimal).

---

### Step 4: Continue with normal Data Flow transformations

* Now you have parsed columns like a normal structured dataset and can apply filters, joins, sinks, etc.

---

## Summary

| Step                 | Description                                     |
| -------------------- | ----------------------------------------------- |
| Source Dataset       | Load file as single string column               |
| Derived Column       | Use `substring()` to extract fields             |
| Data Type Conversion | Cast strings to appropriate types               |
| Further Processing   | Continue with your normal data processing steps |

---


### 23. How to copy last n days data incrementally from ADLS Gen2
#### Answer: To **copy last N days of data incrementally** from **Azure Data Lake Storage Gen2** using Azure Data Factory (ADF), you typically filter files or data based on modified date or folder structure (like partition by date), or filter rows inside files by date column.

Here’s how you can do it step-by-step:

---

## Scenario 1: Copy files modified in last N days

### Steps:

1. **Use Get Metadata Activity**

   * Point to your ADLS Gen2 folder.
   * Get child items (files list).

2. **Filter files by Last Modified Time**

   * ADF’s Get Metadata doesn’t directly provide file modified date.
   * So, you need to use **Azure Functions** or **Azure Logic Apps** to list files with metadata including modified time, or use **Databricks** notebook to list and filter files.

3. **Pass filtered file list to ForEach**

   * Iterate over files modified in last N days.
   * Use Copy Activity inside ForEach to copy them.

---

## Scenario 2: Copy data from files but filter rows with date column in last N days

### Steps:

1. **Use Copy Activity with Source Query/Filter**

   * If source is structured (like Parquet or CSV with a date column), use **Filter on Source dataset** or **Mapping Data Flow** to filter rows where date column >= (current date - N days).

   * Example filter expression in Data Flow Source:

   ```
   toDate(yourDateColumn) >= addDays(currentTimestamp(), -N)
   ```

2. **Use Parameterized Dataset**

   * Pass the date dynamically as a parameter to your pipeline/dataset.

---

## Scenario 3: Folder Partition by Date (Most common)

If your data is partitioned by date folder structure like `/year=2025/month=06/day=01/`, you can:

1. Use **Dataset parameters** for year/month/day.

2. In your pipeline, use **Get Metadata** or **Until** activity to loop over last N days.

3. Dynamically build folder path for each day.

4. Copy data from those folders incrementally.

---

## Summary Table

| Method                       | Description                       | Pros                          | Cons                                       |
| ---------------------------- | --------------------------------- | ----------------------------- | ------------------------------------------ |
| File modified date filter    | Copy files changed in last N days | Good for non-partitioned data | Need extra service for file date filtering |
| Row filtering inside files   | Filter rows by date column        | Works with structured files   | Data read overhead if files large          |
| Partitioned folder structure | Copy folders for last N days      | Efficient & simple            | Needs data partitioning setup              |

---


### 24. How to copy latest or last modified file from ADLS Gen2
#### Answer: To copy the **latest or last modified file** from **Azure Data Lake Storage Gen2** using **Azure Data Factory (ADF)**, you can follow this common approach:

---

## How to Copy Latest (Last Modified) File from ADLS Gen2 Using ADF

---

### Step 1: Use **Get Metadata** Activity

* Configure **Get Metadata** activity with the ADLS Gen2 folder path (container/folder where files reside).
* In **Field list**, select **childItems** to get the list of files.

---

### Step 2: Use **Filter / Lookup / ForEach** Activities

Because **Get Metadata** doesn’t return last modified timestamp, you need an extra way to get file modified time:

---

### Option 1: Use **Azure Function** or **Logic App**

* Create an Azure Function or Logic App to list files in the folder with metadata (including last modified timestamp).
* Return the file with the most recent modification date to ADF via a **Web Activity**.
* Use this filename dynamically in the Copy Activity source dataset.

---

### Option 2: Use **Azure Data Lake Storage REST API** with Web Activity

* Use ADF’s **Web Activity** to call ADLS Gen2 REST API for file listing with timestamps.
* Parse the response in **Lookup** or **Set Variable** activity.
* Pick the file with the latest `lastModified` timestamp.
* Pass filename dynamically to Copy Activity.

---

### Option 3: Use **Filter & ForEach** (if file names include timestamp)

* If your files have timestamps in their names (e.g., `file_20250605.csv`), use a **Filter** or **Sort** activity in a Data Flow or pipeline to select the latest file by name.
* Use a **ForEach** loop to iterate and pick the file with the max date string.
* Then copy that file.

---

### Step 3: Copy Activity

* Use the file name dynamically (from previous steps) in the source dataset path or file name parameter.
* Perform the copy to sink.

---

## Summary Flow

```plaintext
Get file list (via Azure Function / REST API / naming convention) 
      ↓
Find latest file (based on lastModified or name)
      ↓
Copy Activity using dynamic file path
```

---

### Notes

* **Get Metadata** alone can’t get file last modified dates.
* Using **Azure Functions** or REST API is the most robust way.
* If your file names include date/timestamp, parsing by name is simpler.

---


### 25. How to get source file name dynamically in ADF
#### Answer: To **get the source file name dynamically in Azure Data Factory (ADF)**, especially when processing files, you typically want to capture the file name during the pipeline run so you can use it downstream (e.g., add as a column, use in sink path, or logging).

---

## Common Ways to Get Source File Name Dynamically in ADF

---

### 1. Using **ForEach + Get Metadata + Copy Activity**

* Use **Get Metadata** activity to list files (childItems) in a folder.
* Use **ForEach** activity to loop over each file.
* Inside **ForEach**, you can access the current file name via **`@item().name`**.
* Pass this file name as a parameter to your Copy Activity or Data Flow.

---

### 2. Using **Mapping Data Flow: Add File Name as Column**

* In **Mapping Data Flow Source** settings:

  * Enable the option **“Output to single file name column”** (sometimes called **"Add filename as a column"**).
* This adds a column (default named `filename`) to your dataset with the source file name for each row.
* You can rename this column or use it downstream.

---

### 3. Using **Dataset Parameters**

* Define a dataset parameter for the file name.
* In the pipeline, dynamically pass the file name to dataset parameter (e.g., from ForEach `@item().name`).
* This way, Copy Activity or Data Flow can process the file dynamically and you know the file name being processed.

---

### 4. Using **System Variables in Pipeline**

* ADF system variables like `@pipeline().RunId` or `@pipeline().TriggerTime` exist, but no built-in variable for current file name.
* Use ForEach to explicitly capture file names instead.

---

## Example: Capture file name in ForEach

```json
"activities": [
  {
    "name": "GetMetadata",
    "type": "GetMetadata",
    "typeProperties": {
      "dataset": {
        "referenceName": "InputFolderDataset",
        "type": "DatasetReference"
      },
      "fieldList": ["childItems"]
    }
  },
  {
    "name": "ForEachFile",
    "type": "ForEach",
    "typeProperties": {
      "items": "@activity('GetMetadata').output.childItems",
      "activities": [
        {
          "name": "CopyFile",
          "type": "Copy",
          "typeProperties": {
            "source": {
              "type": "DelimitedTextSource"
            },
            "sink": {
              "type": "AzureBlobSink"
            },
            "dataset": {
              "referenceName": "SourceFileDataset",
              "parameters": {
                "FileName": "@item().name"
              }
            }
          }
        }
      ]
    }
  }
]
```

---



