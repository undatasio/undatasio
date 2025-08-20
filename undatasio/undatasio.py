import requests
import json
import logging
import os
from typing import Optional, List, Dict, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UnDatasIO:

    def __init__(self, token: str):
        if not token:
            raise ValueError("API token cannot be empty.")

        self.token = token
        self.base_url = "https://temp.undatas.io/apikey"

        self.headers = {
            "Authorization": f"{self.token}"
        }

    def _make_get_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Union[List, Dict]]:
        api_url = f"{self.base_url}{endpoint}"
        logging.info(f"Sending GET request to {api_url} with params: {params}")
        try:
            response = requests.get(api_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            api_response = response.json()
            if api_response.get("code") == 200:
                return api_response.get("data")
            else:
                logging.error(f"API business error. Code: {api_response.get('code')}, Msg: {api_response.get('msg')}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"GET request error: {e}")
            return None

    def _make_post_request(self, endpoint: str, json_data: Dict) -> Optional[Dict]:

        api_url = f"{self.base_url}{endpoint}"
        logging.info(f"Sending POST request to {api_url} with JSON data.")
        try:
            response = requests.post(api_url, headers=self.headers, json=json_data, timeout=30)
            response.raise_for_status()
            api_response = response.json()
            if api_response.get("code") == 200:
                return api_response.get("data")
            else:
                logging.error(f"API business error. Code: {api_response.get('code')}, Msg: {api_response.get('msg')}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"POST request error: {e}")
            return None

    def workspace_list(self) -> Optional[List[Dict]]:
        return self._make_get_request(endpoint="/workspace/list")

    def task_list(self, work_id: str) -> Optional[List[Dict]]:
        if not work_id: raise ValueError("work_id cannot be empty.")
        return self._make_get_request(endpoint="/task/list", params={"work_id": work_id})

    def get_task_files(self, task_id: str) -> Optional[List[Dict]]:
        if not task_id: raise ValueError("task_id cannot be empty.")
        return self._make_get_request(endpoint="/task/parse/list", params={"task_id": task_id})

    def upload_file(self, task_id: str, file_path: str) -> bool:

        if not task_id: raise ValueError("task_id cannot be empty.")
        if not os.path.exists(file_path):
            logging.error(f"File not found at path: {file_path}")
            return False

        endpoint = "/task/parse/upload"
        api_url = f"{self.base_url}{endpoint}"

        data = {"task_id": task_id}

        file_name = os.path.basename(file_path)
        logging.info(f"Uploading file '{file_name}' to task '{task_id}'...")

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}

                response = requests.post(
                    api_url,
                    headers=self.headers,
                    data=data,
                    files=files,
                    timeout=60
                )

            response.raise_for_status()
            api_response = response.json()

            if api_response.get("code") == 200:
                logging.info(f"File '{file_name}' uploaded successfully.")
                return True
            else:
                logging.error(f"API upload error. Code: {api_response.get('code')}, Msg: {api_response.get('msg')}")
                return False

        except requests.exceptions.RequestException as e:
            logging.error(f"Upload request error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status: {e.response.status_code}")
                logging.error(f"Response body: {e.response.text}")
            return False

    def parse_files(self, task_id: str, file_ids: List[str], ds_id: str = "default", lang: str = "ch",
                    parse_mode: str = "fast") -> bool:
        if not task_id or not file_ids:
            raise ValueError("task_id and file_ids cannot be empty.")

        payload = {
            "task_id": task_id,
            "file_ids": file_ids,
            "ds_id": ds_id,
            "parse_config": {
                "lang": lang,
                "parse_mode": parse_mode
            }
        }

        response = self._make_post_request(endpoint="/task/parse/multiple", json_data=payload)

        return response is not None

    def get_parse_result(self, task_id: str, file_id: str) -> Optional[List[str]]:
        if not task_id or not file_id:
            raise ValueError("task_id and file_id cannot be empty.")

        payload = {
            "task_id": task_id,
            "file_id": file_id
        }

        return self._make_post_request(endpoint="/task/parse/result", json_data=payload)

    def download_parsed_results(self, task_id: str, file_ids: List[str]) -> Optional[str]:
        if not task_id or not file_ids:
            raise ValueError("task_id and file_ids cannot be empty.")

        endpoint = "/task/parse/download"
        payload = {"task_id": task_id, "file_ids": file_ids}

        logging.info(f"Requesting download URL for task {task_id}...")

        response_data = self._make_post_request(endpoint, payload)

        if response_data and isinstance(response_data, dict) and "download_url" in response_data:
            download_url = response_data["download_url"]
            logging.info(f"Successfully obtained download URL: {download_url}")
            return download_url
        else:
            logging.error("Failed to get a valid download URL from the API response.")
            return None

        #
        # try:
        #     os.makedirs(save_directory, exist_ok=True)
        #     local_filename = download_url.split('/')[-1]
        #     local_filepath = os.path.join(save_directory, local_filename)
        #
        #     logging.info(f"Downloading file to {local_filepath}...")
        #     with requests.get(download_url, stream=True, timeout=300) as r:
        #         r.raise_for_status()
        #         with open(local_filepath, 'wb') as f:
        #             for chunk in r.iter_content(chunk_size=8192):
        #                 f.write(chunk)
        #     logging.info("Download complete.")
        #     return local_filepath
        #
        # except (requests.exceptions.RequestException, IOError) as e:
        #     logging.error(f"Failed to download or save file: {e}")
        #     return None




