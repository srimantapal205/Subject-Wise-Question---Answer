# Azure Databricks (ADB) – Interview Cheat Sheet

## 1. Introduction

* **What is Azure Databricks?**
  A cloud-based big data and AI platform built on Apache Spark.
  Combines **data engineering, data science, and machine learning** on a single platform.
* **Why use it?**
  For scalable data processing, analytics, and ML workflows in Azure.

---

## 2. Core Concepts

* **Workspace**: User environment to organize notebooks, clusters, jobs.
* **Cluster**: Set of compute resources (VMs) to run code.

  * Types: Interactive (for dev), Job (scheduled runs), High-concurrency (shared).
* **Notebook**: Interactive code/document (supports Python, Scala, SQL, R).
* **Jobs**: Automated execution of notebooks, scripts, or workflows.
* **Libraries**: External packages (PyPI, Maven, etc.) attached to clusters.

---

## 3. Architecture

* Built on **Apache Spark** (distributed compute).
* Scales automatically on demand.
* Integrates with **Azure services**: Data Lake, Synapse, ADF, Key Vault, ML, Event Hub.
* Uses **Delta Lake** for reliable storage.

---

## 4. Delta Lake

* Storage layer for **ACID transactions** on data lakes.
* Supports schema evolution, time travel, and upserts/merges.
* Best for incremental loads & slowly changing dimensions.
* Common command: `MERGE INTO` for upserts.

---

## 5. Languages Supported

* Python (PySpark)
* SQL (Spark SQL)
* Scala
* R

---

## 6. Databricks Runtime

* Optimized Spark runtime + libraries.
* Includes built-in connectors and performance tuning.
* Variants: ML runtime, Genomics runtime, etc.

---

## 7. Key Features

* **Data Engineering**: ETL pipelines, batch + streaming.
* **Data Science/ML**: MLflow integration for tracking, training, deployment.
* **Streaming**: Structured Streaming for real-time data.
* **Collaboration**: Multiple users can share notebooks.
* **Scalability**: Auto-scaling clusters.

---

## 8. Security

* **Azure AD integration** for authentication.
* **Role-Based Access Control (RBAC)** for workspaces, clusters, jobs.
* **Secret Management**: Store credentials in Key Vault or Databricks Secrets.
* **Network Security**: VNET injection, private link.

---

## 9. CI/CD & DevOps

* Git integration (Azure DevOps, GitHub) for notebooks.
* Jobs API for automation.
* Infrastructure as Code via Terraform/ARM templates.

---

## 10. Cost Optimization

* Use **spot instances** where possible.
* Auto-terminate inactive clusters.
* Use **job clusters** instead of all-purpose clusters for scheduled jobs.

---

## 11. Monitoring

* Native monitoring via Databricks UI (jobs, clusters).
* Integration with **Azure Monitor, Log Analytics, Application Insights**.
* Audit logs for compliance.

---

## 12. Common Interview Q&A Pointers

* **What’s the difference between Databricks and Azure Synapse?**
  Databricks = big data + ML; Synapse = data warehousing + reporting.
* **Why Delta Lake?**
  Brings reliability (ACID), schema evolution, and time travel to data lakes.
* **How do you handle schema drift?**
  Delta Lake with schema evolution options.
* **What is a Job Cluster vs Interactive Cluster?**
  Job cluster is ephemeral (for scheduled jobs), Interactive is for dev/testing.
* **Difference between ADF and Databricks?**
  ADF = orchestration & data movement; Databricks = transformation & ML.

---

## 13. Best Practices

* Keep **clusters small** for dev, scale up for production.
* Use **Delta format** instead of Parquet/CSV.
* Separate environments (Dev, Test, Prod).
* Modularize notebooks and parameterize jobs.
* Store secrets in Key Vault or Databricks Secret Scope.

---

## 14. Real-Time Use Cases

* Data ingestion + transformation for analytics dashboards.
* Machine Learning model training and deployment.
* Real-time fraud detection with structured streaming.
* Data lakehouse architecture using Delta Lake.
* ETL pipelines with ADF + Databricks combo.

---

