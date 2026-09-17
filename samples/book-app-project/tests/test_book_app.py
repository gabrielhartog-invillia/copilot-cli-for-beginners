import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


def test_read_command_marks_book_as_read(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(book_app, "collection", collection)

    monkeypatch.setattr(sys, "argv", ["book_app.py", "read", "Dune"])
    book_app.main()

    output = capsys.readouterr().out
    assert "Book 'Dune' marked as read." in output
    assert collection.find_book_by_title("Dune").read is True


def test_read_command_reports_missing_book(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "data.json"))
    monkeypatch.setattr(book_app, "collection", BookCollection())

    monkeypatch.setattr(sys, "argv", ["book_app.py", "read", "Missing Book"])
    book_app.main()

    output = capsys.readouterr().out
    assert "No book found with title 'Missing Book'." in output
