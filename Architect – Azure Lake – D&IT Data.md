# **D&IT / Enterprise Data Platform Architecture**

---

## SECTION 1: ADLS & ADLS Gen2 (Architecture & Design)

**(Q1–Q35)**

### Q1. What is ADLS and why is it used in enterprise data platforms?

**A:** ADLS (Azure Data Lake Storage) is a hyperscale storage service optimized for analytics workloads. It supports massive data volumes, hierarchical namespaces, and integrates natively with Spark, Databricks, Synapse, and Power BI.

---

### Q2. Difference between ADLS Gen1 and Gen2?

**A:**

| Feature   | Gen1       | Gen2        |
| --------- | ---------- | ----------- |
| Namespace | Native     | HNS on Blob |
| Cost      | Higher     | Lower       |
| Security  | ACL        | RBAC + ACL  |
| Status    | Deprecated | Active      |

---

### Q3. Why ADLS Gen2 is preferred for Lakehouse?

**A:**

* Hierarchical namespace
* Optimized metadata operations
* POSIX-style ACLs
* Native Delta Lake compatibility

---

### Q4. What is Hierarchical Namespace (HNS)?

**A:** HNS allows directory-level operations (rename, move, delete) to be atomic and fast—critical for Spark & Delta Lake performance.

---

### Q5. How does ADLS Gen2 handle security?

**A:**

* **Azure RBAC** → Account/Container
* **ACLs** → Folder/File
* **Private Endpoint** → Network isolation

---

### Q6. When to use RBAC vs ACL?

**A:**

* **RBAC** → Coarse-grained access
* **ACL** → Fine-grained data access

---

### Q7. What is the recommended folder structure?

**A:**

```
/raw
/bronze
/silver
/gold
```

Aligned with **Medallion Architecture**.

---

### Q8. How do you implement data isolation by domain?

**A:**

* Separate containers per domain
* Unity Catalog external locations
* Folder-level ACLs

---

### Q9. How to optimize cost in ADLS?

**A:**

* Lifecycle rules (hot → cool → archive)
* Small file compaction
* Avoid excessive metadata operations

---

### Q10. What are soft delete and versioning?

**A:**

* Soft delete protects accidental deletion
* Versioning allows rollback of blobs

---

### Q11. How do you design multi-region DR?

**A:**

* GRS/RA-GRS replication
* Paired region strategy
* Metadata replication

---

### Q12. What is the role of Private Endpoint?

**A:** Ensures traffic stays within Azure backbone, blocking public internet exposure.

---

### Q13. How does ADLS integrate with Databricks?

**A:**

* ABFS driver
* Managed Identity / Service Principal
* Unity Catalog external locations

---

### Q14. What is a filesystem in ADLS Gen2?

**A:** A filesystem maps to a container in Blob Storage.

---

### Q15. How do you manage metadata at scale?

**A:**

* Delta Lake transaction logs
* Hive Metastore / Unity Catalog

---

### Q16. What is POSIX compliance?

**A:** Unix-like permissions (rwx) for owner, group, others.

---

### Q17. How do you prevent accidental deletes?

**A:**

* Soft delete
* Immutable policies
* Restricted ACLs

---

### Q18. What is namespace performance benefit?

**A:** Faster rename/move vs flat namespace.

---

### Q19. What file formats are best for analytics?

**A:** Parquet, Delta (columnar, compressed).

---

### Q20. How do you handle millions of small files?

**A:**

* Auto Loader
* Delta OPTIMIZE
* File compaction jobs

---

### Q21. How does encryption work in ADLS?

**A:**

* Encryption at rest (Microsoft or CMK)
* TLS in transit

---

### Q22. What is CMK?

**A:** Customer-Managed Keys using Azure Key Vault.

---

### Q23. How do you audit access?

**A:**

* Azure Monitor
* Storage Analytics logs

---

### Q24. What is immutable storage?

**A:** WORM storage for compliance use cases.

---

### Q25. How to design for GDPR?

**A:**

* Data masking
* Right-to-be-forgotten
* Access auditing

---

### Q26. Can ADLS be used as OLTP?

**A:** No. It is optimized for analytics, not transactions.

---

### Q27. What is account-level throttling?

**A:** Azure limits on throughput; mitigated by partitioning.

---

### Q28. How do you isolate dev/test/prod?

**A:**

* Separate storage accounts
* Separate containers

---

### Q29. How do you migrate from Gen1 to Gen2?

**A:** Azure Data Factory + AzCopy.

---

### Q30. What is ABFS?

**A:** Azure Blob File System driver used by Spark.

---

### Q31. How do you design folder naming?

**A:**
`/source/system/entity/load_date=yyyy-mm-dd`

---

### Q32. How do you manage schema evolution?

**A:** Delta Lake + schema enforcement.

---

### Q33. What is eventual consistency?

