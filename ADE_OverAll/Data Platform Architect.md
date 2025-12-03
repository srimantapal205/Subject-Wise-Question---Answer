
# ✅ **SECTION 1 — Azure Cloud Architecture (25 Questions)**

### **1. What are key architectural components of a scalable Azure Data Platform for an enterprise?**

A scalable Azure platform includes:

* **ADLS Gen2** for storage
* **Databricks** for compute
* **Azure SQL / Synapse** for serving
* **Key Vault** for secrets
* **Virtual Networks + Private Endpoints**
* **Purview or Unity Catalog** for governance
* **Power BI Premium** for consumption
* **ADF / Data Factory** for orchestration
  This forms a modular, decoupled, secure architecture.

---

### **2. Scenario: Your ADLS ingestion zone is receiving 5 TB/day and query latency is increasing. What architectural fix would you apply?**

* Move ingestion data to **partitioned layout (year/month/day)**
* Enable **columnar formats like Delta**
* Increase **Databricks cluster autoscale**
* Introduce **OPTIMIZE + ZORDER** jobs.

---

### **3. How do you design ADLS folder structure for enterprise-scale data?**

Use **medallion architecture**:

* Raw
* Bronze
* Silver
* Gold
  Ensure **schema-on-read & Delta format**, enforce naming standards, and apply **container-based RBAC**.

---

### **4. Why use Private Endpoints for data platform components?**

To restrict traffic to **Microsoft backbone network**, blocking public access. Enhances zero-trust compliance.

---

### **5. When should you choose Serverless vs. Dedicated pool in Synapse?**

Use **serverless** for ad-hoc exploration;
Use **dedicated** for predictable high-performance workloads.

---

### **6. Scenario: Migration from on-prem Hadoop to Azure. What would be your target architecture?**

Move HDFS → ADLS Gen2
Hive workloads → Databricks Spark
Oozie → ADF
Ranger → Unity Catalog
Sqoop → ADF pipelines
Kafka → EventHub

---

### **7. How do you design multi-region DR strategy in Azure?**

* Geo-redundant storage (**GRS**)
* Databricks workspace replicated
* Power BI backup tenant
* Failover DNS routing
* Automated IaC redeployment.

---

### **8. What is the best practice for Databricks cluster isolation?**

Create **separate clusters per functional domain**, apply **network policies**, and enforce **Unity Catalog workspace assignment**.

---

### **9. Why use Delta Lake instead of Parquet?**

Delta provides:

* ACID
* Time travel
* Schema enforcement
* DML operations
* Optimized metadata.

---

### **10. How do you implement cost governance for Databricks?**

* Cluster policies
* Job clusters instead of all-purpose clusters
* Photon runtimes
* Auto-terminate
* Usage dashboards.

---

### **11. How do you scale ingestion if ADF Copy throughput is low?**

* Increase DIUs
* Use **binary copy**
* Parallelize by partition
* Use **polybase** integration where applicable.

---

### **12. Why use Managed VNET ADF integration runtime?**

Provides **network isolation**, **no public internet exposure**, and **private endpoints**.

---

### **13. When to use EventHub vs. Kafka on HDInsight?**

EventHub for cloud-native PaaS streaming;
Kafka when workload is heavy and requires open-source ecosystem.

---

### **14. Scenario: Lakehouse queries are slow. What tuning steps?**

* OPTIMIZE
* VACUUM
* Partition pruning
* Smaller file compaction
* ZORDER on key columns.

---

### **15. Why use Dataflows (Power BI) only for light transformations?**

Because heavy transformations should occur in **Databricks/Synapse**, not at the semantic layer.

---

### **16. How do you design CI/CD for Azure Data Factory?**

* Repository in Git
* ARM templates
* Multi-environment pipelines
* Key Vault parameterization
* Automated publishing.

---

### **17. What is a Lakehouse?**

Unified storage+compute model combining **warehouse performance** and **data lake scalability** using Delta.

---

### **18. How do you implement Data Mesh on Azure?**

* Domain-based data products
* Unified governance layer (Unity Catalog / Purview)
* Decentralized ownership
* Shared platform services.

