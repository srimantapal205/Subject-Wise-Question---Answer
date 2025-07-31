# Azure Storage All Levels Combined

---
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

# Azure Sorage Level 2 Question

### Question 11: Can a storage account name be duplicate? Provide the reason.
**Answer:**: 
No, a storage account name cannot be duplicate. This applies not only within your account but across all Azure clients. The reason is tied to the URL created for accessing the storage account. Each storage account has a unique endpoint in the format:'' <storage_account_name> ''.blob.core.windows.net.

If duplicate storage account names were allowed, multiple storage accounts would have the same URL, leading to conflicts in identifying which account to access. To prevent this issue, Azure enforces unique storage account names, ensuring every storage account is accessible via a distinct URL.

This concept is similar to domain names on the internet; for example, if a domain like facebook.com already exists, it cannot be reused by another website because URLs must be unique.

### Question 12: What are the different types of blobs in Azure Storage?
**Answer:**: There are three types of blobs in Azure Storage:
    
1. Block Blobs:
    - Comprises blocks of data, where each block is uploaded separately and then assembled into a blob.
    - Ideal for storing text or binary files such as images, videos, and documents.
    - Maximum storage capacity is 190 terabytes.
    - Default blob type in Azure Storage.
2. Append Blobs:
    - Designed specifically for append operations, such as logging.
    - New data can only be added to the end of the blob, making it ideal for scenarios like maintaining logs.
    - Unlike block blobs, updating or deleting existing blocks is not supported.
3. Page Blobs:
    - Used for random read and write operations.
    - Maximum size is 8 terabytes.
    - Commonly used to store virtual hard drive (VHD) files, which serve as disks for Azure Virtual Machines.
By default, Azure Blob Storage uses block blobs, but users can specify the blob type during the upload process in the Azure portal under advanced options.


### Question 13: What are the factors affecting the cost of a storage account in Azure?
**Answer:**: The cost of an Azure storage account is influenced by the following six factors:

1. Region:
    - The geographical location where the storage account is created affects the cost.
    - Some regions, like the U.S., may have higher storage costs, while others, such as regions with lower living costs, may be cheaper.
2. Account Type:
    - Storage accounts can be of different types, such as Standard or Premium, each with different pricing tiers.
3. Access Tier:
    - Azure storage offers three access tiers: Hot, Cool, and Archive.
        - Hot: Optimized for frequently accessed data but is more expensive.
        - Cool: Suitable for infrequently accessed data, offering moderate cost savings.
        - Archive: Best for rarely accessed data with the lowest storage cost but higher retrieval costs.
4. Redundancy Level:
    - Azure offers various redundancy options:
        - Local Redundant Storage (LRS): Cheapest but only keeps copies within a single region, increasing the risk of data loss.
        - Geo-Redundant Storage (GRS) or Zone-Redundant Storage (ZRS): More expensive but ensures higher resilience by storing data across regions or zones.
5. Transactions:
    - Costs are incurred for data transactions (e.g., reads, writes, and deletes).
    - More frequent transactions result in higher costs.
6. Data Egress:
    - Moving data out of an Azure region incurs additional costs.
    - Keeping data within the same region avoids this expense.

Optimization: To optimize costs, adjust these parameters based on your use case, such as selecting a cost-effective region, using appropriate access tiers, or minimizing cross-region data movement.


### Question 14: What are the different ways of authorizing data access for a storage account?
**Answer:** :There are three main ways to authorize access to a storage account in Azure:
    
1. Account Access Keys:
    - These provide full access to the storage account, including all its services (e.g., blob storage, file shares, queues, containers).
    - Access keys allow actions like adding, deleting, and updating data.
    - This method is powerful but risky due to its broad access scope and is generally avoided.
2. Shared Access Signature (SAS) Token:
    - Provides granular, customizable access to storage resources.
    - Access can be limited to specific services (e.g., blob, file, queue) or specific objects.
    - Permissions (e.g., read, write, list) and the duration of access can also be specified.
3. Azure Active Directory (AAD):
    - Access is granted based on roles assigned to users, service principals, or groups.
    - Roles are managed through the "Access Control (IAM)" option in the Azure Portal.

### Question 15: How does Azure ensure data security for storage accounts?
**Answer:**: Azure ensures data security for storage accounts through the following mechanisms:
    
1. Server-Side Encryption (SSE):
    - All data stored in Azure storage accounts is encrypted at rest.
    - Even if unauthorized access occurs, the data remains unreadable due to encryption.

    - By default, the retention period is 7 days, but it can be configured up to 90 days.
    - During this time, the deleted item remains accessible for restoration.
3. Restoration Process:
    - Navigate to the Azure portal and view deleted containers by toggling the "Show deleted containers" option.
    - Select the deleted container and choose the "Undelete" option to restore it.
