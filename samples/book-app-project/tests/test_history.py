"""Unit tests for HistoryLog class (SCRUM-12)."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
from datetime import datetime
import history
from history import HistoryLog


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch) -> None:
    """Use a temporary history file for each test."""
    temp_file = tmp_path / "history.json"
    monkeypatch.setattr(history.HistoryLog, "HISTORY_FILE", str(temp_file))


def test_record_creates_history_file() -> None:
    """Verify that record() creates history.json."""
    log = HistoryLog()
    log.record("added", "1984")
    assert os.path.exists(log.HISTORY_FILE)


def test_load_returns_list() -> None:
    """Verify that load() returns a list."""
    log = HistoryLog()
    result = log.load()
    assert isinstance(result, list)


def test_load_returns_empty_when_file_not_exists() -> None:
    """Verify that load() returns [] when history.json doesn't exist."""
    log = HistoryLog()
    result = log.load()
    assert result == []
    assert len(result) == 0


def test_record_added_event() -> None:
    """Verify that record('added', ...) creates correct event entry."""
    log = HistoryLog()
    log.record("added", "Livro")
    
    events = log.load()
    assert len(events) == 1
    assert events[0]["event"] == "added"
    assert events[0]["title"] == "Livro"
    assert events[0]["changes"] is None


def test_record_edited_event() -> None:
    """Verify that record('edited', ...) with changes is recorded correctly."""
    log = HistoryLog()
    changes = {"author": {"before": "A", "after": "B"}}
    log.record("edited", "Livro", changes)
    
    events = log.load()
    assert len(events) == 1
    assert events[0]["event"] == "edited"
    assert events[0]["title"] == "Livro"
    assert events[0]["changes"] == changes
    assert events[0]["changes"]["author"]["before"] == "A"
    assert events[0]["changes"]["author"]["after"] == "B"


def test_record_timestamp_format() -> None:
    """Verify that timestamp is in ISO 8601 format."""
    log = HistoryLog()
    log.record("added", "1984")
    
    events = log.load()
    timestamp = events[0]["timestamp"]
    
    # Verify it's a string
    assert isinstance(timestamp, str)
    
    # Verify it can be parsed as ISO 8601
    try:
        parsed = datetime.fromisoformat(timestamp)
        assert parsed is not None
    except ValueError:
        pytest.fail(f"Timestamp '{timestamp}' is not valid ISO 8601 format")


def test_clear_removes_file() -> None:
    """Verify that clear() removes history.json."""
    log = HistoryLog()
    
    # Create file by recording an event
    log.record("added", "Livro")
    assert os.path.exists(log.HISTORY_FILE)
    
    # Clear the file
    log.clear()
    assert not os.path.exists(log.HISTORY_FILE)
    
    # Verify load() returns empty list after clear
    assert log.load() == []


def test_clear_is_silent_if_file_not_exists() -> None:
    """Verify that clear() doesn't raise exception when file doesn't exist."""
    log = HistoryLog()
    
    # Ensure file doesn't exist
    assert not os.path.exists(log.HISTORY_FILE)
    
    # Should not raise any exception
    try:
        log.clear()
    except Exception as e:
        pytest.fail(f"clear() raised {type(e).__name__}: {e}")


def test_record_appends_multiple_events() -> None:
    """Verify that multiple record() calls append events."""
    log = HistoryLog()
    
    log.record("added", "1984")
    log.record("added", "Dune")
    log.record("edited", "1984", {"author": {"before": "X", "after": "Y"}})
    
    events = log.load()
    assert len(events) == 3
    assert events[0]["title"] == "1984"
    assert events[1]["title"] == "Dune"
    assert events[2]["title"] == "1984"
    assert events[2]["changes"] is not None


def test_record_deleted_event() -> None:
    """Verify that record('deleted', ...) creates correct event entry."""
    log = HistoryLog()
    log.record("deleted", "OldBook")
    
    events = log.load()
    assert len(events) == 1
    assert events[0]["event"] == "deleted"
    assert events[0]["title"] == "OldBook"
    assert events[0]["changes"] is None


def test_load_persists_across_instances() -> None:
    """Verify that events persist and can be loaded by new instances."""
    log1 = HistoryLog()
    log1.record("added", "Book1")
    
    # Create new instance
    log2 = HistoryLog()
    events = log2.load()
    
    assert len(events) == 1
    assert events[0]["title"] == "Book1"


def test_record_with_complex_changes_structure() -> None:
    """Verify that record() handles complex changes dictionary."""
    log = HistoryLog()
    changes = {
        "author": {"before": "Old Author", "after": "New Author"},
        "year": {"before": 2000, "after": 2020},
        "read": {"before": False, "after": True}
    }
    log.record("edited", "Complex Book", changes)
    
    events = log.load()
    assert events[0]["changes"] == changes
    assert len(events[0]["changes"]) == 3


def test_clear_followed_by_record() -> None:
    """Verify that recording after clear() works correctly."""
    log = HistoryLog()
    
    log.record("added", "Book1")
    log.clear()
    log.record("added", "Book2")
    
    events = log.load()
    assert len(events) == 1
    assert events[0]["title"] == "Book2"


def test_history_file_contains_valid_json() -> None:
    """Verify that history.json contains valid JSON."""
    log = HistoryLog()
    log.record("added", "JsonTest")
    
    # Read the file directly and parse as JSON
    with open(log.HISTORY_FILE, "r") as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "JsonTest"


def test_load_handles_corrupted_json() -> None:
    """Verify that load() raises JSONDecodeError for corrupted JSON."""
    log = HistoryLog()
    
    # Write corrupted JSON to file
    with open(log.HISTORY_FILE, "w") as f:
        f.write("{invalid json")
    
    # load() should raise JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        log.load()


def test_record_empty_changes() -> None:
    """Verify that record() handles empty changes dict."""
    log = HistoryLog()
    log.record("edited", "EmptyChanges", {})
    
    events = log.load()
    assert events[0]["changes"] == {}


def test_timestamp_not_empty() -> None:
    """Verify that timestamp is never empty."""
    log = HistoryLog()
    log.record("added", "Book")
    
    events = log.load()
    assert events[0]["timestamp"]  # Not None or empty string
    assert len(events[0]["timestamp"]) > 0


def test_all_required_fields_in_event() -> None:
    """Verify that all required fields are present in event entry."""
    log = HistoryLog()
    log.record("added", "FieldTest")
    
    events = log.load()
    event = events[0]
    
    assert "event" in event
    assert "title" in event
    assert "timestamp" in event
    assert "changes" in event