---

### **19. How to enforce dynamic data masking in ADLS?**

Use:

* Unity Catalog column masking policies
* Attribute-based access control (ABAC)
* Row-level security.

---

### **20. Scenario: ADF pipeline latency increased after scale. How to analyse?**

Check:

* IR concurrency
* Source throttling
* Sink write throughput
* Network latency
* Pipeline design (loops, waits).

---

### **21. Why use hybrid architecture?**

To integrate:

* On-prem ERP
* Legacy systems
* Edge devices
  with cloud platforms.

---

### **22. How to avoid small file problem in Delta Lake?**

* Use **Auto Optimize**
* File compaction jobs
* CombineByKey in ETL.

---

### **23. What is Data Product Architecture?**

Reusable, discoverable, governed datasets with ownership, SLAs, and metadata.

---

### **24. How to optimize Power BI refresh when using Direct Lake?**

* Use **Delta**
* Optimize file size
* ZORDER by dimension keys
* Enable auto-optimization in Databricks.

---

### **25. How do you design infrastructure-as-code for a full data platform?**

Use Terraform modules for:

* ADLS
* Databricks Workspace
* Key Vault
* Networking
* ADF
* Purview/Unity Catalog.

---

---

# ✅ **SECTION 2 — Databricks + Spark Architecture (25 Questions)**

### **26. What is Unity Catalog?**

A centralized governance model for:

* Metadata
* Security
* Auditing
* Lineage
  across all Databricks assets.

---

### **27. How do you enforce table-level security in Unity Catalog?**

Using:

* GRANT SELECT/INSERT
* RBAC at catalog/schema/table levels.

---

### **28. How do you implement cross-account data sharing?**

Use **Delta Sharing**, enabling secure share of datasets across organizations without copying.

---

### **29. Scenario: Silver tables have inconsistent schema. Solution?**

* Use **AUTO MERGE SCHEMA** sparingly
* Enforce schema at ingestion
* Validate against schema registry
* Apply DQ checks.

---

### **30. What is Photon engine?**

Databricks’ vectorized execution engine improving:

* Query performance
* CPU efficiency
* Costs.

---

### **31. When to use Autoloader instead of COPY INTO?**

Use **Autoloader** for streaming/incremental ingestion;
Use **COPY INTO** for batch historical loads.

---

### **32. How do you ensure ACID compliance for streaming writes?**

Use **Delta Lake** which manages commits & concurrency automatically.

---

### **33. What causes “Too many files” issue in Delta?**

Small file creation due to:

* Streaming micro-batches
* Parallel writes
  Fix via **OPTIMIZE**.

---

### **34. How to store secrets in Databricks?**

Use Azure Key Vault-backed secret scopes.

---

### **35. Scenario: Job cluster startup taxes pipeline runtime. Optimize?**

* Create interactive cluster with **job light scheduling**
* Use instance pools
* Reduce cluster start overhead.

---

### **36. What is a schema evolution strategy?**

* Enforce allowed changes
* Register schemas
* Versioned schemas
* Use Merge with constraints.

---

### **37. Why use Delta Live Tables?**

For:

* Declarative ETL
* Built-in quality checks
* Auto lineage
* Observability.

---

### **38. How do Lakehouse pipelines support DQ?**

Using **expectations** (e.g., `expect_column_values_to_not_be_null`).

---

### **39. How do you isolate compute in Databricks?**

* Multiple workspaces
* Private Link
* Workspace–VNET isolation.

---

### **40. Scenario: UDFs slow down Spark. Solution?**

Use:

* Pandas UDFs
* Built-in functions
* Native SQL transforms.

---

### **41. How do you manage slow-changing dimensions in Delta Lake?**

Use **MERGE** for type-2 or type-1 SCD patterns.

---

### **42. Why use broadcast joins?**

To avoid shuffles when one dataset is small (< 10 MB).

---

### **43. How to minimize shuffle operations?**

Use:

* partitioning keys
* bucket tables
* avoid explode in large datasets
* optimize join conditions.

---

### **44. When to use caching in Spark?**

