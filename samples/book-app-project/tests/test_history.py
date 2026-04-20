import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import history
from history import HistoryLog


@pytest.fixture(autouse=True)
def use_temp_history_file(tmp_path, monkeypatch):
    """Use a temporary history file for each test."""
    temp_file = tmp_path / "history.json"
    monkeypatch.setattr(history.HistoryLog, "HISTORY_FILE", str(temp_file))


def test_load_empty():
    log = HistoryLog()
    assert log.load() == []


def test_record_creates_event():
    log = HistoryLog()
    log.record("added", "1984")
    events = log.load()
    assert len(events) == 1
    assert events[0]["event"] == "added"
    assert events[0]["title"] == "1984"


def test_record_appends():
    log = HistoryLog()
    log.record("added", "1984")
    log.record("added", "Dune")
    events = log.load()
    assert len(events) == 2


def test_record_with_changes():
    log = HistoryLog()
    changes = {"author": {"before": "A", "after": "B"}}
    log.record("edited", "1984", changes)
    events = log.load()
    assert events[0]["changes"] == changes


def test_clear_removes_file():
    log = HistoryLog()
    log.record("added", "1984")
    log.clear()
    assert log.load() == []


def test_clear_no_file():
    log = HistoryLog()
    log.clear()  # should not raise


def test_event_has_timestamp():
    log = HistoryLog()
    log.record("added", "1984")
    events = log.load()
    assert "timestamp" in events[0]
    assert events[0]["timestamp"] != ""
