from sync_logic import LEAD_TO_TASK_STATUS


def test_mapping_has_new():
    assert LEAD_TO_TASK_STATUS["NEW"] == "to do"


def test_mapping_defaults():
    assert LEAD_TO_TASK_STATUS.get("UNKNOWN", "to do") == "to do"