4. Configuration:
    - Ensure the soft delete feature is enabled under the "Data Protection" settings in your storage account.
    - Specify the desired retention period for soft delete to function effectively.

This feature provides a safeguard against accidental deletions and ensures that data can be recovered within the specified retention timeframe.


### Question 18: What is the AZCopy tool?
**Answer:**: AZCopy is a command-line tool provided by Azure for transferring data to and from Azure storage accounts. It offers a more streamlined and automated alternative to the Azure Portal for data management. Here's what it does:
    
1. Purpose: Facilitates uploading, downloading, and copying data in and out of Azure storage accounts using command-line commands.
2. Use Case: Useful for scenarios where manual uploads/downloads via the Azure Portal are inefficient or when automation is required.
3. How It Works:
    - Download and install the AZCopy tool.
    - Authenticate your Azure account using the tool.
    - Use commands to interact with your storage account, such as:
        - list to view entities.
        - copy to upload or download data.
4. Example Commands:
The AZCopy tool is an efficient way to handle large-scale data transfers programmatically


### Question 19: What is the difference between Azure Blob Storage and Azure Data Lake Storage (ADLS)?
**Answer:**:Azure Blob Storage and Azure Data Lake Storage (ADLS) are both storage solutions in Azure, but they serve different purposes and have distinct features. Here's a comparison:
        
1. Hierarchical Namespace:
    - ADLS: Supports hierarchical namespaces, allowing the creation of a directory-like structure with folders and subfolders, similar to the file system on a laptop.
    - Blob Storage: Uses a flat namespace. While folders can be mimicked through naming conventions, no actual directory structure is created under the hood.
2. Purpose and Performance:
    - ADLS: Optimized for big data workloads. Designed specifically for analytics frameworks like Hadoop and Apache Spark, offering better performance for such use cases.
    - Blob Storage: General-purpose storage used for storing unstructured data, such as images, videos, and documents. Suitable for less complex storage needs.
3. When to Use:
    - Use ADLS for scenarios involving big data analytics or applications requiring hierarchical namespace management.
    - Use Blob Storage for simpler use cases involving unstructured data without complex processing needs.
4. Configuration:
    - ADLS can be enabled by selecting the "Enable hierarchical namespace" option when creating a storage account in Azure. By default, this option is unchecked, creating a standard Blob Storage account. These differences make ADLS the preferred choice for big data applications. 
    - Blob Storage is suited for more straightforward storage requirements

**Answer:**: Azure Storage accounts have two access keys (Key 1 and Key 2) to facilitate key rotation while maintaining uninterrupted access to the storage account. Here's why they are needed:
    
1. Compliance Requirements:
    * Many organizations have compliance policies that mandate periodic key rotation (e.g., every 90 days).
2. Security Concerns:
    * If an access key is suspected of being compromised, it can be regenerated to ensure security.
3. Smooth Key Rotation Process:
    * While rotating keys, you need one key to remain active to prevent disruptions to connected applications or services.
    * Example process:
        + Update all applications to use Key 2 instead of Key 1.
        + Once all applications are confirmed to use Key 2, regenerate Key 1.
        + Update applications to use the regenerated Key 1.
        + Finally, regenerate Key 2 if required.
This approach ensures that the storage account is always accessible during the key rotation process, thereby preventing downtime or service interruptions.

### Question 21: Assume you are working for a website where users will upload images and videos. Which storage solution would you choose in Azure and why?
**Answer:** For this scenario, Azure Blob Storage is the most appropriate solution. Here's why:
1. Designed for Unstructured Data:
    - Images and videos are examples of unstructured data, which are not well-suited for traditional relational databases. Blob storage is optimized for such data types.
2. High Scalability:
    - Blob storage is highly scalable and can handle large amounts of data, making it ideal for applications that store large or numerous files such as user-uploaded videos and images.
3. Fast Access:
    - Websites require quick rendering of images and videos for a seamless user experience. Azure Blob Storage provides low-latency access, ensuring fast data retrieval for real-time access.
4. Durability and Redundancy:
    - Blob storage offers high durability through replication strategies like LRS (Locally Redundant Storage), GRS (Geo-Redundant Storage), etc., ensuring your data remains safe even during hardware failures.
5. Cost-Effective Storage for Large Data:
    - Azure Blob Storage is cost-efficient for storing and managing large data volumes compared to traditional databases.
6. Security:
    - All data in Azure Blob Storage is encrypted by default, ensuring secure storage of sensitive user content.
7. Integration with CDN:
    - Azure Blob Storage can be integrated with Azure Content Delivery Network (CDN) for enhanced content delivery, ensuring faster global access to user-uploaded images and videos.

By considering scalability, performance, durability, and cost-effectiveness, Azure Blob Storage is the best choice for this web application scenario.

### Question  22: Assume you are working as a data engineer for AzureABC.com. Application data is stored in Blob Storage, and it generates reports that need to be accessible to third-party applications for only the next seven days. How would you solve this problem?

