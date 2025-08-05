
# Azure Data Factory (ADF) Data Flows Activity


In **Azure Data Factory (ADF)**, **Data Flows** are powerful **ETL (Extract, Transform, Load)** tools that allow you to design **data transformation logic visually**, without writing code. These are **executed using Azure Spark clusters**, making them suitable for big data transformations.

---

## 🔷 What is a Data Flow in ADF?

> A **Data Flow Activity** in a pipeline executes a **Mapping Data Flow**, which consists of transformation steps like join, filter, derive, aggregate, etc.

---

## 🔹 **Key Components of Data Flow Activity**

| Component          | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| **Source**         | Defines input dataset.                                               |
| **Transformation** | Series of steps (e.g., filter, join, derive, pivot) applied to data. |
| **Sink**           | Destination dataset (e.g., Blob, SQL, Data Lake, etc.).              |
| **Settings**       | Cluster config, partitioning, debugging options.                     |

---

## 🔷 All Important **Data Flow Transformations** with Functionality & Use Case

### 🔹 1. **Source**

* **Functionality:** Ingest data from Blob, SQL, ADLS, REST, etc.
* **Use Case:** Load daily sales data CSV file from Azure Blob.

---

### 🔹 2. **Filter**

* **Functionality:** Filter rows based on condition.
* **Use Case:** Remove rows with `Status = 'Cancelled'` or `Null` entries.

---

### 🔹 3. **Select**

* **Functionality:** Select, rename, reorder columns.
* **Use Case:** Choose only `CustomerID`, `Amount`, `Date` columns for reporting.

---

### 🔹 4. **Derived Column**

* **Functionality:** Add/modify columns using expressions.
* **Use Case:** Create a new column `Profit = Revenue - Cost`.

---

### 🔹 5. **Conditional Split**

* **Functionality:** Branch rows based on condition.
* **Use Case:** Route `HighValue > 10000` orders to a separate path for audit.

---

### 🔹 6. **Aggregate**

* **Functionality:** Perform group by + aggregations.
* **Use Case:** Calculate total sales by region and product category.

---

### 🔹 7. **Join**

* **Functionality:** Join two datasets (inner, left, outer, etc.).
* **Use Case:** Join `Customer` and `Transaction` tables on `CustomerID`.

---

### 🔹 8. **Union**

* **Functionality:** Merge rows from two datasets (same schema).
* **Use Case:** Combine sales data from multiple regional files.

---

### 🔹 9. **Lookup**

* **Functionality:** Retrieve additional values from a secondary dataset.
* **Use Case:** Lookup `Customer Segment` from master table using `CustomerID`.

---

### 🔹 10. **Sort**

* **Functionality:** Sort data by one or more fields.
* **Use Case:** Sort top 10 customers by revenue for dashboard export.

---

### 🔹 11. **Surrogate Key**

* **Functionality:** Add a new sequential key column.
* **Use Case:** Add a `SurrogateKey` to dimension tables in a data warehouse.

---

### 🔹 12. **Exists / Exists Transformation**

* **Functionality:** Check if record exists in a second dataset.
* **Use Case:** Filter out already processed records (e.g., archive checking).

---

### 🔹 13. **Pivot**

* **Functionality:** Convert rows to columns.
* **Use Case:** Convert monthly sales rows into column-based view by month.

---

### 🔹 14. **Unpivot**

* **Functionality:** Convert columns to rows.
* **Use Case:** Normalize wide Excel files into tall format for database insertion.

---

### 🔹 15. **Flatten**

* **Functionality:** Flatten nested JSON arrays into tabular form.
* **Use Case:** Extract order line items from nested order JSON object.

---

### 🔹 16. **Window**

* **Functionality:** Create ranking, lag, lead, row\_number, etc.
* **Use Case:** Assign rank to customers based on monthly spending.

---

### 🔹 17. **Sink**

* **Functionality:** Writes the output to destination (SQL, Blob, ADLS, etc.)
* **Use Case:** Store cleaned and aggregated sales data to Azure SQL DB.

---

## ✅ Scenario-Based Real-World Use Case: Customer Purchase Processing

### **Objective:** Load raw JSON from Blob, clean, transform, and load to Azure SQL.

#### **Flow:**

1. **Source:** Load raw customer purchase JSON.
2. **Flatten:** Flatten nested product list.
3. **Filter:** Remove records with null customer ID.
4. **Join:** Join with product master to get product name.
5. **Derived Column:** Calculate `TotalPrice = Qty * UnitPrice`.
6. **Aggregate:** Sum by `CustomerID` and `Month`.
7. **Window:** Rank customers by monthly spend.
8. **Sink:** Write to SQL Server table `MonthlyCustomerSpend`.

---
