# **Azure Data Factory (ADF) optimization–related interview questions**.

### 1. **How do you optimize data movement in ADF?**

**Answer:**

* Use **PolyBase** or **COPY command** for loading data into Azure Synapse/SQL DW (faster than traditional methods).
* Enable **staging** when copying data between cloud sources (ADF can use Azure Blob or ADLS as staging).
* Choose the right **integration runtime (IR)**:

  * **Azure IR** for cloud-to-cloud.
  * **Self-hosted IR** for on-prem.
* Optimize **batch size, parallelism, and partitioning** for large datasets.

---

### 2. **What are Data Flow optimizations in ADF?**

**Answer:**

* **Optimize data skew**: Use *hash partitioning* or *round-robin* instead of single key if skew exists.
* **Reduce data shuffles** by minimizing unnecessary joins/sorts.
* Use **broadcast join** when one dataset is small enough to fit in memory.
* Enable **debug mode with sampling** for faster testing.
* Adjust **compute size** (General, Memory Optimized, Compute Optimized) and **number of cores**.

---

### 3. **What is partitioning and why is it important in ADF?**

**Answer:**

* Partitioning means **splitting large datasets into smaller chunks** for parallel processing.
* Improves performance by using **parallel copy**.
* Example: When copying from SQL Server → Blob Storage, set **partition column** (like `OrderDate`) to copy different ranges simultaneously.
* Prevents bottlenecks and speeds up ETL pipelines.

---

### 4. **How do you handle performance issues in ADF pipelines?**

**Answer:**

* Check **integration runtime performance** (scale out if needed).
* Review **Data Flow execution details** in monitoring to find bottlenecks.
* Optimize **sink/source queries** (push down filters, avoid `SELECT *`).
* Use **staging** to offload transformation to the target system.
* Tune **degree of parallelism** in copy activity.

---

### 5. **What is the role of integration runtime (IR) in performance?**

**Answer:**

* IR is the compute used for data movement & transformation.
* **Azure IR**: Best for cloud-to-cloud movement, auto-scalable.
* **Self-hosted IR**: Used for on-prem connectivity.
* Performance tuning:

  * Scale up IR nodes.
  * Enable **parallel copies**.
  * Use **data partitioning** for large datasets.

---

### 6. **How do you optimize cost and performance together in ADF?**

**Answer:**

* Use **mapping data flows** only when needed (costly).
* For simple transformations, use **SQL pushdown** instead.
* **Auto-terminate** compute resources when not in use.
* **Schedule pipelines** at off-peak hours to reduce contention.
* Monitor **pipeline run costs** in ADF monitoring + Azure Monitor.

---

### 7. **How would you speed up copy activity in ADF?**

**Answer:**

* Enable **parallelism** (via partitioning).
* Use **PolyBase** or **Bulk Insert** for SQL DW/Synapse.
* Enable **compression** when moving large files.
* Choose **binary copy** for non-structured data.
* Optimize **batch size** in the copy activity.

---

### 8. **What are some common bottlenecks in ADF pipelines?**

**Answer:**

* Slow **source system** (e.g., SQL without indexes).
* Inefficient **sink** (small DW performance tier).
* Large **data skew** in Data Flows.
* Insufficient **IR compute resources**.
* Overuse of **mapping data flows** for simple transformations.

---

### 9. **When would you choose Mapping Data Flows vs. Databricks for transformations?**

**Answer:**

* **Mapping Data Flows**:

  * Low-code, easy to maintain, for medium complexity transformations.
  * Optimized automatically by ADF, good for simple aggregations/joins.
* **Databricks**:

  * Complex transformations, advanced ML, schema evolution, very large-scale data.
  * More expensive but flexible and powerful.

---

### 10. **How do you monitor and troubleshoot performance in ADF?**

**Answer:**

* Use **ADF Monitor** to check pipeline run details.
* Drill down into **activity run duration** to find slow steps.
* Enable **integration runtime metrics**.
* Log pipeline execution to **Log Analytics**.
* Use **retry policies** to handle transient errors instead of re-running entire pipeline.

---