**Answer:** The best solution for this problem is to use a Shared Access Signature (SAS) token. Let’s break it down:

#### Understanding the Requirements:     

1. Data Stored in Blob Storage:  The data (reports) resides in Azure Blob Storage.
2. Third-Party Access: Access is needed for an external, third-party application, which means we cannot use direct credentials like account keys.
3. Time-Bound Access:  Access must be limited to seven days, ensuring the reports become inaccessible automatically after this period.

#### Evaluating the Options:
1. Account Access Keys:
    - Pros: Allows complete access to the storage account.
    - Cons:
        - It exposes the entire storage account to the third-party application.
        - It does not provide time-bound access, as the keys are always valid unless regenerated.
    - Conclusion: Not a suitable choice.
2. Azure Active Directory (AAD):
    - Pros: Enables secure access by creating service principals for third-party applications.
    - Cons:
        - Requires manual intervention to revoke access after seven days.
        - Risk of access lingering if manual revocation is forgotten.
    - Conclusion: A good option for general access control but not ideal for time-bound requirements.
3. Shared Access Signature (SAS):
    - Pros:
        - Allows access to specific resources (e.g., a single blob or container).
        - Enables time-bound access by specifying an expiry time.
        - Automatically invalidates access after the specified duration.
    - Cons: If mishandled, the token could be shared further.
    - Conclusion: The best solution for this scenario.

Steps to Implement SAS Token Solution:
1. Generate a SAS Token:
   - Use Azure Portal, Azure CLI, or Azure SDK to create a SAS token for the specific blob or container containing the reports.
   - Define access permissions (e.g., Read) and specify an expiration date (seven days from the current date).
2. Distribute the SAS Token:
    - Provide the generated SAS URL to the third-party application.
3. Automatic Expiry:
    - Once the seven-day period is over, the SAS token becomes invalid, and the reports are no longer accessible.

##### Why SAS Token is the Best Fit?
- Granular Control: Limits access to only the required blob or container.
- Time-Bound: Automatically enforces access expiry without manual intervention.
- Security: Prevents overexposure of the storage account credentials.

By implementing a SAS token, the problem is solved in an efficient, secure, and automated manner, aligning perfectly with the requirements of the scenario.

 
### Question 23: You have mission-critical data stored in an Azure Storage account. How can you ensure that it is stored securely?
**Answer:** Analysis and Recommended Measures for Data Security:
1. Default Encryption:
    - Azure Storage Encryption for Data at Rest:
        - Azure Storage automatically encrypts data before storing it and decrypts it when accessed.
        - By default, Microsoft-managed keys are used for encryption, ensuring a baseline level of security.
2. Customer-Managed Keys (CMKs):
    - To enhance security further, you can use Customer-Managed Keys in Azure Key Vault.
    - This allows you to bring your own encryption keys (BYOK) for better control over encryption and compliance with organizational security policies.
3. Role-Based Access Control (RBAC):
    - Implement strict RBAC to control who has access to the storage account.
    - Grant access only to necessary users and services following the principle of least privilege.
    - Use Azure Active Directory (AAD) for authentication and authorization.
4. Network Security:
    - Restrict access to your storage account by enabling private endpoints or virtual network service endpoints.
    - This ensures that only traffic from specific networks can access the storage account.
5. Shared Access Signature (SAS) Tokens:
    - For providing temporary or limited access to specific resources, use SAS tokens.
    - Ensure SAS tokens have minimal permissions, a defined expiration time, and restricted IP addresses.
6. Azure Defender for Storage:
    - Enable Azure Defender for Storage to detect and respond to unusual and potentially harmful activities, such as data exfiltration or access by unauthorized IP addresses.
7. Immutable Storage:
    - If the data must be tamper-proof (e.g., for compliance), enable immutable storage with a Write Once, Read Many (WORM) policy.
    - This ensures that once data is written, it cannot be modified or deleted until the retention period expires.
8. Monitoring and Auditing:
    - Use Azure Monitor and Azure Storage Logging to track access and operations on the storage account.
    - Regularly review logs and alerts to detect any unauthorized access attempts.

##### Recommended Steps for Implementation:
1. Encryption:
    - Use Customer-Managed Keys (CMKs) for encryption in Azure Key Vault.
2. Access Control:
    - Set up RBAC to limit access.
    - Authenticate users and applications with Azure AD.
3. Network Security:
    - Restrict public access and use private endpoints.
4. Auditing and Threat Detection:
    - Enable Azure Defender for Storage and regularly review access logs.
5. Data Integrity:
    - Implement immutable storage if tamper-proof storage is required.


### Question 24: You need to provide read-only access to junior team members and read-write access to senior team members for an Azure Storage account. Can this be done, and how?

