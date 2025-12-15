# **End-to-end Microsoft Fabric data flow architecture**

---

## 🔷 Microsoft Fabric – End-to-End Data Flow Architecture

```mermaid
flowchart LR
    %% =========================
    %% Data Sources
    %% =========================
    subgraph SOURCES["Data Sources"]
        A1[OLTP Databases<br/>SQL Server / Oracle]
        A2[SaaS Applications<br/>SAP / Salesforce]
        A3[Files<br/>CSV / JSON / Parquet]
        A4[Streaming Sources<br/>Event Hub / IoT]
        A5[REST APIs]
    end

    %% =========================
    %% Ingestion Layer
    %% =========================
    subgraph INGEST["Fabric Data Factory<br/>Ingestion & Orchestration"]
        B1[Batch Pipelines<br/>Copy Activity]
        B2[Incremental Load<br/>Watermark / CDC]
        B3[Streaming Ingestion]
        B4[Metadata-Driven Framework]
    end

    %% =========================
    %% OneLake Storage
    %% =========================
    subgraph ONELAKE["OneLake (Unified Storage)"]
        C1[Bronze Layer<br/>Raw Delta Tables]
        C2[Silver Layer<br/>Clean & Conformed Delta]
        C3[Gold Layer<br/>Curated & Aggregated Delta]
    end

    %% =========================
    %% Processing Layer
    %% =========================
    subgraph PROCESS["Fabric Compute Engines"]
        D1[Spark Notebooks<br/>PySpark / Spark SQL]
        D2[Lakehouse SQL Endpoint]
        D3[Fabric Data Warehouse]
    end

    %% =========================
    %% Semantic & BI Layer
    %% =========================
    subgraph SEMANTIC["Semantic & Analytics Layer"]
        E1[Semantic Models<br/>Measures / KPIs]
        E2[Direct Lake Mode]
    end

    %% =========================
    %% Consumption Layer
    %% =========================
    subgraph CONSUME["Consumption"]
        F1[Power BI Dashboards]
        F2[Ad-hoc SQL Analytics]
        F3[Data Science / ML]
        F4[External Apps / APIs]
    end

    %% =========================
    %% Governance & Security
    %% =========================
    subgraph GOVERN["Governance & Security"]
        G1[Microsoft Purview<br/>Lineage & Catalog]
        G2[RBAC / RLS / CLS]
        G3[Sensitivity Labels]
        G4[Monitoring & Cost Management]
    end

    %% =========================
    %% Data Flow
    %% =========================
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B3
    A5 --> B1

    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1

    C1 --> D1
    D1 --> C2
    C2 --> D1
    D1 --> C3

    C3 --> D2
    C3 --> D3

    D2 --> E1
    D3 --> E1

    E1 --> E2
    E2 --> F1
    E1 --> F2
    E1 --> F3
    E1 --> F4

    %% =========================
    %% Governance Links
    %% =========================
    C1 -.-> G1
    C2 -.-> G1
    C3 -.-> G1
    E1 -.-> G2
    E1 -.-> G3
    PROCESS -.-> G4
```

---

## 🧠 How to Explain This in an Interview (30 Seconds)

> “Data is ingested from multiple sources using **Fabric Data Factory** into **OneLake Bronze Delta tables**.
> We transform and clean data using **Spark notebooks** into **Silver**, apply business logic and aggregations in **Gold**, expose it through **semantic models** using **Direct Lake**, and finally consume it in **Power BI and analytics workloads**, all governed centrally via **Microsoft Purview and Fabric security**.”

---

## ✅ Why This Architecture Is Production-Ready

✔ Fully SaaS
✔ No data duplication
✔ Delta-based Lakehouse
✔ BI + AI ready
✔ Central governance
✔ Cost-optimized (Direct Lake)

---


---

# ✅ 1️⃣ Microsoft Fabric – Cost Optimization Checklist (Production-Ready)

### 🔹 Capacity & Billing

* ⬜ Choose **lowest possible F-SKU** initially (scale later)
* ⬜ Separate **Dev / Test / Prod capacities**
* ⬜ Pause Dev/Test capacities outside working hours
* ⬜ Avoid running ad-hoc workloads on Prod capacity
* ⬜ Monitor **Capacity Metrics App** weekly

---

### 🔹 Data Ingestion

* ⬜ Prefer **incremental loads (CDC / watermark)**
* ⬜ Avoid full reloads unless required
* ⬜ Batch ingestion instead of frequent micro-batches
* ⬜ Parameterize pipelines (metadata-driven)

---

### 🔹 Lakehouse & Delta Tables

* ⬜ Use **Bronze / Silver / Gold** layers
* ⬜ Append-only in Bronze
* ⬜ MERGE only in Silver (not Bronze)
* ⬜ Partition by **date / business key**
* ⬜ Avoid overusing `OPTIMIZE` (schedule weekly/monthly)

---

### 🔹 Spark Optimization

* ⬜ Avoid full table scans
* ⬜ Use predicate pushdown
* ⬜ Broadcast small dimension tables
* ⬜ Avoid `.collect()` and `.toPandas()`
* ⬜ Schedule notebooks (no always-on)

---

### 🔹 Power BI & Analytics

