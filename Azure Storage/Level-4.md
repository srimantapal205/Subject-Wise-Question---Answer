# Level-4 Azure Storage Question Qnswer

### Question 31:Create a storage account named "your name_underscore Dubey" in the Asia Pacific region with a redundancy level of ZRS (Zone-Redundant Storage). This is an area-less account to be used by the operations team, and it needs to be tagged accordingly.

    Answer: Go to the Azure Portal (portal.azure.com). 2. Click on "Create" to initiate a new storage account creation. 3. Choose your subscription and resource group (you can use an existing one or create a new one). 4. Name the storage account as "your name_underscore Dubey" (e.g., "John_Dubey_25121999"). 5. Select the Asia Pacific region (Central India, for example). 6. Set the redundancy level to ZRS (Zone-Redundant Storage). 7. Enable the "Hierarchical namespace" option to make the account area-less. 8. Tag the storage account with the name "Operations" under the "Team" tag. 9. Review all settings and click "Create" to deploy the storage account.
    This will create a storage account with the specified configurations, including region, redundancy, hierarchical namespace, and appropriate tags.

### Question 32:Create two containers named "raw" and "curated" in an existing storage account. The "raw" container should be private, and the "curated" container should be public.

    Answer: 1. Navigate to the Azure Portal:
    Go to Azure Portal and select the storage account you want to work with. 2. Access the Containers Section:
        ○ In the storage account, select "Containers" from the left-hand menu or under "Data Storage" in the main window. 3. Create the "raw" Container (Private):
        ○ Click on "+ Container" to add a new container.
        ○ Set the name to "raw".
        ○ Set the public access level to Private (no anonymous access).
        ○ Click Create to finalize the creation of the private container. 4. Create the "curated" Container (Public):
        ○ Click on "+ Container" again to add another container.
        ○ Set the name to "curated".
        ○ Set the public access level to Container (anonymous read access for container and blobs).
        ○ Click Create to finalize the creation of the public container. 5. Verify the Containers:
        ○ Ensure the "raw" container has Private access level.
        ○ Ensure the "curated" container has Container (public) access level.
    This completes the task of creating a private and a public container in the specified storage account.

### Question 33: Create a file share account named "your name_underscore further name" within an existing or new storage account.

    Answer: Access the Azure Portal:
        Go to Azure Portal. 2. Select a Storage Account:
        ○ Use an existing storage account (e.g., "Deepak25") or create a new one.
        ○ To create a new storage account, click on "+ Create a resource" > "Storage Account" and configure the settings as needed. 3. Navigate to File Shares:
        ○ In the selected storage account, go to the left-hand menu and click on "File Shares."
        ○ Alternatively, click on "File Shares" from the central window under "Data Storage." 4. Create a File Share:
        ○ Click on the "+ File Share" button to create a new file share.
        ○ Name the file share as "your name_underscore further name" (e.g., "Deepak_Mahesh").
        ○ Optional: Choose a performance tier (Transaction Optimized, Hot, or Cool) based on your requirements. If unsure, keep the default option, Transaction Optimized.
        ○ Click Create to finalize the file share. 5. Mapping the File Share (Optional):
        ○ To map the file share to your local system:
        § Click on the created file share and select Connect from the top menu.
        § Use the provided script or instructions for your operating system to map the file share as a network drive.
        § For Windows, go to This PC > Right-click > Map Network Drive and follow the prompts with the details provided in the Azure portal.
    This completes the task of creating the file share account as per the requirements.

