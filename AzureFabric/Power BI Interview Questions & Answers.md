# 🧩 **Power BI Interview Questions & Answers — For 4 Years of Experience (Part 1)**

---

## 🟩 **SECTION 1: Power BI Basics**

---

### **1. What is Power BI?**

**Answer:**
Power BI is a **Business Intelligence (BI) and data visualization tool** developed by Microsoft that allows users to connect to various data sources, transform raw data, and create interactive reports and dashboards for decision-making.
It combines **Power Query (ETL)**, **Power Pivot (Modeling)**, and **Power View (Visualization)** into one integrated environment.

---

### **2. What are the components of Power BI?**

**Answer:**
Power BI consists of:

* **Power BI Desktop:** Report and model development tool.
* **Power BI Service (Cloud):** Online platform for sharing, collaboration, and data refresh.
* **Power BI Mobile App:** Access dashboards on mobile.
* **Power BI Gateway:** Connects on-premises data to Power BI Service.
* **Power BI Report Server:** For on-premises report hosting.
* **Power BI Dataflow:** Cloud-based ETL for reuse across reports.

---

### **3. What are the different modes of data connectivity in Power BI?**

**Answer:**

1. **Import Mode:**

   * Data is imported into Power BI and stored in its in-memory engine (VertiPaq).
   * Fast performance, but dataset size is limited (1 GB for Pro).
2. **DirectQuery Mode:**

   * No data is imported; queries are sent live to the source.
   * Slower but ensures real-time data.
3. **Composite Model:**

   * Combination of both Import and DirectQuery for flexibility.

---

### **4. Difference between Power BI Desktop and Power BI Service**

| Feature      | Power BI Desktop | Power BI Service            |
| ------------ | ---------------- | --------------------------- |
| Purpose      | Build reports    | Share, collaborate, refresh |
| Location     | Installed on PC  | Cloud-based                 |
| Data refresh | Manual           | Scheduled                   |
| Security     | Local            | Workspace & RLS             |
| Output       | `.pbix` file     | Published dashboard         |

---

### **5. What is Power BI Gateway?**

**Answer:**
A **gateway** acts as a bridge between on-premises data and the Power BI Service.

* **Personal Gateway:** Used by individuals, refresh only.
* **Enterprise Gateway:** Shared gateway for scheduled refresh and DirectQuery connections.
  Used to **securely transfer data** from local servers (SQL, Oracle, etc.) to Power BI Service.

---

### **6. Explain Power BI Architecture**

**Answer:**
Power BI Architecture involves:

1. **Data Source Layer** – databases, files, APIs, etc.
2. **Power Query (ETL)** – clean, transform, and shape data.
3. **Data Modeling** – build relationships, DAX measures.
4. **Visualization** – reports & dashboards.
5. **Service Layer** – cloud publishing, collaboration, refresh scheduling.

---

### **7. What are the advantages of Power BI?**

**Answer:**

* Easy integration with Microsoft tools (Excel, Azure, SQL).
* Supports multiple data sources.
* DAX for advanced analytics.
* Cloud and mobile access.
* Incremental refresh & real-time dashboards.
* Security with RLS and Azure AD.

---

### **8. What is the difference between Dashboard and Report?**

| Feature     | Dashboard                     | Report              |
| ----------- | ----------------------------- | ------------------- |
| Pages       | Single page                   | Multiple pages      |
| Data Source | Can combine multiple datasets | Single dataset      |
| Interaction | Limited                       | Fully interactive   |
| Creation    | In Power BI Service           | In Power BI Desktop |

---

### **9. What is the difference between Dataset and Dataflow?**

**Answer:**

* **Dataset:** Model and data loaded into Power BI used for reporting.
* **Dataflow:** Cloud ETL process using Power Query Online to prepare reusable data transformations.
  👉 Dataflow feeds into multiple datasets.

---

### **10. What is a Semantic Model in Power BI?**

**Answer:**
A **Semantic Model** (formerly called dataset) defines **business logic, relationships, and DAX measures** on top of raw data.
It acts as a **shared data model** used by multiple reports.

---

