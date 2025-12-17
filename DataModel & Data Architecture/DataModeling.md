# **Data Modeling Interview Questions and Answers**


##  **1. What is Data Modeling, and Why is it Important in Data Engineering?**

**Answer:**
Data modeling is the process of designing the structure of data, including tables, fields, relationships, and constraints. It helps in organizing data efficiently for storage, retrieval, and analysis.

**Example:**
In an e-commerce business, data modeling helps structure the `Customers`, `Orders`, and `Products` tables in such a way that relationships are clearly defined, e.g., one customer can place multiple orders.

---

##  **2. Explain the Difference Between OLTP and OLAP Data Models.**

**Answer:**

| Feature    | OLTP                         | OLAP                          |
| ---------- | ---------------------------- | ----------------------------- |
| Purpose    | Transaction processing       | Analytical processing         |
| Schema     | Highly normalized            | Denormalized (Star/Snowflake) |
| Operations | Read & write (insert/update) | Read-heavy (aggregation)      |
| Example    | Banking system               | Sales dashboard               |

---

##  **3. What are the Different Types of Data Models?**

**Answer:**

* **Conceptual Model**: High-level, abstract; defines entities and relationships.
* **Logical Model**: Includes attributes, primary/foreign keys, normalized schema.
* **Physical Model**: Includes actual table structures, data types, indexes, partitions.

**Example:**
In a school system:

* Conceptual: `Student`, `Teacher`, `Course`
* Logical: Student(ID, Name, Age), Teacher(ID, Name), Course(ID, Title, TeacherID)
* Physical: Student table with VARCHAR and INT columns, indexes on ID.

---

##  **4. What is Normalization? Why is it Used?**

**Answer:**
Normalization organizes data to reduce redundancy and dependency by dividing tables into smaller tables and defining relationships.

**Example (1NF to 3NF):**
Unnormalized Table:

```
OrderID | CustomerName | Product1 | Product2
```

Normalized (3NF):

* Orders(OrderID, CustomerID)
* Customers(CustomerID, Name)
* OrderItems(OrderID, ProductID)

---

##  **5. When Would You Denormalize a Data Model?**

**Answer:**
Denormalization is done to improve query performance by reducing joins. Common in OLAP systems or read-heavy dashboards.

**Example:**
In a sales report, instead of joining `Order`, `Customer`, and `Product` tables every time, you create a flat wide table combining necessary fields.

---

##  **6. What Tools Have You Used for Data Modeling?**

**Answer:**
Tools used:

* dbt (for transformations and models)
* SQL Developer Data Modeler
* ER/Studio
* dbdiagram.io
* Lucidchart for documentation

---

##  **7. Explain Star Schema and Snowflake Schema with Examples.**

**Answer:**

* **Star Schema**: Central fact table with denormalized dimension tables.
* **Snowflake Schema**: Normalized dimensions (sub-dimensions).

**Example:**
**Star:**

```
FactSales(SaleID, DateID, CustomerID, ProductID, Amount)
Customer(CustomerID, Name, City)
```

**Snowflake:**

```
Customer(CustomerID, Name, CityID)
City(CityID, CityName, State)
```

---

##  **8. What are Slowly Changing Dimensions (SCD)? Types?**

**Answer:**
SCD tracks changes in dimension data over time.

* **Type 1**: Overwrite old data.
* **Type 2**: Add a new record with timestamp/version.
* **Type 3**: Keep old and current value in same row.

**Example:**
A customer changes city:

* Type 1: Update the city field.
* Type 2: Insert a new row with a new version number.
* Type 3: Add `PreviousCity` column.

---

##  **9. What are Surrogate Keys and Why Use Them?**

**Answer:**
Surrogate keys are system-generated primary keys (e.g., auto-incremented ID) used instead of business keys.

**Example:**
Instead of using `Email` or `SSN` as a primary key, we use `CustomerID (INT)`.

**Why?**

* Business keys may change.
* Surrogate keys ensure uniqueness and performance.

---

##  **10. What are Fact and Dimension Tables? Types of Facts?**

**Answer:**

* **Fact Table**: Quantitative metrics (e.g., sales, revenue).
* **Dimension Table**: Descriptive attributes (e.g., product, customer).

**Types of Facts:**

* **Transactional**: Sales transactions.
* **Snapshot**: Monthly account balances.
* **Accumulating**: Order lifecycle (order placed → shipped → delivered).

---

##  **11. Write SQL to Find Orphan Records Between Fact and Dimension Table.**

**Answer:**

```sql
SELECT f.*
FROM FactSales f
LEFT JOIN DimCustomer d ON f.CustomerID = d.CustomerID
WHERE d.CustomerID IS NULL;
```

**Purpose:** Detect foreign keys in fact table not present in dimension table.

---