For iterative operations or repeated queries on same data.

---

### **45. What is a Databricks Repo?**

Git-backed development environment for notebooks & files.

---

### **46. Scenario: Large streaming jobs failing due to checkpoint corruption. Solution?**

* Stop pipeline
* Clear checkpoint directory
* Reprocess mini-batch
* Use **idempotent writes** to avoid duplicates.

---

### **47. How do you design global governance using multiple UC metastores?**

Create **per-region metastore** with **federated governance**.

---

### **48. Why use delta change data feed (CDF)?**

To capture row-level changes for downstream incremental ETL.

---

### **49. How to debug slow Spark job?**

Inspect:

* Stage DAG
* Shuffle size
* Spill events
* Skew
* Cluster CPU metrics.

---

### **50. What is `OPTIMIZE ZORDER()` used for?**

Optimizing file pruning for high-cardinality columns.

---
---

# ✅ **SECTION 3 — Security, RBAC, Compliance, Zero Trust (20 Questions)**

---

### **51. What is Zero-Trust Architecture?**

A security model where **no user/system is trusted by default**, even inside the network. Continuous verification is required through identity, device posture, conditional access, and micro-segmentation.

---

### **52. How do you implement Zero Trust in a data platform?**

* Use **Private Endpoints** for all services
* Disable public IPs
* RBAC enforcement
* Service principals with least privilege
* Identity-based access to ADLS
* Key Vault for secret storage.

---

### **53. Scenario: A business team needs read access to only specific columns in a table (PII). Solution?**

Use **Unity Catalog Column Masks**:

```sql
CREATE MASKING POLICY pii_mask AS (val STRING) -> STRING
RETURN CASE WHEN is_member('finance') THEN val ELSE '****' END;
```

---

### **54. How do you implement row-level security in Databricks?**

Use UC row filters:

```sql
CREATE ROW FILTER region_filter(region STRING)  
RETURN region = current_user_region();
```

---

### **55. How do you ensure encryption for data at rest in ADLS?**

* SSE with Microsoft-managed keys
* Customer-managed keys (CMK) using Key Vault.
  CMK enables key rotation policies.

---

### **56. How do you secure data in transit?**

Azure enforces **TLS 1.2+** for all communication.

---

### **57. What is the best way to secure notebook credentials?**

Store all secrets in **Key Vault-backed secret scopes**, never inside notebooks.

---

### **58. Scenario: A contractor needs temporary access — how do you design it?**

* Assign **time-bound RBAC roles**
* Use Privileged Identity Management (PIM)
* Log all access in Purview/UC audit logs.

---

### **59. How do you identify data exfiltration risks in Azure?**

Enable:

* Defender for Cloud alerts
* Diagnostic logs
* Activity logs
* Conditional Access restrictions.

---

### **60. What is the purpose of Private Link in Databricks?**

To ensure traffic between workspace & data plane stays within Azure private backbone.

---

### **61. What is network isolation in ADF Managed VNET?**

ADF Integration Runtime runs in **Microsoft-managed VNet**, eliminating public access.

---

### **62. Scenario: How do you block unauthorized copying of ADLS data to external storage?**

* Disable **public access**
* Use **Conditional Access policies**
* Restrict storage firewalls
* Use **service endpoints** only.

---

### **63. How do you design GDPR-compliant architecture?**

* Data minimization
* Data masking
* Subject access request workflows
* Audit logs
* Retention policies.

---

### **64. How do you ensure secrets are never exposed in CI/CD pipelines?**

Use:

* Variable groups with Key Vault references
* Azure DevOps secure files
* Pipeline identity with least privilege.

---

### **65. What’s the difference between RBAC and ACL in ADLS?**

* RBAC: at **resource/service level**
* ACL: at **file/folder level**
  Use RBAC for broader roles, ACL for granular access.

---

### **66. Scenario: A user accidentally gets elevated access. How to mitigate?**

* Analyze audit logs
* Revoke access
* PIM approval workflows
* Implement access reviews.

---

### **67. How do you design Key Vault for multi-region deployment?**

* Region-paired Key Vaults
* Geo-redundant secret replication
* Soft delete + purge protection.

