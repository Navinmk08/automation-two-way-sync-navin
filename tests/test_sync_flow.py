from unittest.mock import MagicMock

import pytest

from sync_logic import run_sync


def test_run_sync_creates_task_and_updates_sheet():
    # Prepare fake lead client
    lead = {"id": "lead-123", "name": "Tina", "email": "tina@example.com", "status": "NEW", "source": "Website", "task_id": "", "__row": 2}
    leads_client = MagicMock()
    leads_client.list_leads.return_value = [lead]
    leads_client.update_task_id = MagicMock()

    # Prepare fake ClickUp client
    cu = MagicMock()
    cu.find_task_by_external_id.return_value = None
    cu.create_task.return_value = {"id": "task-xyz"}

    # Run sync with injected clients
    run_sync(leads_client=leads_client, cu=cu)

    # Expect a task created and sheet updated
    cu.create_task.assert_called_once()
    leads_client.update_task_id.assert_called_once_with(2, "task-xyz")