### **11. What is Direct Lake Mode in Microsoft Fabric?**

**Answer:**
Direct Lake is a new mode (in Fabric) that allows **Power BI to query Delta tables directly from OneLake** with **import-like performance** but **DirectQuery-like freshness** — no data duplication, and real-time reporting on lakehouse data.

---

### **12. What is Row-Level Security (RLS)?**

**Answer:**
RLS restricts data visibility for users based on roles.
For example:

```DAX
[Region] = USERPRINCIPALNAME()
```

This filters data dynamically so each user sees only their assigned region’s data.

---

### **13. What are the types of RLS?**

* **Static RLS:** Fixed filter rules defined manually.
* **Dynamic RLS:** Filters based on user login or lookup table mapping.

---

### **14. What are Filters in Power BI?**

**Answer:**
Filters control data displayed in visuals.
Types:

* **Visual-level filter** – affects only one chart.
* **Page-level filter** – affects all visuals on a page.
* **Report-level filter** – affects all pages.
* **Drillthrough filter** – for detailed data navigation.

---

### **15. What is Drillthrough and Drilldown in Power BI?**

**Answer:**

* **Drillthrough:** Navigate to another page focused on a specific entity (like “Customer Details”).
* **Drilldown:** Explore hierarchical data (e.g., Year → Quarter → Month → Day).

---

### **16. What is a Bookmark in Power BI?**

**Answer:**
Bookmarks capture **current report state (filters, visuals, selections)** and allow users to return to that state later — used for storytelling or navigation buttons.

---

### **17. What is Power BI App?**

**Answer:**
Power BI App is a **packaged collection of reports, dashboards, and datasets** shared within an organization for distribution and version control.

---

### **18. What is the use of Power BI Report Server?**

**Answer:**
Used for **on-premises hosting** of Power BI reports (PBIX), mainly for organizations that cannot use the cloud due to compliance or data sensitivity.

---

### **19. What are Deployment Pipelines?**

**Answer:**
They enable **Dev → Test → Prod deployment** of Power BI content (datasets, reports, dashboards) with controlled publishing and change tracking.

---

### **20. What is Incremental Refresh?**

**Answer:**
Incremental Refresh loads only **new or changed data** instead of the full dataset.
It uses **RangeStart** and **RangeEnd** parameters to refresh data for a rolling time window — improves refresh speed and performance.

---

## 🟦 **SECTION 2: Power Query (Data Transformation)**

---

### **21. What is Power Query?**

**Answer:**
Power Query is the **ETL (Extract, Transform, Load)** component of Power BI used to:

* Connect to data sources
* Clean and shape data
* Combine multiple sources
* Load the prepared data model

Language used: **M (Power Query Formula Language)**

---

### **22. What is Query Folding?**

**Answer:**
Query folding means Power Query pushes transformation logic (filters, joins, aggregations) back to the data source — allowing it to process data efficiently at the source level.
🔹 Not all transformations support folding (e.g., custom columns, index columns).

---

### **23. What is the difference between “Append Queries” and “Merge Queries”?**

| Function | Purpose                                    |
| -------- | ------------------------------------------ |
| Append   | Combine rows from similar tables (UNION)   |
| Merge    | Combine columns from related tables (JOIN) |

---

### **24. What are Parameters in Power Query?**

**Answer:**
Parameters allow **dynamic control of transformations** (e.g., source file path, date range).
Useful for incremental refresh and environment-specific configuration.

---

### **25. What are “Applied Steps” in Power Query?**

**Answer:**
Applied Steps show **each transformation** applied to data in sequence (e.g., Removed Columns, Filtered Rows).
You can **reorder, delete, or rename** steps.
It’s like a **recorded script** of your data preparation.

---

✅ **Next Section (Part 2)** will cover:

* **Data Modeling (Q26–Q40)**
* **DAX (Q41–Q70)** with formulas and examples.

---

# 🧠 **Power BI Interview Questions & Answers – Part 2**

---

## 🟩 **SECTION 3: Data Modeling (Q26–Q40)**

---

### **26. What is Data Modeling in Power BI?**

