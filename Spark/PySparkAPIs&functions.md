# 🔹 PySpark API and Functions Guide

## 1. PySpark Setup

```python
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("PySpark Guide") \
    .getOrCreate()
```

* **Explanation**: Every PySpark program starts with a `SparkSession`, which is the entry point to Spark.

---

## 2. Creating DataFrames

```python
data = [("Alice", 25), ("Bob", 30), ("Cathy", 28)]
columns = ["name", "age"]

df = spark.createDataFrame(data, columns)
df.show()
```

* **Explanation**: `createDataFrame()` is used to make structured datasets.

---

## 3. Basic DataFrame Operations

### Show & Schema

```python
df.show(2)      # Show top 2 rows
df.printSchema()  # Show schema
```

### Select & Filter

```python
df.select("name").show()
df.filter(df.age > 26).show()
```

### With Column

```python
from pyspark.sql.functions import col

df.withColumn("age_plus_5", col("age") + 5).show()
```

### Rename Column

```python
df.withColumnRenamed("age", "years").show()
```

---

## 4. Aggregations

```python
from pyspark.sql.functions import avg, count, max

df.groupBy("name").agg(
    avg("age").alias("avg_age"),
    max("age").alias("max_age")
).show()
```

* **Explanation**: `groupBy` + `agg` are used for summary stats.

---

## 5. Joins

```python
data2 = [("Alice", "F"), ("Bob", "M")]
df2 = spark.createDataFrame(data2, ["name", "gender"])

df.join(df2, "name", "inner").show()
```

* **Explanation**: Supports `inner`, `left`, `right`, `outer` joins.

---

## 6. SQL with DataFrames

```python
df.createOrReplaceTempView("people")
spark.sql("SELECT name, age FROM people WHERE age > 26").show()
```

* **Explanation**: You can use SQL directly on DataFrames.

---

## 7. Common Built-in Functions

```python
from pyspark.sql.functions import lit, when, concat_ws

# Constant column
df.withColumn("country", lit("USA")).show()

# Conditional column
df.withColumn("category", when(df.age > 28, "Senior").otherwise("Junior")).show()

# String concat
df.withColumn("info", concat_ws("-", "name", "age")).show()
```

---

## 8. Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import rank

window_spec = Window.orderBy("age")
df.withColumn("rank", rank().over(window_spec)).show()
```

* **Explanation**: Useful for ranking, running totals, partitioning.

---

## 9. Handling Nulls

```python
df.na.fill({"age": 0}).show()  # Replace nulls
df.na.drop().show()            # Drop rows with nulls
```

---

## 10. Writing & Reading Data

```python
# Write
df.write.mode("overwrite").parquet("people.parquet")

# Read
df_parquet = spark.read.parquet("people.parquet")
df_parquet.show()
```

* **Formats supported**: CSV, JSON, Parquet, ORC, Delta.

---

## 11. RDD API (Low-level)

```python
rdd = spark.sparkContext.parallelize([1, 2, 3, 4])
print(rdd.map(lambda x: x*2).collect())
print(rdd.filter(lambda x: x > 2).collect())
```

* **Explanation**: RDD is the older API, mostly replaced by DataFrames.

---

## 12. MLlib Example (Machine Learning)

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

data = [(1, 2.0, 3.0), (2, 5.0, 7.0), (3, 6.0, 9.0)]
df_ml = spark.createDataFrame(data, ["id", "x", "y"])

assembler = VectorAssembler(inputCols=["x"], outputCol="features")
train = assembler.transform(df_ml)

lr = LinearRegression(featuresCol="features", labelCol="y")
model = lr.fit(train)

model.transform(train).show()
```

* **Explanation**: MLlib supports regression, classification, clustering, etc.

---

## 13. Streaming Example

```python
# Example: read streaming data from a folder
stream_df = spark.readStream \
    .schema(df.schema) \
    .csv("streaming_data/")

query = stream_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
```

* **Explanation**: Handles real-time data pipelines.

---

Awesome 🚀 Here’s a **PySpark Full Reference ** 

---

# 🔹 PySpark Cheatsheet

## 1. Setup

| Operation            | Code                                                        | Explanation             |
| -------------------- | ----------------------------------------------------------- | ----------------------- |
| Create Spark session | `spark = SparkSession.builder.appName("App").getOrCreate()` | Entry point for PySpark |

---

## 2. Create DataFrame

| Operation | Code                                                             | Explanation      |
| --------- | ---------------------------------------------------------------- | ---------------- |
| From list | `df = spark.createDataFrame([("Alice",25)], ["name","age"])`     | Create DataFrame |
| From RDD  | `df = rdd.toDF(["col1","col2"])`                                 | Convert RDD → DF |
| From file | `df = spark.read.csv("file.csv", header=True, inferSchema=True)` | Load CSV         |

