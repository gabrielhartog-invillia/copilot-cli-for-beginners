"""
HistoryLog module for tracking changes to the book collection.
"""

import json
import os
from datetime import datetime
from typing import Optional


class HistoryLog:
    """
    Manages persistent event logging for book collection operations.
    
    Records "added", "edited", and "deleted" events with timestamps
    and optional change tracking to history.json.
    """
    
    HISTORY_FILE = "history.json"

    def record(self, event: str, title: str, changes: Optional[dict] = None) -> None:
        """
        Record a book event to the history file.
        
        Args:
            event: Type of event ("added", "edited", or "deleted")
            title: Title of the book
            changes: Dictionary mapping field names to {"before": ..., "after": ...} dicts.
                    Used for "edited" events. Should be None for "added"/"deleted".
        
        Returns:
            None
        
        Raises:
            IOError: If history file cannot be written
            json.JSONDecodeError: If existing history.json is corrupted
        """
        # Load existing history or create new list
        history = self.load()
        
        # Create new event entry
        event_entry = {
            "event": event,
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "changes": changes
        }
        
        # Append new event
        history.append(event_entry)
        
        # Write back to file
        try:
            with open(self.HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to write to {self.HISTORY_FILE}: {e}")

    def load(self) -> list:
        """
        Load all recorded events from history.json.
        
        Returns:
            List of event dictionaries. Empty list if file doesn't exist.
            Each event dict has keys: event, title, timestamp, changes
        
        Raises:
            json.JSONDecodeError: If history.json exists but is malformed
        """
        if not os.path.exists(self.HISTORY_FILE):
            return []
        
        try:
            with open(self.HISTORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Corrupted history file {self.HISTORY_FILE}: {e.msg}",
                e.doc,
                e.pos
            )

    def clear(self) -> None:
        """
        Remove the history.json file from disk.
        
        Returns:
            None
        
        Silently succeeds if file doesn't exist.
        """
        try:
            if os.path.exists(self.HISTORY_FILE):
                os.remove(self.HISTORY_FILE)
        except OSError as e:
            # Silently fail if we can't delete - file may have been deleted elsewhere
            pass