**Answer:** Yes, you can achieve this using Role-Based Access Control (RBAC) in Azure. RBAC allows you to assign specific roles with defined permissions to users, groups, or applications.

##### Steps to Implement RBAC in Azure Storage Account:
1. Access the Storage Account:
   - Log in to the Azure Portal.
   - Navigate to the specific Storage Account where permissions need to be assigned.
2. Open Access Control (IAM):
   - In the storage account's left-hand menu, click on "Access Control (IAM)".
3. Add Role Assignments:
   - Click on "Add" → "Add Role Assignment".
4. Assign Roles:
   - Junior Team Members (Read-Only Access):
        - hoose the role Reader (grants read-only access).
        - ssign this role to the specific junior team members by selecting their names or group from the Azure Active Directory (AAD) list.
   - Senior Team Members (Read-Write Access):
        - Choose the role Contributor (grants both read and write permissions).
        - Assign this role to the senior team members in the same manner.
5. Review and Confirm:
   - After selecting the roles and users, click Review + Assign to finalize the role assignments.
6. Role Assignments Effective:
   - Once assigned, these roles take effect almost immediately. Users will have the specified level of access to the storage account based on their roles.

##### Important Notes:
1. Authentication and Authorization:    
    - All users will be authenticated and authorized via Azure Active Directory (AAD).
2. Granular Permissions:
    - If you need more granular permissions (e.g., access to specific containers or blobs), you can configure Azure Storage Container-Level Access or use Shared Access Signatures (SAS) for fine-grained control.
3. Revoking Access:
    - To revoke or modify access, return to Access Control (IAM), locate the assigned role, and remove or update it as needed.



### Question 25: How do you handle a situation when multiple clients are accessing a single blob concurrently in Azure Storage?
**Answer:** Azure Blob Storage is designed to handle high concurrency efficiently. However, the handling strategy depends on your specific requirements and workload. Below are the considerations and solutions for managing concurrent access:
1. Default Azure Blob Storage Capability:
        • A single blob can support up to 500 requests per second.
        • This default capacity is sufficient for most applications. Azure Blob Storage is built to automatically scale within this limit without requiring additional configuration.
2. Handling Very High Concurrency Needs:

If your use case exceeds the default capability, consider the following options:
- Use Azure Content Delivery Network (CDN):
    - For static or read-only data (e.g., media files, large documents), use Azure CDN to cache content at edge locations.
    - Benefits:
        - Improved performance: Reduces latency for global clients.
        - Scalability: Offloads traffic from the blob storage account by distributing it across CDN nodes.
        - Cost-effective for heavy concurrent read workloads.
- Partitioning Data Across Blobs:
    - If possible, split large blobs into smaller parts or shards and store them in separate blobs.
    - Clients can then access these shards concurrently, reducing contention on a single blob.
- Implement Read Replication:
    - If your application supports it, replicate the blob data into different blob storage containers or accounts.
    - This creates multiple access points for the same data, reducing load on any single blob.
3. Consideration for Write Concurrency:
    - For write operations, ensure proper coordination to avoid conflicts:
        - Use blob leases to ensure only one client writes to the blob at a time.
        - Implement ETag-based conditional updates to handle version conflicts.
4. Monitoring and Scaling:
    - Use Azure Monitor and Metrics to track blob storage usage.
    - If necessary, scale out by using additional storage accounts or containers to distribute the load.

By implementing these strategies, you can effectively manage concurrent access to a single blob in Azure Storage.

### Question 26: Your application is deployed in the US East region and uses a storage account. Does it make sense to place the storage account in the same region? Why or why not?
**Answer:** The decision to place a storage account in the same region as the application involves evaluating multiple factors: performance, cost, and business requirements. Here's how to analyze the scenario:

1. Performance Considerations:
    - Low Latency:    Keeping the storage account in the same region as the application ensures low network latency, as data does not need to travel across geographical regions.
    - Faster data access improves application responsiveness.
        - Ideal for performance-critical workloads like real-time applications or data-intensive services (e.g., Azure Databricks, Azure Data Factory, etc.).
    - Bandwidth Optimization:     Data transfer between resources within the same region is faster and often cheaper or free, reducing operational delays.
2. Cost Considerations:
    - Data Transfer Costs:
        - Transferring data within the same region is typically free.
        - If the storage account is placed in another region, egress costs are incurred for transferring data across regions.
    - Regional Pricing Differences:
        - Some regions might offer lower storage costs.
        - For non-latency-sensitive workloads (e.g., archival or backup), storing data in a cheaper region might be preferable for cost savings.
3. Business Continuity and Disaster Recovery:
    - If business requirements prioritize redundancy and availability, placing the storage account in a different region might make sense:
        - For Disaster Recovery (DR) scenarios, storing a copy of the data in a geographically distant region ensures that data remains accessible during a regional outage.
        - Consider Geo-Redundant Storage (GRS) or Read-Access Geo-Redundant Storage (RA-GRS) for automatic replication.
