import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    MAX_FIELD_LENGTH = 200

    @staticmethod
    def _validate_text_field(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{field_name} cannot be empty.")
        if len(cleaned) > BookCollection.MAX_FIELD_LENGTH:
            raise ValueError(f"{field_name} must be {BookCollection.MAX_FIELD_LENGTH} characters or fewer.")
        if any(ord(char) < 32 for char in cleaned):
            raise ValueError(f"{field_name} contains invalid characters.")
        return cleaned

    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        current_year = datetime.now().year
        if year < 1 or year > current_year:
            raise ValueError(f"Year must be between 1 and {current_year}.")
        return year

    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print("Warning: data.json must contain a JSON array. Starting with empty collection.")
                    self.books = []
                    return

                validated_books = []
                for index, raw_book in enumerate(data, start=1):
                    try:
                        if not isinstance(raw_book, dict):
                            raise TypeError
                        validated_books.append(
                            Book(
                                title=self._validate_text_field(raw_book["title"], "Title"),
                                author=self._validate_text_field(raw_book["author"], "Author"),
                                year=self._validate_year(raw_book["year"]),
                                read=bool(raw_book.get("read", False)),
                            )
                        )
                    except (TypeError, KeyError, ValueError):
                        print(f"Warning: Skipping invalid book entry #{index} in data.json.")
                self.books = validated_books
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        validated_title = self._validate_text_field(title, "Title")
        validated_author = self._validate_text_field(author, "Author")
        validated_year = self._validate_year(year)
        book = Book(title=validated_title, author=validated_author, year=validated_year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
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
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
