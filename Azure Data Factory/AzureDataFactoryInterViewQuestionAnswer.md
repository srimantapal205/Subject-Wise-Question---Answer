## 1. In Azure Data Factory (ADF) have 200 pipeline and this all are dependency pipeline also need to run all sequentially. How to resolve this problem?

**Answer :** Running 200 dependent pipelines sequentially in Azure Data Factory (ADF) can be done using a few different strategies. Here's a breakdown of the most efficient and manageable approaches:

### Approach 1: Master Pipeline (Recommended)
**Steps:**
* Create a Master Pipeline.

* Use the "Execute Pipeline" activity.

* Chain them sequentially:

* Link Execute Pipeline 1 to Execute Pipeline 2, then 3, and so on.

* Set the dependency condition to "Success" (default).

**Notes:**
* We can group sets of pipelines into smaller master pipelines (e.g., 20 at a time), then call those from a main orchestrator, if performance or UI gets sluggish.

*Use pipeline parameters if pipelines are similar and can be parameterized.

### Approach 2: Metadata-Driven Execution

Dynamic and scalable way to execute large number of pipelines without manually creating 200 Execute Pipeline activities.

**How it works:**
* Create a Lookup activity that reads a list of pipeline names (from a table or JSON in Blob).

* Use a ForEach loop to iterate over the list.

* Inside the loop, use Execute Pipeline activity to run the pipeline using the name from the list.

**Pros:**
* Easy to maintain.

* No need to hard-code all 200 pipelines in the ADF UI.

* Add/remove pipelines easily by updating metadata source.

**Caveat:**
* ForEach by default runs in parallel. You need to set "Batch Count" = 1 and uncheck "isSequential = false" to enforce sequential execution.


###  Approach 3: Use Data Factory Triggers + Dependency Chain
If you want to automatically kick off one pipeline after another based on success, you can chain them using triggers and pipeline dependencies in the ADF UI (Manage > Trigger > New/Edit).

But managing 200 trigger dependencies in this UI may be tedious and not scalable.



---

### 2. **What are the different types of activities in Azure Data Factory (ADF), and how are they used?**

---

### ✅ **Answer:**

In **Azure Data Factory**, **activities** define the **actions** or **operations** to be performed within a pipeline. ADF supports **different types of activities**, broadly categorized into the following:

---

### 1. **Data Movement Activities**
These activities are used to move data from a source to a destination.

- **Copy Activity**:  
  - Most commonly used activity.  
  - Transfers data between supported data stores.  
  - Supports transformations like column mapping and format conversion.  
  - Example: Copy data from Amazon S3 to Azure Blob Storage or from Blob to Azure SQL Database.

---

### 2. **Data Transformation Activities**
Used to transform or process data.

- **Data Flow Activity**:  
  - Executes mapping data flows (visually designed transformations).  
  - Allows schema mapping, joins, filters, aggregations, etc.  

- **Azure Databricks Notebook/Activity**:  
  - Triggers Databricks jobs for large-scale data transformations using Spark.

- **HDInsight Activity**:  
  - Executes Hive, Pig, or custom scripts on HDInsight clusters.

- **Stored Procedure Activity**:  
  - Executes stored procedures in SQL-based systems like Azure SQL Database or Synapse.

- **U-SQL, Hadoop, or ML Activities**:  
  - Executes specific processing logic using those technologies.

---

###  3. **Control Activities**
Used to control the pipeline flow, logic, and execution order.

- **Execute Pipeline Activity**:  
  - Runs a child pipeline from a parent pipeline.  
  - Useful for modular and reusable pipeline designs.

- **If Condition Activity**:  
  - Evaluates an expression and runs different activities based on true/false.

- **ForEach Activity**:  
  - Iterates over a collection of items and executes inner activities for each item.

- **Until Activity**:  
  - Repeats inner activities until a condition is met.

- **Wait Activity**:  
  - Introduces a delay before the next activity executes.

---

###  4. **External Activities**
Used to trigger external services or compute.

- **Web Activity**:  
  - Calls REST APIs to trigger external processes or send messages.  
  - Example: Call a webhook or trigger a Logic App.

- **Azure Function Activity**:  
  - Executes a serverless Azure Function.  
  - Example: Run custom logic like file renaming or data formatting.

- **Custom Activity**:  
  - Allows running custom .NET code on an Azure Batch service.

---

