# Python interview questions and answers with examples.

---

## **Core Python (Advanced Use Cases)**

1. **How do you handle memory-efficient iteration over large datasets?**

```python
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()

for row in read_large_file("bigdata.csv"):
    process(row)
```

✅ Uses **generators** instead of loading full data.

---

2. **How to merge two sorted lists efficiently?**

```python
import heapq
a = [1,3,5]
b = [2,4,6]
merged = list(heapq.merge(a,b))
print(merged)  # [1,2,3,4,5,6]
```

---

3. **What’s the difference between mutable default arguments and immutable ones?**

```python
def add_item(item, lst=[]):  # BAD: same list reused
    lst.append(item)
    return lst

print(add_item(1)) # [1]
print(add_item(2)) # [1,2] ❌
```

✅ Use `None` as default.

---

4. **Explain Python’s `dataclass`. How does it help in ETL coding?**

```python
from dataclasses import dataclass
@dataclass
class Employee:
    id: int
    name: str
    dept: str
```

✅ Avoids boilerplate (`__init__`, `__repr__`). Useful for **schemas**.

---

5. **How to convert a list of dictionaries into a dictionary grouped by a key?**

```python
from collections import defaultdict
data = [{"dept":"HR","emp":"A"},{"dept":"IT","emp":"B"}]
result = defaultdict(list)
for d in data:
    result[d["dept"]].append(d["emp"])
print(result)  # {'HR': ['A'], 'IT': ['B']}
```

---

## **Error Handling & Logging**

6. **How do you implement custom logging in Python ETL pipelines?**

```python
import logging
logging.basicConfig(filename="etl.log", level=logging.INFO)
logging.info("Pipeline started")
```

---

7. **What’s the difference between `try/except` and `try/except/else/finally`?**

* `else`: runs if no exception.
* `finally`: always runs (cleanup).

---

8. **How to retry a failed API call in Python?**

```python
import time, requests
for attempt in range(3):
    try:
        r = requests.get("https://api.example.com")
        break
    except Exception:
        time.sleep(2)
```

---

9. **How do you suppress exceptions temporarily?**

```python
import contextlib
with contextlib.suppress(ZeroDivisionError):
    print(1/0)  # Won’t crash
```

---

10. **How do you create a custom context manager (without `with`)?**

```python
class FileManager:
    def __enter__(self): 
        print("Open file"); return self
    def __exit__(self, exc_type, exc_val, exc_tb): 
        print("Close file")
with FileManager() as fm:
    print("Inside")
```

---

## **Functional Programming**

11. **How do you remove `None` values from nested lists?**

```python
data = [1, None, [2, None, 3]]
clean = str(data).replace("None", "").replace("[,","[").replace(",]","]")
```

---

12. **Explain use of `any()` and `all()` in data checks.**

```python
nums = [2,4,6]
print(all(x%2==0 for x in nums))  # True
print(any(x>5 for x in nums))     # True
```

---

13. **What’s the difference between `enumerate` and `zip`?**

```python
for i,val in enumerate(["a","b"]): print(i,val)
for a,b in zip([1,2],[3,4]): print(a,b)
```

---

14. **How do you deduplicate a list of dicts by a key?**

```python
seen, result = set(), []
for d in [{"id":1},{"id":1},{"id":2}]:
    if d["id"] not in seen:
        result.append(d); seen.add(d["id"])
```

---

15. **What is `functools.lru_cache` and how is it useful?**

```python
from functools import lru_cache
@lru_cache(maxsize=100)
def fib(n): return n if n<2 else fib(n-1)+fib(n-2)
```

✅ Speeds up repeated queries.

---

## **Data Engineering-Oriented**

16. **How to chunk a very large Pandas DataFrame for processing?**

```python
for chunk in pd.read_csv("big.csv", chunksize=100000):
    process(chunk)
```

---

17. **How do you detect schema drift in CSV files?**

```python
import pandas as pd
df1 = pd.read_csv("day1.csv")
df2 = pd.read_csv("day2.csv")
print(set(df1.columns) ^ set(df2.columns))
```

---

18. **How to validate column data types in Pandas?**

```python
expected = {"id":"int64","name":"object"}
print(df.dtypes.to_dict() == expected)
```

---

19. **How to compute rolling average in Pandas?**

```python
df["rolling_avg"] = df["sales"].rolling(window=7).mean()
```

---

20. **How do you convert nested JSON into a flat table in Pandas?**

```python
import pandas as pd
import json
data = {"id":1,"info":{"age":30,"city":"NY"}}
df = pd.json_normalize(data)
```

---

21. **How to detect duplicates in large datasets efficiently?**

```python
dupes = df[df.duplicated(["id"], keep=False)]
```

---

22. **How do you split a DataFrame into train/test sets?**

```python
from sklearn.model_selection import train_test_split
train,test = train_test_split(df, test_size=0.2)
```

---

23. **How do you implement type casting during ETL?**

```python
df["amount"] = df["amount"].astype(float)
```

---

24. **How to calculate top-N by group in Pandas?**

```python
df.groupby("dept").apply(lambda x: x.nlargest(3,"salary"))
```

---

25. **How do you monitor execution time of Python ETL steps?**

```python
import time
start = time.time()
process()
print("Duration:", time.time()-start)
```

---

## **Concurrency & Performance**

26. **How to use ThreadPoolExecutor for parallel ETL?**

```python
from concurrent.futures import ThreadPoolExecutor
def task(x): return x*x
with ThreadPoolExecutor() as ex:
    print(list(ex.map(task, [1,2,3,4])))
```

---

27. **How do you profile slow Python code?**

```python
import cProfile
cProfile.run("process_data()")
```

---

28. **What is memoryview and why is it efficient?**

```python
b = bytearray(b"dataengineer")
m = memoryview(b)
print(m[0:4].tobytes())  # b'data'
```

---

29. **How do you compress large CSV/Parquet files in Python?**

```python
df.to_csv("out.csv.gz", compression="gzip")
df.to_parquet("out.parquet", compression="snappy")
```

---

30. **How to schedule recurring Python ETL jobs?**

```python
import schedule, time
def job(): print("ETL running")
schedule.every().day.at("01:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
```

---
