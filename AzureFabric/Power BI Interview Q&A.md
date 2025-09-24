
---

# 🔹 Power BI Interview Q\&A (Beginner → Mid-Level)

---

## **Power BI Basics**

1. **What is Power BI?**
   → A Microsoft business intelligence tool for data visualization, modeling, and reporting, with cloud and desktop versions.

2. **What are the main components of Power BI?**

   * Power BI Desktop
   * Power BI Service (Cloud)
   * Power BI Mobile
   * Power BI Report Server
   * Power BI Gateway

3. **Difference between Power BI Desktop and Power BI Service?**
   → Desktop = Development tool for building reports.
   Service = Cloud platform for publishing, sharing, and collaboration.

4. **What data sources can Power BI connect to?**
   → 100+ sources: SQL Server, Excel, Azure, Oracle, SharePoint, APIs, etc.

5. **What are Power BI building blocks?**
   → Datasets, Reports, Dashboards, Tiles, and Workspaces.

---

## **Data Loading & Modeling**

6. **What is Power Query in Power BI?**
   → ETL tool (Extract, Transform, Load) for cleaning and transforming data before modeling.

7. **What is the difference between DirectQuery and Import Mode?**

   * **Import**: Data copied into Power BI in-memory model.
   * **DirectQuery**: Data stays in source; queries run in real-time.

8. **When would you use DirectQuery over Import?**
   → When working with large datasets or near real-time reporting needs.

9. **What is a Dataflow in Power BI?**
   → A cloud-based ETL pipeline in Power BI Service that allows reuse of transformations across multiple reports.

10. **What are Relationships in Power BI?**
    → Connections between tables (one-to-many, many-to-many) that enable combined analysis.

---

## **DAX (Data Analysis Expressions)**

11. **What is DAX in Power BI?**
    → A formula language used for creating measures, calculated columns, and calculated tables.

12. **Difference between Calculated Column and Measure?**

* **Calculated Column**: Stored in table; evaluated row by row.
* **Measure**: Calculated on the fly based on filters/context.

13. **What is Row Context in DAX?**
    → The current row being evaluated (mostly applies in calculated columns).

14. **What is Filter Context in DAX?**
    → The set of filters applied when evaluating a measure.

15. **Example: Write a DAX to calculate Year-to-Date Sales.**

```DAX
YTD Sales = TOTALYTD(SUM(Sales[SalesAmount]), 'Date'[Date])
```

---

## **Visualizations & Reports**

16. **What is the difference between Report and Dashboard in Power BI?**

* **Report**: Multi-page, detailed visualization.
* **Dashboard**: Single-page summary with pinned visuals from multiple reports.

17. **What are Slicers in Power BI?**
    → Visual filters that allow interactive selection of values.

18. **What are Bookmarks in Power BI?**
    → A feature to save report states for storytelling and navigation.

19. **What are Drillthrough pages?**
    → Pages designed to show details of a selected data point.

20. **What is Q\&A in Power BI?**
    → Natural language query feature that allows users to ask questions in plain English.

---

## **Power BI Service & Sharing**

21. **What are Workspaces in Power BI Service?**
    → Collaborative environments where teams build, publish, and manage reports and dashboards.

22. **What are Apps in Power BI?**
    → Packaged dashboards/reports shared with users for consumption.

23. **What are Power BI Gateways?**
    → Bridge that enables secure data transfer between on-premises data sources and Power BI Service.

24. **Difference between Personal Gateway and Enterprise Gateway?**

* **Personal**: User-level, only for refresh in Power BI Service.
* **Enterprise**: Org-level, supports multiple sources, live connections, and DirectQuery.

25. **What is Scheduled Refresh in Power BI?**
    → Automatic refresh of imported datasets at defined intervals.

---

## **Performance Optimization**

26. **How to improve Power BI report performance?**

* Use star schema
* Avoid too many visuals
* Use aggregations
* Optimize DAX
* Reduce dataset size

27. **Difference between Star Schema and Snowflake Schema?**

* **Star Schema**: Fact table with denormalized dimension tables.
* **Snowflake**: Fact table with normalized dimension tables.

28. **What is Aggregation in Power BI?**
    → Pre-calculated summaries (like totals) stored for faster query performance.

29. **What is Query Folding in Power Query?**
    → When transformations are pushed back to the data source for execution instead of happening in Power BI.

30. **What is Composite Model in Power BI?**
    → A model that combines **Import + DirectQuery** modes in a single dataset.

---

## **Security & Governance**

31. **What is Row-Level Security (RLS) in Power BI?**
    → Restricting data access for users by applying filters at the row level.

32. **What is Object-Level Security (OLS) in Power BI?**
    → Restricting access to specific tables or columns.

33. **What is Sensitivity Label in Power BI?**
    → A Microsoft Purview label to classify and protect sensitive data.

34. **What is Tenant-Level vs Workspace-Level Security?**

* **Tenant-Level**: Global Power BI settings for the entire organization.
* **Workspace-Level**: Access controls for specific reports/dashboards.

35. **Can Power BI integrate with Active Directory?**
    → Yes, for user authentication and role assignments.

---

## **Advanced & Integration**

36. **How does Power BI integrate with Excel?**
    → You can publish Excel models to Power BI, connect Excel to Power BI datasets, or analyze Power BI data in Excel.

37. **Difference between Power BI and Tableau?**

* **Power BI**: Strong Microsoft ecosystem, lower cost, native Azure/Office 365 integration.
* **Tableau**: Strong visual flexibility, works well with multi-cloud.

38. **What is Paginated Report in Power BI?**
    → Pixel-perfect reports for printing/exporting, built using Power BI Report Builder.

39. **What is Power BI Embedded?**
    → A service that allows embedding Power BI reports into custom applications.

40. **What is Direct Lake mode in Power BI (Fabric)?**
    → A mode where Power BI directly queries **Delta tables in OneLake** without import or DirectQuery, giving real-time speed with in-memory performance.

---
