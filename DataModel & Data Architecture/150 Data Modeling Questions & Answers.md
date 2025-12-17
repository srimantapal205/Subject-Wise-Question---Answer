## 🔹 **PART 1 – DATA MODELING BEGINNER LEVEL (Q1–Q50)**

---

### **1. What is Data Modeling?**

Data Modeling is the process of visually representing data and its relationships in a system. It defines how data is stored, accessed, and structured.

🟢 Example: Designing tables for an e-commerce database:

* Customers table
* Orders table
* Products table
  Relationships define how they link (Customer → Orders → Products).

---

### **2. Why is Data Modeling important?**

It ensures data accuracy, consistency, scalability, and reduces storage and processing costs.

🟢 Example:
Without modeling → Duplicate customer data in multiple systems.
With modeling → Single Customer Master, referenced everywhere.

---

### **3. What are the types of Data Models?**

| Model      | Purpose                                               |
| ---------- | ----------------------------------------------------- |
| Conceptual | High level business understanding                     |
| Logical    | Technical details without physical storage details    |
| Physical   | Final database structure with columns, types, indexes |

---

### **4. Explain Conceptual Data Model**

High-level overview focusing on **entities and relationships**, without attributes.

🟢 Example:
Customer — Places — Order

---

### **5. Explain Logical Data Model**

Contains **entities, attributes, primary keys, foreign keys, cardinalities**, but not physical storage.

🟢 Example Table (Logical)
| CustomerID (PK) | Name | Email |

---

### **6. Explain Physical Data Model**

Final implementation for a specific database with **datatypes, indexes, constraints, partitions**.

🟢 Example (Physical)

| Column     | Datatype                      |
| ---------- | ----------------------------- |
| CustomerID | INT IDENTITY(1,1) PRIMARY KEY |
| Name       | VARCHAR(100)                  |

---

### **7. What is a Primary Key?**

A column or group of columns uniquely identifying a row.

🟢 Example: CustomerID

---

### **8. What is a Foreign Key?**

A field connecting data across tables, referring to a primary key in another table.

🟢 Example: Orders.CustomerID → Customer.CustomerID

---

### **9. What is a Composite Key?**

A combination of two or more columns uniquely identifying a row.

🟢 Example: `OrderProduct(orderID, productID)`

---

### **10. What is a Surrogate Key?**

System-generated key (not business-driven).

🟢 Example: `CustomerID INT IDENTITY`

---

### **11. Difference between Natural Key and Surrogate Key**

| Natural                  | Surrogate        |
| ------------------------ | ---------------- |
| Comes from business data | System generated |
| May change               | Never changes    |
| Not always unique        | Always unique    |

---

### **12. What is Cardinality?**

Defines relationship strength: **1-1, 1-M, M-M**.

🟢 Example:

* One Customer → Many Orders (1-M)

---

### **13. What is Normalization?**

Technique to eliminate redundancy by splitting data logically.

---

### **14. What is Denormalization?**

Combining tables to optimize performance at the cost of redundancy.

---

### **15. What are Normal Forms?**

| Form | Purpose                    |
| ---- | -------------------------- |
| 1NF  | Atomic values              |
| 2NF  | No partial dependencies    |
| 3NF  | No transitive dependencies |
| BCNF | Strict rules on keys       |

---

### **16. What is 1NF?**

All values must be **atomic**, no repeating groups.

❌ mobile: 9001;9002
✔ mobile1, mobile2 in separate rows

---

### **17. What is 2NF?**

Applies only to tables with composite keys—no partial dependency.

---

### **18. What is 3NF?**

No non-key attribute depends on another non-key attribute.

---

### **19. Difference between OLTP and OLAP Modeling**

| OLTP          | OLAP         |
| ------------- | ------------ |
| Transactional | Analytical   |
| Normalized    | Denormalized |
| Real-time     | Historical   |

---

### **20. What is a Fact Table?**

Stores measurable business metrics (transactions).

🟢 Examples:

* SalesAmount
* Quantity
* Revenue

---

### **21. What is a Dimension Table?**

Stores descriptive attributes for analysis.

🟢 Examples:

* Customer
* Location
* Product
* Time

---

### **22. What is a Star Schema?**

A fact table in the center connected to dimensions.

🟢 Sales → Customer, Product, Time, Store

---

### **23. What is a Snowflake Schema?**

Dimensions are normalized further into sub-dimensions.

