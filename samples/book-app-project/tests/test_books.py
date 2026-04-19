import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_add_book_rejects_suspicious_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="invalid characters"):
        collection.add_book("1984; rm -rf /", "George Orwell", 1949)


def test_add_book_rejects_empty_author():
    collection = BookCollection()

    with pytest.raises(ValueError, match="cannot be empty"):
        collection.add_book("1984", "   ", 1949)


def test_find_by_author_rejects_suspicious_input():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.find_by_author("Frank Herbert; ls") == []
    assert [book.title for book in collection.find_by_author("Frank Herbert")] == ["Dune"]


def test_find_book_by_title_rejects_suspicious_input():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    assert collection.find_book_by_title("1984; cat /etc/passwd") is None
    assert collection.find_book_by_title("1984").title == "1984"