##  **12. How Do You Handle Schema Evolution in Data Lakes?**

**Answer:**
Use schema-on-read formats like **Parquet**, **Delta Lake**, or tools like **Databricks Auto Loader** to handle added columns or data type changes.

**Example:**

* Delta Lake can evolve schema during merge:

```python
df.write.option("mergeSchema", "true").format("delta").save("/mnt/sales")
```

---

##  **13. Design a Data Model for an E-commerce Platform.**

**Answer:**
Tables:

* **FactOrders**: OrderID, CustomerID, ProductID, Amount, DateID
* **DimCustomer**: CustomerID, Name, Email
* **DimProduct**: ProductID, Name, Category
* **DimDate**: DateID, Year, Month, Weekday

**Why?**

* Fact table for metrics.
* Dimension tables for filtering and aggregation.

---

##  **14. How Would You Design for Real-Time vs. Batch Analytics?**

**Answer:**

| Metric     | Real-time                       | Batch                  |
| ---------- | ------------------------------- | ---------------------- |
| Storage    | Delta Lake / Kafka / Event Hub  | Blob / ADLS            |
| Schema     | Flat / append-only              | Star/Snowflake         |
| Processing | Stream (e.g., Spark Structured) | Batch jobs (ADF/Spark) |
| Use case   | Fraud detection                 | Monthly sales reports  |

---

##  **15. How Do You Convert Normalized OLTP Schema into Analytical Schema?**

**Answer:**

* Identify facts and dimensions.
* Flatten dimension hierarchies.
* Replace many-to-many with bridge tables.

**Example:**
OLTP: `Order`, `OrderDetails`, `Product`, `Customer`
→ Analytical: `FactSales`, `DimProduct`, `DimCustomer`, `DimDate`

---

##  **16. How Do You Optimize Join Performance in Fact-Dimension Joins?**

**Answer:**

* Use **broadcast joins** in Spark if dimension is small.
* Partition and bucket tables on join keys.
* Use surrogate keys for joining (integers are faster).

---

##  **17. What is Dimensional Conformance?**

**Answer:**
Conformed dimensions are shared across multiple fact tables or subject areas.

**Example:**
A `DimDate` used in both `FactSales` and `FactInventory` ensures consistency in time-based reporting.

---

##  **18. What are the Different Types of Relationships in Data Modeling?**

**Answer:**

* One-to-One
* One-to-Many (most common in dimensions)
* Many-to-Many (handled using bridge tables)

---

##  **19. What is Data Vault Modeling? When Do You Use It?**

**Answer:**
Data Vault is used for enterprise data warehouses with agile, scalable needs.

* **Hub**: Unique business keys
* **Link**: Relationships
* **Satellite**: Descriptive data

**Use case:** Auditable, historical data capture systems.

---

##  **20. How Do You Document and Version Control Data Models?**

**Answer:**

* Use **dbt** with Git for versioning.
* Maintain **ERD diagrams** with documentation tools like **Confluence**.
* Maintain change logs and metadata repositories.

---

##  **21. How Do You Handle Many-to-Many Relationships in a Data Warehouse?**

**Answer:**
Many-to-many relationships are handled using a **bridge (junction) table**.

**Example:**
In a university system:

* One student can enroll in many courses.
* One course can have many students.

**Model:**

* `Student(StudentID, Name)`
* `Course(CourseID, Title)`
* `Enrollment(StudentID, CourseID, EnrollmentDate)` ← Bridge table

In a warehouse, facts can reference the bridge table if necessary.

---

##  **22. What is a Junk Dimension? Give an Example.**

**Answer:**
A Junk Dimension combines several low-cardinality flags and indicators into a single dimension to avoid cluttering the fact table.

**Example:**
Instead of adding 3 separate yes/no fields to `FactSales` (e.g., `IsPromo`, `IsOnline`, `IsReturned`), create:

```sql
DimJunk(ID, IsPromo, IsOnline, IsReturned)
```

Then reference `JunkID` from `FactSales`.

---

##  **23. How Do You Ensure Data Quality at the Modeling Level?**

**Answer:**

* Define **constraints**: primary key, foreign key, not null.
* Use **lookup tables** for consistent values.
* Implement **validation logic** in ETL pipelines (e.g., null checks, type checks).
* Perform **data profiling** using tools like Great Expectations or Deequ.

---

##  **24. How Do You Handle Null Values in Data Models?**

**Answer:**

* Use `NOT NULL` where applicable.
* For dimension tables, use **default records** for unknowns (e.g., `-1: Unknown`).
* Handle with care in joins to avoid loss of rows.
* Replace nulls with defaults during transformation, if appropriate.

**Example:**
If a customer's city is NULL:

```sql
COALESCE(City, 'Unknown')
```

---

##  **25. How Do You Choose Column Data Types When Designing a Model?**

**Answer:**

