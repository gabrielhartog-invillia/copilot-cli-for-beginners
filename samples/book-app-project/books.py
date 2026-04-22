import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"
FORBIDDEN_INPUT_CHARS = {";", "|", "&", "`", "$", ">", "<", "\n", "\r"}


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    @staticmethod
    def _validate_text_input(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")

        cleaned_value = value.strip()
        if len(cleaned_value) > 200:
            raise ValueError(f"{field_name} is too long.")
        if any(char in FORBIDDEN_INPUT_CHARS for char in cleaned_value):
            raise ValueError(f"{field_name} contains forbidden characters.")

        return cleaned_value

    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if year < 0 or year > 9999:
            raise ValueError("Year must be between 0 and 9999.")
        return year

    def add_book(self, title: str, author: str, year: int) -> Book:
        title = self._validate_text_input(title, "Title")
        author = self._validate_text_input(author, "Author")
        year = self._validate_year(year)
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        title = self._validate_text_input(title, "Title")
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        title = self._validate_text_input(title, "Title")
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        author = self._validate_text_input(author, "Author")
        return [b for b in self.books if b.author.lower() == author.lower()]
