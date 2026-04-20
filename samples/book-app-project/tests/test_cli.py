import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import history as history_module
from history import HistoryLog
import book_app


@pytest.fixture(autouse=True)
def isolate_files(tmp_path, monkeypatch):
    """Isolate DATA_FILE and HISTORY_FILE to tmp_path for every test."""
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    history_file = tmp_path / "history.json"
    monkeypatch.setattr(history_module.HistoryLog, "HISTORY_FILE", str(history_file))

    # Reset the global collection so it reads from the new DATA_FILE
    monkeypatch.setattr(book_app, "collection", books.BookCollection())


# ---------------------------------------------------------------------------
# history tests
# ---------------------------------------------------------------------------

def test_history_empty(capsys):
    book_app.handle_history([])
    out = capsys.readouterr().out
    assert "no history" in out.lower() or "empty" in out.lower()


def test_history_shows_events(capsys):
    HistoryLog().record("added", "1984")
    book_app.handle_history([])
    out = capsys.readouterr().out
    assert "added" in out.lower()
    assert "1984" in out


def test_history_filter_by_event(capsys):
    log = HistoryLog()
    log.record("added", "1984")
    log.record("removed", "Dune")
    book_app.handle_history(["--filter", "added"])
    out = capsys.readouterr().out
    assert "added" in out.lower()
    assert "1984" in out
    assert "removed" not in out.lower()


def test_history_filter_by_book(capsys):
    log = HistoryLog()
    log.record("added", "1984")
    log.record("added", "Dune")
    book_app.handle_history(["--book", "1984"])
    out = capsys.readouterr().out
    assert "1984" in out
    assert "Dune" not in out


def test_history_export_csv(tmp_path, monkeypatch):
    export_file = tmp_path / "history_export.csv"
    log = HistoryLog()
    log.record("added", "1984")

    import history_export

    def _export(events, filepath="history_export.csv"):
        history_export.export_to_csv(events, str(export_file))

    monkeypatch.setattr(book_app, "export_to_csv", _export)
    book_app.handle_history(["--export", "csv"])
    assert export_file.exists()
    content = export_file.read_text()
    assert "1984" in content


def test_history_clear_confirmed(monkeypatch, capsys):
    log = HistoryLog()
    log.record("added", "1984")
    assert len(log.load()) == 1

    monkeypatch.setattr("builtins.input", lambda _: "y")
    book_app.handle_history(["clear"])

    assert HistoryLog().load() == []


def test_history_clear_cancelled(monkeypatch):
    log = HistoryLog()
    log.record("added", "1984")

    monkeypatch.setattr("builtins.input", lambda _: "n")
    book_app.handle_history(["clear"])

    assert len(HistoryLog().load()) == 1


# ---------------------------------------------------------------------------
# edit command test
# ---------------------------------------------------------------------------

def test_edit_command(monkeypatch, capsys):
    # Seed the collection with a book to edit
    book_app.collection.add_book("1984", "George Orwell", 1949)

    inputs = iter(["1984", "Eric Arthur Blair", "", ""])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(sys, "argv", ["book_app.py", "edit"])

    book_app.main()

    updated = book_app.collection.find_book_by_title("1984")
    assert updated is not None
    assert updated.author == "Eric Arthur Blair"
