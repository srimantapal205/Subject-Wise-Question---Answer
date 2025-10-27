
# 🧊 **Snowflake Interview Questions**

## 🔹 **Beginner Level (1–35)**

### **1. What is Snowflake?**

**Answer:**
Snowflake is a **cloud-based data warehouse platform** that enables data storage, processing, and analysis using SQL. It is built for the cloud and separates storage and compute resources, allowing users to scale them independently.

**Example:**
A company can store all its sales data in Snowflake and run analytics queries without worrying about managing servers or storage.

---

### **2. What are the key features of Snowflake?**

**Answer:**

* Cloud-native architecture
* Separation of storage and compute
* Auto-scaling and auto-suspend
* Secure data sharing
* Time Travel and Fail-safe
* Support for semi-structured data (JSON, Parquet, etc.)

**Example:**
Snowflake allows scaling compute instantly during peak query hours and auto-suspends when idle to save cost.

---

### **3. How is Snowflake different from traditional data warehouses?**

**Answer:**

| Feature           | Traditional DW  | Snowflake     |
| ----------------- | --------------- | ------------- |
| Deployment        | On-premises     | Cloud-native  |
| Scaling           | Manual          | Auto-scaling  |
| Storage & Compute | Tightly coupled | Separated     |
| Maintenance       | Manual          | Fully managed |

**Example:**
Unlike traditional systems like Teradata, Snowflake automatically handles infrastructure and scaling.

---

### **4. What are the three main layers of Snowflake architecture?**

**Answer:**

1. **Database Storage Layer** – Stores structured and semi-structured data.
2. **Compute Layer (Virtual Warehouses)** – Performs query execution.
3. **Cloud Services Layer** – Handles authentication, metadata, and query optimization.

**Example:**
When a user runs a query, the Cloud Services Layer routes it to the Compute Layer, which reads data from the Storage Layer.

---

### **5. What are virtual warehouses in Snowflake?**

**Answer:**
A **virtual warehouse** is a compute resource in Snowflake used to perform queries, loading, and transformations.

**Example:**
A “SALES_WH” warehouse can be used to run sales-related queries independently of other workloads.

---

### **6. What are micro-partitions in Snowflake?**

**Answer:**
Snowflake automatically divides data into small storage units called **micro-partitions** (typically 50–500 MB in size). These help in faster query performance.

**Example:**
A sales table with 1 TB data may be divided into thousands of micro-partitions for parallel processing.

---

### **7. What are databases, schemas, and tables in Snowflake?**

**Answer:**

* **Database:** Logical container for schemas.
* **Schema:** Logical container for tables, views, etc.
* **Table:** Object that stores data.

**Example:**
`SALES_DB` → `PUBLIC` schema → `ORDERS` table.

---

### **8. What are the different table types in Snowflake?**

**Answer:**

1. **Permanent tables**
2. **Transient tables**
3. **Temporary tables**

---

### **9. What is a transient table in Snowflake?**

**Answer:**
A **transient table** is similar to a permanent table but has **no Fail-safe** period. It’s suitable for short-term data storage.

**Example:**
`CREATE TRANSIENT TABLE TEMP_SALES AS SELECT * FROM SALES;`

---

### **10. What is a temporary table in Snowflake?**

**Answer:**
A **temporary table** exists only within a user session and is automatically dropped after the session ends.

**Example:**
`CREATE TEMPORARY TABLE TEMP_USERS AS SELECT * FROM USERS;`

---

### **11. What is a clone in Snowflake?**

**Answer:**
A **clone** is a copy of a database, schema, or table created instantly without duplicating data.

**Example:**
`CREATE TABLE SALES_CLONE CLONE SALES;`

---

### **12. What is zero-copy cloning in Snowflake?**

**Answer:**
Zero-copy cloning means cloning is done **without physically copying data**. Both original and clone share the same underlying data.

**Example:**
Creating a clone of a 1 TB table takes only seconds and no extra storage initially.

---