🟢 Product → Product Category → Department

---

### **24. What is a Galaxy Schema?**

Also called **Fact Constellation**—multiple fact tables share dimensions.

🟢 Example:

* Sales Fact
* Inventory Fact
  Shared → Product, Store, Time

---

### **25. What is a Degenerate Dimension?**

A dimension without its own table (value stored in Fact).

🟢 Example: Invoice Number in Fact_Sales

---

### **26. What is SCD (Slowly Changing Dimension)?**

Technique to track dimension attribute history.

---

### **27. Types of SCD**

| Type | Behavior                              |
| ---- | ------------------------------------- |
| SCD1 | Overwrite old value                   |
| SCD2 | Preserve history (new row)            |
| SCD3 | Maintain limited history (new column) |

---

### **28. What is a Junk Dimension?**

Stores miscellaneous low-cardinality attributes in one table.

🟢 Example: PromotionFlag, DiscountFlag, EmailOptIn

---

### **29. What is a Role-Playing Dimension?**

Same dimension used in multiple roles.

🟢 Example: Time Dimension as OrderDate, ShipDate

---

### **30. What is Conformed Dimension?**

Dimensions shared across multiple fact tables.

🟢 Example: Product dimension used by Sales & Inventory

---

### **31. What is Factless Fact Table?**

A fact table with **no numeric measures**, tracks events.

🟢 Example:

* Student Attendance
* Patient Visit

---

### **32. What is Additive Fact?**

Facts that can be summed across dimensions.

🟢 Example: Quantity, SalesAmount

---

### **33. What is Semi-Additive Fact?**

Additive across some dimensions only.

🟢 Example: Account Balance (not additive across time)

---

### **34. What is Non-Additive Fact?**

Cannot be aggregated using sum.

🟢 Example: Profit Percentage

---

### **35. What is a Data Dictionary?**

Documentation of database metadata.

---

### **36. What is ER Diagram?**

Entity-Relationship diagram showing entities and relationships.

---

### **37. What is Domain Integrity?**

Ensures valid values for attributes.

🟢 Example: Age cannot be negative.

---

### **38. What is Referential Integrity?**

Foreign keys must match primary key values.

---

### **39. What is Data Redundancy?**

Duplicate data stored multiple times.

---

### **40. What is Hierarchy in Dimension?**

Parent-child structure in attributes.

🟢 Example: Country → State → City

---

### **41. What is Granularity in Fact Table?**

Level of detail stored in the fact.

🟢 Example:

* High granularity → line-item sale
* Low granularity → daily sales summary

---

### **42. Difference between OLAP Cubes and Fact Tables**

| Fact Tables | OLAP Cubes      |
| ----------- | --------------- |
| Raw storage | Pre-aggregated  |
| Database    | Analysis engine |

---

### **43. What is Data Mart?**

Subset of data warehouse for a specific department.

🟢 Example: Finance Data Mart, Sales Data Mart

---

### **44. What is Data Warehouse?**

Central storage for enterprise data for analytics.

---

### **45. What is a Bridge Table?**

Resolves **M-M relationships** between dimensions and facts.

---

### **46. What is Metadata?**

Data about data.

🟢 Example: Column type, table name, size, relation.

---

### **47. What is a Lookup Table?**

Stores code and description pairs.

🟢 Example: StatusID | StatusName

---

### **48. What is Surrogate vs Business Key in Fact Table?**

| Business Key         | Surrogate Key        |
| -------------------- | -------------------- |
| Order ID             | Fact ID              |
| Generated externally | Generated internally |

---

### **49. What is Columnar Storage?**

Stores column-wise instead of row-wise to optimize analytics.

🟢 Example: Azure Synapse, Redshift, Snowflake

### **50. What is a Data Contract?**

Agreement on structure and meaning of data shared between systems.

---

## 🔷 **PART 2 – INTERMEDIATE LEVEL (Q51–Q100)**

---

### **51. What is the difference between Conceptual, Logical, and Physical Data Model?**

| Conceptual                                     | Logical                          | Physical                                                    |
| ---------------------------------------------- | -------------------------------- | ----------------------------------------------------------- |
| High-level business entities and relationships | Attributes, PK/FK, cardinalities | Final DB implementation with datatypes, indexes, partitions |
| No attributes                                  | Attributes included              | Constraints included                                        |
| For business stakeholders                      | For architects                   | For DBAs                                                    |