* ⬜ Prefer **Direct Lake**
* ⬜ Avoid Import mode unless necessary
* ⬜ Reduce refresh frequency
* ⬜ Pre-aggregate data in Gold layer
* ⬜ Reuse semantic models

---

### 🔹 Governance & Control

* ⬜ Assign workspaces to correct capacity
* ⬜ Apply RLS/CLS at semantic layer (not Spark)
* ⬜ Limit ad-hoc SQL access on Gold tables
* ⬜ Use Purview lineage to track misuse

---

# ✅ 2️⃣ Fabric SKUs vs Workloads (Mapping Table)

| Fabric SKU | Best For         | Typical Workloads                  | Notes              |
| ---------- | ---------------- | ---------------------------------- | ------------------ |
| **F2**     | POC / Learning   | Small ingestion, light BI          | Not for production |
| **F4**     | Dev / Test       | Limited pipelines, small Lakehouse | Pause when idle    |
| **F8**     | Department BI    | Daily ingestion, dashboards        | Most common        |
| **F16**    | Enterprise BI    | Large datasets, concurrency        | Balanced choice    |
| **F32**    | Heavy Analytics  | Streaming + BI + ML                | Costly if misused  |
| **F64+**   | Large Enterprise | High concurrency, real-time        | Needs governance   |

📌 **Rule**:

> “Scale capacity only when concurrency increases, not data size alone.”

---

# ✅ 3️⃣ Interview Scenario-Based Questions (Cost Focused)

### Q1. Your Fabric cost suddenly doubled. How do you investigate?

**Answer:**

1. Check Capacity Metrics App
2. Identify workload spikes (Spark / BI / SQL)
3. Look for full refresh or bad joins
4. Validate Direct Lake vs Import
5. Scale down or isolate workloads

---

### Q2. Why is Spark the most expensive Fabric workload?

**Answer:**
Because Spark consumes **distributed compute**, causes **shuffle**, and runs **long-lived executors** if not optimized.

---

### Q3. How do you reduce Power BI cost in Fabric?

**Answer:**

* Use Direct Lake
* Reduce refresh frequency
* Pre-aggregate in Gold
* Share semantic models

---

### Q4. Fabric vs Synapse — which is cheaper?

**Answer:**
Fabric is cheaper for **mixed workloads (ETL + BI)** due to **shared capacity** and **no duplicate storage**.

---

### Q5. When would you NOT recommend Fabric?

**Answer:**

* Very heavy ML training
* Advanced Spark tuning needed
* Multi-cloud requirement

---

# ✅ 4️⃣ Fabric vs Databricks – Decision Matrix

| Dimension           | Microsoft Fabric          | Azure Databricks       |
| ------------------- | ------------------------- | ---------------------- |
| Pricing Model       | Capacity-based            | DBU + VM               |
| Cost Predictability | High                      | Medium                 |
| BI Integration      | Native Power BI           | External               |
| Storage             | OneLake (single copy)     | ADLS                   |
| Governance          | Built-in                  | Manual setup           |
| Spark Control       | Limited                   | Full control           |
| ML Workloads        | Medium                    | Advanced               |
| Best For            | Enterprise BI + Analytics | Heavy Data Engineering |

🎯 **Decision Rule**

* **BI + Analytics + Cost control → Fabric**
* **Advanced Spark / ML → Databricks**

---

# ✅ 5️⃣ Cost-Optimized Microsoft Fabric Reference Architecture (MD Code)

```mermaid
flowchart LR
    subgraph SOURCES["Data Sources"]
        S1[OLTP Databases]
        S2[SaaS Apps]
        S3[Files / APIs]
        S4[Streaming]
    end

    subgraph INGEST["Fabric Data Factory"]
        I1[Batch Ingestion]
        I2[Incremental / CDC]
    end

    subgraph ONELAKE["OneLake Storage"]
        BZ[Bronze<br/>Raw Delta]
        SV[Silver<br/>Clean Delta]
        GD[Gold<br/>Aggregated Delta]
    end

    subgraph COMPUTE["Compute"]
        SP[Spark Notebooks<br/>Scheduled]
        WH[Fabric Warehouse]
    end

    subgraph SEMANTIC["Semantic Layer"]
        SM[Semantic Models]
        DL[Direct Lake]
    end

    subgraph CONSUME["Consumption"]
        BI[Power BI]
        DS[Data Science]
        APP[Apps / APIs]
    end

    subgraph GOVERN["Governance"]
        PV[Purview]
        SEC[RBAC / RLS]
        COST[Capacity Monitoring]
    end

    S1 --> I1
    S2 --> I1
    S3 --> I1
    S4 --> I2

    I1 --> BZ
    I2 --> BZ

    BZ --> SP --> SV --> SP --> GD

    GD --> WH
    GD --> SM --> DL --> BI
    SM --> DS
    SM --> APP

    BZ -.-> PV
    SV -.-> PV
    GD -.-> PV
    SM -.-> SEC
    COMPUTE -.-> COST
```

---

# 🎯 Final Interview One-Liner (Memorize This)

> “Fabric reduces cost by using a **shared capacity model**, **single-copy OneLake storage**, and **Direct Lake analytics**, eliminating duplicated compute and storage seen in traditional Azure analytics stacks.”

---


