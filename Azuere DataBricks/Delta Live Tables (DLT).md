# Delta Live Tables (DLT).


---

## 🔹 1. What is Delta Live Tables (DLT) in Databricks?

**Answer:**
**Delta Live Tables (DLT)** is a **framework for building reliable, maintainable, and declarative data pipelines** in Databricks using **Python or SQL**.
It automates **ETL orchestration**, **data quality checks**, **error handling**, and **data lineage tracking** — all within a Delta Lake environment.

**Key points:**

* Built on top of **Delta Lake**.
* Automatically manages **data dependencies**, **schema evolution**, and **fault recovery**.
* Supports both **batch and streaming** data.
* Defines pipelines using **declarative syntax**, not imperative (you specify *what* to do, not *how*).

**Example (Python DLT pipeline):**

```python
import dlt
from pyspark.sql.functions import *

@dlt.table
def bronze_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/orders")
    )

@dlt.table
def silver_orders():
    return (
        dlt.read("bronze_orders")
        .filter(col("status").isNotNull())
        .withColumn("order_date", to_date("timestamp"))
    )
```

---

## 🔹 2. How does DLT differ from traditional ETL pipelines?

| Aspect               | Traditional ETL                | Delta Live Tables                        |
| -------------------- | ------------------------------ | ---------------------------------------- |
| **Definition style** | Imperative (step-by-step code) | Declarative (`@dlt.table` defines logic) |
| **Orchestration**    | Manual (ADF/Airflow)           | Automatic dependency resolution          |
| **Data quality**     | Custom logic                   | Built-in “Expectations”                  |
| **Lineage**          | Needs manual tracking          | Auto lineage in UI                       |
| **Schema changes**   | Manual handling                | Auto schema evolution                    |
| **Failure recovery** | Manual re-run                  | Managed checkpoints & retries            |

---

## 🔹 3. What are the main components of a DLT pipeline?

1. **Pipeline Definition File** – Python or SQL file containing DLT logic.
2. **Tables & Views** – Defined using `@dlt.table` and `@dlt.view`.
3. **Expectations** – Built-in data quality checks.
4. **Pipeline Configuration** – Cluster settings, target path, libraries, etc.
5. **Event Log** – Stores operational & audit events.
6. **Target Storage** – Delta tables stored in managed/external locations.

---

## 🔹 4. Explain the difference between `@dlt.table` and `@dlt.view`.

| Feature             | `@dlt.table`                   | `@dlt.view`                            |
| ------------------- | ------------------------------ | -------------------------------------- |
| **Materialization** | Data is stored in Delta format | Logical view (not persisted)           |
| **Use case**        | When you want durable output   | When you want intermediate computation |
| **Performance**     | Slower but durable             | Faster, used for transformations       |

**Example:**

```python
@dlt.view
def raw_orders():
    return spark.read.json("/mnt/raw/orders")

@dlt.table
def cleaned_orders():
    return dlt.read("raw_orders").filter("status IS NOT NULL")
```

---

## 🔹 5. What are “expectations” in DLT, and how are they used?

**Expectations** are **data quality rules** defined directly in DLT pipelines.
They validate incoming data and can either **drop**, **quarantine**, or **fail** records that don’t meet conditions.

**Example:**

```python
@dlt.table
@dlt.expect("valid_price", "price > 0")
@dlt.expect_or_drop("valid_date", "order_date IS NOT NULL")
def validated_orders():
    return dlt.read("bronze_orders")
```

---

## 🔹 6. What are the different pipeline modes supported in DLT?

1. **Triggered (Batch)** – Runs manually or on schedule.
2. **Continuous (Streaming)** – Runs continuously for real-time data ingestion.

---

## 🔹 7. How does DLT handle dependencies between tables?

DLT automatically determines the **execution order** based on **references** between tables.

**Example:**

```python
@dlt.table
def silver_orders():
    return dlt.read("bronze_orders").filter("status = 'completed'")
```

Here, `silver_orders` **depends** on `bronze_orders`, so DLT executes the bronze layer first.

---

## 🔹 8. What is the role of the event log in DLT pipelines?

The **DLT event log** records all pipeline events:

* Table creation
* Updates, errors, warnings
* Data quality metrics
* Schema changes

Stored as a **Delta table** (in `_event_log` folder), it can be queried:

```sql
SELECT * FROM delta.`/pipelines/my_pipeline/system/events`
```

---

## 🔹 9. How do you monitor and debug a DLT pipeline in Databricks?