### **13. What is Time Travel in Snowflake?**

**Answer:**
Time Travel allows users to **query, clone, or restore data** from a previous state within a defined retention period.

**Example:**
`SELECT * FROM SALES AT (TIMESTAMP => '2025-10-26 12:00:00');`

---

### **14. How long can data be recovered using Time Travel?**

**Answer:**

* **Standard Edition:** 1 day
* **Enterprise Edition and above:** Up to 90 days

---

### **15. What is Fail-safe in Snowflake?**

**Answer:**
Fail-safe is a **7-day recovery period** after Time Travel expires, used only for disaster recovery by Snowflake support.

---

### **16. What is caching in Snowflake?**

**Answer:**
Caching stores query results and data locally to improve performance and reduce cost.

---

### **17. What are the types of caching available in Snowflake?**

**Answer:**

1. **Result cache** – Stores results of queries.
2. **Metadata cache** – Stores metadata information.
3. **Local disk cache** – Stores data on compute nodes.

---

### **18. What are the supported cloud platforms for Snowflake?**

**Answer:**

* **Amazon Web Services (AWS)**
* **Microsoft Azure**
* **Google Cloud Platform (GCP)**

---

### **19. How is data stored in Snowflake?**

**Answer:**
Data is stored in **columnar format** and compressed into micro-partitions within the cloud storage layer.

---

### **20. What are stages in Snowflake?**

**Answer:**
Stages are **locations used to load or unload data** to and from Snowflake tables.

---

### **21. What are internal and external stages?**

**Answer:**

* **Internal Stage:** Managed by Snowflake (e.g., user, table, or named stage).
* **External Stage:** Points to external storage like AWS S3, Azure Blob, or Google Cloud Storage.

---

### **22. How do you load data into Snowflake?**

**Answer:**

1. Upload data to a stage (using `PUT`).
2. Use the `COPY INTO` command to load data into a table.

**Example:**

```sql
PUT file://orders.csv @%orders;
COPY INTO orders FROM @%orders FILE_FORMAT=(TYPE=CSV);
```

---

### **23. What is the COPY INTO command used for?**

**Answer:**
`COPY INTO` loads data from a stage into a Snowflake table or unloads data from a table to a stage.

---

### **24. What file formats does Snowflake support for data loading?**

**Answer:**

* CSV
* JSON
* Avro
* ORC
* Parquet
* XML

---

### **25. What are Snowflake file format objects?**

**Answer:**
File format objects define how files are structured (e.g., CSV delimiter, compression type).

**Example:**

```sql
CREATE FILE FORMAT my_csv_format TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1;
```

---

### **26. What is the purpose of the PUT command?**

**Answer:**
The `PUT` command uploads local files to an internal stage in Snowflake.

**Example:**
`PUT file://data.csv @my_stage;`

---

### **27. What is the GET command used for?**

**Answer:**
The `GET` command downloads files from a Snowflake stage to a local machine.

**Example:**
`GET @my_stage/data.csv file://localfolder;`

---

### **28. How do you unload data from Snowflake to a stage?**

**Answer:**
Use the `COPY INTO` command with a stage destination.

**Example:**

```sql
COPY INTO @my_stage/unload_ FROM sales FILE_FORMAT=(TYPE=CSV);
```

---

### **29. What is Snowflake Web UI called?**

**Answer:**
It is called **Snowflake Web Interface** or **Snowsight**.

---

### **30. What are roles in Snowflake?**

**Answer:**
Roles define **access control** for users and objects in Snowflake.

**Example:**
`GRANT SELECT ON TABLE sales TO ROLE analyst;`

---

### **31. What are warehouses billed for in Snowflake?**

**Answer:**
Warehouses are billed for **compute usage** based on the time they are running.

---

### **32. How do you suspend or resume a Snowflake warehouse?**

**Answer:**

```sql
ALTER WAREHOUSE my_wh SUSPEND;
ALTER WAREHOUSE my_wh RESUME;
```