**Answer:**
Data modeling is the process of **structuring and organizing data tables** to define relationships between them, creating a foundation for efficient analysis and DAX calculations.
You build a **semantic layer** — combining fact and dimension tables in a meaningful schema.

---

### **27. What is the difference between a Fact and a Dimension table?**

| Type            | Description                                                     | Example                  |
| --------------- | --------------------------------------------------------------- | ------------------------ |
| Fact Table      | Contains **measurable, numeric data** (transactions)            | Sales, Revenue, Quantity |
| Dimension Table | Contains **descriptive attributes** used for grouping/filtering | Customer, Product, Date  |

---

### **28. What is a Relationship in Power BI?**

**Answer:**
A relationship defines how data in two tables is connected based on a **common column (key)**.
Example:

* **Sales[ProductID] → Products[ProductID]**
  This allows Power BI to filter and aggregate across tables.

---

### **29. What is Cardinality?**

**Answer:**
Cardinality defines the **relationship type** between tables:

* **One-to-One (1:1)**
* **One-to-Many (1:*)**
* **Many-to-One (*:1)**
* **Many-to-Many (*:*)**

🔹 Most common: One-to-Many (e.g., Customer–Sales).

---

### **30. What is Cross Filter Direction?**

**Answer:**
Cross-filter direction defines how filters flow between tables in relationships:

* **Single:** Filters flow one way (default).
* **Both:** Filters propagate both ways (use carefully — can affect performance or cause ambiguity).

---

### **31. What are Active and Inactive Relationships?**

**Answer:**

* **Active Relationship:** Used by default in calculations (solid line).
* **Inactive Relationship:** Exists but not used unless activated using `USERELATIONSHIP()` in DAX.

🔹 Example:

```DAX
Sales_Using_ShipDate = CALCULATE([Total Sales], USERELATIONSHIP(Sales[ShipDate], Date[Date]))
```

---

### **32. What is a Star Schema?**

**Answer:**
A **Star Schema** is a data model with:

* One **central fact table**
* Connected **dimension tables**

🟢 Preferred in Power BI because it improves **query performance**, **simplicity**, and **DAX efficiency**.

---

### **33. What is a Snowflake Schema?**

**Answer:**
A **Snowflake Schema** normalizes dimensions into multiple related tables.
E.g., *Customer* → *Region* → *Country*.
❌ Not ideal for Power BI — causes complex joins and slower queries.

---

### **34. What is a Many-to-Many Relationship and how do you handle it?**

**Answer:**
Occurs when both tables contain duplicate keys.
Handled by:

1. Creating a **bridge (junction) table**
2. Using DAX functions like `TREATAS()` or `CROSSFILTER()`

Example:

```DAX
Sales_Bridge = SUMX(
    TREATAS(CustomerRegion[Region], Sales[Region]),
    [Total Sales]
)
```

---

### **35. What is the difference between Calculated Columns and Measures?**

| Type        | Calculated Column         | Measure                                                  |
| ----------- | ------------------------- | -------------------------------------------------------- |
| Evaluation  | Row-by-row                | Aggregate context                                        |
| Storage     | Consumes memory           | Virtual (no storage)                                     |
| Performance | Slower                    | Faster                                                   |
| Example     | Profit = [Sales] - [Cost] | Total Profit = SUMX(Sales, Sales[Revenue] - Sales[Cost]) |

---

### **36. What are Hierarchies in Power BI?**

**Answer:**
Hierarchies organize data into levels for drill-down analysis.
Example:
**Date Hierarchy:** Year → Quarter → Month → Day.
Created in the **Model view** or directly in visuals.

---

### **37. What is a Surrogate Key?**

**Answer:**
A **system-generated key (e.g., integer ID)** used to uniquely identify a record when no natural key exists — improves performance and simplifies joins.

---

### **38. What are Aggregation Tables?**

**Answer:**
Aggregation tables store **pre-summarized data** (like daily sales totals) to speed up queries on large datasets.
They are linked with **aggregation awareness** in Power BI for performance optimization.

---

### **39. What is Auto Date/Time in Power BI?**

