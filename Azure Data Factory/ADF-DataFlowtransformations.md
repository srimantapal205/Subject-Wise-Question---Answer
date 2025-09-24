# 🔹 ADF Data Flow Activities with Static & Dynamic Examples


| **Activity / Transformation** | **Static Example**                                          | **Dynamic Example**                                                                  |
| ----------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Source**                    | Dataset points to fixed file path: `"/input/Sales2025.csv"` | `"path": "@concat('/input/', pipeline().parameters.FileName)"`                       |
| **Sink**                      | Output path = `"/output/Curated/Sales.csv"`                 | `"path": "@concat('/output/Curated/', pipeline().parameters.FileName)"`              |
| **Select**                    | Map column `"Cust_ID" → "CustomerID"`                       | `"@concat('Cust_', toString(CustomerID))"`                                           |
| **Filter**                    | Condition = `Country == 'US'`                               | `"Country == pipeline().parameters.Region"`                                          |
| **Derived Column**            | `FullName = FirstName + ' ' + LastName`                     | `"FullName = concat(FirstName, ' ', LastName, '-', pipeline().parameters.RunID)"`    |
| **Conditional Split**         | `Country == 'US' → Output1`                                 | `"Country == pipeline().parameters.Region"`                                          |
| **Aggregate**                 | Group by `"State"`, compute `SUM(Sales)`                    | Group by `"@pipeline().parameters.GroupByColumn"`, compute `"SUM(toInteger(Sales))"` |
| **Join**                      | Join condition: `left.CustomerID == right.CustomerID`       | `"left.@{pipeline().parameters.JoinKey} == right.@{pipeline().parameters.JoinKey}"`  |
| **Lookup**                    | Fixed key mapping for `"ProductID"`                         | `"Key = pipeline().parameters.LookupKey"`                                            |
| **Union**                     | Combine fixed datasets A + B                                | Combine `@pipeline().parameters.DatasetList`                                         |
| **Pivot**                     | Pivot `Year` column                                         | `"pivotColumn": "@pipeline().parameters.PivotColumn"`                                |
| **Unpivot**                   | Unpivot `Jan, Feb, Mar` columns                             | `"unpivotColumns": "@pipeline().parameters.MonthList"`                               |
| **Surrogate Key**             | `ID = 1,2,3...`                                             | `"ID = @concat('SK_', toString(surrogateKey()))"`                                    |
| **Window**                    | Rank by `Sales` partitioned by `Region`                     | `"rank() over(partitionBy(@pipeline().parameters.PartitionCol) orderBy Sales desc)"` |
| **Exists**                    | Check if `CustomerID` exists in target                      | `"CustomerID == pipeline().parameters.CheckID"`                                      |
| **Assert**                    | Condition: `Sales > 0`                                      | `"Sales > pipeline().parameters.MinThreshold"`                                       |
| **Cross Join**                | Cartesian join fixed datasets                               | `"crossJoinCondition": "@pipeline().parameters.JoinCondition"`                       |
| **Derived Key (Hash)**        | `Hash = sha1(CustomerID)`                                   | `"Hash = sha1(@concat(CustomerID, pipeline().parameters.Salt))"`                     |
| **Flatten**                   | Expand array field `Items[]`                                | `"path": "@pipeline().parameters.JsonPath"`                                          |
| **Rank** (via Window)         | Rank sales by Customer                                      | `"rank() over(orderBy(@pipeline().parameters.SortColumn))"`                          |
| **Cache Sink**                | Store lookup table in cache, path = `"cache1"`              | `"cacheName": "@pipeline().parameters.CacheName"`                                    |

---

# 🔹 Common Functions in Dynamic Parameters

These are **frequently tested** in interviews:

* **String functions**: `concat()`, `substring()`, `replace()`, `toUpper()`, `toLower()`
* **Math functions**: `abs()`, `round()`, `floor()`, `ceiling()`
* **Date functions**: `currentDate()`, `addDays()`, `toTimestamp()`, `formatDateTime()`
* **Conditional**: `iif(condition, trueValue, falseValue)`, `isNull()`
* **Collection**: `array()`, `length()`, `flatten()`
* **ADF pipeline functions inside Data Flows**:

  * `pipeline().parameters.ParamName`
  * `activity('ActivityName').output`
  * `trigger().outputs`

---
