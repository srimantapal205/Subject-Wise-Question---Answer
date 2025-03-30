Lecture: Project Overview


ECDC Website for Covid-19 Data - https://www.ecdc.europa.eu/en/covid-19/data

Euro Stat Website for Population Data - https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/tps00010.tsv.gz

Lecture: Azure Storage Solutions


Introduction to Azure Storage services - https://docs.microsoft.com/en-us/azure/storage/common/storage-introduction



Azure SQL Database - https://docs.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview



Azure Synapse Analytics - https://docs.microsoft.com/en-us/azure/synapse-analytics/overview-what-is



Azure Cosmos DB - https://docs.microsoft.com/en-us/azure/cosmos-db/introduction



Azure Data Lake Storage Gen2 - https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction




Useful Links & Resources
Section: Environment Set-up


Lecture: Creating Azure Free Account


Free Account - https://azure.microsoft.com/en-gb/free/

Students Free Account - https://azure.microsoft.com/en-gb/free/students/



Lecture: Azure Portal Overview


Azure Portal - https://azure.microsoft.com/en-gb/free/students/



Lecture: Creating Azure Data Factory


https://docs.microsoft.com/en-gb/azure/data-factory/quickstart-create-data-factory-portal

https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview#available-regions



Lecture: Creating Azure Storage Account


https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal



Lecture: Installing Azure Storage Explorer


https://azure.microsoft.com/en-us/products/storage/storage-explorer



Lecture: Creating Azure Data Lake Gen2


https://docs.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account



Lecture: Creating Azure SQL Database


https://docs.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?tabs=azure-portal



Lecture: Installing Azure Data Studio


https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver16\

Section: Data Ingestion From Blob


Lecture: Copy Activity Introduction


https://docs.microsoft.com/en-us/azure/data-factory/copy-activity-overview

Lecture: Linked Services & Datasets


https://docs.microsoft.com/en-us/azure/data-factory/concepts-linked-services

https://docs.microsoft.com/en-us/azure/data-factory/concepts-datasets-linked-services



Lecture: Create Pipeline


https://docs.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities



Lecture: Control Flow Activities


Validation Activity - https://docs.microsoft.com/en-us/azure/data-factory/control-flow-validation-activity

Get Metadata Activity - https://docs.microsoft.com/en-us/azure/data-factory/control-flow-get-metadata-activity

If Condition Activity - https://docs.microsoft.com/en-us/azure/data-factory/control-flow-if-condition-activity

Web Activity - https://docs.microsoft.com/en-us/azure/data-factory/control-flow-web-activity

Delete Activity - https://docs.microsoft.com/en-us/azure/data-factory/delete-activity

Fail Activity - https://learn.microsoft.com/en-us/azure/data-factory/control-flow-fail-activity



Lecture: Triggers


https://docs.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers


Frequently Asked Questions - Please Read
FAQ-1 - Wrong content being copied

There are a handful of students who had difficultly copying data from https://github.com. The copy activity sometimes pulled the HTML page rather than the CSV file being requested to be copied across.

This was resolved by using sourceBaseURL as https://raw.githubusercontent.com rather than https://github.com. So, please use the URL https://raw.githubusercontent.com if you come across this issue. Also ensure that the RelativeUrl is also changed to remove "raw" as below

BaseUrl - https://raw.githubusercontent.com


Useful Links & Resources
Section: Data Flow – Cases & Deaths Data Transformation
Lecture: Introduction to Data Flows


Overview - https://docs.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview



Available Regions - https://docs.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview



Lecture: Source Transformation
Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-source



Supported Source Type - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-source#supported-sources



Inline Datasets - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-source#supported-sources



Lecture: Filter Transformation
Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-filter



Expression Builder - https://docs.microsoft.com/en-us/azure/data-factory/concepts-data-flow-expression-builder



Expression Language - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-expression-functions



Lecture – Select Transformation
Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-select



Lecture - Pivot Transformation
Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-pivot



Lecture - Lookup Transformation
Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-lookup



Lecture – Sink Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-sink

Supported Sink Types - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-sink



Lecture – Create ADF Pipeline
Overview - https://docs.microsoft.com/en-us/azure/data-factory/control-flow-execute-data-flow-activity


Useful Links & Resources
Section: Data Flow - Hospital Admissions Data Transformation


Lecture: Conditional Split Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-conditional-split



Lecture: Derived Column Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-derived-column



Lecture: Aggregate Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-aggregate



Lecture: Join Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-join



Lecture: Sort Transformation


Overview - https://docs.microsoft.com/en-us/azure/data-factory/data-flow-sort

Section: HDInsight Activity


Lecture: Create HDInsight Cluster


Overview - https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-overview



Creation via Azure Portal - https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-provision-linux-clusters



Pricing - https://azure.microsoft.com/en-gb/pricing/details/hdinsight/



Lecture: Tour of the HDInsight UI


Ambari UI - https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-manage-ambari



Squirrel download – http://squirrel-sql.sourceforge.net/



DBVisualiser download – https://www.dbvis.com/



Lecture: Create ADF Pipeline with Hive Activity


Hive Activity - https://docs.microsoft.com/en-us/azure/data-factory/v1/data-factory-hive-activity



Lecture - Delete HDInsight Cluster


https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-administer-use-portal-linux#delete-clusters

Section: Data Bricks Activity


Architecture - https://docs.microsoft.com/en-us/azure/databricks/getting-started/overview



Lecture: Create Azure Databricks Service


https://docs.microsoft.com/en-us/azure/databricks/scenarios/quickstart-create-databricks-workspace-portal?tabs=azure-portal



Lecture: Create Azure Databricks Cluster


https://docs.microsoft.com/en-us/azure/databricks/scenarios/quickstart-create-databricks-workspace-portal?tabs=azure-portal#create-a-spark-cluster-in-databricks



Lecture: Mounting Azure Data Lake Storage


https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/azure/azure-datalake-gen2



Lecture: Create ADF Pipeline Databricks Notebook Activity


https://docs.microsoft.com/en-us/azure/data-factory/transform-data-using-databricks-notebook

Section: Copy Data to Azure SQL


Copy Activity - https://docs.microsoft.com/en-us/azure/data-factory/copy-activity-overview



Azure Data Studio download - https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15