---

### **33. What are Snowflake Editions (Standard, Enterprise, Business Critical)?**

**Answer:**

* **Standard:** Basic features.
* **Enterprise:** Includes extended Time Travel.
* **Business Critical:** Enhanced security and compliance.

---

### **34. What is auto-suspend and auto-resume in Snowflake?**

**Answer:**

* **Auto-suspend:** Automatically stops a warehouse after idle time.
* **Auto-resume:** Automatically starts when a new query runs.

**Example:**

```sql
CREATE WAREHOUSE my_wh AUTO_SUSPEND = 300 AUTO_RESUME = TRUE;
```

---

### **35. What is SnowSQL?**

**Answer:**
**SnowSQL** is a **command-line client** for interacting with Snowflake using SQL commands.

**Example:**
`snowsql -a myaccount -u user1`



---

## 🔹 **Intermediate Level (36–70)**

36. Explain Snowflake’s shared data architecture.
37. What is the difference between a virtual warehouse and a database in Snowflake?
38. How does Snowflake ensure data security?
39. What are masking policies in Snowflake?
40. What are row access policies in Snowflake?
41. What is dynamic data masking?
42. How do you implement role-based access control in Snowflake?
43. What is the difference between role and user privileges?
44. What is metadata in Snowflake?
45. How can you query metadata in Snowflake?
46. What are tasks in Snowflake?
47. How do tasks help in scheduling ETL workflows?
48. What are streams in Snowflake?
49. How do streams work with tasks for change data capture (CDC)?
50. What are Snowflake sequences?
51. How do you use stored procedures in Snowflake?
52. What language is used to create stored procedures in Snowflake?
53. What is Snowpark?
54. What languages does Snowpark support?
55. What are user-defined functions (UDFs) in Snowflake?
56. What are external functions in Snowflake?
57. How do you handle semi-structured data (JSON, Parquet, Avro) in Snowflake?
58. What is VARIANT data type?
59. How do you query JSON data using Snowflake SQL?
60. What are lateral flatten and its use case?
61. What are data shares in Snowflake?
62. What is the difference between data sharing and data replication?
63. What are reader accounts in Snowflake?
64. How do you monitor warehouse performance in Snowflake?
65. What are query profiles?
66. How does Snowflake handle concurrency?
67. How do you optimize cost in Snowflake?
68. What is a resource monitor in Snowflake?
69. What is Snowflake Marketplace?
70. What are materialized views in Snowflake?

---

## 🔹 **Advanced Level (71–100)**

71. Explain Snowflake’s architecture in detail (Cloud Services, Query Processing, Storage).
72. How does Snowflake separate compute and storage?
73. What are the internal optimization techniques used by Snowflake?
74. How does Snowflake ensure ACID compliance?
75. Explain how query pruning works in Snowflake.
76. What are clustering keys?
77. When should you use clustering keys?
78. How does reclustering work in Snowflake?
79. What are hybrid tables in Snowflake?
80. What are the differences between materialized views and clustering?
81. How do you optimize queries in Snowflake?
82. How do you identify slow-running queries?
83. What is the role of the query execution plan in optimization?
84. What are query acceleration services in Snowflake?
85. How does Snowflake handle semi-structured data internally?
86. What is external table in Snowflake?
87. What are secure views and secure UDFs?
88. How do you implement SCD Type 2 in Snowflake?
89. How can you build a data pipeline using Snowflake Tasks and Streams?
90. What is Snowpipe?
91. How does Snowpipe handle continuous data loading?
92. What are notification-based Snowpipes?
93. What is auto-ingest in Snowflake?
94. How do you integrate Snowflake with Azure Data Factory or AWS Glue?
95. What are Snowflake’s best practices for handling large data loads?
96. How do you implement data retention policies?
97. What are multi-cluster warehouses?
98. What is the difference between standard and multi-cluster warehouse?
99. What are failover groups in Snowflake?
100. What is replication and how does cross-region replication work?

---