**Answer:**
Auto Date/Time automatically creates hidden date tables for each date column to enable time intelligence.
🔸 Disable it for large models and instead create a **custom Date table**.

---

### **40. What is a Composite Model?**

**Answer:**
Composite models allow combining **Import** and **DirectQuery** tables in the same dataset.
Useful for real-time data scenarios with cached history.

---

## ⚙️ **SECTION 4: DAX (Data Analysis Expressions) (Q41–Q70)**

---

### **41. What is DAX?**

**Answer:**
**DAX (Data Analysis Expressions)** is a formula language in Power BI, Excel, and SSAS used to define **custom calculations** for measures, columns, and tables.

---

### **42. Difference between Calculated Column and Measure (in DAX context)?**

**Answer:**

* **Calculated Column:** Computed per row and stored in the model.
* **Measure:** Calculated on the fly based on user interactions.

Example:

```DAX
-- Calculated Column
Profit = Sales[Revenue] - Sales[Cost]

-- Measure
Total Profit = SUMX(Sales, Sales[Revenue] - Sales[Cost])
```

---

### **43. What is Row Context and Filter Context?**

**Answer:**

* **Row Context:** Exists when iterating over table rows (e.g., in `SUMX`, `FILTER`).
* **Filter Context:** Created by filters/slicers in a report.
  Understanding both is crucial for correct DAX evaluation.

---

### **44. What is Context Transition?**

**Answer:**
Occurs when **row context** is converted into **filter context**, usually via `CALCULATE()`.

Example:

```DAX
TotalSales = CALCULATE(SUM(Sales[Amount]))
```

`CALCULATE()` changes the context so filters apply properly.

---

### **45. What is the CALCULATE function used for?**

**Answer:**
`CALCULATE()` modifies the filter context to evaluate an expression under new conditions.

Example:

```DAX
Sales_West = CALCULATE([Total Sales], Region[Name] = "West")
```

---

### **46. What is the difference between SUM and SUMX?**

| Function | Description                                        |
| -------- | -------------------------------------------------- |
| SUM      | Adds up a single column directly                   |
| SUMX     | Iterates through rows and calculates an expression |

Example:

```DAX
Total Profit = SUMX(Sales, Sales[Revenue] - Sales[Cost])
```

---

### **47. What are Iterator Functions in DAX?**

**Answer:**
Iterators perform row-by-row calculations.
Examples: `SUMX`, `AVERAGEX`, `COUNTX`, `RANKX`, `FILTER`.

---

### **48. What is the purpose of FILTER() in DAX?**

**Answer:**
`FILTER()` returns a table filtered by conditions — often used inside `CALCULATE()`.

Example:

```DAX
HighValueSales = CALCULATE([Total Sales], FILTER(Sales, Sales[Amount] > 10000))
```

---

### **49. What is the ALL() function in DAX?**

**Answer:**
Removes filters from a column or table — used for calculating **% of total**.

Example:

```DAX
% of Total Sales = [Total Sales] / CALCULATE([Total Sales], ALL(Sales))
```

---

### **50. What is REMOVEFILTERS()?**

**Answer:**
Similar to `ALL()` but doesn’t alter relationships. Introduced in newer DAX versions for better clarity.

---

### **51. What are RELATED() and RELATEDTABLE()?**

**Answer:**

* `RELATED()` – fetches a value from a **related table (one-side)**
* `RELATEDTABLE()` – fetches a **table from related rows (many-side)**

Example:

```DAX
CustomerRegion = RELATED(Customer[Region])
```

---

### **52. What is USERELATIONSHIP() used for?**

**Answer:**
Activates an **inactive relationship** for a calculation.
Example:

```DAX
SalesByShipDate = CALCULATE([Total Sales], USERELATIONSHIP(Sales[ShipDate], Date[Date]))
```

---

### **53. What are Time Intelligence functions in DAX?**

**Answer:**
Used for **date-based analysis**:

* `TOTALYTD()`
* `DATESYTD()`
* `SAMEPERIODLASTYEAR()`
* `DATEADD()`
* `PREVIOUSMONTH()`

Example:

```DAX
YTD Sales = TOTALYTD([Total Sales], 'Date'[Date])
```

