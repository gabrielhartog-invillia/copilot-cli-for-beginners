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


def test_find_by_author_exact_match():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("George Orwell")
    assert len(results) == 1
    assert results[0].title == "1984"


def test_find_by_author_partial_last_name():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("Orwell")
    assert len(results) == 1
    assert results[0].title == "1984"


def test_find_by_author_partial_case_insensitive():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("orwell")
    assert len(results) == 1
    assert results[0].title == "1984"


def test_find_by_author_no_match():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("Tolkien")
    assert results == []


def test_find_by_author_multiple_results():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Dune", "Frank Herbert", 1965)
    results = collection.find_by_author("Orwell")
    assert len(results) == 2
