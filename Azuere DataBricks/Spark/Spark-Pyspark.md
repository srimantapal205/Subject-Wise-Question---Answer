# Spark and PySpark Inter View Question & Answer

### 1. What is spark? Explain Architecture
**Answer:**
Apache Spark is an open-source distributed computing framework for big data processing, known for its speed and ease of use. It consists of:

+ Spark Core: The foundation of Spark that includes memory management, fault recovery, and task scheduling.
+ Cluster Manager: Can be YARN, Mesos, or Spark’s standalone cluster manager.
+ Executors: Run tasks assigned by the driver and store computation results.
+ Driver: The main program that coordinates and schedules tasks.

        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName("SparkExample").getOrCreate()

### 2. Explain where did you use spark in your project?
**Answer:**


### 3. What all optimization techniques have you used in spark?
**Answer:**
+ Broadcast Joins to reduce shuffle
+ Caching and Persistence for iterative operations
+ Columnar Storage (Parquet Format) for efficient read/write
+ Partitioning to distribute data evenly
+ Predicate Pushdown to filter early in queries


### 4. Explain transformations and actions have you used?
**Answer:**
+ Transformations: map(), filter(), groupBy(), join(), reduceByKey()
+ Actions: count(), collect(), show(), saveAsTextFile()

        rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
        filtered_rdd = rdd.filter(lambda x: x % 2 == 0) # Transformation
        print(filtered_rdd.collect()) # Action

### 5. What happens when you use shuffle in spark?
**Answer:**
Shuffle occurs when data is redistributed across partitions, causing increased network I/O and execution time.

### 6. Difference between ReduceByKey Vs GroupByKey?
**Answer:**
+ reduceByKey() performs aggregation locally before shuffling, making it more efficient.

+ groupByKey() shuffles all values before aggregation, leading to higher memory usage.

        rdd = spark.sparkContext.parallelize([("a", 1), ("b", 2), ("a", 3)])
        reduced = rdd.reduceByKey(lambda x, y: x + y)
        print(reduced.collect())

### 7. Explain the issues you resolved when you working with spark?
**Answer:**
+ Out of Memory Errors: Fixed by optimizing executor memory.

+ Data Skew: Resolved using salting techniques.

+ Slow Performance: Used caching and broadcast joins.

### 8. Compare Spark vs Hadoop MapReduce?
**Answer:**
* Spark processes data in-memory; MapReduce uses disk-based processing.

* Spark supports real-time streaming; MapReduce is batch-oriented.

### 9. Difference between Narrow & wide transformations?
**Answer:**
+ Narrow Transformation: Data is processed within a partition (e.g., map, filter).

+ Wide Transformation: Requires shuffling across partitions (e.g., groupBy, join).

### 10. What is partition and how spark Partitions the data?
**Answer:** 
Partitions are logical divisions of data in Spark. Spark partitions data automatically based on cluster configuration and input data source.


### 11. What is RDD?
**Answer:** 
Resilient Distributed Dataset (RDD) is Spark's core data structure that provides fault tolerance and distributed processing.

### 11. what is broadcast variable?
**Answer:** 
A broadcast variable is used to efficiently distribute large read-only data across all worker nodes.

### 12. Difference between Sparkcontext Vs Sparksession?
**Answer:** 
SparkContext is the entry point for RDD operations, while SparkSession unifies SQL, DataFrame, and streaming APIs.

### 13. Explain about transformations and actions in the spark?
**Answer:** 
+ SparkContext: Entry point for RDD-based APIs.
+ SparkSession: Unified entry point for DataFrame and Dataset APIs.

### 14. what is Executor memory in spark?
**Answer:** 
Each Spark executor has a memory allocation divided into storage, execution, and overhead.

### 15. What is lineage graph?
**Answer:** 
A lineage graph tracks the sequence of transformations applied to an RDD for fault recovery.

### 16. What is DAG?
**Answer:** 
DAG (Directed Acyclic Graph) is a logical execution plan representing dependencies between RDDs.

### 17. Explain libraries that Spark Ecosystem supports?
**Answer:** 
+ Spark SQL: For structured data processing
+ Spark Streaming: For real-time data processing
+ MLlib: For machine learning
+ GraphX: For graph processing

### 18. What is a DStream?
**Answer:** 
DStream (Discretized Stream) is a sequence of RDDs representing continuous data streams.

### 19. What is Catalyst optimizer and explain it?
**Answer:** 
Catalyst Optimizer is Spark SQL’s query optimizer that improves query performance through logical and physical plan optimizations.

### 20. Why parquet file format is best for spark?
**Answer:** 
+ Columnar storage improves read performance
+ Supports predicate pushdown
+ Compression reduces storage space

### 21. Difference between dataframe Vs Dataset Vs RDD?
**Answer:** 
|Feature | RDD  | DataFrame | Dataset|
|--------|------|--------|--------|
|Type |Safety| No |No| Yes|
|Performance| Low| High| High|
|API Support| Java, Scala, Python |Java, Scala, Python |Scala, Java|

### 22. Explain features of Apache Spark?
**Answer:** 
+ Speed
+ Lazy Evaluation
+ Fault Tolerance
+ Real-Time Processing
+ Unified Analytics

### 23. Explain Lazy evaluation and why is it need?
**Answer:** 
Lazy evaluation means Spark does not execute transformations until an action is called. This optimizes execution.

### 24. Explain Pair RDD?
**Answer:** 
Pair RDDs store key-value pairs, allowing efficient groupByKey and reduceByKey operations.

### 25. What is Spark Core?
**Answer:** 
Spark Core is the foundational engine handling distributed execution, scheduling, and fault tolerance.

### 26. What is the difference between persist() and cache()?
**Answer:** 
+ cache() stores data in memory.

+ persist() allows different storage levels (e.g., disk, memory).

### 27. What are the various levels of persistence in Apache Spark?
**Answer:** 
+ MEMORY_ONLY

+ MEMORY_AND_DISK

+ DISK_ONLY


### 28. Does Apache Spark provide check pointing?
**Answer:** 
Yes, checkpointing saves RDDs to reliable storage for fault tolerance.

### 29. How can you achieve high availability in Apache Spark?
**Answer:** 
+ Deploy Spark on a cluster with multiple worker nodes.

+ Use checkpointing.


### 30. Explain Executor Memory in a Spark?
**Answer:** 
Executor memory is split into storage memory (for caching) and execution memory (for computation).

### 31. What are the disadvantages of using Apache Spark?
**Answer:** 
+ High memory consumption

+ Complexity in tuning

+ No built-in file storage


### 32. What is the default level of parallelism in apache spark?
**Answer:** 
The default level of parallelism is determined by the number of available CPU cores.

### 33. Compare map() and flatMap() in Spark?
**Answer:** 
+ map(): Transforms each element into one output.

+ flatMap(): Transforms each element into multiple outputs.

### 34. Difference between repartition Vs coalesce?
**Answer:** 
* repartition() increases/decreases partitions with shuffle.

* coalesce() only reduces partitions efficiently.

### 35. Explain Spark Streaming?
**Answer:** 
Spark Streaming processes real-time data by dividing it into micro-batches and processing them using DStreams.

### 36. Explain accumulators?
**Answer:** 
Accumulators are shared variables used for aggregating values across worker nodes.

### 37. What is the use of broadcast join?
**Answer:** 
Broadcast join improves performance by sending a small dataset to all worker nodes instead of shuffling large data.