4. Security and Compliance:
    - Data residency and regulatory compliance might dictate that data must remain in a specific region.
    - For instance, if regulatory requirements mandate that data remains in US East, then the storage account must also be in US East, even if latency or cost isn't a concern.

By balancing these factors—performance, cost, and business requirements—you can determine the optimal location for the storage account.

### Question 27: Is it possible to move data between Azure storage access tiers (Hot, Cool, and Archive) automatically? Why would someone want this functionality, and how can it be implemented?
**Answer:**
1. Is it possible to move data between access tier s automatically?
    - Yes, Azure provides the functionality to automatically move data between access tiers (Hot, Cool, and Archive) based on certain rules.
    - This can be achieved using Lifecycle Management Policies in the Azure portal.
2. Why would someone want this functionality?
    - Cost Optimization:
        - Access tiers are priced differently based on their usage.
            - Hot Tier: Optimized for frequently accessed data but has higher storage costs.
            - Cool Tier: Suitable for infrequently accessed data, offering lower storage costs but higher access costs.
            - Archive Tier: Ideal for rarely accessed data with the lowest storage cost but significant latency for data retrieval.
        - Automatically moving data to lower-cost tiers when it becomes infrequently accessed helps reduce storage costs.
    - Predictable Data Lifecycle:
        - Data usage often follows a predictable pattern:
            - Newly generated data is accessed frequently.
            - Over time, the frequency of access decreases.
    - Operational Efficiency:
        - Automation eliminates manual intervention, ensuring that data is moved between tiers based on usage patterns, reducing administrative overhead.
3. How can it be implemented?
    The process involves creating Lifecycle Management Rules in Azure Storage. Here's how:

Steps to Implement Lifecycle Management:
1. Navigate to Azure Portal:
    - Go to your Storage Account.
2. Access Lifecycle Management:
    - Under the Data Management section, click on Lifecycle Management.
3. Create a Rule:
    - Click on Add a Rule to define the conditions for data movement.
4. Define Rule Details:
    - Provide a Name for the rule.
    - Choose the Scope:
        § Apply the rule to all blobs or specific blob types (e.g., Block blobs).
5. Set Conditions:
    - Specify conditions based on Last Modified Date:
        § Example: "If the blob has not been modified for 5 days, move it to the Cool tier."
    - Add multiple conditions if needed (e.g., move to Archive tier after 30 days).
6. Enable the Rule:
    - Review the rule and save it.
        - Azure will automatically move blobs between tiers based on the defined conditions.

Example Use Case:
+ A business stores daily transaction logs in the Hot tier for frequent access.
+ After 7 days, logs are moved to the Cool tier for infrequent access.
+ After 30 days, logs are moved to the Archive tier for long-term storage at minimal cost.

### Question 28: Is it possible to check how much the storage account is costing us in Azure? If yes, how can it be done?

**Answer:**
1. Is it possible to check the cost of a storage account?
    - Yes, Azure provides tools to track and analyze the costs associated with storage accounts and other services.
2. How can you check the cost of a storage account?
To check the costs associated with a storage account, you can use the Cost Management + Billing feature in the Azure portal.
Steps to Check Costs:
- Log in to Azure Portal:
    - Navigate to Azure Portal.
- Search for Cost Management:
    -  In the search bar, type and select Cost Management + Billing.
- Select Your Subscription:
    -  Choose the appropriate Subscription under which the storage account exists.
- Access Cost Analysis:
    -  Click on Cost Analysis to view the overall costs associated with the subscription.
- Filter for Storage Services:
    -  Use the Filter option to narrow down the costs to Storage Accounts:
        - Select Service Name as the filter criteria.
        - Choose Storage or the specific name of your storage account.
- View and Analyze Costs:
    - The dashboard will display:
        - Total costs incurred so far.
        - Forecasted costs for the remaining period.
        - A breakdown of costs for the selected time range.
3. Access Considerations:
    - Ensure you have the appropriate permissions to view Cost Management in your Azure subscription.
    - If you're a junior resource working for a client, you may need admin-level access to view this data.
    - If testing on a personal account, you will have full access.

Example:
- Assume your storage account is part of the East US region.
- Under Cost Analysis, filter by Service Name: Storage.
- You observe that your storage account incurred 1120 INR over the past month with a forecasted cost for the remaining billing cycle.


### Question 29: Assume you want to generate an overview of your containers, blob snapshots, and blob versions within a storage account. How can you create such a report?

**Answer:**
1. Can you generate such a report?
    • Yes, Azure provides a feature called Blob Inventory Report that enables you to generate detailed metadata reports for blobs, containers, snapshots, and blob versions in a storage account.
2. How to Create a Blob Inventory Report:  The Blob Inventory Report collects metadata information about your storage account and provides insights into:
    - Blob names
    - Sizes
    - Blob types
    - Snapshots
    - Versions
    - Other selected fields.