---

### **68. What identity model is used for Databricks?**

Azure AD + Service principals + Unity Catalog identity federation.

---

### **69. Why use conditional access for Power BI?**

To enforce:

* MFA
* IP restrictions
* Device compliance
* Geolocation-based access.

---

### **70. How do you monitor unauthorized data access?**

Use UC and Purview audit logs + Sentinel SIEM integration.

---

---

# ✅ **SECTION 4 — Governance, Metadata, Lineage, Unity Catalog, Purview (20 Questions)**

---

### **71. What is a Data Governance Framework?**

A standardized approach covering:

* Data ownership
* Quality rules
* Data lineage
* Metadata standards
* Classification
* Change management.

---

### **72. How does Unity Catalog support lineage?**

It tracks lineage **from notebook → table → dashboard**, including cross-workspace flows.

---

### **73. Scenario: Teams maintain inconsistent business definitions. Solution?**

Implement **Business Glossary** in Purview/UC with domain owners.

---

### **74. What is the purpose of a data dictionary?**

Provides definitions, meaning, permissible values of attributes ensuring standardized usage.

---

### **75. How do you classify data into sensitivity levels?**

Example:

* Public
* Internal
* Confidential
* Restricted (PII/Financial)

Use Purview classification rules.

---

### **76. What is the difference between Technical vs Business lineage?**

* Technical lineage shows data movement (jobs, pipelines)
* Business lineage shows meaning (business process flow).

---

### **77. How do you enforce governance in Data Mesh?**

* Domain-by-domain governance
* Federated UC metastores
* Central policies (DQ, access, lineage).

---

### **78. Scenario: Analysts use outdated datasets. How do you enforce certified datasets?**

* Certify “gold tables” in UC
* Lock others as deprecated
* Create dashboards highlighting certified assets.

---

### **79. How do you manage schema changes at platform scale?**

* Schema registry
* Schema versioning
* Auto evolution rules
* Validation pipelines.

---

### **80. What is “Data Trust Score”?**

Metric combining:

* Data quality
* Freshness
* Completeness
* Accuracy
  Used in governance dashboards.

---

### **81. How does Purview integrate with Databricks?**

Through **Unity Catalog -> Purview connectors** enabling metadata + lineage sync.

---

### **82. Why enforce tagging on data assets?**

Tags help automate:

* Access policies
* Cost allocation
* GDPR compliance
* Discovery.

---

### **83. Scenario: Thousands of tables exist with no ownership. Solution?**

* Enforce data product ownership
* Auto metadata scanning
* Assign default stewards.

---

### **84. Why use Data Contracts?**

To ensure stable, validated, backward-compatible data APIs between producers & consumers.

---

### **85. How do you audit access across the platform?**

Collect logs from:

* ADLS
* Databricks
* ADF
* Power BI
  Feed into Sentinel.

---

### **86. What is metadata-driven ingestion?**

Ingestion logic is based on metadata tables defining:

* Source paths
* Formats
* Schema
* DQ rules
* Load strategy.

---

### **87. What is the difference between a Data Catalog and a Business Glossary?**

Catalog → Technical metadata
Glossary → Business terms

---

### **88. How does UC enforce consistent security across tables?**

Central RBAC at catalog → schema → table levels.

---

### **89. What is Holistic Data Governance?**

End-to-end governance covering security, metadata, quality, lineage, lifecycle, and ownership.

---

### **90. Why enforce retention policies?**

To comply with GDPR + control storage cost.

---

---

# ✅ **SECTION 5 — Reusable Frameworks, Accelerators, Data Contracts, Quality (20 Questions)**

---

### **91. What is a reusable data ingestion framework?**

A configurable, parameterized pipeline supporting:

* Copy
* Merge
* Delta conversion
* Metadata-driven execution.

---

### **92. Scenario: You must ingest 500+ tables from SAP. Approach?**

Create metadata tables for:

* Table name
* Keys
* Schedule
* Incremental logic
* DQ rules
  Ingestion becomes automated.

---

### **93. What is Metadata-Driven ETL?**

