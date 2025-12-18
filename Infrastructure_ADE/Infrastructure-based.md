# Infrastructure-based Azure Data Engineering Interview Questions & Answers

---
---

## SECTION 1: Azure Infrastructure Fundamentals (Q1–Q20)

---

### **Q1. What core Azure infrastructure components does a data engineer work with?**

**Answer:**
An Azure Data Engineer primarily works with:

* **Compute:** Azure Databricks, Synapse Spark pools, Azure Functions
* **Storage:** ADLS Gen2, Blob Storage
* **Networking:** VNETs, Private Endpoints, NSGs
* **Security:** Azure AD, RBAC, Managed Identity
* **Integration:** Azure Data Factory, Event Hub
* **Monitoring:** Azure Monitor, Log Analytics

👉 *Example:* Databricks inside a VNET accessing ADLS via Private Endpoint.

---

### **Q2. Difference between Azure Blob Storage and ADLS Gen2?**

**Answer:**

| Feature   | Blob Storage | ADLS Gen2       |
| --------- | ------------ | --------------- |
| Namespace | Flat         | Hierarchical    |
| Analytics | Limited      | Optimized       |
| ACLs      | No           | Yes             |
| Cost      | Lower        | Slightly higher |

👉 **ADLS Gen2 is preferred for analytics workloads.**

---

### **Q3. Why is hierarchical namespace important?**

**Answer:**

* Enables **directory-level operations**
* Faster metadata operations
* Required for **Spark, Delta Lake, Synapse**

👉 *Example:* Efficient partition pruning in Delta tables.

---

### **Q4. What is a VNET and why is it needed for data platforms?**

**Answer:**
A VNET provides **network isolation**, secure communication, and private access.

👉 *Example:* Databricks + ADLS + SQL DB in same VNET.

---

### **Q5. What is a Private Endpoint?**

**Answer:**
Private Endpoint allows access to Azure services **without public internet**.

👉 *Example:* ADF → ADLS over private IP.

---

### **Q6. Difference between Service Endpoint and Private Endpoint?**

**Answer:**

* **Service Endpoint:** Traffic stays on Azure backbone
* **Private Endpoint:** Resource has private IP inside VNET (recommended)

---

### **Q7. What is Managed Identity and why is it important?**

**Answer:**

* Eliminates secrets/passwords
* Secure authentication to Azure services

👉 *Example:* ADF accessing ADLS without keys.

---

### **Q8. How do you secure ADLS Gen2?**

**Answer:**

* RBAC + ACLs
* Private Endpoint
* Firewall rules
* Encryption at rest (default)

---

### **Q9. What is Azure Key Vault used for?**

**Answer:**

* Stores secrets, keys, certificates
* Integrated with ADF, Databricks

👉 *Example:* Store DB passwords securely.

---

### **Q10. Explain Azure RBAC in data engineering**

**Answer:**
Controls **who can do what** at resource level.

👉 *Example:*

* Reader → Read only
* Contributor → Create resources

---

### **Q11. What are NSGs?**

**Answer:**
Network Security Groups control inbound/outbound traffic.

---

### **Q12. What is Azure Monitor used for?**

**Answer:**

* Metrics
* Logs
* Alerts

👉 *Example:* Alert if Databricks job fails.

---

### **Q13. Difference between Availability Zone and Region?**

**Answer:**

* **Region:** Geographic location
* **Zone:** Physically isolated datacenter

---

### **Q14. How does Azure handle high availability for storage?**

**Answer:**

* LRS
* ZRS
* GRS
* RA-GRS

---

### **Q15. Which replication is best for analytics?**

**Answer:**
**ZRS** – balances cost and availability.

---

### **Q16. What is Azure Landing Zone?**

**Answer:**
Standardized cloud foundation with:

* Networking
* Security
* Governance

---

### **Q17. Why separate resource groups for data layers?**

**Answer:**

* Cost tracking
* Access control
* Isolation

---

### **Q18. What is Azure Policy?**

**Answer:**
Enforces rules (e.g., deny public storage).

---

### **Q19. How do you isolate DEV, QA, PROD?**

**Answer:**

* Separate subscriptions
* Separate VNETs
* Separate service principals

---

### **Q20. What is Zero Trust in Azure?**

**Answer:**
Never trust, always verify – identity-based access.

---

## SECTION 2: Cost Management & Optimization (Q21–Q60)

---

### **Q21. What are major cost drivers in Azure data platforms?**

**Answer:**

* Databricks compute
* Synapse DWUs
* Data Factory activities
* Storage I/O
* Power BI capacity

---

### **Q22. How do you reduce Databricks cost?**

**Answer:**

* Auto-termination
* Job clusters
* Spot instances
* Right-sizing clusters

👉 *Example:* Job cluster auto-deletes after run.

