import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import pytest
from history_export import export_to_csv

EVENTS = [
    {
        "event": "added",
        "title": "O Senhor dos Anéis",
        "timestamp": "2026-04-18T22:04:55",
        "changes": None,
    },
    {
        "event": "edited",
        "title": "1984",
        "timestamp": "2026-04-18T22:05:10",
        "changes": {"author": {"before": "Eric Blair", "after": "George Orwell"}},
    },
]


def test_export_creates_file(tmp_path):
    filepath = str(tmp_path / "out.csv")
    export_to_csv(EVENTS, filepath)
    assert os.path.exists(filepath)


def test_export_csv_headers(tmp_path):
    filepath = str(tmp_path / "out.csv")
    export_to_csv(EVENTS, filepath)
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert set(reader.fieldnames) == {"timestamp", "event", "title", "changes"}


def test_export_csv_rows(tmp_path):
    filepath = str(tmp_path / "out.csv")
    export_to_csv(EVENTS, filepath)
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(EVENTS)


def test_export_empty_events(tmp_path):
    filepath = str(tmp_path / "empty.csv")
    export_to_csv([], filepath)
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows == []
    assert set(reader.fieldnames) == {"timestamp", "event", "title", "changes"}


def test_export_changes_serialized(tmp_path):
    filepath = str(tmp_path / "out.csv")
    export_to_csv(EVENTS, filepath)
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    edited_row = next(r for r in rows if r["event"] == "edited")
    assert edited_row["changes"] != ""


def test_export_changes_none_empty_string(tmp_path):
    filepath = str(tmp_path / "out.csv")
    export_to_csv(EVENTS, filepath)
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    added_row = next(r for r in rows if r["event"] == "added")
    assert added_row["changes"] == ""


def test_export_custom_filepath(tmp_path):
    filepath = str(tmp_path / "custom_dir" / "export.csv")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    export_to_csv(EVENTS, filepath)
    assert os.path.exists(filepath)