---

### **54. Difference between SAMEPERIODLASTYEAR() and PARALLELPERIOD()**

| Function           | Description                                   |
| ------------------ | --------------------------------------------- |
| SAMEPERIODLASTYEAR | Shifts current period by 1 year               |
| PARALLELPERIOD     | Shifts by any interval (month, quarter, year) |

---

### **55. What is the EARLIER() function?**

**Answer:**
Used to access a **previous row context** in calculated columns.

Example:

```DAX
Rank = RANKX(FILTER(Sales, Sales[Product] = EARLIER(Sales[Product])), Sales[Amount])
```

---

### **56. How to calculate Running Total in DAX?**

```DAX
RunningTotal = 
CALCULATE(
    [Total Sales],
    FILTER(
        ALL('Date'[Date]),
        'Date'[Date] <= MAX('Date'[Date])
    )
)
```

---

### **57. How to calculate Percentage of Total?**

```DAX
% of Total Sales =
DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Sales)))
```

---

### **58. How to calculate Distinct Count?**

```DAX
UniqueCustomers = DISTINCTCOUNT(Sales[CustomerID])
```

---

### **59. Difference between VALUES() and DISTINCT()**

| Function   | Description                                      |
| ---------- | ------------------------------------------------ |
| VALUES()   | Returns unique values **with filter context**    |
| DISTINCT() | Returns unique values **without filter context** |

---

### **60. What is DIVIDE() used for?**

**Answer:**
Safer alternative to `/` operator — avoids divide-by-zero errors.

```DAX
Profit Margin = DIVIDE([Profit], [Revenue])
```

---

### **61. What is VAR in DAX?**

**Answer:**
`VAR` defines variables for intermediate calculation.

```DAX
Profit Margin =
VAR TotalProfit = [Total Sales] - [Total Cost]
VAR Margin = DIVIDE(TotalProfit, [Total Sales])
RETURN Margin
```

---

### **62. What are the differences between DAX and SQL?**

| Feature    | DAX                 | SQL              |
| ---------- | ------------------- | ---------------- |
| Purpose    | In-memory analytics | Database queries |
| Output     | Aggregated results  | Tabular results  |
| Context    | Filter-based        | Row-based        |
| Evaluation | Dynamic             | Static           |

---

### **63. What is SWITCH() in DAX?**

**Answer:**
Similar to CASE statement in SQL.

```DAX
Rating = 
SWITCH(
    TRUE(),
    [Score] >= 90, "Excellent",
    [Score] >= 75, "Good",
    "Average"
)
```

---

### **64. What is SELECTEDVALUE()?**

**Answer:**
Returns the **current selected value** in context; blank if multiple.

```DAX
SelectedCity = SELECTEDVALUE(City[Name], "Multiple Cities")
```

---

### **65. What are the advantages of using Measures over Calculated Columns?**

* Lighter memory footprint
* Evaluated dynamically
* Faster query performance
* Reusable across visuals

---

### **66. What is a Virtual Table in DAX?**

**Answer:**
A temporary table created using DAX functions (`FILTER`, `SUMMARIZE`, `ADDCOLUMNS`) — used inside calculations but not stored in the model.

---

### **67. What is TREATAS() in DAX?**

**Answer:**
Applies the result of one table as filters on another.

```DAX
Sales_Filtered =
CALCULATE([Total Sales], TREATAS(VALUES(Region[RegionName]), Sales[Region]))
```

---

### **68. What is CROSSFILTER() used for?**

**Answer:**
Temporarily changes relationship direction.

```DAX
SalesBoth =
CALCULATE([Total Sales], CROSSFILTER(Customer[ID], Sales[CustID], BOTH))
```

---

### **69. What is ISFILTERED() used for?**

**Answer:**
Returns TRUE if a column or table is filtered.

```DAX
IsFilteredRegion = IF(ISFILTERED(Region[Name]), "Filtered", "Not Filtered")
```

---

### **70. What is SUMMARIZE() in DAX?**

**Answer:**
Creates a **summary table** by grouping.

```DAX
Summary =
SUMMARIZE(Sales, Customer[Region], "Total Sales", [Total Sales])
```