---

### **52. What is the first step when starting a data model?**

Understanding **business requirements**: KPIs, Data sources, Expected outputs.

🟢 Example: For Sales Analytics → metrics = SalesAmount, UnitsSold.

---

### **53. What is a Business Entity?**

A representation of a real-world business object.

🟢 Example: Customer, Product, SalesOrder.

---

### **54. How do you identify entities in requirement workshops?**

Look for **nouns** in requirements.

🟢 Example: “Customer places order” → Customer, Order.

---

### **55. What is an Attribute?**

A property that describes an entity.

🟢 Example: CustomerName, OrderDate.

---

### **56. What is Domain?**

Allowed values or datatype constraints of an attribute.

🟢 Example: Gender domain → {M, F, O}.

---

### **57. What is an Optional Attribute?**

An attribute whose value may be NULL.

🟢 Example: MiddleName.

---

### **58. What is Data Type Selection in Physical Modeling?**

Choosing efficient column types for performance and storage.

🟢 Example:
Use `INT` instead of `VARCHAR(10)` for StatusCode.

---

### **59. What is Indexing in Data Modeling?**

Technique to improve data retrieval speed.

🟢 Example: Creating index on `OrderDate` to speed reporting queries.

---

### **60. Types of Indexes**

| Index Type          | Purpose             |
| ------------------- | ------------------- |
| Clustered Index     | Physical row order  |
| Non-Clustered Index | Logical access path |
| Composite Index     | Multi-column index  |
| Unique Index        | Ensures uniqueness  |

---

### **61. What is a Grain Declaration in Fact Tables?**

Specifying the **level of detail per row**.

🟢 Example:
Grain = One row per product per order transaction.

---

### **62. Why is Grain Important?**

If not defined, facts may contain:
❌ double counting
❌ inconsistent aggregation

---

### **63. Should surrogate keys be used for dimension tables?**

Yes — because surrogate keys:
✔ Never change
✔ Avoid business dependency
✔ Perform faster joins

---

### **64. Can a Fact Table have a Primary Key?**

Yes — usually via **FactID** or **Composite PK** of foreign keys & date.

🟢 Example PK: (OrderID, ProductID, DateID).

---

### **65. Can a Fact Table have Foreign Keys?**

Yes — fact tables must include FK references to related dimensions.

---

### **66. What is a Mini-Dimension?**

A separate dimension for rapidly changing attributes to avoid SCD2 explosion.

🟢 Example:
CustomerPreferences (AgeGroup, IncomeBand, LoyaltyTier)

---

### **67. How do you handle Multi-Valued Dimensions?**

Using **Bridge Tables** or **Mini-Dimensions**.

---

### **68. What is a Surrogate Key Drift?**

When a dimension row gets updated incorrectly and historical FK links break.

❌ Wrong: Reassigning existing surrogate key during SCD2 update.

---

### **69. What is an Outrigger Dimension?**

A dimension linked to another dimension (not directly to fact).

🟢 Example:
Customer → Geography dimension

---

### **70. What is a Snowflaked Dimension?**

A dimension normalized into multiple related tables.

🟢 Product → Category → Department

---

### **71. What is Fact Table Normalization?**

Splitting fact into header & detail facts.

🟢 Example:

* FactOrderHeader
* FactOrderLine

---

### **72. What is a Derived / Calculated Fact?**

A fact computed from other measures.

🟢 Example: Profit = Revenue − Cost

---

### **73. What is a Snapshot Fact Table?**

Captures periodic state of data (daily/monthly snapshot).

🟢 Example:
Daily Account Balance Snapshot.

---

### **74. What is a Transaction Fact Table?**

Captures events as they happen.

🟢 Example:
One row per order transaction.

---

### **75. What is an Accumulating Snapshot Fact Table?**

Tracks lifecycle of a process, updated multiple times.

🟢 Example:
Order Lifecycle Fact
PlacedDate → PackedDate → ShippedDate → DeliveredDate

---

### **76. What is Fact Granularity vs Dimension Granularity?**

Fact grain must align with the lowest grain of dimensions.

---

### **77. What is a Slowly Changing Fact?**

A fact whose values change over time and need history.

🟢 Example:
RefundAmount updated after return approval.

---

### **78. What is a Centralized Data Model?**

All domains share same dimensions and facts (Enterprise Warehouse approach).

---

