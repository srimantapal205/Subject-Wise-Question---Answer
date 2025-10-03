# Azure Data Factory (ADF) – Interview Cheat Sheet

## 1. Introduction

* **What is ADF?**
  Azure Data Factory (ADF) is a cloud-based data integration service to move, transform, and load data (ETL/ELT).
* **Use case:** Orchestrate data pipelines across on-premises and cloud sources.

---

## 2. Core Components

* **Pipeline**: A workflow that defines a sequence of activities.
* **Activity**: A single step (copy, transformation, lookup, stored proc, etc.).
* **Datasets**: Schema + location of data (input/output).
* **Linked Services**: Connection info to data sources/destinations.
* **Triggers**: Schedule or event-based pipeline execution.
* **Integration Runtime (IR)**: Compute environment for data movement/activities (AutoResolve IR, Self-hosted IR, Azure-SSIS IR).

---

## 3. Data Integration Patterns

* **ETL (Extract, Transform, Load)**: Data transformed before loading.
* **ELT (Extract, Load, Transform)**: Load raw data first, transform later (common with Azure Synapse/Databricks).
* **Data Movement**: Copy data from source to sink.
* **Data Transformation**: Data Flow activities, Databricks notebooks, Azure Functions, etc.

---

## 4. Triggers

* **Schedule trigger**: Time-based (daily, hourly).
* **Tumbling window trigger**: Fixed-size, contiguous intervals.
* **Event-based trigger**: Responds to Blob/file creation/deletion.
* **Manual (On-demand)**: Trigger pipeline run manually.

---

## 5. Integration Runtime (IR) Types

* **Azure IR**: Fully managed, for cloud data movement.
* **Self-Hosted IR**: For on-premises or private network data.
* **Azure-SSIS IR**: To lift-and-shift SSIS packages.

---

## 6. Activities

* **Data Movement Activities**: Copy Activity.
* **Data Transformation Activities**: Mapping Data Flows, Databricks, HDInsight, Azure Batch.
* **Control Activities**: If Condition, ForEach, Until, Execute Pipeline, Set Variable, Web, Lookup.
* **External Activities**: Stored procedure execution, custom code, functions.

---

## 7. Monitoring

* **ADF Studio** → Monitor tab.
* Provides run history, logs, success/failure status.
* Integration with Azure Monitor, Log Analytics, Alerts.

---

## 8. Security

* **Authentication**: Managed Identity, Service Principal, Key Vault.
* **Data Protection**: SSL, encryption at rest.
* **RBAC**: Role-Based Access Control in ADF.

---

## 9. CI/CD in ADF

* Git integration with Azure DevOps or GitHub.
* Branching strategy: collaboration branch, feature branch.
* ARM templates for deployment across environments.

---

## 10. Pricing

* Based on:

  * Pipeline orchestration runs.
  * Data movement (per DIU-hour).
  * Data Flow execution (vCores + time).

---

## 11. Common Interview Q&A Pointers

* **Difference between Dataset and Linked Service?**
  Linked service = connection string; Dataset = data structure reference.
* **How do you handle incremental loads?**
  Use watermark columns, parameters, tumbling window triggers.
* **Difference between ETL and ELT in ADF?**
  ETL = transformation before load; ELT = load raw, transform in destination.
* **What is Self-Hosted IR used for?**
  Access on-prem or private network data.
* **How to handle schema drift?**
  Use Mapping Data Flows with "Auto Mapping" & schema drift handling.

---

## 12. Best Practices

* Use **parameters** and **variables** for dynamic pipelines.
* Modularize pipelines using **Execute Pipeline activity**.
* Store secrets in **Azure Key Vault**.
* Monitor with alerts and retry policies.
* Optimize data flows by **partitioning** and **debugging before publish**.

---

## 13. Integrations

* Works with Azure Synapse, Databricks, Data Lake, Cosmos DB, SQL DB, Blob, SAP, Salesforce, etc.
* Can trigger **Databricks notebooks** or **Azure Functions**.

---

## 14. Real-Time Use Cases

* Migrating on-prem databases to Azure SQL / Synapse.
* Data lake ingestion from multiple sources.
* Orchestrating machine learning pipelines.
* Incremental data loading for reporting dashboards.
* Event-driven data movement (e.g., new file in Blob triggers pipeline).

---