Steps to Configure Blob Inventory:
1. Log in to Azure Portal:
    ○ Navigate to Azure Portal.
2. Select the Storage Account:
    ○ Choose the storage account where you want to generate the report.
3. Access Blob Inventory Feature:
    ○ On the left-hand menu, find and click on Blob Inventory.
4. Add a Rule:
    ○ Click on Add Rule to create a new inventory rule.
5. Configure the Rule:
    - Scope:
        - Choose whether to apply the rule to a specific container or to all containers.
    - Blob Types:
        - Decide whether to include:
            - Snapshots, and/or
            - Blob Versions.
            - Base blobs (current versions of blobs),
    - Deleted Blobs:
        - Select whether to include soft-deleted blobs in the report.
    - Fields:
        - Choose the metadata fields you want in the report, such as:
            - Blob name,
            - Blob type,
            - Size,
            - Last modified date, etc.
    - Frequency:
        - Specify the frequency of report generation: Daily or Weekly.
6. Select the Destination Container:
    - Specify a container where the inventory reports will be stored. Ensure this container has write access enabled.
7. Finalize the Rule:
    - Review the settings and click Create to save the rule.
3. Benefits of Blob Inventory Report:
    - Provides detailed metadata for auditing and compliance.
    - Helps monitor blob utilization and optimize storage.
    - Can be automated with daily or weekly reports.
    - Simplifies blob management across containers.
 Example: If you are managing a folder receiving critical files daily, the Blob Inventory Report can track:
- How many files were uploaded.
- Their sizes, last modified dates, and other metadata.
- Whether snapshots or versions exist.

This enables easy monitoring and metadata analysis without manually querying the blobs.



### Question 30: You have a checklist or cheat sheet you want to share with the world, like through a blog or website. How can you do this using an Azure Storage Account?

**Answer:**
1. Can this be achieved with Azure Storage Account?
    - Yes, you can use the Static Website feature in Azure Storage to host and share static content, such as an HTML page, cheat sheet, or checklist, directly over the internet.
2. Overview of the Solution:
    - The Static Website feature in Azure Storage allows you to host static web pages (e.g., HTML, CSS, JS files) within a blob container.
    - These pages can then be accessed publicly via a unique URL provided by Azure.

Steps to Enable and Share Static Content:
1. Log in to Azure Portal:
    - Navigate to Azure Portal.
2. Select the Storage Account:
    -  Choose the storage account where you want to host your static content.
3. Enable Static Website:
    - In the left-hand menu, find and click Static website.
    - Enable the feature by toggling the option to On.
    - Specify the index document name (e.g., index.html). This file will be the main page served to users.
4. Upload Your Content:
    - After enabling static website, Azure creates a special blob container named $web.
    - Upload your static files (e.g., index.html, CSS, images) into this $web container.
5. Access the Content:
    - Once the static website feature is enabled, Azure provides a public URL for your static site, typically in the format: https://<storage-account-name>.z13.web.core.windows.net
    - Share this URL with anyone who needs access to the content.
3. Key Considerations:
    - Static Content Only: The feature supports static content (HTML, CSS, JavaScript, etc.). It does not support dynamic content that requires server-side processing.
    - Public Access: Content in the $web container is publicly accessible, so ensure you are not sharing sensitive information.
    - Scalability and Performance: Azure Storage can handle high levels of traffic, making it suitable for sharing widely.
4. Use Case Examples:
    - Hosting a personal blog with static pages.
    - Sharing a downloadable cheat sheet or checklist.
    - Providing read-only documentation or manuals.

# Level-4 Azure Storage Question Qnswer

### Question 31:Create a storage account named "your name_underscore Dubey" in the Asia Pacific region with a redundancy level of ZRS (Zone-Redundant Storage). This is an area-less account to be used by the operations team, and it needs to be tagged accordingly.

**Answer:** 
1. Go to the Azure Portal (portal.azure.com). 
2. Click on "Create" to initiate a new storage account creation. 
3. Choose your subscription and resource group (you can use an existing one or create a new one). 
4. Name the storage account as "your name_underscore Dubey" (e.g., "John_Dubey_25121999"). 
5. Select the Asia Pacific region (Central India, for example). 
6. Set the redundancy level to ZRS (Zone-Redundant Storage). 
7. Enable the "Hierarchical namespace" option to make the account area-less. 
8. Tag the storage account with the name "Operations" under the "Team" tag. 
9. Review all settings and click "Create" to deploy the storage account.
    
This will create a storage account with the specified configurations, including region, redundancy, hierarchical namespace, and appropriate tags.

### Question 32:Create two containers named "raw" and "curated" in an existing storage account. The "raw" container should be private, and the "curated" container should be public.

