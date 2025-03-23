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
2. Encryption Keys Management:
    - By default, Microsoft-managed keys are used for encryption.
    - Customers can opt for their own keys (Customer-Managed Keys), stored securely in Azure Key Vault.
3. Key Vault Integration:
    - Azure Key Vault is a secure service for storing and managing keys, secrets, and passwords.
    - It ensures strict access control and security for encryption keys.
4. Mandatory Encryption:
    - Encryption is enabled by default and cannot be disabled, ensuring robust data security.

### Question 16: How can you ensure data protection in Azure Blob Storage?
**Answer:**: To ensure data protection in Azure Blob Storage, you can use the following strategies:
    
1. Azure Resource Manager Logs:
    - Enable logging on your storage account to monitor and track changes, protecting against unauthorized updates or deletions.
2. Soft Delete:
    - Enable the soft delete feature to recover accidentally deleted blobs.
    - By default, deleted data is retained for 7 days, but this period can be extended up to 90 days for recovery.
3. Blob Versioning:
    - Enable versioning to maintain previous versions of blobs.
    - This allows you to revert to an earlier version if needed, similar to version control systems like Git.
4. Snapshots:
    - Take periodic snapshots of your blobs to create point-in-time backups.
    - These snapshots can be used to restore data if accidental changes or deletions occur.
These practices ensure that data is accessible only to the right users and is protected against accidental loss or modification.

### Question 17: How does the soft delete feature work for containers in Azure Blob Storage?
**Answer:**: The soft delete feature in Azure Blob Storage ensures that deleted containers or files are not permanently removed immediately. Instead, they are retained for a specified period, allowing recovery if needed. Here's how it works:
    
1. Soft Delete Functionality:
    - When a file or container is deleted, it is marked as "deleted" but is not permanently removed.
    - This behavior is similar to a recycle bin on a computer.
2. Retention Period:
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
    - azcopy copy <source> <destination> to transfer files between local systems and Azure storage.
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

### Question 20: Why does an Azure Storage account have two access keys, Key 1 and Key 2?
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

