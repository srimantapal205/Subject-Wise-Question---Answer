 # **Azure Fabric interview questions with answers**

---

# 🔹 Azure Fabric Interview Questions & Answers (Beginner → Mid-Level)

### **Basics & Concepts**

1. **What is Microsoft Fabric?**
   → Microsoft Fabric is a unified SaaS analytics platform that combines data engineering, data science, data integration, real-time analytics, and BI into one solution. It integrates services like Power BI, Synapse, and Data Factory under a single lake-first architecture called **OneLake**.

2. **What is OneLake in Fabric?**
   → OneLake is the data foundation of Fabric, a single logical data lake that automatically organizes, secures, and provides access to all organizational data.

3. **Difference between Fabric and Azure Synapse Analytics?**
   → Synapse focuses mainly on data warehousing and analytics. Fabric extends beyond that to cover **data integration (ADF), data science, real-time analytics, and BI (Power BI)** in one SaaS platform.

4. **What are the main workloads of Fabric?**

   * Data Engineering
   * Data Factory
   * Data Science
   * Data Warehouse
   * Real-Time Analytics
   * Power BI
   * Data Activator

5. **What is the advantage of Fabric over using standalone services (ADF, Synapse, Power BI)?**
   → Unified billing, single governance model, integrated security, seamless data sharing, and elimination of data silos.

---

### **OneLake & Storage**

6. **What file format does OneLake use by default?**
   → **Delta Lake (Parquet + transaction log)** format for all tabular data.

7. **What is a Lakehouse in Fabric?**
   → A Lakehouse is a data architecture in Fabric that combines the flexibility of a data lake with the structure of a data warehouse using Delta tables.

8. **Can OneLake connect to external storage like ADLS Gen2 or S3?**
   → Yes, using **Shortcuts**, Fabric can create virtual links to external storage (ADLS, S3, Dataverse) without duplicating data.

9. **Difference between Lakehouse and Data Warehouse in Fabric?**
   → Lakehouse = Schema-less, unstructured + structured data.
   Data Warehouse = Schema-based, optimized for BI/analytics.

10. **What is a Shortcut in OneLake?**
    → A reference to data stored in external systems (ADLS, S3, etc.) so Fabric can use it without data duplication.

---

### **Data Integration (Data Factory in Fabric)**

11. **What is the role of Data Factory in Fabric?**
    → Provides data integration with **data pipelines, copy activities, dataflows, and orchestration** for ETL/ELT processes.

12. **Difference between Dataflows Gen1 and Dataflows Gen2 in Fabric?**
    → Gen2 dataflows run on Fabric compute, support Delta tables in OneLake, and integrate tightly with Fabric workloads.

13. **What connectors are supported in Fabric Data Factory?**
    → 200+ connectors, including SQL, Oracle, Salesforce, SAP, ADLS, Blob, S3, Dataverse, etc.

14. **How does Fabric handle incremental data loads?**
    → Through **watermarking, CDC (Change Data Capture), or delta-based queries** in pipelines.

15. **How is pipeline monitoring done in Fabric?**
    → Using Fabric’s monitoring hub with activity run details, success/failure logs, and retry options.

---

### **Data Engineering (Synapse in Fabric)**

16. **What is Spark in Fabric Data Engineering?**
    → A managed Spark compute environment for large-scale data processing, ML, and transformations.

17. **What languages are supported in Fabric Notebooks?**
    → PySpark, Python, SQL, R, and Scala.

18. **What is a Semantic Model in Fabric?**
    → The dataset model used in Power BI, created automatically from Lakehouse/Warehouse for BI.

19. **How does Fabric ensure ACID transactions in Lakehouse?**
    → Through **Delta Lake transaction logs**.

20. **What is the difference between Lakehouse tables and Warehouse tables?**
    → Lakehouse → Delta tables (open-source format).
    Warehouse → Proprietary structured tables optimized for T-SQL queries.

---

### **Data Warehouse in Fabric**

21. **What engine does Fabric Warehouse use?**
    → A **distributed SQL-based engine** optimized for T-SQL queries and BI workloads.

22. **Can Fabric Warehouse scale automatically?**
    → Yes, Fabric provides elastic scaling with SaaS-based compute allocation.

23. **How does Fabric Warehouse integrate with Power BI?**
    → Direct connection through semantic models with no ETL required.

24. **What kind of workloads are best for Fabric Warehouse?**
    → Highly structured data, reporting, financials, OLAP queries.

25. **Can you query Lakehouse data using T-SQL in Fabric?**
    → Yes, using Warehouse or SQL endpoints in Lakehouse.

---

### **Real-Time Analytics**

26. **What is Real-Time Analytics in Fabric?**
    → A workload designed for streaming data ingestion and analytics using **KQL (Kusto Query Language)**.

27. **What type of data sources are supported for streaming in Fabric?**
    → Event Hubs, IoT Hub, Kafka, Azure Stream Analytics.

28. **What is KQL?**
    → Kusto Query Language, used for log/telemetry/stream data queries in Fabric.

29. **Difference between Real-Time Analytics and Data Engineering?**
    → Real-Time = Streaming, telemetry, log data.
    Data Engineering = Batch ETL, large-scale transformations.

30. **What are Eventstreams in Fabric?**
    → A no-code experience in Fabric to ingest, transform, and route real-time event data.

---

### **Power BI & Data Visualization**

31. **How does Power BI integrate with Fabric?**
    → Power BI is built into Fabric; every Lakehouse, Warehouse, and Dataflow automatically creates semantic models for reporting.

32. **What are Semantic Models in Power BI Fabric?**
    → Tabular models that support measures, KPIs, and relationships for reporting.

33. **Difference between Import and Direct Lake mode in Fabric Power BI?**

* **Import**: Data copied into Power BI memory.
* **Direct Lake**: Queries Lakehouse/Warehouse Delta tables directly without import.

34. **When should you use Direct Lake mode?**
    → For **large datasets** where refresh times are an issue and near real-time analytics are needed.

35. **What are Data Activators in Fabric?**
    → A feature that monitors real-time data and triggers actions (alerts, workflows) when conditions are met.

---

### **Security & Governance**

36. **How is security handled in Fabric?**
    → Through **Azure AD, role-based access control (RBAC), sensitivity labels, row-level security (RLS), and column-level security**.

37. **What is Purview integration in Fabric?**
    → For data cataloging, lineage tracking, and governance.

38. **How does Fabric support multi-tenant data architecture?**
    → With workspaces, domains, RBAC, and shared OneLake storage.

39. **What is domain-driven architecture in Fabric?**
    → Organizing Fabric workspaces around **business domains (Finance, Sales, HR)** for better governance.

40. **Can you enable row-level security in Fabric Warehouse?**
    → Yes, using T-SQL security functions in semantic models.

---

