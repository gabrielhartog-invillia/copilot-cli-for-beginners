"""CSV export functionality for book history events."""

import csv
import json
from typing import Any, Optional


def export_to_csv(events: list[dict[str, Any]], filepath: str = "history_export.csv") -> None:
    """
    Export book history events to a CSV file.

    Args:
        events: List of event dictionaries with keys: timestamp, event, title, changes.
                Each event should have the format:
                {"timestamp": str, "event": str, "title": str, "changes": dict | None}
        filepath: Path where the CSV file will be written. Defaults to "history_export.csv"
                  in the current working directory.

    Returns:
        None

    Raises:
        ValueError: If the events list is empty.

    Notes:
        - The 'changes' column contains a JSON string representation when the changes
          value is not None, and remains empty when None.
        - CSV is written with columns: timestamp, event, title, changes
    """
    if not events:
        raise ValueError("Events list cannot be empty")

    fieldnames = ["timestamp", "event", "title", "changes"]

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for event in events:
            row = {
                "timestamp": event.get("timestamp", ""),
                "event": event.get("event", ""),
                "title": event.get("title", ""),
                "changes": (
                    json.dumps(event["changes"]) if event.get("changes") is not None else ""
                ),
            }
            writer.writerow(row)
