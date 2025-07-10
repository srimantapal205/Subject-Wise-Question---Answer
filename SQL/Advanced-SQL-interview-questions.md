# Advanced SQL interview questions

---

### 🔷 **Window Functions**

Here is a detailed explanation with examples for each of your SQL window function questions:

---

### **1. What is a window function in SQL? How is it different from aggregate functions?**

**Window Function:**
A window function performs a calculation across a set of table rows that are somehow related to the current row. Unlike aggregate functions, window functions **do not group rows into a single output row**—they **preserve the number of rows** in the result set.

**Key Syntax:**

```sql
function_name(...) OVER (PARTITION BY ... ORDER BY ...)
```

**Aggregate Function vs Window Function:**

| Feature       | Aggregate Function      | Window Function                                 |
| ------------- | ----------------------- | ----------------------------------------------- |
| Rows returned | Reduces rows (GROUP BY) | Keeps all rows                                  |
| Example       | `SUM(salary)`           | `SUM(salary) OVER (PARTITION BY department_id)` |
| Use case      | Summary reports         | Running totals, rankings, moving averages       |

**Example:**

```sql
-- Aggregate Function
SELECT department_id, SUM(salary) 
FROM employees
GROUP BY department_id;

-- Window Function
SELECT employee_id, department_id, salary,
       SUM(salary) OVER (PARTITION BY department_id) AS dept_total_salary
FROM employees;
```

---

### **2. Explain the use of `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, and `NTILE()` with examples.**

These are **ranking window functions**, which assign a number to each row based on a specified ordering.

**Dataset:**

```sql
-- employees table
+----+----------+-------------+
| ID | Name     | Salary      |
+----+----------+-------------+
| 1  | Alice    | 5000        |
| 2  | Bob      | 7000        |
| 3  | Charlie  | 7000        |
| 4  | David    | 4000        |
+----+----------+-------------+
```

#### **ROW\_NUMBER()**

Assigns a unique number to each row, regardless of duplicate values.

```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;
```

**Output:**

```
Bob – 7000 – 1  
Charlie – 7000 – 2  
Alice – 5000 – 3  
David – 4000 – 4
```

#### **RANK()**

Gives the same rank for duplicate values but **skips** the next ranks.

```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
```

**Output:**

```
Bob – 7000 – 1  
Charlie – 7000 – 1  
Alice – 5000 – 3  
David – 4000 – 4
```

#### **DENSE\_RANK()**

Like `RANK()` but does **not skip** ranks.

```sql
SELECT name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;
```

**Output:**

```
Bob – 7000 – 1  
Charlie – 7000 – 1  
Alice – 5000 – 2  
David – 4000 – 3
```

#### **NTILE(n)**

Distributes rows into `n` buckets (approximately equal-sized groups).

```sql
SELECT name, salary,
       NTILE(2) OVER (ORDER BY salary DESC) AS bucket
FROM employees;
```

**Output:**

```
Bob – 7000 – 1  
Charlie – 7000 – 1  
Alice – 5000 – 2  
David – 4000 – 2
```

---

### **3. How would you calculate a running total using window functions?**

**Running Total = cumulative sum of a column ordered by some field.**

```sql
SELECT employee_id, salary,
       SUM(salary) OVER (ORDER BY employee_id) AS running_total
FROM employees;
```

**If partitioned by department:**

```sql
SELECT employee_id, department_id, salary,
       SUM(salary) OVER (PARTITION BY department_id ORDER BY employee_id) AS running_total
FROM employees;
```

---

### **4. Difference between `PARTITION BY` and `GROUP BY`**

| Feature     | `GROUP BY`                   | `PARTITION BY` (used with window functions) |
| ----------- | ---------------------------- | ------------------------------------------- |
| Output rows | Aggregates rows (fewer rows) | Does not reduce row count                   |
| Scope       | Applies to the entire query  | Applies to the window function only         |
| Use case    | Summarization reports        | Rankings, running totals, moving averages   |

**Example:**

```sql
-- GROUP BY example
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;

-- PARTITION BY example (retains all rows)
SELECT employee_id, department_id, salary,
       AVG(salary) OVER (PARTITION BY department_id) AS avg_dept_salary
FROM employees;
```

---

### **5. Use a window function to find the second highest salary in each department**

```sql
WITH RankedSalaries AS (
  SELECT employee_id, department_id, salary,
         DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
  FROM employees
)
SELECT *
FROM RankedSalaries
WHERE salary_rank = 2;
```

---

### **6. How to calculate a moving average or cumulative sum with window functions?**

#### **Cumulative Sum (Running Total):**

```sql
SELECT employee_id, salary,
       SUM(salary) OVER (ORDER BY employee_id) AS running_total
FROM employees;
```

#### **Moving Average (e.g., 3-row window):**

```sql
SELECT employee_id, salary,
       AVG(salary) OVER (ORDER BY employee_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
FROM employees;
```