### **79. What is Federated / Distributed Data Model?**

Teams maintain domain-specific warehouses (Data Mesh concept).

---

### **80. What is a Metadata-Driven Model?**

Model where schema & pipelines are generated dynamically using metadata.

🟢 Example:
Column mapping table controls ETL.

---

### **81. What is Active Metadata?**

System automatically manages and updates metadata during operations.

🟢 Example:
Lineage auto-tracking in Databricks Unity Catalog.

---

### **82. What is Dimensional Hierarchy Navigation?**

Ability to drill down or roll up between levels.

🟢 Example:
Year → Quarter → Month → Day

---

### **83. What is Attribute Explosion?**

Dimension grows too wide because too many attributes are added.

📌 Solution: Mini-dimensions or snowflaking.

---

### **84. What is Cardinality Trap?**

In ER modeling, incorrect relationship leads to ambiguity.

🟢 Example:
Student–Teacher–Class without proper link.

---

### **85. What is a Role-Playing Dimension?**

Same dimension used multiple times in a fact table.

🟢 Example:
Date dimension used as:
OrderDateID, ShipDateID, DeliveryDateID.

---

### **86. What is Data Vault Modeling?**

A scalable model for real-time warehousing consisting of:

* **Hubs**
* **Links**
* **Satellites**

---

### **87. Benefits of Data Vault**

✔ Handles schema evolution
✔ Suitable for big data and real-time pipelines
✔ Auditable & traceable

---

### **88. When to use 3NF over Star Schema?**

Use 3NF when transaction performance and storage efficiency matter (OLTP).
Use Star Schema when query speed matters (OLAP).

---

### **89. Can OLTP and OLAP Models Coexist?**

Yes — via separate layers:

* OLTP → Source systems
* OLAP → Warehouses for analytics

---

### **90. What is Anti-Pattern in Data Modeling?**

Design choices that reduce performance or usability.

❌ Very wide tables
❌ Too many nullable columns
❌ Storing JSON blobs instead of structured attributes

---

### **91. What is Data Stewardship in Modeling?**

Assigning ownership of each domain's data quality, definitions, and lineage.

---

### **92. What is a Data Model Review Checklist?**

Includes:

* Naming standards
* Grain definition
* PK/FK verification
* Indexing strategy
* SCD handling
* Performance considerations

---

### **93. What is Referential Integrity in Warehouses?**

Ensuring FK values exist in dimension tables before loading facts.

📌 Implemented in ETL/ELT.

---

### **94. What is Late-Arriving Fact?**

Fact arrives before its dimension record.

📌 Solution:
Assign default surrogate key (Unknown Member) initially → update later.

---

### **95. What is Late-Arriving Dimension?**

Dimension arrives after corresponding facts have been loaded.

📌 Solution:
Reprocess affected facts and replace “Unknown” FK values.

---

### **96. What is a Parent-Child Dimension?**

Recursive hierarchy within same dimension.

🟢 Example:
EmployeeID → ManagerID

---

### **97. What is Junk Dimension vs Degenerate Dimension?**

| Junk                                   | Degenerate                      |
| -------------------------------------- | ------------------------------- |
| Stores low-cardinality flags and codes | Dimension attribute inside fact |
| Has its own table                      | No separate table               |
| CustomerFlagsDim                       | InvoiceNumber in fact           |

---

### **98. What is Null Handling Strategy in Dimensions?**

Unknown and Not Applicable rows are added intentionally:

| SurKey | Value          |
| ------ | -------------- |
| -1     | Unknown        |
| -2     | Not Applicable |

---

### **99. What is a Lookup Failure in ETL?**

Fact cannot find matching FK in dimension.

📌 Solutions:

* Insert into Unknown Member
* Capture in error table
* Request data fix

---

### **100. What is Data Churn & Why Does It Matter?**

Frequent updates to rows cause high change volume and table bloat.

📌 Mitigation:

* Mini-dimensions
* Partitioning
* Clustered indexes

---

## 🔥 **PART 3 – ADVANCED LEVEL (Q101–Q130)**

---

### **101. What are the most important performance considerations in data modeling?**

1. Proper grain definition
2. Surrogate keys for joins
3. Correct indexing strategy
4. Partitioning large fact tables
5. Avoiding unnecessary normalization in analytical systems
6. Using columnar storage for OLAP workloads

---

### **102. Why does Fact Table size grow much faster than Dimension Table size?**