ETL logic defined via metadata tables instead of hard-coded pipelines.

---

### **94. What are Data Quality dimensions?**

* Completeness
* Accuracy
* Timeliness
* Validity
* Consistency
* Uniqueness.

---

### **95. How do you implement DQ rules in Databricks?**

Using Delta Live Tables expectations or Great Expectations.

---

### **96. Scenario: Scattered ETL jobs with inconsistent naming. Fix?**

Create standardized naming conventions like:
`src_<domain>_<entity>_ingest`.

---

### **97. What are platform accelerators?**

Reusable components:

* Logging
* Error handling
* DQ modules
* Code templates
* Monitoring dashboards.

---

### **98. How to design multi-tenant pipelines?**

Use metadata flags + environment routing.

---

### **99. How do you manage error handling in pipelines?**

* Dead-letter storage
* Error codes
* Retry policies
* Failure alerts.

---

### **100. What is a Data Contract violation?**

Consumer expectations break because producer changes schema breaking compatibility.

---

### **101. How do you enforce idempotency?**

Use:

* Merge logic
* Checksums
* File metadata tracking.

---

### **102. How do you monitor pipeline SLAs?**

Implement:

* Monitor tables
* Logging
* ADF Alerts
* Databricks metrics.

---

### **103. Why adopt orchestration templates?**

To reduce duplicated logic and onboarding time.

---

### **104. Scenario: Frequently changing schemas from vendor files. Solution?**

Use schema evolution with constraints + quarantine invalid files.

---

### **105. How do you ensure consistency across global markets?**

Create **global framework libraries** imported in all pipelines.

---

### **106. How do you design reusable parameterized notebooks?**

Use widgets and config JSON files.

---

### **107. What is the pattern for batch incremental loading?**

Use watermark + merge:

```SQL
MERGE INTO silver t USING staging s ON t.key = s.key 
WHEN MATCHED THEN UPDATE 
WHEN NOT MATCHED THEN INSERT;
```

---

### **108. What is a data onboarding checklist?**

Checklist covering:

* Ownership
* Classification
* Schema
* DQ rules
* SLAs.

---

### **109. Why implement observability?**

To detect:

* Latency
* Failures
* Schema drifts
* Quality issues.

---

### **110. What is a computation pushdown strategy?**

Push filters to storage, reducing compute load.

---

---

# ✅ **SECTION 6 — CI/CD, DevOps, Automation, Terraform (20 Questions)**

---

### **111. How do you design CI/CD for Databricks?**

Use:

* Repos connected to Git
* Bundle files (dbx)
* Automated cluster setup
* Delta test data
* Deploy to PROD using release pipelines.

---

### **112. What is Infrastructure-as-Code?**

Provisioning environments using code (Terraform/ARM/Bicep).

---

### **113. Scenario: Two developers overwrite code in ADF. Solution?**

Enable **Git Integration** for ADF.

---

### **114. How do you manage multi-environment configurations in pipelines?**

Use variable groups and Key Vault references.

---

### **115. Why use Terraform for data platform provisioning?**

For:

* Repeatability
* Consistency
* Versioning
* Automated deployments.

---

### **116. How do you automate Databricks cluster creation?**

Terraform `databricks_cluster` resource.

---

### **117. What is dbx?**

A Databricks DevOps tool supporting:

* Job deployment
* Testing
* Bundle management.

---

### **118. How do you validate infrastructure changes?**

Use Terraform plan + static code analysis.

---

### **119. Scenario: Pipeline fails in PROD but passes in DEV. What’s the cause?**

Most common issues:

* Missing secrets
* Wrong connection strings
* Missing permissions
* Data size difference.

---

### **120. How do you automate Power BI deployment?**

Use Power BI deployment pipelines + service principal.

---

### **121. Why containerize frameworks using Docker?**

For reproducible development/test environments.

---

### **122. What is blue-green deployment?**

Switching between two identical environments for zero-downtime releases.

---

### **123. How do you automate data quality checks in CI/CD?**

Run DQ unit tests using PySpark test frameworks.

---

### **124. Why use Git branching strategies?**