* `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means:

  * Take current row and 2 previous rows → 3-row window.
* You can also use `RANGE` if based on values instead of row positions.


---

### 🔷 **Query Optimization & Performance**

Here are the revised **SQL performance tuning and optimization** questions starting from **question number 7**, each explained in detail with examples:

---

### **7. How do you identify slow SQL queries?**

To identify slow SQL queries, you can use the following techniques:

#### ✅ **Tools & Methods:**

* **Execution time analysis** (e.g., SQL Server Profiler, EXPLAIN/EXPLAIN PLAN).
* **Slow query logs** (MySQL has a built-in slow query log feature).
* **Query profiling** (`SHOW PROFILE` in MySQL).
* **Database monitoring tools** (e.g., pgBadger, AWS Performance Insights, SQL Monitor).

#### ✅ **Common Indicators of Slow Queries:**

* High **I/O waits**
* **Full table scans**
* High **CPU usage**
* Use of **temporary tables** or **filesort**
* **Missing indexes**

---

### **8. Explain the concept of a *query execution plan*. How do you read one?**

A **query execution plan** shows how the database engine will execute a SQL statement, including the operations (scans, joins, sorts) and their order.

#### ✅ How to view:

* **MySQL:** `EXPLAIN SELECT ...`
* **PostgreSQL:** `EXPLAIN ANALYZE SELECT ...`
* **SQL Server:** Use **"Display Estimated Execution Plan"** or `SET SHOWPLAN_ALL ON`

#### ✅ Key elements:

| Element    | Meaning                                              |
| ---------- | ---------------------------------------------------- |
| Seq Scan   | Sequential table scan (inefficient for large tables) |
| Index Scan | Uses an index (better)                               |
| Filter     | Rows filtered (can slow down performance)            |
| Join Type  | Nested Loop, Hash Join, Merge Join                   |
| Cost       | Estimated cost (lower is better)                     |

#### ✅ Example:

```sql
EXPLAIN SELECT name FROM employees WHERE department_id = 5;
```

Look for:

* **"type"** column: `ALL` = full scan, `index` = index used
* **"key"** column: shows which index is used

---

### **9. What are the best practices to optimize a SQL query?**

Here are some important optimization techniques:

#### ✅ Best Practices:

* **Use proper indexes** on filter (`WHERE`) and join columns
* \*\*Avoid SELECT \*\*\* – retrieve only needed columns
* **Use WHERE clauses** to limit result set
* **Avoid functions on indexed columns** (`WHERE UPPER(name) = 'X'` disables index)
* **Use EXISTS instead of IN** for subqueries with large results
* **Use LIMIT** when fetching top records
* **Avoid correlated subqueries** in SELECT clause
* **Partition large tables** for better performance
* **Analyze and vacuum** (in PostgreSQL) to update statistics

---

### **10. How do indexes affect query performance?**

Indexes improve query performance by reducing the number of rows scanned.

#### ✅ Benefits:

* Speed up **SELECT**, **JOIN**, **WHERE**, **ORDER BY**
* Can **eliminate the need for table scan**

#### ✅ Downsides:

* Slower **INSERT/UPDATE/DELETE** due to index maintenance
* Requires **storage space**

#### ✅ Example:

```sql
-- Index speeds up this query
CREATE INDEX idx_emp_dept ON employees(department_id);

SELECT * FROM employees WHERE department_id = 5;
```

---

### **11. When should you use a *covering index*?**

A **covering index** is an index that contains **all the columns** needed by a query—meaning the database can fulfill the query **without accessing the table (no table lookup needed)**.

#### ✅ Benefits:

* Boosts performance significantly for **read-heavy queries**
* Eliminates **random I/O**

#### ✅ Example:

```sql
-- Index includes all needed columns
CREATE INDEX idx_cover ON employees(department_id, name, salary);

SELECT name, salary FROM employees WHERE department_id = 3;
```

---

### **12. How would you optimize a slow join between two large tables?**

#### ✅ Techniques:

1. **Use indexes** on join columns
2. **Avoid joining large intermediate results**
3. **Use EXISTS** instead of JOIN if only existence is needed
4. **Break query into smaller parts** (CTEs or temp tables)
5. **Filter rows before joining** (apply WHERE early)
6. **Use appropriate join types**:

   * Nested loop = good for small datasets
   * Hash join = good for large joins
7. **Partitioning** large tables may help

#### ✅ Example:

```sql
-- Ensure indexes exist on joining columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