---

### **Q23. Difference between Job Cluster and All-Purpose Cluster?**

**Answer:**

* Job Cluster → Cheaper, ephemeral
* All-Purpose → Interactive, expensive

---

### **Q24. What is cluster auto-scaling?**

**Answer:**
Automatically adjusts workers based on workload.

---

### **Q25. What is cluster auto-termination?**

**Answer:**
Stops idle clusters after inactivity.

---

### **Q26. How does ADLS pricing work?**

**Answer:**

* Storage volume
* Transactions
* Data retrieval

---

### **Q27. How to optimize ADLS cost?**

**Answer:**

* Lifecycle policies
* Compression (Parquet)
* Partitioning

---

### **Q28. What are lifecycle policies?**

**Answer:**
Automatically move data to cool/archive tiers.

---

### **Q29. Difference between Hot, Cool, Archive tiers?**

**Answer:**

| Tier    | Cost   | Access     |
| ------- | ------ | ---------- |
| Hot     | High   | Frequent   |
| Cool    | Medium | Occasional |
| Archive | Low    | Rare       |

---

### **Q30. How do you reduce ADF pipeline cost?**

**Answer:**

* Avoid unnecessary activities
* Use bulk copy
* Minimize retries

---

### **Q31. Which ADF activity is most expensive?**

**Answer:**

* Data Flow
* Lookup on large datasets

---

### **Q32. How does ADF pricing work?**

**Answer:**

* Activity runs
* Data movement
* Data flow compute

---

### **Q33. When should you avoid ADF Data Flow?**

**Answer:**
For large transformations → Use Databricks.

---

### **Q34. How do you monitor Azure cost?**

**Answer:**

* Cost Management + Billing
* Budgets
* Alerts

---

### **Q35. What are Azure Budgets?**

**Answer:**
Alerts when spending crosses threshold.

---

### **Q36. How do you tag resources for cost tracking?**

**Answer:**
Tags like:

* Environment
* Project
* Owner

---

### **Q37. What is Reserved Instance (RI)?**

**Answer:**
Prepay compute → 40–70% cost savings.

---

### **Q38. Is RI applicable for Databricks?**

**Answer:**
Yes (VM level).

---

### **Q39. What is Spot Instance?**

**Answer:**
Unused Azure capacity at lower price (can be evicted).

---

### **Q40. When should Spot instances be used?**

**Answer:**

* Batch jobs
* Non-critical workloads

---

### **Q41. How do you optimize Synapse cost?**

**Answer:**

* Pause DW when idle
* Scale down DWUs
* Use serverless SQL

---

### **Q42. Difference between Serverless and Dedicated SQL pool?**

**Answer:**

* Serverless → Pay per query
* Dedicated → Pay per hour

---

### **Q43. Which is cheaper for ad-hoc queries?**

**Answer:**
Serverless SQL pool.

---

### **Q44. How do you reduce Power BI cost?**

**Answer:**

* Use Pro licenses smartly
* Pause Premium capacity
* Reduce refresh frequency

---

### **Q45. What is capacity throttling in Power BI?**

**Answer:**
Performance degradation when capacity is overloaded.

---

### **Q46. How do you optimize data refresh cost?**

**Answer:**

* Incremental refresh
* Partitioning

---

### **Q47. How does data format impact cost?**

**Answer:**
Parquet reduces:

* Storage
* Compute
* Scan cost

---

### **Q48. Why avoid small files?**

**Answer:**
Small files increase:

* Metadata overhead
* Compute cost

---

### **Q49. What is file compaction?**

**Answer:**
Merging small files into larger ones.

---

### **Q50. How does partitioning reduce cost?**

**Answer:**
Scans only required data.

---

### **Q51. What is FinOps?**

**Answer:**
Cloud cost governance practice.

---

### **Q52. What FinOps metrics matter?**

**Answer:**

* Cost per pipeline
* Cost per domain
* Compute utilization

---

### **Q53. How do you estimate Azure cost before deployment?**

**Answer:**
Azure Pricing Calculator.

---

### **Q54. What is chargeback vs showback?**

**Answer:**

* Chargeback → Teams pay
* Showback → Visibility only

---

### **Q55. How do you optimize network cost?**

**Answer:**

* Avoid cross-region traffic
* Use Private Endpoints

---

### **Q56. What causes unexpected Azure cost spikes?**

**Answer:**

* Infinite loops
* Unbounded data scans
* Forgotten clusters

---

### **Q57. How do you prevent accidental cost explosion?**

**Answer:**

* Budgets
* Policies
* Auto-termination

---

### **Q58. How do you manage cost in multi-tenant platforms?**

**Answer:**

* Workload isolation
* Resource quotas
* Tagging

---

### **Q59. How do you optimize streaming cost?**