### Question 34: Create and deploy a static webpage using the given code inside an Azure storage account as a static website.

    Answer: Prepare the Static Webpage File:
        ○ Copy the provided HTML code and save it as a file (e.g., abc.html). 2. Access the Azure Portal:
        ○ Go to Azure Portal and select the existing storage account you want to use for the static website. 3. Enable Static Website Hosting:
        ○ In the storage account, type "Static Website" in the search bar or find it in the left-hand menu.
        ○ Click on Static Website and enable the feature by clicking Enable.
        ○ Specify an index document name (e.g., abc.html). Optionally, specify an error document.
        ○ Save the changes. 4. Verify Container Creation:
        ○ Enabling static website hosting automatically creates a container named $web. 5. Upload the HTML File:
        ○ Navigate to the $web container.
        ○ Click on Upload and select the saved HTML file (abc.html).
        ○ Confirm the upload. 6. Access the Static Website:
        ○ Once the file is uploaded, copy the Primary Endpoint URL provided under the Static Website section (e.g., https://<storage-account-name>.z13.web.core.windows.net).
        ○ Append the file name (abc.html) to the URL (e.g., https://<storage-account-name>.z13.web.core.windows.net/abc.html).
        ○ Open the URL in a browser to view the static webpage.
    Result: The static webpage will be accessible via the generated URL, and you can share the link with anyone for public access.

### Question 35: Assign read-only access to your junior and read-write access to your manager for the storage account created in the previous exercise.

    Answer:  Access the Azure Portal:
        ○ Log in to Azure Portal and navigate to the storage account. 2. Go to Access Control (IAM):
        ○ In the selected storage account, click on Access Control (IAM) from the left-hand menu. 3. Assign Read Access for Junior:
        ○ Click on + Add and choose Add role assignment.
        ○ In the Role dropdown, select Reader (read-only access).
        ○ Click Next.
        ○ Under Select members, search for and select the junior's user account.
        ○ Click Review + Assign to finalize the role assignment. 4. Assign Contributor Access for Manager:
        ○ Click on + Add and choose Add role assignment again.
        ○ In the Role dropdown, select Contributor (read-write access).
        ○ Click Next.
        ○ Under Select members, search for and select the manager's user account.
        ○ Click Review + Assign to complete the role assignment. 5. Verify Role Assignments:
        ○ Return to the Access Control (IAM) panel.
        ○ Go to the Role assignments tab to confirm the junior is listed with the Reader role and the manager is listed with the Contributor role.
    Result:
        • The junior has read-only access to the storage account and can view but not modify data.
        • The manager has contributor access, allowing both read and write operations.

### Question 36: Assume that the data being stored in your Azure Storage Account is mission-critical. How can you change the retention period from the default 7 days to 90 days?

    Answer: The retention period defines how long deleted data (blobs) remains available for recovery when soft delete is enabled. Here’s how you can change the retention period: 1. If the storage account is already created:
        ○ Go to the Azure portal and navigate to the storage account.
        ○ Select the Data Protection section.
        ○ Enable the option "Recovery enabled soft delete for block blobs."
        ○ Set the retention period to 90 days instead of the default 7 days.
        ○ Save the changes.
        ○ (Optional) Similarly, enable retention for containers to ensure even deleted containers are retained for 90 days. 2. If you are creating a new storage account:
        ○ Go to the Azure portal and start the process to create a new storage account.
        ○ In the Data Protection tab, enable the soft delete option.
        ○ Specify the retention period (e.g., 90 days).
        ○ Complete the storage account setup. 3. Optional adjustments:
        ○ If you do not want any retention period, you can disable soft delete entirely.
    This ensures that deleted data can be recovered within 90 days, safeguarding against accidental deletions.

### Question 37: How can you configure the Azure Storage Explorer to easily access your storage account?

    Answer: Azure Storage Explorer is a free tool from Microsoft that simplifies navigating and managing Azure Storage Accounts. Here's how to configure it: 1. Download and Install Azure Storage Explorer:
        ○ Search for Azure Storage Explorer download on Google.
        ○ Download and install the tool using the standard installation process (Next, Next, Finish). 2. Launch and Configure Azure Storage Explorer:
        ○ Open the installed tool.
        ○ Click "Open Connect" to set up a connection. 3. Connection Options:
        ○ Choose one of the following methods to connect to your storage account:
            § Azure Active Directory (AAD):
                □ Select Subscription, click Next, and log in via the browser when prompted.
                □ Authenticate and allow it to fetch all storage accounts under your subscription.
            § Storage Account Access Keys:
                □ Use the access key from the Azure portal.
            § Shared Access Signature (SAS) Token:
                □ Use a SAS token generated for the storage account. 4. View and Manage Storage Accounts:
        ○ Once authenticated, refresh the list to view all your subscriptions and storage accounts.
        ○ You can now navigate, upload, download, rename, or perform other operations on your storage account.
    This setup makes accessing and managing storage accounts faster and more efficient compared to using the Azure Portal.

### Question 38: Is it possible to move a storage account from one resource group to another in Azure? If yes, how can it be done?

    Answer: Yes, it is possible to move a storage account from one resource group to another in Azure. Here’s how you can do it: 1. Understand Resource Groups:
        ○ Resource groups are logical containers in Azure that group resources for easy management. 2. Steps to Move a Storage Account:
        ○ Log in to portal.azure.com.
        ○ Navigate to the Storage Account you want to move.
        ○ In the storage account overview, locate the Resource Group section and click on Move. 3. Specify the Target Resource Group:
        ○ Choose the current subscription (or a different subscription if applicable).
        ○ Specify the target resource group:
        § You can select an existing resource group or create a new one (e.g., "Resource_Group_2").
        ○ Click Next to proceed. 4. Validation:
        ○ Azure performs a validation check to ensure the resource can be moved.
        ○ Once the validation is successful, click Next. 5. Review and Confirm:
        ○ Review the details of the move (source resource group and target resource group).
        ○ Confirm by checking the acknowledgment box and click Move. 6. Wait for Completion:
        ○ The move process may take some time. Once complete, the storage account will be in the new resource group.

### Question 39: How can you generate a SAS token valid for seven days with read access to an Azure Blob object?

    Answer: A SAS (Shared Access Signature) token allows secure and customized access to Azure resources. Here’s how to create a SAS token with read access for seven days:
    Navigate to the Azure Portal:
        ○ Log in to portal.azure.com.
        ○ Go to the desired Storage Account. 2. Access the Shared Access Signature (SAS) Panel:
        ○ In the left-hand menu, locate and click on Shared Access Signature (or search for it in the search bar). 3. Configure SAS Token Settings:
        ○ Services: Select Blob service for the SAS token.
        ○ Resource Types: Choose Object (uncheck Container and Service if not needed).
        ○ Permissions: Select Read permission as required by the question.
        ○ Start and Expiry Time: Set the start time as the current date and the expiry time for seven days from the start date. 4. Generate SAS Token:
        ○ Click Generate SAS and connection string.
        ○ Copy the generated SAS token from the provided details. 5. Validate the Token:
        ○ Ensure the token’s validity period is from today’s date for the next seven days, with permissions scoped to read access only.
    This SAS token can now be used to grant read access to the specified Azure Blob object for seven days.

### Question 40: Can you change the redundancy level of an Azure Storage Account after its creation? If yes, how can it be done?

    Answer: Yes, it is possible to change the redundancy level of an Azure Storage Account after its creation. Here’s how to do it: 1. Navigate to the Azure Portal:
        ○ Log in to portal.azure.com.
        ○ Open the Storage Account whose redundancy level you want to change. 2. Access the Configuration Settings:
        ○ On the left-hand side menu, under the Settings section, click on Configuration. 3. Change the Redundancy Level:
        ○ In the Replication section, select the desired redundancy level (e.g., from ZRS to GRS).
        ○ Click Save to apply the changes. 4. Other Configurations:
        ○ The Configuration tab also allows you to modify other settings like default access tier, protocol versions, and account key settings.
    This change ensures that the new redundancy configuration is applied to your storage account. Note that changing redundancy might incur data transfer and storage costs, depending on the selected redundancy type.