SELECT o.order_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date > '2024-01-01';
```

---

### **13. Difference between `EXISTS` vs `IN` vs `JOIN` – which is faster and when?**

#### ✅ `IN`:

* Compares value to a list
* **Slow** for large subqueries
* **Can return wrong results** if NULLs are involved

```sql
SELECT name FROM employees WHERE department_id IN (SELECT id FROM departments);
```

#### ✅ `EXISTS`:

* Checks **whether rows exist**
* Stops on first match = **faster for large data**

```sql
SELECT name FROM employees e 
WHERE EXISTS (SELECT 1 FROM departments d WHERE e.department_id = d.id);
```

#### ✅ `JOIN`:

* Combines rows from two tables
* **Returns additional data**, not just existence
* May return **duplicate rows** unless DISTINCT is used

```sql
SELECT e.name, d.name FROM employees e
JOIN departments d ON e.department_id = d.id;
```

#### ✅ Performance Summary:

| Use case                    | Best choice                                     |
| --------------------------- | ----------------------------------------------- |
| Check existence only        | `EXISTS`                                        |
| Small subquery              | `IN`                                            |
| Need data from both tables  | `JOIN`                                          |
| Subquery returns large data | Avoid `IN`, use `EXISTS` or `JOIN` with filters |


---

### 🔷 **Indexing and Storage**

Here are your **SQL indexing-related questions**, renumbered starting from **question 14**, with detailed explanations and examples:

---

### **14. What are the types of indexes in SQL?**

SQL databases support several types of indexes, depending on the engine:

#### ✅ Common Types:

| Index Type              | Description                                                                     |
| ----------------------- | ------------------------------------------------------------------------------- |
| **Clustered Index**     | Determines the physical order of data in the table (only one per table)         |
| **Non-Clustered Index** | Separate from data; contains pointers to the data                               |
| **Unique Index**        | Ensures all values in the indexed column are unique                             |
| **Composite Index**     | Index on two or more columns                                                    |
| **Full-text Index**     | Used for fast text searching (e.g., articles, documents)                        |
| **Bitmap Index**        | Uses bitmaps, efficient for low-cardinality columns (common in data warehouses) |
| **Spatial Index**       | Optimized for geographical data types (e.g., PostGIS)                           |

#### ✅ Example:

```sql
-- Create a non-clustered index
CREATE INDEX idx_emp_name ON employees(name);

-- Composite index
CREATE INDEX idx_emp_dept_salary ON employees(department_id, salary);
```

---

### **15. What is a *clustered vs non-clustered index*?**

#### ✅ Clustered Index:

* Sorts and stores the data rows **physically** in order.
* Only **one clustered index per table**.
* Faster for **range queries**.

#### ✅ Non-Clustered Index:

* Has a **separate structure** from the data.
* Points to actual data rows via **row locators**.
* Can have **multiple non-clustered indexes** per table.

#### ✅ Analogy:

* **Clustered index** = table of contents that also holds the content.
* **Non-clustered index** = index at the back of a book with page references.

#### ✅ Example (SQL Server / MySQL):

```sql
-- Clustered index on primary key
CREATE TABLE employees (
  id INT PRIMARY KEY, -- this becomes a clustered index
  name VARCHAR(50),
  salary INT
);

-- Non-clustered index
CREATE INDEX idx_name ON employees(name);
```

---

### **16. What is an *index scan* vs *index seek*?**

| Term           | Meaning                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| **Index Seek** | Efficient; the database **navigates directly** to matching rows using the index. |
| **Index Scan** | Slower; scans the **entire index**, even if only a few rows match.               |

#### ✅ Example:

Given an index on `salary`:

```sql
-- Index Seek (uses equality condition)
SELECT * FROM employees WHERE salary = 5000;

-- Index Scan (broad condition or function on column)
SELECT * FROM employees WHERE salary > 5000;
SELECT * FROM employees WHERE UPPER(name) = 'ALICE'; -- function disables index
```

Use `EXPLAIN` or `QUERY PLAN` to observe whether the optimizer chooses **seek** or **scan**.

---

### **17. When should you avoid indexing a column?**

While indexes boost read performance, there are cases where indexing is **not beneficial or even harmful**.

#### ❌ Avoid Indexing When:

1. **Low selectivity** (e.g., gender, status flags like "active/inactive")
2. **Small tables** (index overhead > benefit)
3. **Columns frequently updated** (causes index maintenance overhead)
4. **Volatile tables** (frequent insert/delete operations)
5. **Functions applied to indexed column** in WHERE clause (can disable index)

#### ✅ Example:

```sql
-- Avoid indexing columns with few distinct values:
-- bad candidate for index
ALTER TABLE users ADD INDEX idx_is_active (is_active);
```

---

### **18. Explain the concept of a *bitmap index* and its use case.**

A **bitmap index** uses a **bit array** (0s and 1s) to represent the existence of values. It is highly efficient for columns with **low cardinality** (few distinct values).

#### ✅ Use Cases:

* Analytical workloads, OLAP systems
* Columns like gender, status, region, etc.
* Data warehouses

#### ✅ Benefits:

* Very space-efficient
* Fast for complex **AND/OR** conditions

#### ✅ Drawbacks:

* Not suitable for high-concurrency OLTP systems (locking issues)

#### ✅ Example (Oracle syntax):

```sql
CREATE BITMAP INDEX idx_gender ON employees(gender);
```

---

### **19. How to analyze index fragmentation and fix it?**

**Index fragmentation** occurs when the logical order of pages does not match physical order—affecting performance.

#### ✅ How to check (SQL Server):

```sql
SELECT index_id, avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('employees'), NULL, NULL, 'LIMITED');
```

#### ✅ Fixing Fragmentation:

| Fragmentation Level | Action     |
| ------------------- | ---------- |
| < 10%               | No action  |
| 10–30%              | REORGANIZE |
| > 30%               | REBUILD    |

#### ✅ Commands (SQL Server):

```sql
-- Reorganize (online)
ALTER INDEX idx_name ON employees REORGANIZE;

