import json
import logging
import os
from typing import Dict, List, Optional

import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)


class GoogleSheetsLeadClient:
    """Simple client to read/write leads from a Google Sheet.

    Expects a sheet with headers: id,name,email,status,source,task_id
    """

    def __init__(self, creds_json: str, spreadsheet_id: str, worksheet_name: str = "Leads"):
        # creds_json can be a path or raw JSON string
        if os.path.exists(creds_json):
            with open(creds_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(creds_json)

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        creds = Credentials.from_service_account_info(data, scopes=scopes)
        client = gspread.authorize(creds)

        self.spreadsheet = client.open_by_key(spreadsheet_id)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)

    def _ensure_headers(self):
        headers = self.worksheet.row_values(1)
        expected = ["id", "name", "email", "status", "source", "task_id"]
        if headers != expected:
            logger.warning("Headers do not match expected. Current headers: %s", headers)

    def list_leads(self) -> List[Dict]:
        self._ensure_headers()
        rows = self.worksheet.get_all_records()
        # attach row index for updates
        leads = []
        for i, row in enumerate(rows, start=2):
            row['__row'] = i
            leads.append(row)
        return leads

    def update_task_id(self, row_index: int, task_id: str):
        try:
            col = self._col_index('task_id')
            self.worksheet.update_cell(row_index, col, task_id)
            logger.info("Wrote task_id %s to row %d", task_id, row_index)
        except Exception:
            logger.exception("Failed to write task_id for row %s", row_index)

    def update_lead_status(self, row_index: int, new_status: str):
        try:
            col = self._col_index('status')
            self.worksheet.update_cell(row_index, col, new_status)
            logger.info("Updated status to %s for row %d", new_status, row_index)
        except Exception:
            logger.exception("Failed to update status for row %s", row_index)

    def _col_index(self, header_name: str) -> int:
        headers = self.worksheet.row_values(1)
        try:
            return headers.index(header_name) + 1
        except ValueError:
            raise RuntimeError(f"Header {header_name} not found in sheet")