**A:** Blob metadata consistency delay (reduced in Gen2).

---

### Q34. What is storage account limit?

**A:** ~5 PB per account (soft limit).

---

### Q35. Best practice for enterprise data lake?

**A:**
Security-first, domain-oriented, Delta-based, governed.

---

## SECTION 2: Azure Data Factory (ADF – Architecture)

**(Q36–Q75)**

### Q36. What is ADF?

**A:** Cloud ETL/ELT orchestration service.

---

### Q37. Difference between ETL and ELT?

**A:**

* ETL → Transform before load
* ELT → Transform after load (Databricks)

---

### Q38. Core components of ADF?

**A:**

* Pipelines
* Activities
* Datasets
* Linked Services
* Triggers

---

### Q39. What is Integration Runtime (IR)?

**A:** Compute infrastructure for data movement.

---

### Q40. Types of IR?

**A:**

* Azure IR
* Self-Hosted IR
* Azure-SSIS IR

---

### Q41. When to use Self-Hosted IR?

**A:** On-prem or private network sources.

---

### Q42. How do you design metadata-driven pipelines?

**A:**

* Control tables
* Dynamic datasets
* Parameterized pipelines

---

### Q43. How do you handle incremental loads?

**A:**

* Watermark columns
* CDC
* Delta merge

---

### Q44. How does ADF handle schema drift?

**A:** Limited; better handled in Databricks.

---

### Q45. What is a trigger?

**A:** Scheduling mechanism (schedule, tumbling, event).

---

### Q46. What is a tumbling window trigger?

**A:** Fixed-interval, dependency-aware trigger.

---

### Q47. How do you handle failures?

**A:**

* Retry policies
* Alerts
* Logging to Log Analytics

---

### Q48. How do you secure ADF?

**A:**

* Managed Identity
* Key Vault
* Private Endpoints

---

### Q49. What is Managed Identity?

**A:** Azure-managed service identity for auth.

---

### Q50. How do you pass parameters to Databricks?

**A:**

* Base parameters
* Notebook widgets

---

### Q51. What is mapping data flow?

**A:** Spark-based transformation in ADF.

---

### Q52. When NOT to use data flows?

**A:** Complex logic, heavy joins → use Databricks.

---

### Q53. How do you optimize ADF cost?

**A:**

* Avoid long-running data flows
* Use ELT
* Parallel copy tuning

---

### Q54. What is copy activity?

**A:** Core activity for data movement.

---

### Q55. How do you handle SCD in ADF?

**A:** Orchestrate → Databricks handles logic.

---

### Q56. How do you enable CI/CD?

**A:**

* Git integration
* ARM templates

---

### Q57. How do you deploy across environments?

**A:** Parameterized ARM templates.

---

### Q58. What is event-based trigger?

**A:** Trigger on blob arrival.

---

### Q59. How do you monitor pipelines?

**A:**

* ADF Monitor
* Azure Monitor

---

### Q60. What is pipeline concurrency?

**A:** Number of parallel runs allowed.

---

### Q61. How do you manage secrets?

**A:** Azure Key Vault integration.

---

### Q62. Can ADF transform data?

**A:** Yes, but limited compared to Databricks.

---

### Q63. How do you handle large tables?

**A:** Partitioned copy + parallelism.

---

### Q64. What is linked service?

**A:** Connection definition.

---

### Q65. How do you orchestrate dependencies?

**A:**

* Pipeline chaining
* Tumbling windows

---

### Q66. How do you debug pipelines?

**A:** Debug mode + activity logs.

---

### Q67. What is fault tolerance?

**A:** Retry, timeout, compensation logic.

---

### Q68. How do you handle schema changes?

**A:** Store schema metadata, validate downstream.

---

### Q69. What is global parameter?

**A:** Shared config across pipelines.

---

### Q70. How do you handle late arriving data?

**A:** Reprocessing window logic.

---

### Q71. ADF vs Synapse Pipelines?

**A:** Same engine; Synapse integrated with analytics.

---

### Q72. How do you throttle copy?

**A:** DIUs and parallel copy settings.

---

### Q73. What is cost driver in ADF?

**A:**

* Data movement
* Data flows
* Pipeline runs

---

### Q74. Can ADF do streaming?

**A:** No. Batch only.

---

### Q75. Best role of ADF in architecture?

**A:** **Orchestration, not transformation.**

---

## SECTION 3: Azure Databricks (ADB – Architecture & Lakehouse)

**(Q76–Q130)**

### Q76. What is Azure Databricks?

**A:** Managed Apache Spark platform optimized for Azure.

---

### Q77. What is Lakehouse?

**A:** Combines data lake + data warehouse capabilities.

---

### Q78. Why Databricks over Synapse Spark?

**A:** Better performance, Delta Lake, Unity Catalog.

---

### Q79. What is Delta Lake?

