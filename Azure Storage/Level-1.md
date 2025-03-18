# Azure storage Level 1 Question Answer

### Question 1: What is Azure storage?

**Answer:** 

Azure storage is a cloud-based storage solution provided by Microsoft. It allows users to store different types of data such as images, files, audio, video, and binary data on the cloud. This data can be accessed in various ways, including through a browser, programmatically, or using protocols like HTTPS and REST APIs. Azure storage supports access via PowerShell scripts and is designed for flexible and secure data handling.
 
### Question 2: What are the benefits of Azure storage?
**Answer:** The benefits of Azure storage include:

- Durability: Data is replicated across multiple locations to ensure availability, even during server failures or natural disasters.
- Security: Data is stored and transmitted in an encrypted form.
- Scalability: Storage capacity can be scaled up or down as needed without predefined limits.
- Managed Service: Azure handles maintenance, performance tuning, and patch deployment.
- Accessibility: Data can be accessed through multiple methods, including REST APIs, programmatic access, and PowerShell scripts.

### Question 3: What are the different Azure storage data services?
**Answer:**
1. Azure Blobs: Stores text and binary data, including files like CSV, images, and videos.
2. Azure Files: A shared folder service for applications that require shared folder access.
3. Azure Queues: Facilitates message queuing for communication between services.
4. Azure Tables: A NoSQL storage solution for high-performance, schema-less data storage.
5. Azure Disks: Block-level storage volumes that can be attached to virtual machines, similar to local hard disks.

### Question 4: What is Azure Blob storage?
**Answer:** Azure Blob storage is a service for storing unstructured data like documents and multimedia files. It supports data access through REST APIs and is suitable for use cases such as image/document storage, streaming applications, log storage, and backup solutions. It is a durable solution due to its data replication capabilities, making it a good choice for disaster recovery.

### Question 5: What is Azure Data Lake Storage Gen2?
**Answer:** Azure Data Lake Storage Gen2 is an advanced storage solution built for big data analytics. It combines the advantages of Azure Blob storage with features optimized for high-performance analytics. It supports hierarchical file systems, which enable the organization of data into nested folders and subfolders for better data management.

### Question 6: What is Azure Files?
**Answer:** Azure Files is a file-sharing service in the cloud, accessible via SMB or NFS protocols. It enables shared folder functionality across Windows, Linux, and macOS, allowing users to map it as a local drive for collaborative access.
 
### Question 7: What are the key benefits of Azure Files?
**Answer:**
1. Shared Access: Accessible by multiple users/groups.
2. Fully Managed: No need for manual maintenance; Azure handles all backend management.
3. Scripting and Tooling: Can be accessed via PowerShell or Bash scripts.
4. Resilience: Fault-tolerant with high availability.
5. Programmability: Supports familiar programming languages for integration.

### Question 8: What is Azure Queue Storage?
**Answer:** Azure Queue Storage stores large volumes of messages, with each message being up to 64 KB in size. It supports asynchronous communication between heterogeneous applications (e.g., .NET and Java) and can hold millions of messages, making it ideal for decoupling systems. Access is available via HTTPS or authenticated calls.

### Question 9:Does Azure Queue Storage guarantee ordering?
**Answer:** No. While Azure Queue Storage generally follows a first-in, first-out (FIFO) model where messages are pushed and popped in sequence, the ordering may sometimes be disturbed. Therefore, Azure Queue Storage does not guarantee message ordering. If strict ordering is required, Azure Service Bus is a better option as it guarantees message ordering.

### Question 10:What is Azure Table Storage?
**Answer:** Azure Table Storage is a type of NoSQL database. Unlike relational databases, which have a fixed schema with structured rows and columns, Azure Table Storage supports unstructured data where rows can have different numbers of columns or entirely different columns. It is a column-oriented database that does not enforce a fixed schema. Azure Table Storage is cost-effective, capable of storing terabytes of data, and optimized for fast data retrieval, even from large datasets. It is an excellent choice for scenarios requiring high-speed querying and retrieval of data.
