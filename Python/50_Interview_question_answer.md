# 50 Python Interview Questions & Answers for Data Engineers

---

## **Core Python & Data Structures**

1. **What are Python’s key features?**

   * Interpreted, dynamically typed, high-level, portable, supports OOP & functional programming, large ecosystem.

---

2. **Difference between list, tuple, set, and dictionary?**

```python
lst = [1, 2, 3]       # mutable, ordered, allows duplicates
tpl = (1, 2, 3)       # immutable, ordered
st  = {1, 2, 2, 3}    # mutable, unordered, unique values
dct = {"a": 1, "b": 2} # key-value pairs
```

---

3. **How do you remove duplicates from a list while preserving order?**

```python
lst = [1,2,2,3,4,4,5]
unique = list(dict.fromkeys(lst))
print(unique)  # [1,2,3,4,5]
```

---

4. **What is list comprehension?**

```python
squares = [x*x for x in range(5)]
print(squares)  # [0,1,4,9,16]
```

---

5. **How to merge two dictionaries in Python 3.9+?**

```python
a = {"x": 1}
b = {"y": 2}
merged = a | b
print(merged)  # {'x': 1, 'y': 2}
```

---

6. **How to reverse a string in Python?**

```python
s = "DataEngineer"
print(s[::-1])  # reenignEataD
```

---

7. **What is the difference between `is` and `==`?**

* `is` checks object identity (same memory).
* `==` checks equality of values.

---

8. **What are Python generators?**

```python
def num_gen(n):
    for i in range(n):
        yield i

for val in num_gen(3):
    print(val)  # 0,1,2
```

---

9. **How do you flatten a nested list?**

```python
nested = [[1,2],[3,4],[5]]
flat = [x for sub in nested for x in sub]
print(flat)  # [1,2,3,4,5]
```

---

10. **Explain `*args` and `**kwargs`.**

```python
def func(*args, **kwargs):
    print(args)   # tuple
    print(kwargs) # dict
func(1,2,3, name="John")
```

---

## **File Handling & Serialization**

11. **How do you read a large file line by line?**

```python
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```

---

12. **How to write JSON to a file?**

```python
import json
data = {"id": 1, "name": "Alice"}
with open("out.json","w") as f:
    json.dump(data,f)
```

---

13. **How to handle CSV files in Python?**

```python
import csv
with open("data.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

---

14. **Pickle vs JSON?**

* **Pickle**: Python-specific, faster, not human-readable.
* **JSON**: Language-independent, human-readable.

---

15. **How to check if a file exists in Python?**

```python
import os
print(os.path.exists("data.csv"))
```

---

## **OOP (Object-Oriented Programming)**

16. **Difference between class and instance variables?**

```python
class Employee:
    company = "ABC"   # class variable
    def __init__(self, name):
        self.name = name  # instance variable
```

---

17. **Explain Python inheritance.**

```python
class Parent:
    def greet(self): print("Hello")
class Child(Parent):
    pass
c = Child()
c.greet()
```

---

18. **What is method overriding?**

```python
class Parent:
    def work(self): print("Parent work")
class Child(Parent):
    def work(self): print("Child work")
```

---

19. **What is `@staticmethod` vs `@classmethod`?**

```python
class Example:
    @staticmethod
    def greet(): print("Static method")
    @classmethod
    def cls_info(cls): print("Class method")
```

---

20. **What is multiple inheritance in Python?**

* A class can inherit from multiple parents.
* Uses **MRO (Method Resolution Order)** to resolve conflicts.

---

## **Exception Handling**

21. **How do you handle exceptions?**

```python
try:
    1/0
except ZeroDivisionError:
    print("Divide by zero error")
```

---

22. **What is `finally` block?**

* Always executes, regardless of exception.

---

23. **Custom exceptions in Python?**

```python
class DataError(Exception): pass
raise DataError("Invalid data")
```

---

24. **What is `with` statement in Python?**

* Manages resources automatically (context manager).

```python
with open("file.txt") as f:
    data = f.read()