* Use **smaller types** for better performance (`INT` over `BIGINT`, `VARCHAR(50)` instead of `VARCHAR(MAX)`).
* Ensure **compatibility** with tools (e.g., use `STRING` in Hive/Spark).
* Consider **compression efficiency** (e.g., integers compress better than strings).

---

##  **26. How Do You Model Historical Data?**

**Answer:**

* Use **Type 2 SCD** for dimensions to store changes over time.
* Use **snapshot fact tables** to capture point-in-time metrics.

**Example:**
Monthly snapshot of customer balances → `FactCustomerBalance(Month, CustomerID, Balance)`

---

##  **27. How Do You Perform Impact Analysis When a Schema Changes?**

**Answer:**

* Use **data lineage tools** (e.g., Azure Purview, Unity Catalog, dbt docs).
* Track dependencies between columns and downstream tables/views.
* Perform **automated tests** after schema evolution.
* Communicate changes via **schema registry or changelog**.

---

##  **28. What is a Conformed Fact?**

**Answer:**
A fact that is shared across multiple business processes and uses **conformed dimensions**.

**Example:**

* `FactSales` and `FactReturns` may share `DimProduct`, `DimCustomer`, and `DimDate`.

---

##  **29. What Are Degenerate Dimensions?**

**Answer:**
A **degenerate dimension** is a dimension key stored in the fact table that does not have its own dimension table.

**Example:**
Invoice number in `FactSales`:

```sql
FactSales(InvoiceNo, CustomerID, ProductID, Amount)
```

Here, `InvoiceNo` is a degenerate dimension—it holds business meaning but doesn’t need a dimension table.

---

##  **30. What Is Data Lineage and Why Is It Important in Data Modeling?**

**Answer:**
**Data lineage** tracks the flow of data from source to destination, showing how data is transformed and used.

**Importance:**

* Helps in debugging data issues.
* Ensures regulatory compliance (GDPR, HIPAA).
* Supports impact analysis.

**Tools:** Azure Purview, Alation, Informatica, dbt docs, Unity Catalog (Databricks).

---

##  **31. How Would You Approach Versioning a Data Model?**

**Answer:**

* Use **semantic versioning**: e.g., v1.0 → v1.1 → v2.0
* Maintain DDL scripts in **Git**
* Use **feature branches** for schema changes
* Tag releases and maintain backward compatibility for downstream systems

---

##  **32. What Is the Difference Between Primary Key and Unique Key?**

**Answer:**

| Feature    | Primary Key                 | Unique Key                    |
| ---------- | --------------------------- | ----------------------------- |
| Uniqueness | Must be unique and not null | Must be unique (null allowed) |
| Count      | Only one per table          | Multiple allowed              |
| Purpose    | Row identification          | Enforce uniqueness            |

---

##  **33. What is Cardinality? How Does It Impact Data Modeling?**

**Answer:**
**Cardinality** refers to the number of unique values in a column.

* High cardinality: e.g., `CustomerID`
* Low cardinality: e.g., `Gender`, `Yes/No`

**Impact:**

* High cardinality dimensions may increase storage and query complexity.
* Low cardinality attributes are good candidates for junk dimensions.

---

##  **34. Explain the Role of Indexes in Physical Data Models.**

**Answer:**
Indexes help improve query performance by allowing faster lookup.

* **Clustered index**: Sorts the table rows.
* **Non-clustered index**: Points to data locations.

**Trade-off:** Indexes speed up reads but slow down inserts/updates.

---

##  **35. What is a Factless Fact Table? Give an Example.**

**Answer:**
A fact table that contains **only foreign keys** and **no measurable facts**.

**Use case:** Track events or coverage.

**Example:**
To track course enrollment:

```sql
FactEnrollment(StudentID, CourseID, DateID)
```

No measures—just the event.

---

##  **36. How Do You Decide When to Use Snowflake Schema Over Star Schema?**

**Answer:**
Use **Snowflake** when:

* Dimensional hierarchies need normalization.
* Data redundancy is a concern.
* Storage is a constraint.
* You want better control over updates.

Use **Star** when:

* Query performance is priority.
* Simpler reporting needed.
* Storage is cheap.

---

##  **37. What’s Your Approach to Creating a Data Dictionary?**

**Answer:**

* Define each table and column with:

  * Name
  * Data type
  * Description
  * Source
  * Business rules

Tools: dbt docs, Confluence, Excel templates, Dataedo.

---

##  **38. How Do You Model Real-Time Streaming Data into a Warehouse?**

**Answer:**

* Use **append-only models**.
* Design fact tables with timestamps and partitioning.
* Store immutable records.
* Use tools like Kafka, Event Hubs → Stream → Delta Lake.

**Example:**
Real-time orders → streamed into `FactOrderStream` partitioned by `order_date`.

---
