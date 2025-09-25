# 🔹 **Power BI Interview Questions & Answers**

---

## **Mid-Level (25 Questions)**

### 1. What are the main components of Power BI?

**Answer:**

* Power BI Desktop (report authoring)
* Power BI Service (cloud-based publishing & collaboration)
* Power BI Mobile (viewing reports)
* Power BI Gateway (on-premises data refresh/connection)
* Power BI Report Server (on-premises report hosting)

---

### 2. Difference between DirectQuery, Import, and Live Connection?

**Answer:**

* **Import**: Data copied into PBIX; best for performance.
* **DirectQuery**: Data remains in source; queries run on-demand.
* **Live Connection**: Real-time connection to SSAS (Tabular/Multidimensional).
  **Use Case**: Import for smaller datasets, DirectQuery for large/real-time, Live for enterprise SSAS.

---

### 3. What is a Gateway in Power BI? Types?

**Answer:**

* A **gateway** bridges on-premises data sources and Power BI Service.
* **Types**:

  * **Personal Gateway** – single user, no scheduling
  * **On-premises Gateway** – enterprise use, scheduling, multiple sources

---

### 4. How do you handle performance issues in Power BI reports?

**Answer:**

* Optimize DAX calculations
* Use star schema, avoid snowflake
* Use aggregations/pre-calculated tables
* Filter unnecessary columns/rows during ETL
* Use Import mode where possible
* Optimize visuals (limit slicers, use fewer visuals)

---

### 5. Explain Star Schema vs. Snowflake Schema in Power BI.

**Answer:**

* **Star Schema**: Fact table at center connected to denormalized dimension tables → faster queries, simpler.
* **Snowflake Schema**: Dimensions normalized into multiple related tables → complex, slower performance.
  **Best Practice**: Always use **star schema** for Power BI.

---

### 6. What is a Fact Table and Dimension Table?

**Answer:**

* **Fact Table**: Contains numeric measures (e.g., sales amount, quantity).
* **Dimension Table**: Contains descriptive attributes (e.g., product, region, time).

---

### 7. What is Row-level Security (RLS) in Power BI?

**Answer:**

* Restricts data access at the row level using **roles & DAX filters**.
* Example: `[Region] = "East"` → users only see East region data.
* Can use **Static RLS** (predefined roles) or **Dynamic RLS** (based on user identity via `USERNAME()` function).

---

### 8. What is the difference between a Calculated Column and a Measure?

**Answer:**

* **Calculated Column**: Computed at row-level, stored in the model (increases size).
* **Measure**: Computed on aggregation/context, calculated at runtime (better performance).

---

### 9. What are Hierarchies in Power BI?

**Answer:**

* Logical levels of data (e.g., Year → Quarter → Month → Day).
* Helps drill-down in visuals.

---

### 10. Explain Aggregations in Power BI.

**Answer:**

* Pre-calculated summary tables that speed up queries on large fact tables.
* Example: Store **Sales by Region & Year** instead of querying billions of transactions.

---

### 11. Explain difference between Calculated Table and Table in Power Query.

**Answer:**

* **Calculated Table**: Created using DAX after loading data.
* **Power Query Table**: Transformed/created during ETL before loading into model.
  **Best Practice**: Use Power Query for transformations, DAX only when needed.

---

### 12. What is a Bookmark in Power BI?

**Answer:**

* Saves the **state of a report page** (filters, slicers, visuals).
* Used for navigation, storytelling, and interactive dashboards.

---

### 13. What are Tooltips in Power BI?

**Answer:**

* Small popups showing additional insights when hovering over visuals.
* Can create **custom tooltip pages**.

---

### 14. What are Filters in Power BI? Levels?

**Answer:**

* **Report-level filter** – applies to entire report.
* **Page-level filter** – applies to one page.
* **Visual-level filter** – applies to a single visual.

---

### 15. How do you optimize a Power BI dataset size?

**Answer:**

* Remove unnecessary columns/rows
* Use proper data types (Int instead of String)
* Avoid high cardinality columns
* Use **Aggregations**
* Prefer Measures over Calculated Columns

---

### 16. Difference between ALL, ALLSELECTED, REMOVEFILTERS in DAX?

**Answer:**

* **ALL**: Ignores all filters.
* **ALLSELECTED**: Respects user selections but ignores visual filters.
* **REMOVEFILTERS**: Newer, same as ALL but more readable.

---

### 17. Explain Difference between SUM and SUMX.

**Answer:**

* **SUM**: Aggregates column directly.
* **SUMX**: Row-by-row calculation, then aggregation.
  Example: `SUMX(Sales, Sales[Quantity] * Sales[Price])`

---

### 18. What is a KPI in Power BI?

**Answer:**

* Key Performance Indicator visual to track business metrics against a target.

---

### 19. What is a Relationship Cardinality in Power BI?

**Answer:**

* Defines type of relation between tables:

  * One-to-Many (most common)
  * Many-to-Many
  * One-to-One

---

### 20. What is the difference between Manage Relationships and Auto-detect?

**Answer:**

* **Manage Relationships**: User defines relationships.
* **Auto-detect**: Power BI suggests relationships based on column names/data types.

---

### 21. Explain difference between Merge and Append in Power Query.

**Answer:**

* **Merge**: Join two tables on keys (SQL JOIN).
* **Append**: Stack rows of two tables (SQL UNION).

---

### 22. What is Drillthrough in Power BI?

**Answer:**

* Allows users to **right-click on data** and navigate to another page with detailed insights.

---

### 23. What are Quick Measures?

**Answer:**

* Pre-built DAX measures (YTD, Running Total, % of Total, etc.) created via UI.

---