**Answer:**

* Batch micro-batches
* Tune trigger intervals

---

### **Q60. What is cost vs performance trade-off?**

**Answer:**
Balance SLA needs with infrastructure size.

---

## SECTION 3: Real-World Scenario & Architecture Questions (Q61–Q120)

---

### **Q61. How would you design a cost-optimized Azure Lakehouse?**

**Answer:**

* ADLS Gen2
* Databricks job clusters
* Delta Lake
* Lifecycle policies

---

### **Q62. How do you handle cost in 24×7 pipelines?**

**Answer:**

* Serverless
* Autoscaling
* Pause unused resources

---

### **Q63. How do you manage infrastructure for global teams?**

**Answer:**

* Multi-region deployment
* Read replicas
* Cost-aware routing

---

### **Q64. How do you reduce ETL compute time?**

**Answer:**

* Parallelism
* Predicate pushdown
* Partition pruning

---

### **Q65. How do you design DR with cost control?**

**Answer:**

* Warm standby
* Selective replication

---

### **Q66. How do you balance security vs cost?**

**Answer:**
Private endpoints where required, not everywhere.

---

### **Q67. How do you optimize schema evolution cost?**

**Answer:**
Use Delta auto-merge selectively.

---

### **Q68. How do you optimize merge operations?**

**Answer:**

* Z-Order
* Partition pruning

---

### **Q69. How do you handle cost spikes from ad-hoc users?**

**Answer:**

* Query limits
* Dedicated workspaces

---

### **Q70. How do you size Databricks clusters?**

**Answer:**
Based on:

* Data volume
* SLA
* Shuffle size

---

### **Q71. What happens if clusters are oversized?**

**Answer:**
Wasted cost.

---

### **Q72. What happens if clusters are undersized?**

**Answer:**
Longer runtimes → higher cost.

---

### **Q73. How do you reduce storage scan cost?**

**Answer:**

* Partitioning
* File pruning

---

### **Q74. How do you manage cost in CI/CD?**

**Answer:**

* Ephemeral environments
* Automated teardown

---

### **Q75. How do you monitor pipeline cost per run?**

**Answer:**
Azure Monitor + custom logging.

---

### **Q76. How do you explain cost optimization to business?**

**Answer:**
Translate cost into **per report / per insight**.

---

### **Q77. How do you avoid vendor lock-in cost?**

**Answer:**
Open formats (Parquet, Delta).

---

### **Q78. How do you control shadow IT cost?**

**Answer:**
Policies + RBAC.

---

### **Q79. How do you manage cost in streaming ingestion?**

**Answer:**
Auto-scale streaming clusters.

---

### **Q80. How do you handle unpredictable workloads?**

**Answer:**
Serverless + autoscaling.

---

### **Q81. How do you estimate cost for a new project?**

**Answer:**
POC → Measure → Project.

---

### **Q82. How do you justify Databricks cost?**

**Answer:**
Reduced processing time & better SLA.

---

### **Q83. How do you reduce cost without impacting SLA?**

**Answer:**
Off-peak scheduling.

---

### **Q84. How do you design cost-efficient archival?**

**Answer:**
Move cold data to archive tier.

---

### **Q85. How do you optimize cross-team data usage cost?**

**Answer:**
Shared curated layers.

---

### **Q86. How do you manage cost in Data Mesh?**

**Answer:**
Domain-level budgets.

---

### **Q87. How do you prevent cost abuse?**

**Answer:**
Quota + monitoring.

---

### **Q88. How do you optimize SQL query cost?**

**Answer:**
Avoid SELECT *.

---

### **Q89. How do you manage cost during peak season?**

**Answer:**
Temporary scale-up.

---

### **Q90. How do you design for elastic cost?**

**Answer:**
Scale up/down dynamically.

---

### **Q91. How do you reduce retry cost in ADF?**

**Answer:**
Better error handling.

---

### **Q92. How do you manage cost in Power BI refresh?**

**Answer:**
Incremental refresh.

---

### **Q93. How do you monitor unused resources?**

**Answer:**
Azure Advisor.

---

### **Q94. How do you optimize ingestion cost?**

**Answer:**
Batch ingestion.

---

### **Q95. How do you handle cost reporting?**

**Answer:**
Monthly dashboards.

---

### **Q96. How do you optimize network egress cost?**

**Answer:**
Same-region services.

---

### **Q97. How do you reduce transformation cost?**

**Answer:**
Push logic to storage.

---

### **Q98. How do you optimize job scheduling?**

**Answer:**
Consolidate jobs.

---

### **Q99. How do you avoid over-provisioning?**

**Answer:**
Continuous monitoring.

---

### **Q100. How do you prepare cost discussion for leadership?**

**Answer:**
Business impact metrics.

---
