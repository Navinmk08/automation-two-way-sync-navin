import logging
from typing import Dict

from lead_client import GoogleSheetsLeadClient
from task_client import ClickUpClient
from config import (
    GOOGLE_SHEETS_CREDS_JSON,
    GOOGLE_SHEETS_SPREADSHEET_ID,
    GOOGLE_SHEETS_WORKSHEET_NAME,
    CLICKUP_API_TOKEN,
    CLICKUP_TEAM_ID,
    CLICKUP_LIST_ID,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Simple status mapping
LEAD_TO_TASK_STATUS = {
    "NEW": "to do",
    "CONTACTED": "in progress",
    "QUALIFIED": "done",
}


def run_sync(leads_client: GoogleSheetsLeadClient = None, cu: ClickUpClient = None):
    if not all([GOOGLE_SHEETS_CREDS_JSON, GOOGLE_SHEETS_SPREADSHEET_ID, CLICKUP_API_TOKEN, CLICKUP_LIST_ID]):
        # allow injected clients for tests
        if not (leads_client and cu):
            raise RuntimeError("Missing required configuration. Check environment variables.")

    if leads_client is None:
        leads_client = GoogleSheetsLeadClient(GOOGLE_SHEETS_CREDS_JSON, GOOGLE_SHEETS_SPREADSHEET_ID, GOOGLE_SHEETS_WORKSHEET_NAME)
    if cu is None:
        cu = ClickUpClient(CLICKUP_API_TOKEN, CLICKUP_TEAM_ID, CLICKUP_LIST_ID)

    leads = leads_client.list_leads()
    logger.info("Found %d leads in sheet", len(leads))

    # Lead -> Task: ensure task exists for leads not LOST
    for lead in leads:
        try:
            lead_id = lead.get("id")
            status = (lead.get("status", "") or "").upper()
            row = lead.get("__row")

            if status == "LOST":
                logger.info("Skipping lost lead %s", lead_id)
                continue

            task_id = (lead.get("task_id") or "").strip()
            desired_task_status = LEAD_TO_TASK_STATUS.get(status, "to do")

            if not task_id:
                # Check for an existing task with external_id to avoid duplicates
                existing = None
                try:
                    existing = cu.find_task_by_external_id(lead_id)
                except Exception:
                    logger.exception("Failed to search ClickUp by external_id for lead %s", lead_id)

                if existing:
                    new_task_id = existing.get("id")
                    leads_client.update_task_id(row, new_task_id)
                    # also ensure status matches
                    try:
                        current_status = (existing.get("status") or "").lower()
                        if current_status != desired_task_status:
                            cu.update_task(new_task_id, {"status": desired_task_status})
                    except Exception:
                        logger.exception("Failed to update found task %s status", new_task_id)
                else:
                    # create a task
                    name = f"Follow up: {lead.get('name')}"
                    desc = f"Lead: {lead.get('name')} ({lead.get('email')})\nSource: {lead.get('source')}\nLeadID: {lead_id}"
                    task = cu.create_task(name=name, description=desc, status=desired_task_status, external_id=str(lead_id))
                    new_task_id = task.get("id")
                    if new_task_id:
                        leads_client.update_task_id(row, new_task_id)
            else:
                # ensure task status matches
                try:
                    task = cu.get_task(task_id)
                    current_status = (task.get("status") or "").lower()
                    if current_status != desired_task_status:
                        cu.update_task(task_id, {"status": desired_task_status})
                        logger.info("Updated ClickUp task %s status to %s", task_id, desired_task_status)
                except Exception:
                    logger.exception("Failed to sync task for lead %s", lead_id)
        except Exception:
            logger.exception("Error processing lead: %s", lead)

    # Task -> Lead: poll tasks and update sheet when needed
    try:
        tasks = cu.list_tasks()
        logger.info("Fetched %d tasks from ClickUp list", len(tasks))
        for t in tasks:
            try:
                tid = t.get("id")
                t_status = (t.get("status") or "").upper()
                # find the lead row by matching task_id in sheet
                for lead in leads:
                    if (lead.get("task_id") or "") == tid:
                        row = lead.get("__row")
                        # if task is done, mark lead QUALIFIED
                        if t_status == "DONE" and lead.get("status") != "QUALIFIED":
                            leads_client.update_lead_status(row, "QUALIFIED")
                            logger.info("Updated lead %s to QUALIFIED based on task %s", lead.get("id"), tid)
                        break
            except Exception:
                logger.exception("Error processing task %s", t.get("id"))
    except Exception:
        logger.exception("Failed to list ClickUp tasks")


if __name__ == "__main__":
    run_sync()
