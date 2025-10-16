# Here’s a **complete guide to PySpark date and time functions** — covering **all types** of operations such as date extraction, formatting, arithmetic, and conversions, along with **clear examples**.

---

## 📘 1. Setup

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName("DateTimeExamples").getOrCreate()

data = [("2025-10-16", "2025-09-20 14:30:45")]
df = spark.createDataFrame(data, ["date_str", "timestamp_str"])

df = df.withColumn("date_col", to_date(col("date_str"), "yyyy-MM-dd")) \
       .withColumn("timestamp_col", to_timestamp(col("timestamp_str"), "yyyy-MM-dd HH:mm:ss"))

df.show(truncate=False)
```

Output:

```
+----------+---------------------+----------+-------------------+
|date_str  |timestamp_str        |date_col  |timestamp_col      |
+----------+---------------------+----------+-------------------+
|2025-10-16|2025-09-20 14:30:45  |2025-10-16|2025-09-20 14:30:45|
+----------+---------------------+----------+-------------------+
```

---

## 🧭 2. Date Extraction Functions

| Function       | Description             | Example                                    |
| -------------- | ----------------------- | ------------------------------------------ |
| `year()`       | Extract year            | `df.select(year("date_col")).show()`       |
| `month()`      | Extract month           | `df.select(month("date_col")).show()`      |
| `dayofmonth()` | Extract day of month    | `df.select(dayofmonth("date_col")).show()` |
| `dayofweek()`  | 1=Sunday, 7=Saturday    | `df.select(dayofweek("date_col")).show()`  |
| `dayofyear()`  | Day number in the year  | `df.select(dayofyear("date_col")).show()`  |
| `weekofyear()` | Week number of the year | `df.select(weekofyear("date_col")).show()` |
| `quarter()`    | Quarter of the year     | `df.select(quarter("date_col")).show()`    |

Example:

```python
df.select(
    year("date_col").alias("year"),
    month("date_col").alias("month"),
    dayofmonth("date_col").alias("day"),
    weekofyear("date_col").alias("week"),
    quarter("date_col").alias("quarter")
).show()
```

---

## ⏳ 3. Time Extraction Functions

| Function   | Description    | Example                                     |
| ---------- | -------------- | ------------------------------------------- |
| `hour()`   | Extract hour   | `df.select(hour("timestamp_col")).show()`   |
| `minute()` | Extract minute | `df.select(minute("timestamp_col")).show()` |
| `second()` | Extract second | `df.select(second("timestamp_col")).show()` |

Example:

```python
df.select(
    hour("timestamp_col").alias("hour"),
    minute("timestamp_col").alias("minute"),
    second("timestamp_col").alias("second")
).show()
```

---

## 🧮 4. Date Arithmetic Functions

| Function           | Description                         | Example                                                        |
| ------------------ | ----------------------------------- | -------------------------------------------------------------- |
| `date_add()`       | Add days to a date                  | `df.select(date_add("date_col", 5)).show()`                    |
| `date_sub()`       | Subtract days from a date           | `df.select(date_sub("date_col", 10)).show()`                   |
| `add_months()`     | Add months to a date                | `df.select(add_months("date_col", 2)).show()`                  |
| `months_between()` | Months difference between two dates | `df.select(months_between(current_date(), "date_col")).show()` |
| `datediff()`       | Days difference between two dates   | `df.select(datediff(current_date(), "date_col")).show()`       |
| `next_day()`       | Next specific weekday               | `df.select(next_day("date_col", "Sunday")).show()`             |
| `last_day()`       | Last day of month                   | `df.select(last_day("date_col")).show()`                       |

---

## 🕓 5. Current Date and Time Functions

| Function              | Description                    | Example                                 |
| --------------------- | ------------------------------ | --------------------------------------- |
| `current_date()`      | Current system date            | `df.select(current_date()).show()`      |
| `current_timestamp()` | Current timestamp              | `df.select(current_timestamp()).show()` |
| `now()`               | Alias of `current_timestamp()` | `df.select(now()).show()`               |

---

## 🧰 6. Date and Timestamp Conversion Functions

| Function           | Description                     | Example                                                                  |
| ------------------ | ------------------------------- | ------------------------------------------------------------------------ |
| `to_date()`        | Convert string to date          | `df.select(to_date("date_str", "yyyy-MM-dd")).show()`                    |
| `to_timestamp()`   | Convert string to timestamp     | `df.select(to_timestamp("timestamp_str", "yyyy-MM-dd HH:mm:ss")).show()` |
| `unix_timestamp()` | Convert timestamp to Unix epoch | `df.select(unix_timestamp("timestamp_col")).show()`                      |
| `from_unixtime()`  | Convert Unix epoch to timestamp | `df.select(from_unixtime(unix_timestamp("timestamp_col"))).show()`       |
| `date_format()`    | Format date/timestamp           | `df.select(date_format("timestamp_col", "yyyy/MM/dd HH:mm")).show()`     |

---

## ⏱️ 7. Truncation and Rounding Functions

| Function       | Description                               | Example                                                 |
| -------------- | ----------------------------------------- | ------------------------------------------------------- |
| `trunc()`      | Truncate to month/year                    | `df.select(trunc("date_col", "month")).show()`          |
| `date_trunc()` | Truncate timestamp to hour/day/month/etc. | `df.select(date_trunc("hour", "timestamp_col")).show()` |

Example:

```python
df.select(
    trunc("date_col", "month").alias("trunc_month"),
    date_trunc("hour", "timestamp_col").alias("trunc_hour")
).show()
```

---

## 🧠 8. Conditional and Comparison Examples

```python
df.select(
    when(col("date_col") > current_date(), "Future").otherwise("Past").alias("date_status")
).show()
```

---

## 🌍 9. Timezone and UTC Functions

| Function               | Description                   | Example                                                                 |
| ---------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| `from_utc_timestamp()` | Convert UTC to local timezone | `df.select(from_utc_timestamp("timestamp_col", "Asia/Kolkata")).show()` |
| `to_utc_timestamp()`   | Convert local to UTC          | `df.select(to_utc_timestamp("timestamp_col", "Asia/Kolkata")).show()`   |

---

## 🧩 10. Complex Example

```python
df.select(
    col("timestamp_col"),
    current_timestamp().alias("current_ts"),
    datediff(current_date(), to_date("timestamp_col")).alias("days_diff"),
    months_between(current_date(), to_date("timestamp_col")).alias("months_diff"),
    date_add("date_col", 30).alias("plus_30_days"),
    date_format("timestamp_col", "EEEE, MMM dd yyyy HH:mm:ss").alias("formatted")
).show(truncate=False)
```

---

## ✅ Summary Table

| Category   | Common Functions                                                            |
| ---------- | --------------------------------------------------------------------------- |
| Extraction | `year`, `month`, `dayofmonth`, `hour`, `minute`, `second`                   |
| Arithmetic | `date_add`, `date_sub`, `add_months`, `months_between`, `datediff`          |
| Current    | `current_date`, `current_timestamp`, `now`                                  |
| Conversion | `to_date`, `to_timestamp`, `unix_timestamp`, `from_unixtime`, `date_format` |
| Truncation | `trunc`, `date_trunc`                                                       |
| Timezone   | `from_utc_timestamp`, `to_utc_timestamp`                                    |

---

