import json
import os
from datetime import datetime


class HistoryLog:
    HISTORY_FILE = "history.json"

    def record(self, event: str, title: str, changes: dict = None) -> None:
        history = self.load()
        history.append({
            "event": event,
            "title": title,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "changes": changes,
        })
        with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def load(self) -> list:
        try:
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear(self) -> None:
        try:
            os.remove(self.HISTORY_FILE)
        except FileNotFoundError:
            pass