---

Perfect ✅ — Here’s **Part 3** of your **Power BI Interview Q&A Guide (for 4 + Years Experience)**
We’ll now cover:
📊 **Visualizations (Q71–Q90)**
⚙️ **Performance Optimization (Q91–Q105)**
🌐 **Real-World Scenarios (Q106–Q120)**

Each answer is **interview-ready**, but also detailed enough for **hands-on revision**.

---

# 🧩 Power BI Interview Questions & Answers – Part 3

---

## 🟦 SECTION 5 – Visualizations (Q71–Q90)

---

### **71. What are the different visualization types available in Power BI?**

**Answer:**
Common categories:

* **Charts:** Column, Bar, Line, Pie, Area, Combo
* **Advanced:** Waterfall, Funnel, Scatter, Decomposition Tree, Histogram
* **KPIs & Cards:** Card, Multi-Row Card, Gauge, KPI
* **Tables:** Table, Matrix
* **Maps:** Filled Map, ArcGIS, Shape Map
* **AI visuals:** Key Influencers, Smart Narrative
* **Custom visuals:** Marketplace visuals (e.g., Bullet, Gantt, Chiclet Slicer)

---

### **72. What is a Slicer?**

A slicer is an **on-canvas filter** that lets users interactively restrict data shown in visuals (e.g., select Region = “West”).
You can sync slicers across multiple pages or make them single/multi-select.

---

### **73. Difference between Filter and Slicer**

| Aspect           | Filter                    | Slicer             |
| ---------------- | ------------------------- | ------------------ |
| Location         | Pane (side panel)         | Visual on report   |
| User interaction | Hidden                    | Interactive        |
| Use case         | Developer-level filtering | End-user filtering |

---

### **74. What are Bookmarks in Power BI?**

Bookmarks **capture a report’s state** (filters, visuals, page).
They enable:

* Storytelling / navigation
* Reset or toggle buttons
  Example : “Show Top 10” vs “Show All” views.

---

### **75. What is Drill-Down vs Drill-Through?**

* **Drill-Down:** Explore hierarchy within the same visual (Year → Quarter → Month).
* **Drill-Through:** Navigate to another page focusing on one item (e.g., customer details).
  👉 Enable by right-click → Drill Through.

---

### **76. What are Tooltips?**

Tooltips display contextual details when hovering over visuals.
You can create:

* **Default tooltips** (auto)
* **Custom tooltip pages** (fully designed mini-reports)

---

### **77. What is a KPI visual?**

Shows progress toward a goal.
Elements: **Indicator (value)**, **Target**, **Trend (Axis)**.
Example: KPI comparing actual sales vs target for current month.

---

### **78. What are Field Parameters?**

Field Parameters allow users to **dynamically switch dimensions or measures** in visuals.
Created via Modeling → New Parameter → Fields.
Example: Switch between “Sales by Product” and “Sales by Region”.

---

### **79. What is Conditional Formatting?**

Used to format colors or text based on values.
Examples:

* Change bar color if Sales < Target
* Gradient color by Profit margin

---

### **80. What is the difference between Matrix and Table visuals?**

| Visual | Description                                                     |
| ------ | --------------------------------------------------------------- |
| Table  | Flat structure (rows & columns)                                 |
| Matrix | Pivot-like, supports row & column groups, subtotals, drill-down |

---

### **81. How to display Top N values dynamically in Power BI?**

Steps:

1. Create a measure:

   ```DAX
   RankSales = RANKX(ALL(Product[Name]), [Total Sales])
   ```
2. Add slicer parameter for N (e.g., 5 or 10).
3. Filter visual → RankSales ≤ Selected N.

---

### **82. What are Report-Level, Page-Level, and Visual-Level filters?**

* **Report-Level:** Affects all pages.
* **Page-Level:** Affects one page.
* **Visual-Level:** Affects only that chart.

---

### **83. What is the use of Sync Slicers?**

Allows same slicer selection to apply across multiple report pages — controlled from **View → Sync Slicers** pane.

---

### **84. What are Custom Visuals?**