**A:** ACID-compliant storage layer on ADLS.

---

### Q80. What problems does Delta solve?

**A:**

* Schema drift
* Small files
* Data corruption

---

### Q81. What is Delta transaction log?

**A:** `_delta_log` maintains table state.

---

### Q82. What is OPTIMIZE?

**A:** File compaction.

---

### Q83. What is Z-ORDER?

**A:** Data skipping optimization.

---

### Q84. How do MERGE operations work?

**A:** Efficient upsert using Delta.

---

### Q85. What is Unity Catalog?

**A:** Central governance for data & AI.

---

### Q86. Unity Catalog benefits?

**A:**

* Fine-grained access
* Lineage
* Central metastore

---

### Q87. What is an external location?

**A:** Secure ADLS path registered in UC.

---

### Q88. How do you secure Databricks?

**A:**

* SCIM
* UC
* Private Link

---

### Q89. What cluster types exist?

**A:**

* Interactive
* Job clusters

---

### Q90. Job cluster vs interactive?

**A:** Job clusters are ephemeral & cheaper.

---

### Q91. How do you optimize Spark jobs?

**A:**

* Partitioning
* Broadcast joins
* Caching

---

### Q92. What is data skew?

**A:** Uneven data distribution.

---

### Q93. How do you fix skew?

**A:**

* Salting
* AQE
* Repartition

---

### Q94. What is Auto Loader?

**A:** Incremental file ingestion.

---

### Q95. How does Auto Loader work?

**A:** Uses file notifications or directory listing.

---

### Q96. What is checkpointing?

**A:** Maintains ingestion state.

---

### Q97. How do you handle schema evolution?

**A:**

* `mergeSchema`
* Auto Loader schema inference

---

### Q98. What is time travel?

**A:** Query historical Delta versions.

---

### Q99. How do you implement SCD Type 2?

**A:** Delta MERGE with effective dates.

---

### Q100. How do you manage deletes?

**A:**

* Soft delete flag
* GDPR delete workflows

---

### Q101. What is Photon?

**A:** Vectorized execution engine.

---

### Q102. How do you reduce Databricks cost?

**A:**

* Auto-termination
* Job clusters
* Spot VMs

---

### Q103. What is DBFS?

**A:** Databricks File System (abstract layer).

---

### Q104. DBFS vs ADLS?

**A:** DBFS is abstraction; ADLS is storage.

---

### Q105. What is workspace isolation?

**A:** Separate workspaces per environment.

---

### Q106. How do you orchestrate jobs?

**A:**

* ADF
* Databricks Jobs

---

### Q107. How do you monitor jobs?

**A:**

* Ganglia
* Job UI
* Logs

---

### Q108. What is cluster autoscaling?

**A:** Dynamic worker scaling.

---

### Q109. What is AQE?

**A:** Adaptive Query Execution.

---

### Q110. How do you handle large joins?

**A:**

* Broadcast
* Repartition
* Bucketing

---

### Q111. What is data lineage?

**A:** Track data movement & usage.

---

### Q112. How does Unity Catalog provide lineage?

**A:** Column-level lineage automatically.

---

### Q113. How do you manage notebooks?

**A:** Repo integration (Git).

---

### Q114. Python vs SQL in Databricks?

**A:**

* Python → logic
* SQL → analytics

---

### Q115. What is multi-hop architecture?

**A:** Raw → Bronze → Silver → Gold.

---

### Q116. What is Bronze layer?

**A:** Raw ingested data.

---

### Q117. What is Silver layer?

**A:** Cleaned & conformed data.

---

### Q118. What is Gold layer?

**A:** Business-ready aggregates.

---

### Q119. How do you handle PII?

**A:**

* Column masking
* Tokenization

---

### Q120. How do you enable row-level security?

**A:** Unity Catalog row filters.

---

### Q121. How do you expose data to Power BI?

**A:**

* Databricks SQL Warehouse
* Direct Lake (Fabric)

---

### Q122. What is SQL Warehouse?

**A:** Serverless SQL compute.

---

### Q123. How do you manage concurrency?

**A:** Separate SQL warehouses.

---

### Q124. What is vacuum?

**A:** Deletes old Delta files.

---

### Q125. Why not vacuum immediately?

**A:** Breaks time travel.

---

### Q126. What is cluster policy?

**A:** Controls cluster configurations.

---

### Q127. How do you implement CI/CD?

**A:**

* Repos
* Jobs API
* Terraform

---

### Q128. How do you test data quality?

**A:**

* Expectations
* Custom validation frameworks

---

### Q129. What is the role of Databricks in D&IT?

**A:** Core **processing, transformation, and governance engine**.

---

### Q130. Final architecture best practice?

**A:**
**ADF = Orchestration
ADLS = Storage
Databricks = Processing
Unity Catalog = Governance**

---