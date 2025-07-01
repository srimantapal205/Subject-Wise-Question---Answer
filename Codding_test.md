**Online or Live Coding**

---

### 📌 **1. SQL (Most Important)**

You’ll definitely face SQL-based problems. Focus on:

* Joins (Inner, Left, Self)
* Aggregation (`COUNT`, `SUM`, `AVG`)
* Subqueries & CTEs
* Window Functions (`ROW_NUMBER`, `RANK`, `LAG`, etc.)
* String/date manipulation
* Grouping and filtering

#### ✅ Example SQL Questions:

1. **Get the second highest salary**

   ```sql
   SELECT MAX(salary) FROM employees 
   WHERE salary < (SELECT MAX(salary) FROM employees);
   ```

2. **List departments with more than 5 employees**

   ```sql
   SELECT department_id, COUNT(*) as total 
   FROM employees 
   GROUP BY department_id 
   HAVING COUNT(*) > 5;
   ```

3. **Find customers who made purchases in January but not in February**

   ```sql
   SELECT DISTINCT customer_id
   FROM sales
   WHERE MONTH(purchase_date) = 1
   AND customer_id NOT IN (
     SELECT customer_id FROM sales WHERE MONTH(purchase_date) = 2
   );
   ```

4. **Running total of sales per month**

   ```sql
   SELECT 
     customer_id, 
     order_date, 
     SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
   FROM orders;
   ```

---

### 📌 **2. Python for Data Manipulation (Optional but Useful)**

Used for file handling, data cleaning, etc., especially in ADF/Databricks scenarios.

#### ✅ Example Python Questions:

1. **Read a CSV and filter data**

   ```python
   import pandas as pd
   df = pd.read_csv("data.csv")
   df_filtered = df[df["age"] > 30]
   ```

2. **Count word frequency in a string**

   ```python
   from collections import Counter
   text = "this is a test this is"
   result = Counter(text.split())
   ```

3. **Flatten a nested list**

   ```python
   nested = [[1, 2], [3, 4], [5]]
   flat = [item for sublist in nested for item in sublist]
   ```

4. **Transform JSON to CSV**

   ```python
   import pandas as pd
   import json
   with open('data.json') as f:
       data = json.load(f)
   df = pd.json_normalize(data)
   df.to_csv('output.csv', index=False)
   ```

---

### 📌 **3. Data Transformation Logic (Case Study Style)**

These are "business rule"-based transformation problems.

#### ✅ Example:

> You are given a flat file with columns: `customer_id`, `amount`, `region`, and `date`.
> You need to:
>
> * Remove duplicates
> * Calculate total `amount` per region
> * Convert date to `YYYY-MM` format

*Answer:* Expect to write either a SQL query or use Pandas.

---

### 📌 **4. File Handling / Scripting Basics**

Used in data ingestion or cleansing automation.

#### ✅ Example:

1. **Move files from one folder to another in Python**

   ```python
   import shutil
   shutil.move("source/file.csv", "destination/file.csv")
   ```

2. **Read multiple CSVs from a directory and concatenate**

   ```python
   import os
   import pandas as pd
   all_files = [pd.read_csv(f) for f in os.listdir('data/') if f.endswith('.csv')]
   combined = pd.concat(all_files)
   ```

---

### 📌 **5. Spark/Databricks (If Included)**

Usually they’ll ask about concepts, but occasionally you may be asked to:

* Write PySpark transformations
* Filter/aggregate data using DataFrames

#### ✅ PySpark Example:

```python
df.groupBy("region").agg({"amount": "sum"}).show()
```


---

### ✅ **1. Top N Records Per Group**

> **Q:** Find the top 2 highest-paid employees per department.

```sql
SELECT *
FROM (
  SELECT *, 
         RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
  FROM employees
) AS ranked
WHERE rnk <= 2;
```

---

### ✅ **2. Date Difference Calculation**

> **Q:** Find the number of days between order date and delivery date.

