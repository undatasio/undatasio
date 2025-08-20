**[English](README.md), [中文](README_ZH.md).**

# UnDatasIO Python SDK Documentation

<p align="center">
  <a href="https://undatas.io">
    <img src="content/undatasio.png" width="100%" alt="UnDatasIO" />
  </a>
</p>

[![License](https://img.shields.io/npm/l/mithril.svg)](https://github.com/MithrilJS/mithril.js/blob/main/LICENSE) &nbsp;
[![Supported Python versions](https://shields.mitmproxy.org/pypi/pyversions/mitmproxy.svg)](https://pypi.python.org/pypi/mitmproxy)

💫Welcome to the UnDatasIO Python SDK
-------------------

**Official Website:** https://undatas.io/

UnDatasIO provides powerful, cloud-based file parsing capabilities. This Python SDK offers a streamlined, developer-friendly interface for interacting with the UnDatasIO API. It allows you to programmatically manage workspaces, tasks, and files, enabling you to focus on data analysis and application development.

## Key Features
------------

* **Workspace & Task Management:** Easily list and navigate through your workspaces and tasks.
* **Comprehensive File Handling:** Upload new files to specific tasks and list existing ones.
* **Asynchronous Parsing:** Trigger parsing jobs for one or multiple files with configurable parameters.
* **Flexible Result Retrieval:** Fetch structured parsing results as text or request a downloadable ZIP archive containing all artifacts.
* **Pythonic Design:** Methods return data directly (e.g., a list of dictionaries) on success and None on failure, with detailed errors logged for easy debugging.

## Installation
------------

🤖You can easily install the UnDatasIO Python SDK using `pip`:
```bash
pip install undatasio
```

## Quick Start
------------

🥇 The new workflow follows a logical hierarchy: Workspace -> Task -> File. Here's a complete example demonstrating the entire process:

```python
import time
from undatasio import UnDatasIO

# 1. Initialize the UnDatasIO client with your token and the API base URL
client = UnDatasIO(
    token='your_api_key_here'
)

# 2. List available workspaces and select the first one
workspaces = client.workspace_list()
if not workspaces:
    exit("No workspaces found.")
first_workspace_id = workspaces[0]['work_id']
print(f"Using workspace: {first_workspace_id}")

# 3. List tasks within the selected workspace and select the first one
tasks = client.task_list(work_id=first_workspace_id)
if not tasks:
    exit(f"No tasks found in workspace {first_workspace_id}.")
first_task_id = tasks[0]['task_id']
print(f"Using task: {first_task_id}")

# 4. Upload a new file to this task
# Make sure 'path/to/your/document.pdf' exists
if client.upload_file(task_id=first_task_id, file_path='path/to/your/document.pdf'):
    print("File uploaded successfully!")

# 5. List all files in the task to get a file_id
files = client.get_task_files(task_id=first_task_id)
if not files:
    exit("No files found in the task.")
file_to_process = files[0]
file_id = file_to_process['file_id']
print(f"Processing file: {file_to_process['file_name']} (ID: {file_id})")

# 6. Trigger the parsing process for the file
if client.parse_files(task_id=first_task_id, file_ids=[file_id]):
    print("Parsing task successfully triggered. Waiting for completion...")
    # In a real application, you might poll for status. Here, we just wait.
    time.sleep(10)

    # 7. Get the parsed text result
    result_text = client.get_parse_result(task_id=first_task_id, file_id=file_id)
    if result_text:
        print("\n--- Parsed Result (Text) ---")
        print("\n".join(result_text)[:500] + "...") # Print first 500 characters

    # 8. Get the download URL for the result archive
    download_url = client.download_parsed_results(task_id=first_task_id, file_ids=[file_id])
    if download_url:
        print("\n--- Download URL ---")
        print(download_url)
```

## API Reference
------------

🔥 The UnDatasIO Python SDK provides the following methods:

* **``UnDatasIO(token: str)``**

    - 🛠️ Initializes the client.
        -  ``token (str)``: Your API key, obtained from the UnDatasIO platform.

* **``workspace_list(self) -> Optional[List[Dict]]``**

    - 🏢 Retrieves a list of all workspaces accessible by your API key.
        -  ``file_dir_path (str)``: The path to the directory containing the files to upload.
        - Returns: A list of dictionaries, where each dictionary represents a workspace, or ``None`` on failure.

* **``task_list(self, work_id: str) -> Optional[List[Dict]]``**

    - 📋 Retrieves a list of all tasks within a specific workspace.
      - ``task_id (str)``: The ID of the target task.
      - Returns: A list of dictionaries representing tasks, or ``None`` on failure.

* **``get_task_files(self, task_id: str) -> Optional[List[Dict]]``**

    - 📂 Retrieves a list of all files within a specific task.
        -  ``task_id (str)``: The ID of the target task.
        - Returns: A list of dictionaries representing files, or ``None`` on failure.

* **``upload_file(self, task_id: str, file_path: str) -> bool``**

    - 📤 Uploads a single file to a specific task.
        -  ``task_id (str)``: The ID of the task to upload the file to.
        -  ``file_path (str)``: The local path to the file to be uploaded.
        - Returns: ``True`` on successful upload, ``False`` on failure.

* **``parse_files(self, task_id: str, file_ids: List[str], **kwargs) -> bool``**

    - 🌟 Triggers a parsing job for one or more files.
        -  ``task_id (str)``: The local path to the file to be uploaded.
        -  ``file_ids (List[str])``: The local path to the file to be uploaded.
        -  Optional keyword arguments like ``lang='ch'`` or ``parse_mode='fast'`` can be passed.
        - Returns: ``True`` if the parsing job was successfully triggered, ``False`` otherwise.

* **``get_parse_result(self, task_id: str, file_id: str) -> Optional[List[str]]``**

    - 📄 Fetches the parsed text result of a single file.
        -  ``task_id (str)``: The ID of the task.
        -  ``file_id (str)``: The ID of the file.
        - Returns: A list of strings, where each string is a block of parsed text, or None on failure.

* **``download_parsed_results(self, task_id: str, file_ids: List[str]) -> Optional[str]``**

    - 🔗 Requests a download URL for a ZIP archive containing the full parsing results.
        -  ``task_id (str)``: The ID of the task.
        -  ``file_ids (List[str])``: A list of file IDs to include in the archive.
        - Returns: A string containing the download URL, or None on failure.

## Colab Example
------------

📄 The following ipynb file is designed to run in a Colab environment. Clicking on it will allow you to run it directly in Colab.

## Error Handling
------------

📚 This SDK is designed for simplicity. All methods that fetch data will return the data directly on success or ``None`` on failure. Methods that perform an action will return ``True`` on success or ``False`` on failure.

- `Check for ``None`` or ``False``.` :Always check the return value of a method call to handle potential failures gracefully.
- `Check the Logs` In case of failure, the SDK will log detailed error information to the console using Python's standard logging module. This is your primary tool for debugging.

## Contact Us
------------

If you have any questions or need support, please visit our official website or contact us through our support channels.