**Answer:** Navigate to the Azure Portal: Go to Azure Portal and select the storage account you want to work with. 2. Access the Containers Section:
- In the storage account, select "Containers" from the left-hand menu or under "Data Storage" in the main window. 3. Create the "raw" Container (Private):
- Click on "+ Container" to add a new container.
- Set the name to "raw".
- Set the public access level to Private (no anonymous access).
- Click Create to finalize the creation of the private container. 4. Create the "curated" Container (Public):
- Click on "+ Container" again to add another container.
- Set the name to "curated".
- Set the public access level to Container (anonymous read access for container and blobs).
- Click Create to finalize the creation of the public container. 5. Verify the Containers:
- Ensure the "raw" container has Private access level.
- Ensure the "curated" container has Container (public) access level.

This completes the task of creating a private and a public container in the specified storage account.

### Question 33: Create a file share account named "your name_underscore further name" within an existing or new storage account.

**Answer:** Access the Azure Portal:

Go to Azure Portal. 2. Select a Storage Account:

- Use an existing storage account (e.g., "Deepak25") or create a new one.
- To create a new storage account, click on "+ Create a resource" > "Storage Account" and configure the settings as needed. 3. Navigate to File Shares:
- In the selected storage account, go to the left-hand menu and click on "File Shares."
- Alternatively, click on "File Shares" from the central window under "Data Storage." 4. Create a File Share:
- Click on the "+ File Share" button to create a new file share.
- Name the file share as "your name_underscore further name" (e.g., "Deepak_Mahesh").
- Optional: Choose a performance tier (Transaction Optimized, Hot, or Cool) based on your requirements. If unsure, keep the default option, TransactioOptimized.
- Click Create to finalize the file share. 5. Mapping the File Share (Optional):
- To map the file share to your local system:
    - Click on the created file share and select Connect from the top menu.
    - Use the provided script or instructions for your operating system to map the file share as a network drive.
    - For Windows, go to This PC > Right-click > Map Network Drive and follow the prompts with the details provided in the Azure portal.
This completes the task of creating the file share account as per the requirements.

### Question 34: Create and deploy a static webpage using the given code inside an Azure storage account as a static website.

