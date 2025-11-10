# Azure DataBricks System Design
---

## 🚀 **System Design Interview: Handling 500GB Daily with PySpark**

## 🎯 **Scenario**

You are tasked with designing and optimizing a **PySpark-based data pipeline** that processes **500 GB of data per day**.
Your goal: build a **scalable, cost-efficient, and high-performance architecture** — and explain **how to size the cluster**.

---

## 🧱 **1. High-Level Architecture**

```
                ┌────────────────────┐
                │  Data Sources       │
                │ (CSV / JSON / APIs) │
                └────────┬────────────┘
                         │
                         ▼
                ┌──────────────────────────────┐
                │  Raw Zone (ADLS / S3)        │
                │  - Landing 500 GB daily      │
                └────────┬─────────────────────┘
                         │
                         ▼
                ┌──────────────────────────────┐
                │  Processing Layer (PySpark)   │
                │  - Cleansing / Joins / ETL    │
                │  - Incremental Processing     │
                └────────┬─────────────────────┘
                         │
                         ▼
                ┌──────────────────────────────┐
                │  Storage Layer (Delta Lake)  │
                │  - Optimized for Analytics    │
                └────────┬─────────────────────┘
                         │
                         ▼
                ┌──────────────────────────────┐
                │ Serving Layer (Power BI, SQL) │
                │  - Dashboards & Reports       │
                └──────────────────────────────┘
```

---

## ⚙️ **2. The 5-Step Optimization Blueprint**

### **Step 1️⃣ – Format Optimization**

**Action:** Convert raw data (CSV/JSON) → **Parquet or Delta Lake** format immediately.
**Why:**

* Columnar compression
* Predicate pushdown
* Reduced I/O

✅ **Boosts performance by 3–5×**

---

### **Step 2️⃣ – Partitioning Strategy**

Each Spark task ≈ **128 MB** of data.

**Calculation:**

```
500 GB × 1024 MB ÷ 128 MB = 4000 partitions
```

➡️ Spark now executes **~4000 parallel tasks**, ensuring balanced processing.

📊 **Partitioning Recommendation:**

* Partition by `ingestion_date`, `region`, or `business_key` for incremental loading.

---

### **Step 3️⃣ – Cluster Sizing**

**Assumptions:**

* 10 worker nodes
* 8 cores & 32 GB RAM per node

**Parallelism Calculation:**

```
10 nodes × 8 cores = 80 cores
Each core handles 2–3 tasks  → ~240 tasks concurrently
```

**Execution Time Estimate:**

```
4000 ÷ 240 ≈ 17 waves of execution
1–2 minutes per wave → ~25–30 minutes total runtime
```

✅ **Balanced trade-off** between cost and performance.

---

### **Step 4️⃣ – Memory Management**

Spark needs ~**3× data volume** during joins and shuffles.

**Memory Requirement:**

```
(500 GB × 3) ÷ 10 nodes = 150 GB per node
```

With **32 GB per node**, some disk spill is expected (acceptable with SSD).
For heavy joins → use **64 GB nodes**.

💡 **Best Practices:**

* Use broadcast joins for small lookup tables
* Persist only reusable dataframes
* Optimize shuffle partitions

---

### **Step 5️⃣ – Performance Tuning**

| Setting                             | Recommended Value | Purpose                             |
| ----------------------------------- | ----------------- | ----------------------------------- |
| `spark.sql.shuffle.partitions`      | `400`             | Reduces shuffle overhead            |
| `spark.sql.adaptive.enabled`        | `true`            | Enables adaptive query optimization |
| `spark.sql.files.maxPartitionBytes` | `128MB`           | Controls input split size           |

✅ **Additional Tips:**

* Implement **Incremental Loads** using Delta MERGE
* Avoid full reloads
* Compact small files (`OPTIMIZE` + Z-ORDER in Databricks)

---

## 💾 **3. Cost vs. Performance Balance**

| Parameter       | Trade-Off          | Example Decision                         |
| --------------- | ------------------ | ---------------------------------------- |
| Cluster Size    | Cost ↑, Speed ↑    | Choose 10 nodes, scale up only if needed |
| File Format     | Speed ↑, Storage ↓ | Use Delta/Parquet over CSV               |
| Partition Count | More parallelism   | Target 128 MB per partition              |
| Memory          | Avoid spill        | Consider SSDs or larger memory nodes     |

---

## 🧠 **4. Key Takeaways**

* Optimize **format, partitioning, and configuration** before scaling up compute.
* Measure and adjust **task size (128 MB)** and **shuffle partitions (400)**.
* Implement **incremental and adaptive** processing strategies.

---

## 🧭 **5. Final Interview Summary**

> “To process 500 GB daily in PySpark efficiently,
> I’d architect a **Delta Lake-based pipeline** with **optimized partitions, adaptive execution, and right-sized clusters.**
> Performance is not just about adding nodes — it’s about designing smart, efficient systems.”

---

Would you like me to include a **Databricks-specific version** of this (showing cluster configuration + adaptive execution diagram) so you can use it as a visual reference in interviews or presentations?