Because facts represent transactions/events that occur frequently, while dimensions store descriptive info that changes slowly.

🟢 Example: 500M Sales rows per year (Fact) vs 200K Products (Dimension).

---

### **103. When should you partition tables?**

When:

* Table is very large
* Queries filter by a predictable dimension (Date, Region, Category)

🟢 Example:
Partition FactSales by `SaleDate` (monthly or daily).

---

### **104. What factors influence the choice of partition key?**

✔ Query filtering pattern
✔ Data volume distribution (to avoid skew)
✔ Load frequency
✔ Pruning capacity of engine

❌ Do not partition low-cardinality columns (Gender, Yes/No flags).

---

### **105. What is a Bitmap Index?**

Index using bitmaps instead of B-trees. Ideal for low-cardinality columns in large analytic tables.

🟢 Example: Gender, MembershipType.

---

### **106. What is Columnar Storage and why is it useful in analytics?**

Stores data **column-wise** → queries read only required columns → faster aggregation and compression.

🟢 Tools: Snowflake, Synapse, BigQuery, Redshift, Databricks Delta.

---

### **107. Why is Normalization bad for BI systems?**

It increases JOINs → reduces query performance → complex model for reporting.

✔ Preferred: Denormalized star schema for OLAP.

---

### **108. How do you choose between Star Schema and Snowflake Schema?**

| Star              | Snowflake                    |
| ----------------- | ---------------------------- |
| Best for speed    | Best for storage savings     |
| Few joins         | More joins                   |
| Flat dimensions   | Normalized dimensions        |
| Analysts friendly | Used for complex hierarchies |

---

### **109. What is Data Grain Mismatch Problem?**

When facts are aggregated at different levels, joining them causes incorrect analytics.

🟢 Example:

* Sales daily
* Inventory monthly

❌ Direct join produces wrong results.

📌 Solution: Conform grain via bridge snapshot fact.

---

### **110. What is a Bridge Table in Many-to-Many Modeling?**

A table inserted to resolve M-M relationships.

🟢 Example:
Students ↔ Subjects
StudentsSubjectsBridge(StudentID, SubjectID)

---

### **111. Why is Data Vault preferred in modern architectures?**

✔ Handles schema evolution
✔ Scales easily
✔ Supports multi-source integration
✔ Auditable and traceable

---

### **112. What are the components of Data Vault Modeling?**

| Element   | Purpose                       |
| --------- | ----------------------------- |
| Hub       | Core business entity keys     |
| Link      | Relationships between hubs    |
| Satellite | Context/history of hubs/links |

---

### **113. Difference between Data Vault and Dimensional Modeling**

| Dimensional Model        | Data Vault                         |
| ------------------------ | ---------------------------------- |
| For analytics            | For raw storage integration        |
| Designed for performance | Designed for flexibility & history |
| Star schema              | Hub-Link-Satellite                 |
| Not audit friendly       | 100% audit friendly                |

---

### **114. What is a PIT (Point-In-Time) table in Data Vault?**

A table that provides fast access to the latest satellite records for point-in-time analytics.

---

### **115. What is a Bridge table in Data Vault?**

Table that flattens hierarchies (e.g., bill of materials) for easier BI consumption.

---

### **116. What is a Hybrid Data Model?**

Mix of modeling techniques:

* Data Vault for raw layer
* Star schema for consumption layer
* OLTP models for operational workloads

---

### **117. What is a Unified Star Schema (USS)?**

A reusable star schema with a **single central bridge fact** that links everything into one model.

Used in **Power BI & Fabric** for faster self-service modeling.

---

### **118. Why is Fact Table Surrogate Key not always recommended?**

Because composite PK using FKs ensures uniqueness and eliminates need for additional lookup.

📌 But some ETL tools prefer surrogate PK to track lineage and avoid duplicates.

---

### **119. What causes Fact Table Degeneration?**

When facts contain too many textual attributes instead of numeric metrics.

📌 Solution:
Move attributes to dimensions.

---

### **120. What is Data Bitemporality?**

Maintaining **valid time** and **system time**:

| Time Type   | Meaning                          |
| ----------- | -------------------------------- |
| Valid Time  | When the business event occurred |
| System Time | When the record was stored in DB |

Useful for **legal/audit compliance**.

---

### **121. What is Anchor Modeling?**

A highly normalized modeling technique designed for extremely flexible schema evolution.