-- Rebuild (offline by default)
ALTER INDEX idx_name ON employees REBUILD;
```


---

### 🔷 **Advanced Joins & Subqueries**



---

### **14. What are the types of indexes in SQL?**

SQL databases support several types of indexes, depending on the engine:

#### ✅ Common Types:

| Index Type              | Description                                                                     |
| ----------------------- | ------------------------------------------------------------------------------- |
| **Clustered Index**     | Determines the physical order of data in the table (only one per table)         |
| **Non-Clustered Index** | Separate from data; contains pointers to the data                               |
| **Unique Index**        | Ensures all values in the indexed column are unique                             |
| **Composite Index**     | Index on two or more columns                                                    |
| **Full-text Index**     | Used for fast text searching (e.g., articles, documents)                        |
| **Bitmap Index**        | Uses bitmaps, efficient for low-cardinality columns (common in data warehouses) |
| **Spatial Index**       | Optimized for geographical data types (e.g., PostGIS)                           |

#### ✅ Example:

```sql
-- Create a non-clustered index
CREATE INDEX idx_emp_name ON employees(name);

-- Composite index
CREATE INDEX idx_emp_dept_salary ON employees(department_id, salary);
```

---

### **15. What is a *clustered vs non-clustered index*?**

#### ✅ Clustered Index:

* Sorts and stores the data rows **physically** in order.
* Only **one clustered index per table**.
* Faster for **range queries**.

#### ✅ Non-Clustered Index:

* Has a **separate structure** from the data.
* Points to actual data rows via **row locators**.
* Can have **multiple non-clustered indexes** per table.

#### ✅ Analogy:

* **Clustered index** = table of contents that also holds the content.
* **Non-clustered index** = index at the back of a book with page references.

#### ✅ Example (SQL Server / MySQL):

```sql
-- Clustered index on primary key
CREATE TABLE employees (
  id INT PRIMARY KEY, -- this becomes a clustered index
  name VARCHAR(50),
  salary INT
);

-- Non-clustered index
CREATE INDEX idx_name ON employees(name);
```

---

### **16. What is an *index scan* vs *index seek*?**

| Term           | Meaning                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| **Index Seek** | Efficient; the database **navigates directly** to matching rows using the index. |
| **Index Scan** | Slower; scans the **entire index**, even if only a few rows match.               |

#### ✅ Example:

Given an index on `salary`:

```sql
-- Index Seek (uses equality condition)
SELECT * FROM employees WHERE salary = 5000;

-- Index Scan (broad condition or function on column)
SELECT * FROM employees WHERE salary > 5000;
SELECT * FROM employees WHERE UPPER(name) = 'ALICE'; -- function disables index
```

Use `EXPLAIN` or `QUERY PLAN` to observe whether the optimizer chooses **seek** or **scan**.

---

### **17. When should you avoid indexing a column?**

While indexes boost read performance, there are cases where indexing is **not beneficial or even harmful**.

#### ❌ Avoid Indexing When:

1. **Low selectivity** (e.g., gender, status flags like "active/inactive")
2. **Small tables** (index overhead > benefit)
3. **Columns frequently updated** (causes index maintenance overhead)
4. **Volatile tables** (frequent insert/delete operations)
5. **Functions applied to indexed column** in WHERE clause (can disable index)

#### ✅ Example:

```sql
-- Avoid indexing columns with few distinct values:
-- bad candidate for index
ALTER TABLE users ADD INDEX idx_is_active (is_active);
```

---

### **18. Explain the concept of a *bitmap index* and its use case.**

A **bitmap index** uses a **bit array** (0s and 1s) to represent the existence of values. It is highly efficient for columns with **low cardinality** (few distinct values).

#### ✅ Use Cases:

* Analytical workloads, OLAP systems
* Columns like gender, status, region, etc.
* Data warehouses

#### ✅ Benefits:

* Very space-efficient
* Fast for complex **AND/OR** conditions

#### ✅ Drawbacks:

* Not suitable for high-concurrency OLTP systems (locking issues)

#### ✅ Example (Oracle syntax):

```sql
CREATE BITMAP INDEX idx_gender ON employees(gender);
```

---

### **19. How to analyze index fragmentation and fix it?**

**Index fragmentation** occurs when the logical order of pages does not match physical order—affecting performance.

#### ✅ How to check (SQL Server):

```sql
SELECT index_id, avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('employees'), NULL, NULL, 'LIMITED');
```

#### ✅ Fixing Fragmentation:

| Fragmentation Level | Action     |
| ------------------- | ---------- |
| < 10%               | No action  |
| 10–30%              | REORGANIZE |
| > 30%               | REBUILD    |

#### ✅ Commands (SQL Server):

```sql
-- Reorganize (online)
ALTER INDEX idx_name ON employees REORGANIZE;

