
This is **100% on-prem / self-hosted friendly** (no Azure / AWS / GCP).

---

## 1️⃣ Data Ingestion Tools (On-Prem, Open Source)

Used to **collect data from databases, files, logs, APIs, streams**.

### Batch Ingestion

* **Apache Sqoop** – RDBMS → HDFS
* **Apache NiFi** – GUI-based ingestion, flow management
* **Talend Open Studio** – ETL ingestion
* **Pentaho Data Integration (Kettle)**
* **Singer** – Lightweight ELT ingestion
* **Airbyte OSS (Self-Hosted)**

### Streaming / Real-Time Ingestion

* **Apache Kafka**
* **Apache Pulsar**
* **Apache Flume**
* **Apache RocketMQ**
* **Redpanda (Kafka-compatible)**

---

## 2️⃣ Data Transformation Tools (On-Prem)

Used for **cleansing, enrichment, aggregation, joins**.

### Big Data / Distributed

* **Apache Spark (Core, SQL, PySpark)**
* **Apache Flink**
* **Apache Beam**
* **Apache Hive (SQL on Hadoop)**
* **Apache Pig**

### SQL-Based Transformation

* **dbt Core (Self-Hosted)**
* **Apache Calcite**
* **Trino / Presto**

### Python / Script-Based

* **Pandas**
* **Dask**
* **PySpark**
* **SQLAlchemy**

---

## 3️⃣ Data Pipeline & Orchestration Tools

Used to **schedule, monitor, retry, and manage dependencies**.

* **Apache Airflow**
* **Apache Oozie**
* **Luigi**
* **Dagster**
* **Argo Workflows**
* **Prefect (Self-Hosted)**
* **Control-M (Enterprise On-Prem)**

---

## 4️⃣ Pipeline Execution / Processing Engines

Where pipelines **actually run**.

* **Apache Spark**
* **Apache Hadoop (MapReduce, YARN)**
* **Apache Flink**
* **Apache Storm**
* **Apache Samza**
* **Kubernetes (On-Prem clusters)**
* **Mesos**

---

## 5️⃣ Data Storage Platforms (On-Prem)

### File & Object Storage

* **HDFS**
* **Ceph**
* **MinIO**
* **GlusterFS**

### Databases (OLTP)

* **PostgreSQL**
* **MySQL**
* **MariaDB**
* **Oracle**
* **SQL Server**
* **MongoDB**
* **Cassandra**
* **HBase**

### Data Warehouse / Analytics

* **Greenplum**
* **ClickHouse**
* **Apache Druid**
* **Apache Pinot**
* **Vertica**
* **Apache Kylin**

### Lake / Table Formats

* **Apache Iceberg**
* **Apache Hudi**
* **Delta Lake (Open Source)**

---

## 6️⃣ Data Visualization & BI Tools (On-Prem)

Used for **dashboards, reporting, analytics**.

### Open Source

* **Apache Superset**
* **Metabase**
* **Redash**
* **Grafana**
* **Kibana**

### Enterprise On-Prem

* **Tableau Server**
* **Qlik Sense**
* **MicroStrategy**
* **IBM Cognos**

---

## 7️⃣ Platforms (On-Prem Data Engineering Platforms)

### Hadoop Ecosystem

* **Apache Hadoop**
* **Cloudera CDP (On-Prem)**
* **Hortonworks (Legacy)**

### Container & Platform

* **Kubernetes**
* **OpenShift**
* **Docker**
* **Rancher**

### Metadata & Governance

* **Apache Atlas**
* **Amundsen**
* **DataHub**
* **OpenMetadata**

---

## 8️⃣ Programming Languages Used (Non-Cloud)

### Core Languages

* **SQL**
* **Python**
* **Java**
* **Scala**

### Supporting / Scripting

* **Bash / Shell**
* **Groovy**
* **R**
* **Perl**

---

## 9️⃣ Typical On-Prem Data Engineer Tech Stack (Example)

```text
Source Systems
   ↓
Apache NiFi / Kafka
   ↓
Apache Spark / Hive
   ↓
HDFS / Iceberg / Delta
   ↓
Airflow (Orchestration)
   ↓
ClickHouse / Greenplum
   ↓
Superset / Tableau Server
```

---

## 🔟 Role Mapping for On-Prem Data Engineers

| Skill Area    | Tools                     |
| ------------- | ------------------------- |
| Ingestion     | NiFi, Kafka, Sqoop        |
| Processing    | Spark, Flink              |
| Storage       | HDFS, Iceberg, PostgreSQL |
| Orchestration | Airflow                   |
| Visualization | Superset, Tableau         |
| Platform      | Hadoop, Kubernetes        |
| Language      | SQL, Python, Scala        |

---