To manage parallel development, e.g.:

* Main
* Develop
* Feature
* Release.

---

### **125. How do you manage library version conflicts?**

Use pinned versions in `requirements.txt`.

---

### **126. How to validate ADF pipelines?**

Use ARM template validation + ADF publish test.

---

### **127. What is Databricks Asset Bundle?**

A unified package containing:

* Jobs
* Notebooks
* Libraries
  for deployment.

---

### **128. How to secure Terraform state?**

Store in **Azure Storage with SAS disabled** + Key Vault encryption.

---

### **129. How do you automate cluster policy assignments?**

Using Terraform resource `databricks_cluster_policy`.

---

### **130. Why use automated code linting?**

To enforce code quality, readability, consistency.

---

---

# ✅ **SECTION 7 — ADF, Orchestration, Pipelines, Integration (20 Questions)**

---

### **131. What is the role of ADF in the data platform?**

ADF orchestrates movement + transformation using:

* Pipelines
* Data flows
* Integration Runtime.

---

### **132. Scenario: Copy activity from Oracle is slow. Solution?**

* Enable partitioning
* Use Oracle staging
* Optimize query
* Increase DIUs.

---

### **133. How do you design incremental loading from SAP?**

Use:

* ODP extractors
* Change pointers
* Delta queues
* Last-run watermark tables.

---

### **134. What are Integration Runtimes?**

Execution engines in ADF:

* Auto (cloud IR)
* Self-hosted
* Managed VNET IR.

---

### **135. Why avoid complex Data Flows in ADF?**

Use Databricks for scalable compute instead of ADF DF runtime.

---

### **136. Scenario: You need to ingest 10,000 files daily. How?**

Use Databricks **Autoloader** inside ADF pipeline.

---

### **137. How do you alert on pipeline failures?**

Use ADF alerts integrated with email/SMS/Teams.

---

### **138. What is Lookup activity used for?**

Fetching metadata values for dynamic pipelines.

---

### **139. How do you implement ADF naming conventions?**

Prefix by layer:
`pl_ingest_customer`,
`ds_src_oracle_customer`.

---

### **140. What is a tumbling window trigger?**

Schedules periodic executions supporting late arrival handling.

---

### **141. How do you pass parameters across pipelines?**

Using pipeline parameters + global parameters + system variables.

---

### **142. Scenario: Pipeline needs retry logic. How to implement?**

Use **Retry policy** in each activity with exponential backoff.

---

### **143. What is the difference between ADF and Synapse Pipelines?**

Synapse provides tighter integration with workspace + SQL pools.

---

### **144. How do you handle schema drift in ADF?**

Enable schema drift & map drift in Mapping Data Flows.

---

### **145. How do you load data into Delta from ADF?**

Use COPY Command or Databricks Notebook Activity.

---

### **146. What is the best way for ADF to trigger Databricks?**

Use Databricks activity with job clusters for cost efficiency.

---

### **147. What is the purpose of pipeline concurrency control?**

To avoid duplicate/overlapping pipeline runs.

---

### **148. How do you orchestrate end-to-end medallion ETL?**

ADF → triggers Databricks → quality checks → metadata update.

---

### **149. How do you enable secure access from ADF to ADLS?**

Use Managed Identity + RBAC.

---

### **150. How do you track run metadata for auditing?**

Use logging tables storing:

* Pipeline name
* Timestamp
* Duration
* Row counts.

---

---

# ✅ **SECTION 8 — Power BI Enterprise Governance & Semantic Layer (20 Questions)**

---

### **151. How do you enforce Power BI governance at scale?**

* Tenant settings
* Certified datasets
* Workspace governance
* Data sensitivity labels.

---

### **152. Scenario: Report refresh takes 5 hours. Solution?**

* Use **Direct Lake**
* Switch to **Incremental Refresh**
* Optimize model
* Materialize DAX.

---

### **153. Why use Power BI service principal?**

For CI/CD deployments, automated refreshes, and enhanced security.

---

### **154. What is an endorsed dataset?**

Certified or promoted datasets approved by data governance team.

---

### **155. What is Incremental Refresh?**