```sql
SELECT order_id, DATEDIFF(day, order_date, delivery_date) AS days_to_deliver
FROM orders;
```

---

### ✅ **3. Conditional Aggregation**

> **Q:** Count number of male and female employees by department.

```sql
SELECT department_id,
       COUNT(CASE WHEN gender = 'M' THEN 1 END) AS male_count,
       COUNT(CASE WHEN gender = 'F' THEN 1 END) AS female_count
FROM employees
GROUP BY department_id;
```

---

### ✅ **4. NULL Handling**

> **Q:** Replace NULLs in a salary column with the average salary.

```sql
SELECT employee_id,
       ISNULL(salary, (SELECT AVG(salary) FROM employees)) AS updated_salary
FROM employees;
```

---

### ✅ **5. Self Join**

> **Q:** Find employees who share the same manager.

```sql
SELECT e1.employee_id, e2.employee_id AS colleague
FROM employees e1
JOIN employees e2
  ON e1.manager_id = e2.manager_id
WHERE e1.employee_id != e2.employee_id;
```

---

## 🧠 **SECTION 2: Python Coding for Data Engineering**

### ✅ **1. Parse Nested JSON**

> **Q:** Flatten a nested JSON object for transformation.

```python
import json
import pandas as pd

with open("data.json") as f:
    data = json.load(f)

df = pd.json_normalize(data, sep='_')
```

---

### ✅ **2. Group and Aggregate using Pandas**

> **Q:** Find total sales per region and month.

```python
df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
df.groupby(['region', 'month'])['sales'].sum().reset_index()
```

---

### ✅ **3. Handle Missing Values**

> **Q:** Fill missing values in a Pandas DataFrame with column mean.

```python
df.fillna(df.mean(numeric_only=True), inplace=True)
```

---

### ✅ **4. Compare Two Files**

> **Q:** Find rows present in `file1.csv` but not in `file2.csv`

```python
df1 = pd.read_csv('file1.csv')
df2 = pd.read_csv('file2.csv')

diff = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)
```

---

## 🧠 **SECTION 3: ADF/Databricks Simulation Style Logic**

These aren’t usually written in code but might be asked in a **live explanation or whiteboard round.**

### ✅ **1. File Processing Logic (Pseudocode)**

> Process files from a folder, validate schema, then move to archive if valid or error folder if invalid.

```python
# Pseudocode
for file in incoming_folder:
    df = read_file(file)
    if validate_schema(df):
        write_to_lake(valid_folder)
    else:
        move_file(file, error_folder)
```

---

### ✅ **2. Merge Two Tables with Deduplication**

```sql
MERGE INTO target_table AS tgt
USING staging_table AS src
ON tgt.id = src.id
WHEN MATCHED THEN
  UPDATE SET tgt.name = src.name, tgt.updated_on = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
  INSERT (id, name, updated_on) VALUES (src.id, src.name, CURRENT_TIMESTAMP);
```

---

## 🧠 **SECTION 4: Miscellaneous Questions (Fast 1-Liners)**

| Task                                  | Sample Code                                      |
| ------------------------------------- | ------------------------------------------------ |
| Count total lines in a file           | `len(open('file.txt').readlines())`              |
| Convert column to lowercase in Pandas | `df['col'] = df['col'].str.lower()`              |
| Remove duplicate rows                 | `df.drop_duplicates(inplace=True)`               |
| Get today's date                      | `from datetime import date; print(date.today())` |

---

## 🚀 Bonus Practice Challenges

You can try solving these:

### 🔸 **Challenge 1: Find Duplicate Rows in a Table**

```sql
SELECT col1, COUNT(*) 
FROM table_name 
GROUP BY col1 
HAVING COUNT(*) > 1;
```

---

### 🔸 **Challenge 2: Convert CSV to Parquet (Python)**

```python
import pandas as pd
df = pd.read_csv('input.csv')
df.to_parquet('output.parquet')
```