```

---

25. **Difference between `assert` and exception handling?**

* `assert` → debugging aid, checks conditions.
* `try/except` → handles runtime errors.

---

## **Functional Programming**

26. **How does `map` work?**

```python
nums = [1,2,3]
squares = list(map(lambda x: x*x, nums))
```

---

27. **How does `filter` work?**

```python
nums = [1,2,3,4]
evens = list(filter(lambda x: x%2==0, nums))
```

---

28. **How does `reduce` work?**

```python
from functools import reduce
nums = [1,2,3,4]
sum_all = reduce(lambda a,b: a+b, nums)
```

---

29. **What is `lambda` function?**

* Anonymous function:

```python
square = lambda x: x*x
```

---

30. **Difference between deep copy and shallow copy?**

```python
import copy
lst = [[1,2],[3,4]]
shallow = copy.copy(lst)
deep = copy.deepcopy(lst)
```

---

## **Multithreading & Multiprocessing**

31. **What is GIL (Global Interpreter Lock)?**

* Only one thread executes Python bytecode at a time.

---

32. **How to use threading in Python?**

```python
import threading
def task(): print("Running")
t = threading.Thread(target=task)
t.start()
```

---

33. **When to use multiprocessing vs threading?**

* **Threading**: I/O bound tasks.
* **Multiprocessing**: CPU bound tasks.

---

34. **How do you implement parallel processing?**

```python
from multiprocessing import Pool
def square(x): return x*x
with Pool(4) as p:
    print(p.map(square, [1,2,3,4]))
```

---

35. **What is asyncio?**

```python
import asyncio
async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
asyncio.run(main())
```

---

## **Database & ETL**

36. **How to connect to a database in Python?**

```python
import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("SELECT sqlite_version();")
```

---

37. **How to read SQL query into Pandas?**

```python
import pandas as pd
df = pd.read_sql("SELECT * FROM users", conn)
```

---

38. **How to load CSV into SQL using Pandas?**

```python
df = pd.read_csv("data.csv")
df.to_sql("table", conn, if_exists="replace", index=False)
```

---

39. **How do you handle missing data in Pandas?**

```python
df.fillna(0, inplace=True)
df.dropna(inplace=True)
```

---

40. **How to optimize large Pandas DataFrames?**

* Use `dtype` optimization, chunk reading, `categorical` data type.

---

## **Data Engineering-Specific**

41. **How to read large CSVs in chunks?**

```python
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

---

42. **How do you handle schema evolution?**

* Use libraries like **PySpark, Pandas**, and enforce schema during ETL.

---

43. **Difference between JSON, Parquet, and Avro?**

* **JSON**: human-readable.
* **Parquet**: columnar, compressed, efficient.
* **Avro**: row-based, schema evolution support.

---

44. **How to read Parquet in Python?**

```python
import pandas as pd
df = pd.read_parquet("data.parquet")
```

---

45. **Explain partitioning in data pipelines.**

* Splitting large datasets by columns (e.g., `year`, `month`) for faster queries.

---

46. **What is PySpark DataFrame vs Pandas DataFrame?**

* **Pandas**: in-memory, single machine.
* **PySpark**: distributed, handles big data.

---

47. **How to convert Pandas to PySpark DataFrame?**

```python
from pyspark.sql import SparkSession
import pandas as pd
spark = SparkSession.builder.getOrCreate()
pdf = pd.DataFrame({"id":[1,2]})
df = spark.createDataFrame(pdf)
```

---

48. **How do you handle duplicate rows in PySpark?**

```python
df.dropDuplicates(["id"])
```

---

49. **What are UDFs in PySpark?**

* User Defined Functions to extend Spark SQL.

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType
square_udf = udf(lambda x: x*x, IntegerType())
df.withColumn("squared", square_udf("id"))
```

---

50. **Explain Delta Lake in Databricks (Python usage).**

* Supports ACID transactions on data lakes.

```python
df.write.format("delta").mode("overwrite").save("/delta/table")
```

---

👉 These **50 questions** give you a strong **Python + Data Engineering** interview prep.
