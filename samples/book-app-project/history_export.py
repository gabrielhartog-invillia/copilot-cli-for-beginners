import csv
import json


def export_to_csv(events: list, filepath: str = "history_export.csv") -> None:
    """Write events to a CSV file with columns: timestamp, event, title, changes."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "event", "title", "changes"])
        writer.writeheader()
        for event in events:
            changes = event.get("changes")
            writer.writerow({
                "timestamp": event.get("timestamp", ""),
                "event": event.get("event", ""),
                "title": event.get("title", ""),
                "changes": json.dumps(changes) if changes is not None else "",
            })