Refreshes only modified partitions reducing time & cost.

---

### **156. How do you enforce RLS in Power BI?**

DAX filters like:

```DAX
[Region] = USERPRINCIPALNAME()
```

---

### **157. Scenario: 100+ market teams build duplicate reports. Solution?**

Implement **central semantic models** + certified datasets.

---

### **158. How do you optimize Power BI models?**

* Reduce cardinality
* Star schema
* Avoid bi-directional relationships
* Limit calculated columns.

---

### **159. Why use Power BI dataflows?**

For reusable ETL across multiple datasets.

---

### **160. How do you integrate UC with Power BI?**

Direct Lake or SQL endpoint integration using service principal.

---

### **161. How to monitor dataset refresh failures?**

Enable:

* Refresh history logs
* Admin API
* Power BI activity logs.

---

### **162. Why use Power BI deployment pipelines?**

To enable dev-test-prod release governance.

---

### **163. What is Power BI Gateway used for?**

To access on-prem data securely.

---

### **164. How do you handle large fact tables?**

Use **Hybrid Tables** (DirectQuery + Import mode).

---

### **165. How to implement semantic layering strategy?**

Bronze → Silver → Gold → Dataset → Report.

---

### **166. Scenario: Security requires masking PII before BI consumption. Solution?**

Mask data at gold layer or use UC **column masking policies**.

---

### **167. Why choose DirectQuery?**

When data needs real-time freshness (trading, logistics).

---

### **168. What is Fabric OneLake?**

Unified storage layer integrating Lakehouse + Warehouse + Real-time data.

---

### **169. Why avoid heavy transformations in Power BI?**

To maintain performance and centralize logic in Databricks/Synapse.

---

### **170. How to handle shared datasets for global markets?**

Use multi-geo Premium capacities.

---

---

# ✅ **SECTION 9 — Real-Time Scenarios, Failures, Root Cause, Architecture Decisions (25 Questions)**

---

### **171. Scenario: Your pipeline suddenly doubles in duration. Root causes?**

* Source throttling
* Hot partitions
* Cluster downgraded
* Network latency
* Schema drift.

---

### **172. Scenario: Lakehouse storage growing too fast. What to do?**

* Enable VACUUM
* Optimize retention policies
* Delete orphaned checkpoints
* Review audit logs for dumps.

---

### **173. Scenario: Power BI dashboards slow after migration to Lakehouse. Solution?**

* ZORDER fact tables
* Optimize model
* Use summary/aggregation tables.

---

### **174. Scenario: You must integrate ingestion with external SFTP. Approach?**

Use ADF Self-hosted IR + private network connectivity.

---

### **175. Scenario: Databricks job failing with OOM. Fix?**

* Increase workers
* Avoid wide transformations
* Cache selectively
* Repartition appropriately.

---

### **176. Scenario: Data duplication in silver layer. Causes?**

* Non-idempotent ingestion
* Missing merge logic
* Duplicate files.

---

### **177. Scenario: Need to isolate PII datasets from wider team. Solution?**

Create dedicated UC catalog with strict RBAC.

---

### **178. Scenario: Analysts complain of inconsistent metric definitions. Solution?**

Implement unified semantic model or metrics layer.

---

### **179. Scenario: Need cross-region data access for analytics. Solution?**

Use geo-replicated ADLS + cross-region UC metastore access.

---

### **180. Scenario: Migration to Unity Catalog – what steps?**

* Inventory tables
* Migrate Hive metastore
* Update code for UC paths
* Migrate permissions.

---

### **181. Scenario: Kafka streaming ingestion failing due to increasing lag. Fix?**

* Scale consumer
* Optimize micro-batch size
* Parallel readers
* Increase partitions.

---

### **182. Scenario: False failures due to transient network issues. Solution?**

Use retry patterns with exponential backoff.

---

### **183. Scenario: Teams bypass governance by creating unmanaged tables. Solution?**

Disable external/hive metastore & enforce Unity Catalog only.

---

### **184. Scenario: How to support both batch and streaming in the same pipeline?**