Used in **finance and telco** domains.

---

### **122. What is Matrix Dimension / Cross-Dimension?**

Dimension that describes combinations of two other dimensions.

🟢 Example:
Product × Store → ProductStore matrix with pricing attributes.

---

### **123. What is Snapshot Aging?**

Older snapshot partitions are archived to cheaper storage to reduce warehouse cost.

---

### **124. How do you secure PII in Dimension Tables?**

Options:

* Tokenization
* Hashing
* Masking
* Encryption
* Splitting identifying attributes into separate secure dimension

---

### **125. What is Schema Evolution?**

Ability to change schema over time without disrupting consumption.

🟢 Example: Adding new attribute to ProductDimension.

---

### **126. Which modeling technique supports Schema Evolution best?**

| Technique                 | Schema Evolution |
| ------------------------- | ---------------- |
| OLTP ER Model             | ❌ Risky          |
| Star Schema               | ⚠ Limited        |
| Data Vault                | ✔ Excellent      |
| Lakehouse (Delta/Parquet) | ✔ Great          |

---

### **127. What are Cross-System Referential Breaks?**

When facts refer to dimension keys that exist in some data sources but not others.

📌 Solution: Global conformed dimensions via MDM (Master Data Management).

---

### **128. What is Semantic Layer in Data Modeling?**

A business-friendly abstraction layer that maps physical tables to business metrics and fields.

🟢 Tools: Fabric Semantic Model, Power BI Dataset, LookML, SSAS Tabular, dbt Semantic Layer.

---

### **129. Why do Lakehouse & Fabric still require Data Modeling?**

Because raw data lakes do not guarantee:

* Relationships
* Referential integrity
* Conformed dimensions
* Business metric consistency

Modeling → Converts storage into **governed analytics**.

---

### **130. What is the ideal Data Model architecture in 2025?**

```
Bronze → Raw → Data Vault
Silver → Business Model → Star Schema / Semantic Model
Gold → Presentation Layer → Metrics / Data Marts / Dashboards
```

✔ Supports real-time
✔ Maintains history
✔ Enables governed self-service BI
✔ Cloud and Lakehouse friendly

---

## 🔥 **PART-4 — Scenario-Based & Case-Study Data Modeling Questions (Q131–Q150)**

---

### **131. Scenario: Retail — A product can have multiple prices based on store & promotion. How do you model it?**

📌 Many-to-Many relationship between **Product ↔ Store** with pricing details → **Bridge / Matrix Dimension**

**Tables**

* DimProduct
* DimStore
* DimPromotion
* MatrixProductStorePricing (price, promotion, validity)
* FactSales (links to MatrixProductStorePricingID)

👉 Helps track price variations at store-level and promotion-level over time.

---

### **132. Scenario: E-commerce — Orders can be updated (returns, cancellations). How do you model sales?**

Use **Accumulative Snapshot Fact Table** for order lifecycle.

| OrderPlaced | Packed | Shipped | Delivered | Returned | Refunded |

Each milestone updates the fact rather than inserting new rows.

---

### **133. Scenario: Banking — Balance is non-additive over time. How do you store it?**

📌 Use **Snapshot Fact Table** (Daily or Monthly)

FactAccountSnapshot
| AccountID | BalanceDate | BalanceAmount |

📌 For BI reports, use **semi-additive aggregation**:

* SUM across Accounts
* NOT across Dates → Use MAX last balance per date

---

### **134. Scenario: Insurance — Customer address changes frequently. How do you track history?**

📌 SCD Type-2 dimension

DimCustomer
| CustomerSK | CustomerID | Name | Address | EffectiveFrom | EffectiveTo | IsCurrent |

History preserved → analytics on past and current residence possible.

---

### **135. Scenario: Subscription model — users can subscribe to multiple plans at once.**

📌 Many-to-Many → **Bridge Table**

UserPlanBridge
| UserID | PlanID | StartDate | EndDate |

FactSubscription tracks revenue events.

---

### **136. Scenario: Airline — Passenger Name Record (PNR) has many passengers & flights.**

Complex relationship → **Factless Fact Table + Bridge**

Tables:

* DimFlight
* DimPassenger
* BridgePNRPassenger
* BridgePNRFlight
* FactPNR (PNR created event)
* FactTicketSale

---

### **137. Scenario: Healthcare — A patient sees multiple doctors; bills generated at visit.**

