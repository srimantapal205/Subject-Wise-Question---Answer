
# 🔹 Azure Data Factory Activities – Static vs Dynamic Parameters

| **Activity**            | **Static Example**                            | **Dynamic Example**                                                                                  |
| ----------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Copy Activity**       | `"fileName": "Sales_2025.csv"`                | `"fileName": "@concat('Sales_', pipeline().parameters.Year, '.csv')"`                                |
| **Data Flow Activity**  | Sink = `"adls/container/fixed/"`              | Sink = `"@concat('adls/container/', pipeline().parameters.FolderName)"`                              |
| **Databricks Notebook** | `"FilePath": "/mnt/data/raw/Sales.csv"`       | `"FilePath": "@concat('/mnt/data/raw/', pipeline().parameters.FileName)"`                            |
| **Stored Procedure**    | `"Year": { "value": "2025" }`                 | `"Year": { "value": "@pipeline().parameters.Year" }"`                                                |
| **Execute Pipeline**    | `"FileName": "Sales.csv"`                     | `"FileName": "@pipeline().parameters.FileName"`                                                      |
| **If Condition**        | `"@equals(1,1)"`                              | `"@equals(pipeline().parameters.Environment, 'Prod')"`                                               |
| **Switch**              | `"on": "US"`                                  | `"on": "@pipeline().parameters.Region"`                                                              |
| **ForEach**             | `"items": ["US", "EU", "APAC"]`               | `"items": "@pipeline().parameters.RegionList"`                                                       |
| **Until**               | `"@equals(1,1)"`                              | `"@less(activity('CheckStatus').output.status, 100)"`                                                |
| **Wait**                | `"waitTimeInSeconds": 60`                     | `"waitTimeInSeconds": "@pipeline().parameters.DelayTime"`                                            |
| **Set Variable**        | `"ProdFile.csv"`                              | `"@concat('File_', pipeline().parameters.Date, '.csv')"`                                             |
| **Get Metadata**        | `"fieldList": ["LastModified"]`               | `"@activity('CopyFile').output.destinationBlobPath"`                                                 |
| **Lookup**              | `"query": "SELECT TOP 1 * FROM Config"`       | `"query": "@concat('SELECT * FROM Config WHERE Env = ''', pipeline().parameters.Environment, '''')"` |
| **Web Activity**        | `"url": "https://api.example.com/data/fixed"` | `"url": "@concat('https://api.example.com/data/', pipeline().parameters.ID)"`                        |
| **Execute Data Flow**   | `"SourceTable": "Customer"`                   | `"SourceTable": "@pipeline().parameters.TableName"`                                                  |
| **Delete Activity**     | `"fileName": "OldData.csv"`                   | `"fileName": "@concat(pipeline().parameters.FileName, '.csv')"`                                      |
| **Azure Function**      | `"body": {"FileName": "Sales.csv"}`           | `"body": {"FileName": "@pipeline().parameters.FileName"}`                                            |

---