-- Rebuild (offline by default)
ALTER INDEX idx_name ON employees REBUILD;
```


---

### 🔷 **Common Table Expressions (CTE)**


---

### **20. What is a CTE? How is it different from a subquery?**

**CTE (Common Table Expression)** is a temporary result set defined using the `WITH` clause, which can be referred to within a SQL statement.

#### **Syntax:**

```sql
WITH cte_name AS (
   SELECT ...
)
SELECT * FROM cte_name;
```

#### **CTE vs Subquery:**

| Feature     | CTE                                         | Subquery                        |
| ----------- | ------------------------------------------- | ------------------------------- |
| Readability | More readable, especially for complex logic | Less readable when nested       |
| Reusability | Can be referenced multiple times            | Typically not reusable          |
| Recursion   | Supports recursion                          | Cannot be recursive             |
| Debugging   | Easier to debug                             | Harder to trace in deep nesting |

---

### **21. Use a recursive CTE to flatten a hierarchy (e.g., employee-manager tree).**

Assume a table `Employees`:

```sql
CREATE TABLE Employees (
    EmployeeID INT,
    Name VARCHAR(100),
    ManagerID INT
);
```

#### **Recursive CTE to get hierarchy:**

```sql
WITH EmployeeHierarchy AS (
    -- Anchor member: top-level managers (no ManagerID)
    SELECT EmployeeID, Name, ManagerID, 0 AS Level
    FROM Employees
    WHERE ManagerID IS NULL

    UNION ALL

    -- Recursive member: get employees reporting to above
    SELECT e.EmployeeID, e.Name, e.ManagerID, eh.Level + 1
    FROM Employees e
    INNER JOIN EmployeeHierarchy eh
        ON e.ManagerID = eh.EmployeeID
)
SELECT * FROM EmployeeHierarchy
ORDER BY Level, ManagerID;
```

---

### **22. What are the pros and cons of using a CTE?**

#### **Pros:**

* **Improves readability**: Complex queries are easier to understand and manage.
* **Modular structure**: Breaks query logic into parts.
* **Recursive queries**: Easily handle hierarchical data.
* **Reusability**: Can be referenced multiple times in a query (unlike subqueries).

#### **Cons:**

* **Performance**: Not always optimized well by some SQL engines.
* **Materialization overhead**: May create temporary result sets.
* **Not indexed**: CTEs are not stored or indexed like temp tables.

---

### **23. Can you reference a CTE multiple times in the same query?**

Yes, **you can reference a CTE multiple times** in the same SQL statement.

#### **Example:**

```sql
WITH Sales_CTE AS (
    SELECT SalespersonID, SUM(SalesAmount) AS TotalSales
    FROM Sales
    GROUP BY SalespersonID
)
SELECT * FROM Sales_CTE WHERE TotalSales > 50000
UNION ALL
SELECT * FROM Sales_CTE WHERE TotalSales <= 50000;
```

> 💡 The CTE will be **re-evaluated** each time unless the optimizer decides to reuse the result.


---

### 🔷 **Data Quality & Validation**

Great! Here's a detailed breakdown of the next set of **advanced SQL interview questions**, focusing on **data validation, duplicates, and NULL handling**.

---

### **24. How do you find duplicates in a dataset?**

To find duplicates, you typically group by the column(s) and use `HAVING COUNT(*) > 1`.

#### **Example: Find duplicate email addresses in a users table:**

```sql
SELECT Email, COUNT(*) AS DuplicateCount
FROM Users
GROUP BY Email
HAVING COUNT(*) > 1;
```

#### **To view the full duplicate rows:**

```sql
SELECT *
FROM Users
WHERE Email IN (
    SELECT Email
    FROM Users
    GROUP BY Email
    HAVING COUNT(*) > 1
);
```

---

### **25. How to compare two tables to check for data mismatches?**

You can use several approaches like `EXCEPT`, `JOIN`, or `FULL OUTER JOIN`.

#### **Example: Compare `TableA` and `TableB` for mismatches:**

##### **1. Using EXCEPT:**

```sql
SELECT * FROM TableA
EXCEPT
SELECT * FROM TableB;

SELECT * FROM TableB
EXCEPT
SELECT * FROM TableA;
```

This shows rows in one table but not in the other.

##### **2. Using FULL OUTER JOIN:**

```sql
SELECT *
FROM TableA a
FULL OUTER JOIN TableB b
ON a.ID = b.ID
WHERE a.Column1 IS DISTINCT FROM b.Column1
   OR a.Column2 IS DISTINCT FROM b.Column2;
```

> `IS DISTINCT FROM` is useful because it treats `NULL <> NULL` (which regular `=` doesn’t).

---

### **26. How do you handle NULLs in aggregations or comparisons?**

NULLs can produce unexpected results in SQL, so they must be handled explicitly.

#### **Handling NULLs in Aggregation:**

| Function     | NULL Behavior               |
| ------------ | --------------------------- |
| `COUNT(*)`   | Counts all rows             |
| `COUNT(col)` | Ignores NULLs in the column |
| `SUM`, `AVG` | Ignores NULLs               |
| `MAX`, `MIN` | Ignores NULLs               |

#### **Example:**

```sql
-- Total sales including NULLs as 0
SELECT SUM(COALESCE(SalesAmount, 0)) FROM Orders;
```

#### **Handling NULLs in Comparison:**

```sql
-- This won't return rows where col1 is NULL
SELECT * FROM table WHERE col1 = 100;

-- This is required to include NULLs
SELECT * FROM table WHERE col1 IS NULL;

