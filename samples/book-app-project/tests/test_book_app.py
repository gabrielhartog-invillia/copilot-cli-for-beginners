import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app


def test_handle_remove_shows_success_message(monkeypatch, capsys) -> None:
    class StubCollection:
        def remove_book(self, title: str) -> bool:
            return title == "The Hobbit"

    monkeypatch.setattr(book_app, "collection", StubCollection())
    monkeypatch.setattr("builtins.input", lambda _prompt: "The Hobbit")

    book_app.handle_remove()

    captured = capsys.readouterr()
    assert "Book 'The Hobbit' removed." in captured.out


def test_handle_remove_shows_missing_book_message(monkeypatch, capsys) -> None:
    class StubCollection:
        def remove_book(self, title: str) -> bool:
            return False

    monkeypatch.setattr(book_app, "collection", StubCollection())
    monkeypatch.setattr("builtins.input", lambda _prompt: "Unknown Book")

    book_app.handle_remove()

    captured = capsys.readouterr()
    assert "No book found with title 'Unknown Book'." in captured.out
