"""Unit tests for CSV export functionality."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
from typing import Any
import pytest
from history_export import export_to_csv


class TestExportCreatesCsvFile:
    """Test that export_to_csv() creates a CSV file."""

    def test_export_creates_csv_file(self, tmp_path) -> None:
        """Verify that export_to_csv() creates the file at the specified path."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Test Book",
                "changes": None,
            }
        ]

        export_to_csv(events, str(csv_file))

        assert csv_file.exists(), "CSV file was not created"
        assert csv_file.stat().st_size > 0, "CSV file is empty"


class TestExportCsvFormat:
    """Test CSV format and structure."""

    def test_export_csv_format(self, tmp_path) -> None:
        """Verify that CSV has the correct columns: timestamp, event, title, changes."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Test Book",
                "changes": None,
            }
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            assert fieldnames == [
                "timestamp",
                "event",
                "title",
                "changes",
            ], f"Expected columns [timestamp, event, title, changes], got {fieldnames}"


class TestExportAddedEvent:
    """Test export of 'added' events."""

    def test_export_added_event(self, tmp_path) -> None:
        """Export 'added' event (changes=null) and verify changes column is empty."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Clean Code",
                "changes": None,
            }
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1, "Should have one event row (plus header)"
            row = rows[0]
            assert row["timestamp"] == "2024-01-01T10:00:00"
            assert row["event"] == "added"
            assert row["title"] == "Clean Code"
            assert row["changes"] == "", "changes column should be empty for null values"


class TestExportEditedEvent:
    """Test export of 'edited' events with changes."""

    def test_export_edited_event(self, tmp_path) -> None:
        """Export 'edited' event with changes and verify JSON is correct."""
        csv_file = tmp_path / "test_export.csv"
        changes = {"old_year": 1949, "new_year": 1950}
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-02T14:30:00",
                "event": "edited",
                "title": "1984",
                "changes": changes,
            }
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            row = rows[0]
            assert row["event"] == "edited"
            
            # Parse JSON from changes column
            parsed_changes = json.loads(row["changes"])
            assert parsed_changes == changes
            assert parsed_changes["old_year"] == 1949
            assert parsed_changes["new_year"] == 1950


class TestExportMultipleEvents:
    """Test export of multiple events."""

    def test_export_multiple_events(self, tmp_path) -> None:
        """Export 3+ events and verify all are present in CSV."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Book 1",
                "changes": None,
            },
            {
                "timestamp": "2024-01-02T11:00:00",
                "event": "added",
                "title": "Book 2",
                "changes": None,
            },
            {
                "timestamp": "2024-01-03T12:00:00",
                "event": "edited",
                "title": "Book 1",
                "changes": {"marked_as_read": True},
            },
            {
                "timestamp": "2024-01-04T13:00:00",
                "event": "removed",
                "title": "Book 2",
                "changes": None,
            },
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 4, f"Expected 4 events, got {len(rows)}"
            
            # Verify each event
            assert rows[0]["title"] == "Book 1"
            assert rows[1]["title"] == "Book 2"
            assert rows[2]["title"] == "Book 1"
            assert rows[2]["event"] == "edited"
            assert rows[3]["title"] == "Book 2"
            assert rows[3]["event"] == "removed"


class TestExportSpecialCharacters:
    """Test export with special characters."""

    def test_export_handles_special_chars(self, tmp_path) -> None:
        """Test that titles with quotes, commas, etc. are escaped correctly."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": 'The "Hobbit": A Journey',
                "changes": None,
            },
            {
                "timestamp": "2024-01-02T11:00:00",
                "event": "added",
                "title": "Book with, comma, characters",
                "changes": None,
            },
            {
                "timestamp": "2024-01-03T12:00:00",
                "event": "added",
                "title": "Book with\nnewline character",
                "changes": None,
            },
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3

            # Verify that special characters are preserved correctly
            assert rows[0]["title"] == 'The "Hobbit": A Journey'
            assert rows[1]["title"] == "Book with, comma, characters"
            assert rows[2]["title"] == "Book with\nnewline character"


class TestExportEmptyList:
    """Test export with empty events list."""

    def test_export_empty_list(self, tmp_path) -> None:
        """Verify that export_to_csv([]) raises ValueError."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = []

        with pytest.raises(ValueError, match="Events list cannot be empty"):
            export_to_csv(events, str(csv_file))


class TestExportEdgeCases:
    """Test edge cases and special scenarios."""

    def test_export_with_complex_json_changes(self, tmp_path) -> None:
        """Test export with nested JSON structures in changes."""
        csv_file = tmp_path / "test_export.csv"
        changes = {
            "metadata": {"old": {"year": 1949}, "new": {"year": 1950}},
            "tags": ["classic", "fiction"],
            "count": 42,
        }
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "edited",
                "title": "Complex Book",
                "changes": changes,
            }
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            row = rows[0]
            parsed_changes = json.loads(row["changes"])
            assert parsed_changes == changes
            assert parsed_changes["metadata"]["old"]["year"] == 1949
            assert parsed_changes["tags"] == ["classic", "fiction"]
            assert parsed_changes["count"] == 42

    def test_export_with_missing_fields(self, tmp_path) -> None:
        """Test export when event dict is missing optional fields."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Partial Event",
            }
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            row = rows[0]
            assert row["changes"] == ""

    def test_export_unicode_characters(self, tmp_path) -> None:
        """Test export with Unicode characters."""
        csv_file = tmp_path / "test_export.csv"
        events: list[dict[str, Any]] = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "event": "added",
                "title": "Dom Casmurro - Machado de Assis",
                "changes": None,
            },
            {
                "timestamp": "2024-01-02T11:00:00",
                "event": "added",
                "title": "こんにちは (Japanese)",
                "changes": None,
            },
            {
                "timestamp": "2024-01-03T12:00:00",
                "event": "added",
                "title": "Émile Zola's Novels",
                "changes": None,
            },
        ]

        export_to_csv(events, str(csv_file))

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3
            assert rows[0]["title"] == "Dom Casmurro - Machado de Assis"
            assert rows[1]["title"] == "こんにちは (Japanese)"
            assert rows[2]["title"] == "Émile Zola's Novels"