Use Delta Lake which supports **unified batch + streaming**.

---

### **185. Scenario: ADLS access denied for service principal. Fix?**

Grant:

* RBAC: Storage Blob Data Contributor
* ACLs on folder.

---

### **186. Scenario: Backfill of 5 years of data required. Approach?**

* Use job clusters
* Partitioned ingestion
* Parallel historical loads.

---

### **187. Scenario: Power BI export fails due to security restrictions. Fix?**

Use **sensitivity labels** + **conditional access exceptions**.

---

### **188. Scenario: Vendor provides corrupt CSV files. Approach?**

* Validate schema
* Quarantine invalid files
* Send automated alerts.

---

### **189. Scenario: Cross-team collaboration issues in large data platform. Solution?**

Create:

* Architecture Review Board
* Data Product Owners
* Standards committees.

---

### **190. Scenario: Query skew causing slow joins. Solution?**

* Salting
* Repartition on join keys
* Broadcast smaller dataset.

---

### **191. Scenario: Need GDPR “Right To Be Forgotten”. How to implement?**

Use Delta **DELETE** and VACUUM after retention window.

---

### **192. Scenario: API ingestion hitting 429 throttling. Solution?**

* Increase retries
* Backoff
* Concurrent threads with limit
* Caching responses.

---

### **193. Scenario: Need to run 100+ workflows daily. Orchestration approach?**

Use ADF pipeline factory pattern + control tables.

---

### **194. Scenario: Multi-tenant access isolation. Solution?**

Use UC metastore per tenant or catalog per tenant.

---

### **195. Scenario: Audit team requires weekly privileged access logs. Solution?**

Deliver Sentinel reports + UC audit tables.

---

---

# ✅ **SECTION 10 — Leadership, Architectural Review, Best Practices, Stakeholder Guidance (20 Questions)**

---

### **196. How do you conduct an Architecture Review Board (ARB)?**

Checklist:

* Security
* Scalability
* Cost
* SLAs
* Governance
* DR
* Maintainability.

---

### **197. How do you ensure projects follow standards?**

* Design patterns library
* Guardrails
* Checklists
* Code templates
* Mandatory ARB approval.

---

### **198. How do you manage conflicting stakeholder requirements?**

Use:

* Prioritization framework
* Trade-off analysis
* Documented ADRs.

---

### **199. How do you mentor engineers?**

* Code reviews
* Design sessions
* Internal forum
* Reusable templates
* Hackathons.

---

### **200. What leadership qualities define a Data Platform Architect?**

* Strategic thinking
* Technical depth
* Communication
* Decision-making
* Governance mindset.

---

### **201. How do you justify architecture decisions to leadership?**

Use an **Architecture Decision Record (ADR)** documenting:

* Context
* Options
* Pros/Cons
* Recommendation.

---

### **202. How do you reduce platform operational cost?**

* Auto-terminate clusters
* Monitor idle pipelines
* Optimize storage tiers
* Use serverless compute where possible.

---

### **203. How do you measure platform maturity?**

Across pillars:

* Governance
* Security
* Observability
* Automation
* Performance.

---

### **204. How do you ensure innovation in the data platform?**

* POCs
* R&D budget
* Tech radar updates
* Pilot GenAI, semantic layer, DLT.

---

### **205. How do you define KPIs for a global data platform?**

* Data quality SLAs
* Freshness SLAs
* Cost per TB
* Adoption rate
* PII issues count.

---

### **206. How do you manage multi-vendor integration?**

* Interface contracts
* Standard API formats
* SLA governance
* Change control.

---

### **207. How do you drive cross-market adoption of the platform?**

* Training sessions
* Enablement playbooks
* Standard onboarding.

---

### **208. How do you design a long-term platform roadmap?**

Include:

* Tech modernization
* Governance maturity
* AI integration
* Cost optimization
* Scalability milestones.

---

### **209. How do you approach technical debt?**

* Identify
* Prioritize
* Mitigate
* Plan technical sprints.

---

### **210. How do you communicate complex tech to business users?**

Storytelling using:

* Visual diagrams
* Value impact
* Simplified terminology.

---