Custom visuals are **3rd-party or in-house developed visuals** imported from AppSource or as `.pbiviz` files.
Example: Bullet Chart, Hierarchy Slicer, Radar Chart.

---

### **85. What is the Decomposition Tree visual?**

AI-powered visual that breaks down a metric (e.g., Sales) into contributing factors (Region → Product → Salesperson) interactively.

---

### **86. What is Smart Narrative?**

Automatically summarizes key insights using natural language — adds **auto-generated text** like “Sales grew 10% MoM”.

---

### **87. What is a Q&A visual?**

Allows users to type natural-language questions (“show sales by region”) → Power BI generates a visual dynamically.

---

### **88. How can you show/hide visuals dynamically?**

Create a DAX measure returning 1/0 and set it as **visual-level filter** (show when = 1).
Example: Show different visuals when “Metric Type” slicer changes.

---

### **89. What is Tooltip Page Navigation?**

Use buttons/bookmarks to navigate between main report and **tooltip detail pages** for deeper context.

---

### **90. How do you create dynamic titles in Power BI?**

Use a DAX measure:

```DAX
DynamicTitle =
"Sales Report for " & SELECTEDVALUE(Region[Name], "All Regions")
```

→ Bind to visual title property using “fx”.

---

## ⚙️ SECTION 6 – Performance Optimization (Q91–Q105)

---

### **91. How do you improve Power BI report performance?**

1. Use Star Schema (modeling best practice).
2. Reduce columns & rows.
3. Use Import mode where possible.
4. Avoid complex DAX on large tables.
5. Use aggregation tables.
6. Optimize data types.
7. Disable Auto Date/Time.
8. Use DAX Studio and Performance Analyzer.

---

### **92. What is Query Folding and why is it important?**

Power Query pushes transformations to the **source** (SQL, etc.) instead of doing them locally.
✅ Keeps processing close to data → faster, less memory usage.
Avoid steps that break folding (e.g., Add Index, Custom Functions).

---

### **93. What is the VertiPaq engine?**

Power BI’s **in-memory columnar engine** that compresses data using dictionaries and stores it efficiently for ultra-fast aggregation queries.

---

### **94. How to reduce dataset size?**

* Remove unnecessary columns/rows
* Use correct data types
* Use measures instead of calculated columns
* Use Aggregations and Summarization
* Disable Auto Date/Time

---

### **95. What are Aggregation tables and how do they help?**

They store **pre-aggregated summaries** (e.g., daily sales) to speed up queries.
Power BI can automatically redirect queries to these smaller tables.

---

### **96. How to identify slow visuals?**

Use **Performance Analyzer** in Power BI Desktop (View → Performance Analyzer).
It shows each visual’s **DAX query time**, **render time**, and **total duration**.

---

### **97. What is the use of DAX Studio?**

External tool to:

* Run and debug DAX queries
* Measure query performance
* Analyze storage and VertiPaq memory
* Export model metadata

---

### **98. What is the difference between Import, DirectQuery, and Composite modes (performance-wise)?**

| Mode        | Storage   | Performance | Freshness           |
| ----------- | --------- | ----------- | ------------------- |
| Import      | In-memory | Fastest     | Stale until refresh |
| DirectQuery | Source    | Slower      | Real-time           |
| Composite   | Hybrid    | Balanced    | Partial real-time   |

---

### **99. What is Incremental Refresh and how does it help performance?**

Loads only **new or changed data** instead of reloading entire dataset.
Uses `RangeStart` & `RangeEnd` parameters.
Speeds up refresh and reduces service load.

---

### **100. What is Aggregation Awareness?**

Power BI automatically routes queries to the smallest possible aggregation table when configured — reducing query time for large datasets.

---

### **101. How can DAX code affect performance?**

Poor patterns (e.g., nested IFs, EARLIER misuse, too many CALCULATE calls) can slow queries.
Best practices:

* Use variables
* Reduce row context iterations
* Replace complex columns with measures

---

### **102. What is a Composite Model and when should you use it?**

Combines **Import** and **DirectQuery** tables.
Useful when you need **real-time data** (DirectQuery) alongside **historical cached data** (Import).