* Use the **DLT UI** (under *Workflows → Delta Live Tables*).
* Monitor:

  * Execution progress
  * Data quality metrics
  * Error messages
  * Event log
* You can query `_event_log` for deeper debugging.

---

## 🔹 10. Explain the difference between continuous and triggered pipelines.

| Mode           | Description                        | Use Case                 |
| -------------- | ---------------------------------- | ------------------------ |
| **Triggered**  | Executes once or on schedule       | Daily batch ETL          |
| **Continuous** | Keeps running, processing new data | Real-time streaming data |

---

## 🔹 11. What are the advantages of using DLT over standard notebooks?

✅ Less boilerplate ETL code
✅ Automatic orchestration
✅ Built-in error handling
✅ Automatic schema evolution
✅ Data quality enforcement
✅ UI-based monitoring and lineage

---

## 🔹 12. How does DLT manage schema changes automatically?

DLT supports **Automatic Schema Evolution**:

* If a new column is added, it updates schema without failure.
* Controlled by setting:

  ```python
  spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
  ```
* DLT also validates incompatible changes and flags them in the event log.

---

## 🔹 13. Can DLT process both batch and streaming data?

✅ **Yes.**
DLT seamlessly handles **streaming** (via Auto Loader) and **batch** data ingestion.
You can switch between them with minimal code changes.

**Example:**

```python
@dlt.table
def bronze_streaming():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/events")
    )
```

---

## 🔹 14. What are common data quality checks you can apply using DLT?

1. **Null checks** → `@dlt.expect("not_null", "id IS NOT NULL")`
2. **Range checks** → `@dlt.expect("valid_amount", "amount BETWEEN 0 AND 10000")`
3. **Uniqueness** → Use `dropDuplicates()` or expectation on key column.
4. **Data type validation** → Cast validation.
5. **Business rule validation** → e.g., `order_date <= current_date()`

---

## 🔹 15. How does DLT ensure data reliability and fault tolerance?

* Uses **Delta Lake ACID transactions**.
* **Checkpointing** ensures recovery after failures.
* **Automatic retries** for transient errors.
* **Idempotent writes** prevent duplicates.

---

## 🔹 16. What’s the difference between managed and external DLT tables?

| Type                  | Managed Table               | External Table                           |
| --------------------- | --------------------------- | ---------------------------------------- |
| **Storage control**   | Managed by Databricks       | You control the path                     |
| **Deletion behavior** | Dropping table deletes data | Dropping only removes metadata           |
| **Use case**          | Internal pipelines          | Integration with existing lakehouse data |

---

## 🔹 17. How do you configure storage and compute settings for a DLT pipeline?

In **DLT Pipeline UI**, specify:

* **Storage Location** → `/mnt/dlt_output`
* **Cluster Mode** → Continuous or Triggered
* **Compute** → Auto-scaling, cluster size, runtime
* **Libraries** → Attach custom Python/SQL dependencies

You can also configure via JSON:

```json
{
  "clusters": [{"num_workers": 2}],
  "storage": "/mnt/dlt_pipeline",
  "target": "delta_live_output"
}
```

---

## 🔹 18. What is the significance of the Bronze, Silver, and Gold layers in a DLT architecture?

| Layer      | Purpose                      | Example Transformation            |
| ---------- | ---------------------------- | --------------------------------- |
| **Bronze** | Raw ingestion (landing zone) | Load JSON/CSV using Auto Loader   |
| **Silver** | Cleaned & validated          | Apply schema, filter invalid rows |
| **Gold**   | Business-level aggregates    | KPI reports, dashboards           |

**Example DLT flow:**

```
Bronze → Silver → Gold
Raw data → Cleaned data → Analytics-ready data
```

---

## 🔹 19. How does DLT improve data lineage and auditability?

* DLT automatically captures **upstream/downstream dependencies**.
* **Lineage Graph** is visible in the UI.
* You can trace **data flow**, **schema evolution**, and **quality metrics** per table.

This simplifies **impact analysis** and **auditing**.

---

## 🔹 20. How can you integrate DLT with other Databricks features like Unity Catalog or Repos?

✅ **Unity Catalog Integration**

* DLT tables can be registered in Unity Catalog for governance.
* Use `target` in DLT config to point to a Unity Catalog schema:

  ```json
  "target": "main.analytics"
  ```

✅ **Repos Integration**

* Store your DLT Python/SQL files in Databricks Repos.
* Enables **version control**, **CI/CD**, and **collaboration**.

---