-- Safe comparison using COALESCE
SELECT * FROM table WHERE COALESCE(col1, 0) = 100;
```

> 💡 Use `COALESCE()` or `IS NULL` explicitly to avoid logic errors in filters and joins.


---

### 🔷 **Partitioning & Sharding**

Excellent — these are key **performance and data architecture** topics often discussed in advanced SQL or data engineering interviews. Here's a breakdown:

---

### **27. What is Table Partitioning and How Does It Help in Performance?**

**Table partitioning** is the process of dividing a large table into smaller, more manageable **physical units** (partitions) while keeping it logically as one table.

#### ✅ **Benefits:**

* **Improved query performance**: Only relevant partitions are scanned (partition pruning).
* **Faster maintenance**: Easy to archive, delete, or load data partition-wise.
* **Better parallelism**: Operations can be executed in parallel across partitions.
* **Manageability**: Easier index management on large datasets.

---

### **28. Difference Between Horizontal and Vertical Partitioning**

| Feature                | **Horizontal Partitioning**                           | **Vertical Partitioning**                                |
| ---------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| **Definition**         | Divides rows across multiple tables                   | Divides columns across multiple tables                   |
| **Goal**               | Improve access by filtering by data ranges            | Improve performance by reducing column read load         |
| **Use Case**           | Time-based log tables, region-specific data           | Wide tables with rarely used columns                     |
| **Logical Table View** | Rows from all partitions still make up the full table | Columns from all partitions still make up the full table |
| **Example**            | `Sales_2024`, `Sales_2025`, `Sales_2026`              | `Customer_Core`, `Customer_Preferences`                  |

---

### **29. How Do You Implement Table Partitioning in SQL Server / PostgreSQL?**

#### **A. SQL Server – Range Partitioning Example**

**Step 1: Create Partition Function**

```sql
CREATE PARTITION FUNCTION SalesPartitionFunction (DATE)
AS RANGE LEFT FOR VALUES ('2024-01-01', '2025-01-01', '2026-01-01');
```

**Step 2: Create Partition Scheme**

```sql
CREATE PARTITION SCHEME SalesPartitionScheme
AS PARTITION SalesPartitionFunction
ALL TO ([PRIMARY]);  -- You can assign filegroups here
```

**Step 3: Create Partitioned Table**

```sql
CREATE TABLE Sales (
    SaleID INT,
    SaleDate DATE,
    Amount DECIMAL(10, 2)
)
ON SalesPartitionScheme (SaleDate);
```

#### ✅ SQL Server Notes:

* Indexes should be created with partition scheme.
* You can split/merge partitions using `ALTER PARTITION FUNCTION`.

---

#### **B. PostgreSQL – Native Declarative Partitioning**

**Step 1: Create Partitioned Table**

```sql
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    amount NUMERIC(10, 2)
) PARTITION BY RANGE (sale_date);
```

**Step 2: Create Partitions**

```sql
CREATE TABLE sales_2024 PARTITION OF sales
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE sales_2025 PARTITION OF sales
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

**Step 3 (Optional): Index Partitions**

```sql
CREATE INDEX ON sales_2024 (sale_date);
```

#### ✅ PostgreSQL Notes:

* PostgreSQL automatically prunes irrelevant partitions during queries.
* Can also partition by `LIST` or `HASH`.

---


### 🔷 **Transactions & Concurrency**

---

### **30. What Are the Different Isolation Levels in SQL?**

**Isolation levels** control how visible the data changes made by one transaction are to other concurrent transactions.

| Isolation Level      | Dirty Read | Non-Repeatable Read | Phantom Read |
| -------------------- | ---------- | ------------------- | ------------ |
| **READ UNCOMMITTED** | ✅ Allowed  | ✅ Allowed           | ✅ Allowed    |
| **READ COMMITTED**   | ❌ Avoided  | ✅ Allowed           | ✅ Allowed    |
| **REPEATABLE READ**  | ❌ Avoided  | ❌ Avoided           | ✅ Allowed    |
| **SERIALIZABLE**     | ❌ Avoided  | ❌ Avoided           | ❌ Avoided    |

#### ✅ **Definitions:**

* **Dirty Read**: Reading uncommitted changes from another transaction.
* **Non-Repeatable Read**: Getting different values on re-reading the same row.
* **Phantom Read**: Seeing new rows in a repeated query due to other inserts.

#### 🔍 Example in PostgreSQL:

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

---

### **31. Explain Optimistic vs Pessimistic Locking**

| Feature              | **Optimistic Locking**                      | **Pessimistic Locking**                      |
| -------------------- | ------------------------------------------- | -------------------------------------------- |
| **Assumption**       | Conflicts are rare                          | Conflicts are likely                         |
| **Locking Behavior** | No locks until update/commit                | Locks data when reading to prevent conflicts |
| **Common in**        | Web applications, high-concurrency systems  | Critical sections, bank transactions         |
| **How It Works**     | Use a version/timestamp to detect conflicts | Use `SELECT ... FOR UPDATE` to lock the rows |
| **Performance**      | Better for read-heavy workloads             | Safer but can block other operations         |

#### 🔁 **Optimistic Locking Example (via version check):**

```sql
UPDATE Employees
SET Salary = Salary + 5000,
    Version = Version + 1
WHERE EmployeeID = 101 AND Version = 5;
```

#### 🔒 **Pessimistic Locking Example:**

```sql
BEGIN;
SELECT * FROM Employees WHERE EmployeeID = 101 FOR UPDATE;
-- Data is locked until commit/rollback
```

---

### **32. What Is a Deadlock? How Can You Detect and Resolve One?**

#### ❗ **Deadlock Definition:**

A **deadlock** occurs when two or more transactions block each other by holding locks on resources the other needs.