📌 Many-to-Many Visit relationship

* FactDoctorVisit (one row per visit)
* DimPatient
* DimDoctor
* BridgeDoctorSpeciality (if multiple)

Add **FactPayment** for billing & revenue analytics.

---

### **138. Scenario: Logistics — Package may move across multiple hubs. Track movement.**

📌 Fact Movement Table

FactShipmentMovement
| PackageID | HubID | EventTime | EventType |

📌 DimHub for hub/geography hierarchy
📌 FactShipment for final delivery metrics

---

### **139. Scenario: HR — Employee hierarchy reporting (Manager → Subordinate).**

📌 **Parent-Child Dimension**

DimEmployee
| EmployeeID | EmployeeName | ManagerID |

Enable recursive hierarchy for BI (e.g., Power BI PATH function).

---

### **140. Scenario: Manufacturing — Bill of Materials (assembly containing sub-components).**

📌 Recursive hierarchy → **Bridge / Explosion Table**

DimMaterial
BridgeComponentHierarchy (ParentMaterialID, ChildMaterialID, Quantity)
FactProductionOrder

---

### **141. Scenario: Ecommerce returns — How do you track both sale and return?**

Two facts:

* FactSales — at purchase
* FactReturn — at return event

Tie both using **original SalesOrderLineID**.

Prevents negative metrics corruption.

---

### **142. Scenario: Real-time streaming events (IoT devices every second).**

Store two layers:

* **Hot Layer (Delta / Parquet)** — granular events in time-series structure
* **Aggregated Layer (FactDeviceMetrics)** — device KPIs calculated per minute/hour

BI connects to aggregated layer for performance.

---

### **143. Scenario: Data Warehouse — One product present in two different systems with different IDs.**

Resolve using **Conformed Master Data (Golden Record)**

Tables:

* StagingProduct
* MDMProduct (Golden Business Key)
* DimProduct (Surrogate key for warehouse)

---

### **144. Scenario: Multiple time dimensions — StartDate, DueDate, ClosedDate**

Model using **Role-Playing Dimensions**

FactTask
| TaskID | StartDateID | DueDateID | ClosedDateID |

All refer to **DimDate**.

---

### **145. Scenario: Customer Level Marketing — 200 small boolean flags (emailOptIn, isVIP, couponUsed…)**

Don't store in the Dimension directly → **Junk Dimension**

DimCustomer
JunkMarketingFlagsDim
FactMarketingEvent

Reduces nulls & improves manageability.

---

### **146. Scenario: Dimension attribute grows too frequently (Customer income level changes monthly)**

⚠ Avoid SCD explosion
📌 Use **Mini-Dimension**
DimCustomer → Slowly changing attributes only
DimCustomerMini → Fast-changing attributes
FactSales links to both.

---

### **147. Scenario: Power BI/Fabric — Model becomes slow with many relationships.**

Fix using:

* **Unified Star Schema / Single Direction relationships**
* **Avoid snowflaking**
* **Use bridge tables for Many-to-Many**

🚫 Avoid bi-directional filter unless mandatory.

---

### **148. Scenario: Denormalizing too much makes a dimension extremely wide**

📌 Split into:

* Main Dimension
* Mini-Dimensions (for fast-changing groups)
* Outrigger Dimensions (for hierarchies)

Result → scalable, efficient joins.

---

### **149. Scenario: Fact loads fail when referenced dimension rows are missing**

📌 Use **Unknown / Not Applicable surrogate keys** strategy

DimCustomer contains:
| -1 | Unknown |
| -2 | Not Applicable |

Fact defaults FK to `-1` then updates later after dimension arrival.

---

### **150. Case-Study Interview: Design a Customer 360 Model**

Goal: Complete customer view across Marketing, Sales, Support.

**Layers**

| Layer       | Model                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------- |
| Raw         | Data Vault (HubCustomer, HubOrder, LinkCustomerOrder, SatContactDetails, SatPreferences) |
| Business    | Star Schema                                                                              |
| Fact Tables | FactSales, FactSupportTickets, FactWebsiteClick                                          |
| Dimensions  | DimCustomer (SCD2), DimChannel, DimProduct, DimGeography, DimTime                        |

Capabilities:
✔ Customer lifetime value
✔ Campaign performance
✔ Support impact on sales
✔ Behavioural segmentation

→ Final analytics served through **Semantic Model to Power BI / Fabric**.

---
