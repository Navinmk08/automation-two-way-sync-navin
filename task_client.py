import logging
from typing import Dict, List, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


class ClickUpClient:
    BASE = "https://api.clickup.com/api/v2"

    def __init__(self, api_token: str, team_id: str, list_id: str):
        self.token = api_token
        self.team_id = team_id
        self.list_id = list_id
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), retry=retry_if_exception_type(Exception))
    def create_task(self, name: str, description: str, status: str, external_id: Optional[str] = None) -> Dict:
        url = f"{self.BASE}/list/{self.list_id}/task"
        payload = {
            "name": name,
            "description": description,
            "status": status,
        }
        if external_id:
            payload["external_id"] = external_id

        r = requests.post(url, headers=self.headers, json=payload, timeout=15)
        if not r.ok:
            logger.error("ClickUp create_task error: %s %s", r.status_code, r.text)
            r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), retry=retry_if_exception_type(Exception))
    def update_task(self, task_id: str, fields: Dict) -> Dict:
        url = f"{self.BASE}/task/{task_id}"
        r = requests.put(url, headers=self.headers, json=fields, timeout=15)
        if not r.ok:
            logger.error("ClickUp update_task error: %s %s", r.status_code, r.text)
            r.raise_for_status()
        return r.json()

    def list_tasks(self) -> List[Dict]:
        # Paginate through tasks in the list
        url = f"{self.BASE}/list/{self.list_id}/task"
        params = {"page": 0}
        tasks = []
        while True:
            r = requests.get(url, headers=self.headers, params=params, timeout=15)
            if not r.ok:
                logger.error("ClickUp list_tasks error: %s %s", r.status_code, r.text)
                r.raise_for_status()
            data = r.json()
            tasks.extend(data.get("tasks", []))
            if not data.get("tasks") or len(data.get("tasks")) == 0:
                break
            params["page"] += 1
            # safety: avoid infinite loop
            if params["page"] > 50:
                break
        return tasks

    def get_task(self, task_id: str) -> Dict:
        url = f"{self.BASE}/task/{task_id}"
        r = requests.get(url, headers=self.headers, timeout=15)
        if not r.ok:
            logger.error("ClickUp get_task error: %s %s", r.status_code, r.text)
            r.raise_for_status()
        return r.json()

    def find_task_by_external_id(self, external_id: str) -> Optional[Dict]:
        """Search tasks in the list for a task with matching external_id.

        This is linear search across tasks in the list; OK for small lists used in demo.
        """
        for t in self.list_tasks():
            if t.get("external_id") == str(external_id):
                return t
        return None
