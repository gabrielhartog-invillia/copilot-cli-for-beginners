import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()
COMMAND_HANDLERS = {
    "list": lambda: handle_list(),
    "add": lambda: handle_add(),
    "remove": lambda: handle_remove(),
    "find": lambda: handle_find(),
    "help": lambda: show_help(),
}


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    try:
        title = input("Enter the title of the book to remove: ").strip()
        collection.remove_book(title)
        print("\nBook removed if it existed.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_find():
    print("\nFind Books by Author\n")

    try:
        author = input("Author name: ").strip()
        books = collection.find_by_author(author)
        show_books(books)
    except ValueError as e:
        print(f"\nError: {e}\n")


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].strip().lower()
    handler = COMMAND_HANDLERS.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