### 24. What are Custom Visuals in Power BI?

**Answer:**

* Additional visuals imported from AppSource or custom-built using Power BI SDK (e.g., Sankey chart, Word Cloud).

---

### 25. What is the difference between Power BI Free, Pro, and Premium?

**Answer:**

* **Free**: Personal use, no sharing.
* **Pro**: Collaboration, sharing, publishing to service.
* **Premium**: Dedicated capacity, larger dataset sizes, paginated reports, enterprise features.

---

## **Advanced Level (25 Questions)**

### 26. Explain the Power BI Architecture in enterprise deployment.

**Answer:**

* Data Sources → Power Query (ETL) → Data Model (Tabular) → Reports → Power BI Service → Sharing (Apps, Workspaces, RLS, Security).

---

### 27. What is Composite Model in Power BI?

**Answer:**

* Combines **Import + DirectQuery** tables in one model.
* Useful for balancing performance and real-time data needs.

---

### 28. Explain Incremental Refresh in Power BI.

**Answer:**

* Loads **historical data once** and only refreshes **new/changed data**.
* Improves refresh time for large datasets.

---

### 29. What is Aggregation Table in Power BI?

**Answer:**

* Pre-aggregated summary tables for performance.
* Power BI decides whether to query aggregation or detail table.

---

### 30. Explain the role of VertiPaq engine.

**Answer:**

* In-memory columnar storage engine used in Import mode.
* Uses compression & dictionary encoding → super-fast queries.

---

### 31. Explain Evaluation Context in DAX.

**Answer:**

* **Row Context**: Calculations applied per row (like Calculated Columns).
* **Filter Context**: Filters applied by visuals/slicers.
* **Context Transition**: Converts row context → filter context (CALCULATE).

---

### 32. Explain Difference between CALCULATE and CALCULATETABLE.

**Answer:**

* **CALCULATE**: Returns scalar value after applying filters.
* **CALCULATETABLE**: Returns a table object with modified filter context.

---

### 33. How do you implement Dynamic Row Level Security?

**Answer:**

* Create security table mapping **User → Region**.
* Apply DAX filter:

  ```DAX
  [Region] = LOOKUPVALUE(UserRegion[Region], UserRegion[User], USERNAME())
  ```

---

### 34. How to handle Slowly Changing Dimensions (SCD) in Power BI?

**Answer:**

* Best handled in ETL (Dataflows/ADF/SQL).
* For Type 2 (historical tracking), keep effective date columns in dimension table and use DAX for filtering active record.

---

### 35. What is the maximum dataset size supported?

**Answer:**

* **Pro**: 1 GB
* **Premium**: 400 GB per dataset (with large models enabled).

---

### 36. What are Dataflows in Power BI?

**Answer:**

* Cloud-based ETL in Power BI Service.
* Based on Power Query, reusable across datasets.

---

### 37. Explain usage of Tabular Editor in Power BI.

**Answer:**

* External tool for advanced DAX editing, measures management, calculation groups.
* Helps with version control (scripts, automation).

---

### 38. What are Calculation Groups?

**Answer:**

* Feature in Tabular Editor allowing **reusable DAX logic** (e.g., YTD, MTD, % Growth).
* Reduces duplication of measures.

---

### 39. Explain difference between Workspace and App in Power BI.

**Answer:**

* **Workspace**: Collaboration area for developers.
* **App**: Packaged report/dashboard for end-users.

---

### 40. What is Deployment Pipeline in Power BI?

**Answer:**

* CI/CD for Power BI (Dev → Test → Prod).
* Allows versioning and controlled publishing.

---

### 41. How do you manage performance for large datasets (billion+ rows)?

**Answer:**

* Aggregations, Incremental refresh, Composite models, Pre-aggregation in SQL, Partitioning, Optimize relationships, Use DirectQuery with aggregations.

---

### 42. Explain difference between Push Dataset and Streaming Dataset.

**Answer:**

* **Push Dataset**: Data pushed via API and stored in Power BI.
* **Streaming Dataset**: Data streamed in real-time, not stored (used in dashboards).

---

### 43. How does Power BI handle Many-to-Many relationships?

**Answer:**

* Supported since July 2018 release.
* Requires bridging table or bi-directional filtering.

---

### 44. Explain security best practices in Power BI.

**Answer:**

* Implement RLS/Dynamic RLS
* Use Service Principals for automation
* Restrict export/download
* Governance with Premium/Capacity metrics
* Use sensitivity labels

---

### 45. How do you monitor Power BI performance?

**Answer:**

* Performance Analyzer (Desktop)
* DAX Studio (query timings)
* Power BI Service Audit Logs
* Usage Metrics reports

---

### 46. Explain difference between Paginated Reports and Power BI Reports.

**Answer:**

* **Paginated Reports**: Pixel-perfect, paged, SSRS-style.
* **Power BI Reports**: Interactive, visual dashboards.

---

### 47. Explain usage of XMLA Endpoints in Power BI.

**Answer:**

* Allows external tools (SSMS, Tabular Editor) to connect to Power BI Premium datasets for advanced modeling.

---

### 48. What are Limitations of DirectQuery mode?

**Answer:**

* Slower performance (depends on source DB)
* Limited DAX functionality
* 1M row limit per query
* Higher load on source system

---

### 49. What is Data Lineage in Power BI?

**Answer:**

* Visualization showing data flow from sources → Dataflows → Datasets → Reports → Dashboards.
* Useful for governance & impact analysis.

---

### 50. How do you share a Power BI Report with external users?

**Answer:**

* Guest users via Azure AD B2B
* Publish to Web (not secure, public)
* Power BI Embedded (API-based)

---

