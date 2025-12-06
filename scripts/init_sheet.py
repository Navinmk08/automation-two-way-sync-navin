"""Initialize a Google Sheet worksheet with headers and optional sample rows.

Usage: set env vars (or .env) and run:
    python scripts/init_sheet.py
"""
import logging
from config import GOOGLE_SHEETS_CREDS_JSON, GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_SHEETS_WORKSHEET_NAME
from lead_client import GoogleSheetsLeadClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_sheet():
    if not all([GOOGLE_SHEETS_CREDS_JSON, GOOGLE_SHEETS_SPREADSHEET_ID]):
        raise RuntimeError("Set GOOGLE_SHEETS_CREDS_JSON and GOOGLE_SHEETS_SPREADSHEET_ID")

    client = GoogleSheetsLeadClient(GOOGLE_SHEETS_CREDS_JSON, GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_SHEETS_WORKSHEET_NAME)
    ws = client.worksheet

    headers = ["id", "name", "email", "status", "source", "task_id"]
    # write headers
    ws.update('A1:F1', [headers])
    logger.info("Wrote headers to worksheet %s", GOOGLE_SHEETS_WORKSHEET_NAME)

    sample = [
        ["lead-1", "Alice Example", "alice@example.com", "NEW", "Website", ""],
        ["lead-2", "Bob Sample", "bob@example.com", "CONTACTED", "LinkedIn", ""],
    ]
    ws.update('A2:F3', sample)
    logger.info("Wrote %d sample rows", len(sample))


if __name__ == "__main__":
    init_sheet()
