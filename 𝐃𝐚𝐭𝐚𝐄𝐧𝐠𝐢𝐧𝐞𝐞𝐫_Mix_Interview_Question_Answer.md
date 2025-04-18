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