**Answer:** Prepare the Static Webpage File:
- Copy the provided HTML code and save it as a file (e.g., abc.html). 2. Access the Azure Portal:
- Go to Azure Portal and select the existing storage account you want to use for the static website. 3. Enable Static Website Hosting:
- In the storage account, type "Static Website" in the search bar or find it in the left-hand menu.
- Click on Static Website and enable the feature by clicking Enable.
- Specify an index document name (e.g., abc.html). Optionally, specify an error document.
- Save the changes. 4. Verify Container Creation:
- Enabling static website hosting automatically creates a container named $web. 5. Upload the HTML File:
- Navigate to the $web container.
- Click on Upload and select the saved HTML file (abc.html).
- Confirm the upload. 6. Access the Static Website:
- Once the file is uploaded, copy the Primary Endpoint URL provided under the Static Website section (e.g., https://<storage-account-name>.z13.web.core.windows.net).
- Append the file name (abc.html) to the URL (e.g., https://<storage-account-name>.z13.web.core.windows.net/abc.html).
- Open the URL in a browser to view the static webpage.
    
Result: The static webpage will be accessible via the generated URL, and you can share the link with anyone for public access.

### Question 35: Assign read-only access to your junior and read-write access to your manager for the storage account created in the previous exercise.

**Answer:**  Access the Azure Portal:
- Log in to Azure Portal and navigate to the storage account. 2. Go to Access Control (IAM):
- In the selected storage account, click on Access Control (IAM) from the left-hand menu. 3. Assign Read Access for Junior:
- Click on + Add and choose Add role assignment.
- In the Role dropdown, select Reader (read-only access).
- Click Next.
- Under Select members, search for and select the junior's user account.
- Click Review + Assign to finalize the role assignment. 4. Assign Contributor Access for Manager:
- Click on + Add and choose Add role assignment again.
- In the Role dropdown, select Contributor (read-write access).
- Click Next.
- Under Select members, search for and select the manager's user account.
- Click Review + Assign to complete the role assignment. 5. Verify Role Assignments:
- Return to the Access Control (IAM) panel.
- Go to the Role assignments tab to confirm the junior is listed with the Reader role and the manager is listed with the Contributor role.
    
Result:
- The junior has read-only access to the storage account and can view but not modify data.
- The manager has contributor access, allowing both read and write operations.

### Question 36: Assume that the data being stored in your Azure Storage Account is mission-critical. How can you change the retention period from the default 7 days to 90 days?

**Answer:** The retention period defines how long deleted data (blobs) remains available for recovery when soft delete is enabled. Here’s how you can change the retention period: 
If the storage account is already created:

- Go to the Azure portal and navigate to the storage account.
- Select the Data Protection section.
- Enable the option "Recovery enabled soft delete for block blobs."
- Set the retention period to 90 days instead of the default 7 days.
- Save the changes.
- (Optional) Similarly, enable retention for containers to ensure even deleted containers are retained for 90 days. 2. If you are creating a new storage account:
- Go to the Azure portal and start the process to create a new storage account.
- In the Data Protection tab, enable the soft delete option.
- Specify the retention period (e.g., 90 days).
- Complete the storage account setup. 3. Optional adjustments:
- If you do not want any retention period, you can disable soft delete entirely.

This ensures that deleted data can be recovered within 90 days, safeguarding against accidental deletions.

### Question 37: How can you configure the Azure Storage Explorer to easily access your storage account?

**Answer:** Azure Storage Explorer is a free tool from Microsoft that simplifies navigating and managing Azure Storage Accounts. Here's how to configure it: 

Download and Install Azure Storage Explorer:

- Search for Azure Storage Explorer download on Google.
- Download and install the tool using the standard installation process (Next, Next, Finish). 2. Launch and Configure Azure Storage Explorer:
- Open the installed tool.
- Click "Open Connect" to set up a connection. 3. Connection Options:
- Choose one of the following methods to connect to your storage account:
    - Azure Active Directory (AAD):
        - Select Subscription, click Next, and log in via the browser when prompted.
        - Authenticate and allow it to fetch all storage accounts under your subscription.
    - Storage Account Access Keys:
        - Use the access key from the Azure portal.
    - Shared Access Signature (SAS) Token:
        - Use a SAS token generated for the storage account. 4. View and Manage Storage Accounts:
- Once authenticated, refresh the list to view all your subscriptions and storage accounts.
- You can now navigate, upload, download, rename, or perform other operations on your storage account.
    
This setup makes accessing and managing storage accounts faster and more efficient compared to using the Azure Portal.

### Question 38: Is it possible to move a storage account from one resource group to another in Azure? If yes, how can it be done?

**Answer:** Yes, it is possible to move a storage account from one resource group to another in Azure. Here’s how you can do it: 

Understand Resource Groups:

- Resource groups are logical containers in Azure that group resources for easy management. 2. Steps to Move a Storage Account:
- Log in to portal.azure.com.
- Navigate to the Storage Account you want to move.
- In the storage account overview, locate the Resource Group section and click on Move. 3. Specify the Target Resource Group:
- Choose the current subscription (or a different subscription if applicable).
- Specify the target resource group:
- You can select an existing resource group or create a new one (e.g., "Resource_Group_2").
- Click Next to proceed. 4. Validation:
- Azure performs a validation check to ensure the resource can be moved.
- Once the validation is successful, click Next. 5. Review and Confirm:
- Review the details of the move (source resource group and target resource group).
- Confirm by checking the acknowledgment box and click Move. 6. Wait for Completion:
- The move process may take some time. Once complete, the storage account will be in the new resource group.

### Question 39: How can you generate a SAS token valid for seven days with read access to an Azure Blob object?

**Answer:** A SAS (Shared Access Signature) token allows secure and customized access to Azure resources. Here’s how to create a SAS token with read access for seven days:
Navigate to the Azure Portal:

- Log in to portal.azure.com.
- Go to the desired Storage Account. 2. Access the Shared Access Signature (SAS) Panel:
- In the left-hand menu, locate and click on Shared Access Signature (or search for it in the search bar). 3. Configure SAS Token Settings:
- Services: Select Blob service for the SAS token.
- Resource Types: Choose Object (uncheck Container and Service if not needed).
- Permissions: Select Read permission as required by the question.
- Start and Expiry Time: Set the start time as the current date and the expiry time for seven days from the start date. 4. Generate SAS Token:
- Click Generate SAS and connection string.
- Copy the generated SAS token from the provided details. 5. Validate the Token:
- Ensure the token’s validity period is from today’s date for the next seven days, with permissions scoped to read access only.

This SAS token can now be used to grant read access to the specified Azure Blob object for seven days.

### Question 40: Can you change the redundancy level of an Azure Storage Account after its creation? If yes, how can it be done?

**Answer:** Yes, it is possible to change the redundancy level of an Azure Storage Account after its creation. Here’s how to do it:
Navigate to the Azure Portal:

- Log in to portal.azure.com.
- Open the Storage Account whose redundancy level you want to change. 2. Access the Configuration Settings:
- On the left-hand side menu, under the Settings section, click on Configuration. 3. Change the Redundancy Level:
- In the Replication section, select the desired redundancy level (e.g., from ZRS to GRS).
- Click Save to apply the changes. 4. Other Configurations:
- The Configuration tab also allows you to modify other settings like default access tier, protocol versions, and account key settings.

This change ensures that the new redundancy configuration is applied to your storage account. Note that changing redundancy might incur data transfer and storage costs, depending on the selected redundancy type.

