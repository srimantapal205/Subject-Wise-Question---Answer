## 1. In Azure Data Factory (ADF) have 200 pipeline and this all are dependency pipeline also need to run all sequentially. How to resolve this problem?

**Answer :** Running 200 dependent pipelines sequentially in Azure Data Factory (ADF) can be done using a few different strategies. Here's a breakdown of the most efficient and manageable approaches:

### Approach 1: Master Pipeline (Recommended)
**Steps:**
* Create a Master Pipeline.

* Use the "Execute Pipeline" activity.

* Chain them sequentially:

* Link Execute Pipeline 1 to Execute Pipeline 2, then 3, and so on.

* Set the dependency condition to "Success" (default).

**Notes:**
* We can group sets of pipelines into smaller master pipelines (e.g., 20 at a time), then call those from a main orchestrator, if performance or UI gets sluggish.

*Use pipeline parameters if pipelines are similar and can be parameterized.

### Approach 2: Metadata-Driven Execution

Dynamic and scalable way to execute large number of pipelines without manually creating 200 Execute Pipeline activities.

**How it works:**
* Create a Lookup activity that reads a list of pipeline names (from a table or JSON in Blob).

* Use a ForEach loop to iterate over the list.

* Inside the loop, use Execute Pipeline activity to run the pipeline using the name from the list.

**Pros:**
* Easy to maintain.

* No need to hard-code all 200 pipelines in the ADF UI.

* Add/remove pipelines easily by updating metadata source.

**Caveat:**
* ForEach by default runs in parallel. You need to set "Batch Count" = 1 and uncheck "isSequential = false" to enforce sequential execution.


###  Approach 3: Use Data Factory Triggers + Dependency Chain
If you want to automatically kick off one pipeline after another based on success, you can chain them using triggers and pipeline dependencies in the ADF UI (Manage > Trigger > New/Edit).

But managing 200 trigger dependencies in this UI may be tedious and not scalable.

