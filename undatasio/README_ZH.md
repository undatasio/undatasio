**[English](README.md), [中文](README_ZH.md).**

# UnDatasIO Python SDK 中文文档

<p align="center">
  <a href="https://undatas.io">
    <img src="content/undatasio.png" width="100%" alt="UnDatasIO" />
  </a>
</p>

[![License](https://img.shields.io/npm/l/mithril.svg)](https://github.com/MithrilJS/mithril.js/blob/main/LICENSE) &nbsp;
[![Supported Python versions](https://shields.mitmproxy.org/pypi/pyversions/mitmproxy.svg)](https://pypi.python.org/pypi/mitmproxy)

💫 欢迎使用 UnDatasIO Python SDK
-------------------

**官方网站:** https://undatas.io/

UnDatasIO 提供强大的、基于云的文件解析能力。本 Python SDK 为您提供了一个流畅、开发者友好的接口，用于与 UnDatasIO API 进行交互。它允许您以编程方式管理工作区、任务和文件，让您专注于数据分析和应用开发。

## 主要特性
------------

*   **工作区与任务管理:** 轻松列出并浏览您的工作区和任务。
*   **全面的文件处理:** 将新文件上传到指定任务，并列出已存在的文件。
*   **异步解析任务:** 使用可配置的参数，为一个或多个文件触发解析作业。
*   **灵活的结果获取:** 获取结构化的文本解析结果，或请求一个包含所有产物（如Markdown、图片等）的可下载ZIP压缩包。
*   **Pythonic 设计风格:** 方法在成功时直接返回数据（例如，字典列表），在失败时返回 `None`，并通过日志记录详细的错误信息，便于调试。

## 安装
------------

🤖 您可以使用 `pip` 轻松安装 UnDatasIO Python SDK：
```bash
pip install undatasio
```

## 快速上手
------------

🥇 新的工作流遵循一个清晰的层级结构：工作区 -> 任务 -> 文件。下面是一个完整的示例，演示了整个流程：

```python
import time
from undatasio import UnDatasIO

# 1. 使用您的 token 和 API 基础URL 初始化客户端
client = UnDatasIO(
    token='your_api_key_here',
    base_url='https://temp.undatas.io/apikey'
)

# 2. 列出可用工作区，并选择第一个
workspaces = client.workspace_list()
if not workspaces:
    exit("未找到任何工作区。")
first_workspace_id = workspaces[0]['work_id']
print(f"正在使用工作区: {first_workspace_id}")

# 3. 列出所选工作区内的任务，并选择第一个
tasks = client.task_list(work_id=first_workspace_id)
if not tasks:
    exit(f"在工作区 {first_workspace_id} 中未找到任何任务。")
first_task_id = tasks[0]['task_id']
print(f"正在使用任务: {first_task_id}")

# 4. 上传一个新文件到此任务
# 请确保 'path/to/your/document.pdf' 文件真实存在
if client.upload_file(task_id=first_task_id, file_path='path/to/your/document.pdf'):
    print("文件上传成功！")

# 5. 列出任务中的所有文件，以获取 file_id
files = client.get_task_files(task_id=first_task_id)
if not files:
    exit("任务中未找到任何文件。")
file_to_process = files[0]
file_id = file_to_process['file_id']
print(f"正在处理文件: {file_to_process['file_name']} (ID: {file_id})")

# 6. 为该文件触发解析流程
if client.parse_files(task_id=first_task_id, file_ids=[file_id]):
    print("解析任务已成功触发，等待完成...")
    # 在实际应用中，您可能需要轮询状态。此处我们仅做等待演示。
    time.sleep(10)

    # 7. 获取解析后的文本结果
    result_text = client.get_parse_result(task_id=first_task_id, file_id=file_id)
    if result_text:
        print("\n--- 解析结果 (文本) ---")
        print("\n".join(result_text)[:500] + "...") # 打印前500个字符

    # 8. 获取结果压缩包的下载链接
    download_url = client.download_parsed_results(task_id=first_task_id, file_ids=[file_id])
    if download_url:
        print("\n--- 下载链接 ---")
        print(download_url)
```

## API 参考
------------

🔥 UnDatasIO Python SDK 提供以下方法：

*   **`UnDatasIO(token: str)`**
    -   🛠️ 初始化客户端。
        -   `token (str)`: 您从 UnDatasIO 平台获取的 API 密钥。

*   **`workspace_list(self) -> Optional[List[Dict]]`**
    -   🏢 获取您 API 密钥可访问的所有工作区列表。
        -   **返回**: 一个包含工作区信息的字典列表，失败时返回 `None`。

*   **`task_list(self, work_id: str) -> Optional[List[Dict]]`**
    -   📋 获取指定工作区内的所有任务列表。
        -   `work_id (str)`: 目标工作区的 ID。
        -   **返回**: 一个包含任务信息的字典列表，失败时返回 `None`。

*   **`get_task_files(self, task_id: str) -> Optional[List[Dict]]`**
    -   📂 获取指定任务内的所有文件列表。
        -   `task_id (str)`: 目标任务的 ID。
        -   **返回**: 一个包含文件信息的字典列表，失败时返回 `None`。

*   **`upload_file(self, task_id: str, file_path: str) -> bool`**
    -   📤 上传单个文件到指定的任务。
        -   `task_id (str)`: 文件要上传到的任务 ID。
        -   `file_path (str)`: 要上传的本地文件的路径。
        -   **返回**: 上传成功返回 `True`，失败返回 `False`。

*   **`parse_files(self, task_id: str, file_ids: List[str], **kwargs) -> bool`**
    -   🌟 为一个或多个文件触发解析作业。
        -   `task_id (str)`: 包含文件的任务 ID。
        -   `file_ids (List[str])`: 需要解析的文件 ID 列表。
        -   可选的关键字参数，例如 `lang='ch'` 或 `parse_mode='fast'`。
        -   **返回**: 解析作业成功触发返回 `True`，否则返回 `False`。

*   **`get_parse_result(self, task_id: str, file_id: str) -> Optional[List[str]]`**
    -   📄 获取单个文件的文本解析结果。
        -   `task_id (str)`: 任务的 ID。
        -   `file_id (str)`: 文件的 ID。
        -   **返回**: 一个字符串列表，其中每个字符串是一个解析后的文本块；失败时返回 `None`。

*   **`download_parsed_results(self, task_id: str, file_ids: List[str]) -> Optional[str]`**
    -   🔗 请求一个包含完整解析结果的 ZIP 压缩包的下载链接。
        -   `task_id (str)`: 任务的 ID。
        -   `file_ids (List[str])`: 需要包含在压缩包中的文件 ID 列表。
        -   **返回**: 一个包含下载链接的字符串，失败时返回 `None`。

## Colab 示例
------------

📄 以下 ipynb 文件被设计为在 Colab 环境中运行。点击链接即可在 Colab 中直接运行。


## 错误处理
------------

📚 本 SDK 的设计力求简洁。所有获取数据的方法在成功时会直接返回数据，失败时返回 `None`。所有执行操作的方法在成功时返回 `True`，失败时返回 `False`。

-   **检查 `None` 或 `False` 返回值**: 务必检查方法调用的返回值，以便优雅地处理潜在的失败情况。
-   **查看日志**: 如果发生失败，SDK 会使用 Python 标准的 `logging` 模块向控制台输出详细的错误信息。这是您进行调试的主要工具。

## 联系我们
------------

如果您有任何问题或需要支持，请访问我们的官方网站或通过我们的支持渠道与我们联系。