#### 🔁 **Simple Example:**

* **Txn A** locks **Row 1**, needs **Row 2**.
* **Txn B** locks **Row 2**, needs **Row 1**.
* Neither can proceed — this is a **deadlock**.

---

#### ✅ **Deadlock Detection:**

* **SQL Server**: Detects automatically and kills one transaction (victim).
* **PostgreSQL**: Detects and throws an error like:

  > `ERROR: deadlock detected`

#### 📈 **Monitoring Tools:**

* SQL Server: Extended Events, Profiler.
* PostgreSQL: `pg_stat_activity`, `pg_locks`.

---

#### 🔧 **Deadlock Resolution Techniques:**

* Always access tables/rows in a consistent **order**.
* Keep **transactions short**.
* Use **lower isolation levels** if possible (e.g., READ COMMITTED).
* Use **timeout or retry logic** for failed transactions.
* **Indexing**: Helps avoid full-table locks by speeding up access.


---

### 🔷 **Real-world Problem Scenarios**

---

### **33. How to Find the Longest Streak of User Activity**

#### 🧠 Goal: Find the longest sequence of **consecutive active days** per user.

Assume table `UserActivity(user_id, activity_date)`.

```sql
WITH RankedActivity AS (
  SELECT 
    user_id,
    activity_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY activity_date) AS rn
  FROM UserActivity
),
ActivityGroups AS (
  SELECT 
    user_id,
    activity_date,
    DATE(activity_date) - INTERVAL '1 day' * rn AS streak_group
  FROM RankedActivity
),
Streaks AS (
  SELECT 
    user_id,
    COUNT(*) AS streak_length,
    MIN(activity_date) AS streak_start,
    MAX(activity_date) AS streak_end
  FROM ActivityGroups
  GROUP BY user_id, streak_group
)
SELECT * FROM (
  SELECT *, 
         RANK() OVER (PARTITION BY user_id ORDER BY streak_length DESC) AS rnk
  FROM Streaks
) t
WHERE rnk = 1;
```

---

### **34. How to Pivot or Unpivot Data in SQL**

#### ✅ **Pivot Example: Monthly sales per product**

```sql
SELECT 
  product_id,
  SUM(CASE WHEN MONTH(sale_date) = 1 THEN amount ELSE 0 END) AS Jan,
  SUM(CASE WHEN MONTH(sale_date) = 2 THEN amount ELSE 0 END) AS Feb
FROM Sales
GROUP BY product_id;
```

#### 🔄 **Unpivot Example: From wide to tall**

From:

| user\_id | Jan | Feb |
| -------- | --- | --- |
| 1        | 10  | 20  |

To:

| user\_id | month | amount |
| -------- | ----- | ------ |
| 1        | Jan   | 10     |
| 1        | Feb   | 20     |

```sql
SELECT user_id, 'Jan' AS month, Jan AS amount FROM SalesByMonth
UNION ALL
SELECT user_id, 'Feb', Feb FROM SalesByMonth;
```

---

### **35. Query to Find Customers Who Made Purchases in 3 Consecutive Months**

Assume: `Purchases(customer_id, purchase_date)`

```sql
WITH PurchaseMonths AS (
  SELECT DISTINCT
    customer_id,
    DATE_TRUNC('month', purchase_date)::date AS month
  FROM Purchases
),
RankedMonths AS (
  SELECT 
    customer_id,
    month,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY month) AS rn
  FROM PurchaseMonths
),
GroupedMonths AS (
  SELECT 
    customer_id,
    month,
    rn,
    month - INTERVAL '1 month' * rn AS grp
  FROM RankedMonths
)
SELECT customer_id
FROM GroupedMonths
GROUP BY customer_id, grp
HAVING COUNT(*) >= 3;
```

> This logic detects sequences of consecutive months using date - row\_number pattern.

---

### **36. Find First and Last Login per User per Day**

Assume: `Logins(user_id, login_time)`

```sql
SELECT 
  user_id,
  DATE(login_time) AS login_date,
  MIN(login_time) AS first_login,
  MAX(login_time) AS last_login
FROM Logins
GROUP BY user_id, DATE(login_time);
```

---

### **37. Detect Anomalies in Daily Sales Trends Using SQL**

Assume: `Sales(sale_date, amount)`

#### **Detect days where sales are much higher/lower than usual (z-score method):**

```sql
WITH DailySales AS (
  SELECT 
    DATE(sale_date) AS sale_day,
    SUM(amount) AS total_sales
  FROM Sales
  GROUP BY DATE(sale_date)
),
Stats AS (
  SELECT 
    AVG(total_sales) AS avg_sales,
    STDDEV(total_sales) AS stddev_sales
  FROM DailySales
)
SELECT ds.*
FROM DailySales ds, Stats s
WHERE ABS(ds.total_sales - s.avg_sales) > 2 * s.stddev_sales;
```

> 💡 This detects **statistical outliers** — sales that are 2+ standard deviations from the mean.


---

### 🔷 **Analytical & Reporting Queries**

---

### **38. How to Generate a Report Showing % Growth Month-over-Month**

Assume: `Sales(sale_date, amount)`