---

### **103. How do you handle schema changes in data source?**

* Enable “Detect data type/structure changes” in Power Query.
* Use parameters for dynamic sources.
* Refresh and edit queries to re-map fields.
* Use Dataflows to decouple transformations.

---

### **104. What is Storage Mode per table?**

Each table can be set to:

* **Import**
* **DirectQuery**
* **Dual (mode)** – acts as Import or DirectQuery depending on context.

---

### **105. How to test report load performance?**

1. Use Performance Analyzer.
2. Measure refresh duration in Service.
3. Monitor Gateway CPU/Memory.
4. Optimize model size & query folding.

---

## 🌐 SECTION 7 – Real-World Scenarios (Q106–Q120)

---

### **106. Scenario – You need to design a Sales Dashboard. What visuals will you use?**

* KPI cards → Sales, Profit, Margin
* Line chart → Trend over time
* Map → Sales by region
* Bar/Column → Top Products / Categories
* Donut → Market share
* Slicer → Year, Region, Product

---

### **107. How would you handle dynamic currency conversion?**

Create a Currency table with exchange rates and use:

```DAX
Sales in USD =
DIVIDE([Total Sales], LOOKUPVALUE(Currency[Rate], Currency[Code], SelectedCurrency))
```

---

### **108. How to manage multiple environments (Dev/Test/Prod)?**

Use **Deployment Pipelines** or separate workspaces for each environment.
Promote content after testing.
Automate using PowerShell or REST API.

---

### **109. How do you implement security for different departments?**

Use **Row-Level Security (RLS)**:

* Create Department table (User–Dept mapping)
* Filter fact table via USERPRINCIPALNAME()
  Example:

```DAX
DeptFilter = Sales[DeptID] = LOOKUPVALUE(UserDept[DeptID], UserDept[Email], USERPRINCIPALNAME())
```

---

### **110. What steps do you take if a report is slow to load?**

1. Identify slow visuals (Performance Analyzer).
2. Optimize DAX and relationships.
3. Limit data and columns.
4. Use Import mode.
5. Check gateway performance.

---

### **111. How to create a rolling 12-month sales measure?**

```DAX
Rolling12M =
CALCULATE(
  [Total Sales],
  DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH)
)
```

---

### **112. How to create a dynamic date filter (Last N days)?**

Create parameter N and measure:

```DAX
LastNDaysSales =
CALCULATE([Total Sales], FILTER('Date', 'Date'[Date] >= TODAY() - N))
```

---

### **113. How to show a message when no data exists?**

Use **Card Visual + DAX**:

```DAX
NoDataMsg =
IF(ISBLANK([Total Sales]), "No data available for selected period", BLANK())
```

---

### **114. How to automate dataset refresh in Power BI Service?**

* Schedule refresh in Service.
* Orchestrate via **Power Automate** (flow → refresh dataset).
* Or trigger through REST API call.

---

### **115. How to integrate Power BI with Azure Data Factory / Databricks?**

* Load processed data to SQL DB / ADLS.
* Connect Power BI to that output path (DirectQuery / Import).
* Optionally use Fabric for Direct Lake mode.

---

### **116. What is a Paginated Report?**

Pixel-perfect, printable reports (like invoices, statements) built with Power BI Report Builder using RDL files.

---

### **117. How to connect Power BI with REST APIs?**

Use **Web connector** in Power Query → Provide API URL + headers → Parse JSON response using “Record to Table” steps.

---

### **118. How does Power BI integrate with Excel?**

* “Analyze in Excel” feature
* Export dataset tables to Excel
* Import Excel Power Query into Power BI

---

### **119. What is Microsoft Fabric and how does it relate to Power BI?**

Fabric is Microsoft’s unified analytics platform (Data Factory + Synapse + Power BI).
Power BI acts as the **visualization and semantic layer**, using **Direct Lake** to query Fabric data instantly.

---

### **120. How to create drill-through between different reports?**

1. Enable cross-report drill-through in Power BI Service.
2. Define target report page with “Drill-through filters”.
3. Link both datasets via shared fields (e.g., Customer ID).

---