---

## 3. Inspect Data

| Operation | Code               | Explanation    |
| --------- | ------------------ | -------------- |
| Show rows | `df.show(5)`       | Display 5 rows |
| Schema    | `df.printSchema()` | Show schema    |
| Columns   | `df.columns`       | List columns   |
| Count     | `df.count()`       | Row count      |

---

## 4. Select & Filter

| Operation     | Code                                            | Explanation     |
| ------------- | ----------------------------------------------- | --------------- |
| Select col    | `df.select("name")`                             | Pick column     |
| Filter        | `df.filter(df.age > 25)`                        | Apply condition |
| Multiple cond | `df.filter((df.age > 25) & (df.name=="Alice"))` | AND/OR filters  |

---

## 5. Column Ops

| Operation  | Code                                          | Explanation |
| ---------- | --------------------------------------------- | ----------- |
| Add col    | `df.withColumn("age2", df.age+2)`             | New column  |
| Rename col | `df.withColumnRenamed("age","years")`         | Rename      |
| Drop col   | `df.drop("age")`                              | Remove col  |
| Cast col   | `df.withColumn("age", df.age.cast("string"))` | Change type |

---

## 6. Aggregations

| Operation    | Code                                            | Explanation        |
| ------------ | ----------------------------------------------- | ------------------ |
| GroupBy      | `df.groupBy("name").count()`                    | Group + count      |
| Agg funcs    | `df.agg({"age":"avg"})`                         | Avg, sum, max, min |
| Multiple agg | `df.groupBy("dept").agg(avg("age"),max("age"))` | Multi stats        |

---

## 7. Joins

| Operation  | Code                         | Explanation |
| ---------- | ---------------------------- | ----------- |
| Inner join | `df1.join(df2,"id","inner")` | Match keys  |
| Left join  | `df1.join(df2,"id","left")`  | Keep left   |
| Full join  | `df1.join(df2,"id","outer")` | Keep all    |

---

## 8. SQL Queries

| Operation      | Code                                   | Explanation     |
| -------------- | -------------------------------------- | --------------- |
| Register table | `df.createOrReplaceTempView("people")` | Use in SQL      |
| Run SQL        | `spark.sql("SELECT * FROM people")`    | Query DataFrame |

---

## 9. Built-in Functions

| Operation     | Code                                           | Explanation    |
| ------------- | ---------------------------------------------- | -------------- |
| Literal col   | `lit("USA")`                                   | Constant value |
| Conditional   | `when(df.age>30,"Senior").otherwise("Junior")` | IF-ELSE        |
| String concat | `concat_ws("-",df.name,df.age)`                | Concatenate    |
| Date func     | `current_date(), date_add(df.date,10)`         | Date ops       |

---

## 10. Window Functions

| Operation     | Code                                    | Explanation   |
| ------------- | --------------------------------------- | ------------- |
| Define window | `w = Window.orderBy("age")`             | Create window |
| Rank          | `df.withColumn("rank", rank().over(w))` | Ranking       |
| Row number    | `row_number().over(w)`                  | Sequential ID |

---

## 11. Null Handling

| Operation  | Code                    | Explanation    |
| ---------- | ----------------------- | -------------- |
| Drop nulls | `df.na.drop()`          | Remove rows    |
| Fill nulls | `df.na.fill({"age":0})` | Replace values |

---

## 12. File I/O

| Operation     | Code                                         | Explanation |
| ------------- | -------------------------------------------- | ----------- |
| Write Parquet | `df.write.mode("overwrite").parquet("out/")` | Save        |
| Read Parquet  | `spark.read.parquet("out/")`                 | Load        |
| Write CSV     | `df.write.csv("out.csv",header=True)`        | Save CSV    |

---

## 13. RDD API

| Operation  | Code                                            | Explanation |
| ---------- | ----------------------------------------------- | ----------- |
| Create RDD | `rdd = spark.sparkContext.parallelize([1,2,3])` | New RDD     |
| Map        | `rdd.map(lambda x:x*2).collect()`               | Transform   |
| Filter     | `rdd.filter(lambda x:x>2).collect()`            | Keep values |

---

## 14. MLlib (Basic)

| Operation       | Code                                                            | Explanation |
| --------------- | --------------------------------------------------------------- | ----------- |
| VectorAssembler | `VectorAssembler(inputCols=["x"],outputCol="features")`         | Features    |
| Train model     | `LinearRegression(featuresCol="features",labelCol="y").fit(df)` | ML model    |

---

## 15. Streaming

| Operation    | Code                                              | Explanation   |
| ------------ | ------------------------------------------------- | ------------- |
| Read stream  | `df = spark.readStream.csv("path",schema=schema)` | Stream input  |
| Write stream | `df.writeStream.format("console").start()`        | Stream output |

---