```sql
WITH MonthlySales AS (
  SELECT 
    DATE_TRUNC('month', sale_date)::DATE AS month,
    SUM(amount) AS total_sales
  FROM Sales
  GROUP BY DATE_TRUNC('month', sale_date)
),
SalesWithLag AS (
  SELECT 
    month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY month) AS prev_month_sales
  FROM MonthlySales
)
SELECT 
  month,
  total_sales,
  prev_month_sales,
  ROUND(
    (total_sales - prev_month_sales) * 100.0 / NULLIF(prev_month_sales, 0),
    2
  ) AS pct_growth
FROM SalesWithLag;
```

#### ✅ Output Columns:

* `month`
* `total_sales`
* `prev_month_sales`
* `pct_growth` → MoM %

---

### **39. How to Compare Current Year vs Previous Year Sales Using SQL**

Assume: `Sales(sale_date, amount)`

```sql
WITH YearlySales AS (
  SELECT 
    DATE_TRUNC('month', sale_date)::DATE AS month,
    EXTRACT(YEAR FROM sale_date) AS year,
    SUM(amount) AS total_sales
  FROM Sales
  GROUP BY DATE_TRUNC('month', sale_date), EXTRACT(YEAR FROM sale_date)
),
PivotedSales AS (
  SELECT 
    month,
    MAX(CASE WHEN year = EXTRACT(YEAR FROM CURRENT_DATE) THEN total_sales END) AS current_year_sales,
    MAX(CASE WHEN year = EXTRACT(YEAR FROM CURRENT_DATE) - 1 THEN total_sales END) AS prev_year_sales
  FROM YearlySales
  GROUP BY month
)
SELECT 
  month,
  current_year_sales,
  prev_year_sales,
  ROUND(
    (current_year_sales - prev_year_sales) * 100.0 / NULLIF(prev_year_sales, 0),
    2
  ) AS yoy_growth_pct
FROM PivotedSales;
```

> ✅ Works at a **monthly level** — compare YoY % for same month (e.g., Jan 2025 vs Jan 2024).

---

### **40. How to Rank Products by Sales Contribution Percentage**

Assume: `Sales(product_id, amount)`

```sql
WITH ProductSales AS (
  SELECT 
    product_id,
    SUM(amount) AS product_sales
  FROM Sales
  GROUP BY product_id
),
TotalSales AS (
  SELECT SUM(product_sales) AS total_sales
  FROM ProductSales
),
SalesWithPct AS (
  SELECT 
    ps.product_id,
    ps.product_sales,
    ROUND(ps.product_sales * 100.0 / NULLIF(ts.total_sales, 0), 2) AS sales_pct
  FROM ProductSales ps
  CROSS JOIN TotalSales ts
)
SELECT *,
       RANK() OVER (ORDER BY sales_pct DESC) AS sales_rank
FROM SalesWithPct;
```

#### ✅ Output:

* `product_id`
* `product_sales`
* `% contribution to total sales`
* `ranking by contribution`

---

### 🔷 **Temporal & Date-Based Queries**

---

### **41. Find Gaps Between Timestamped Events**

Assume: `Events(user_id, event_time)` — sorted by `event_time`.

#### 🧠 Goal: Find gaps between consecutive events greater than a threshold (e.g., 1 hour).

```sql
WITH EventWithLag AS (
  SELECT 
    user_id,
    event_time,
    LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_event_time
  FROM Events
)
SELECT 
  user_id,
  prev_event_time,
  event_time,
  EXTRACT(EPOCH FROM event_time - prev_event_time)/60 AS gap_minutes
FROM EventWithLag
WHERE event_time - prev_event_time > INTERVAL '1 hour';
```

> ✅ You get the **gaps in minutes** and can filter based on your threshold.

---

### **42. How to Calculate Time Spent Between Login and Logout Events**

Assume: `Log(user_id, action, event_time)`
Where `action` = `'login'` or `'logout'`.

#### 🧠 Match each `login` with the next `logout` **per user**:

```sql
WITH LogEvents AS (
  SELECT 
    user_id,
    event_time,
    action,
    ROW_NUMBER() OVER (PARTITION BY user_id, action ORDER BY event_time) AS rn
  FROM Log
),
MatchedLogins AS (
  SELECT 
    l.user_id,
    l.event_time AS login_time,
    o.event_time AS logout_time,
    EXTRACT(EPOCH FROM (o.event_time - l.event_time)) / 60 AS session_minutes
  FROM LogEvents l
  JOIN LogEvents o
    ON l.user_id = o.user_id AND l.rn = o.rn
   AND l.action = 'login' AND o.action = 'logout'
)
SELECT * FROM MatchedLogins;
```

> ✅ Assumes login/logout events are paired and ordered. Each `ROW_NUMBER()` helps sync pairs.

---

### **43. Write a Query to Bucket Timestamps into 15-Minute Intervals**

Assume: `Events(event_time)`.

#### 🕒 Round down each timestamp to the nearest 15-minute interval.

```sql
SELECT
  event_time,
  DATE_TRUNC('hour', event_time) +
    INTERVAL '1 minute' * FLOOR(EXTRACT(MINUTE FROM event_time) / 15) * 15
    AS bucket_start
FROM Events
ORDER BY event_time;
```

> ✅ This gives clean 15-min windows like:

* `12:00–12:14`
* `12:15–12:29`, etc.

---


