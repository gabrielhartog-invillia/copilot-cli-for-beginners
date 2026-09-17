import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()


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


def handle_add(args=None):
    print("\nAdd a New Book\n")

    if args and len(args) >= 2:
        title = args[0].strip()
        author = args[1].strip()
        year_str = args[2].strip() if len(args) >= 3 else ""
    else:
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        year_str = input("Year: ").strip()

    try:
        if not year_str:
            raise ValueError("Year cannot be empty")
        try:
            year = int(year_str)
        except ValueError:
            raise ValueError("Year must be a valid integer")

        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove(args=None):
    print("\nRemove a Book\n")

    if args and len(args) >= 1:
        title = args[0].strip()
    else:
        title = input("Enter the title of the book to remove: ").strip()

    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find(args=None):
    print("\nFind Books by Author\n")

    if args and len(args) >= 1:
        author = args[0].strip()
    else:
        author = input("Author name: ").strip()

    books = collection.find_by_author(author)

    show_books(books)


def handle_read(args: list[str] | None = None) -> None:
    print("\nMark a Book as Read\n")

    if args and len(args) >= 1:
        title = args[0].strip()
    else:
        title = input("Enter the title of the book to mark as read: ").strip()

    if collection.mark_as_read(title):
        print(f"\nBook '{title}' marked as read.\n")
    else:
        print(f"\nNo book found with title '{title}'.\n")


def show_help():
    print("""
Book Collection Helper

Commands:
  list                          - Show all books
  add [title] [author] [year]   - Add a new book (prompts if omitted)
  remove [title]                - Remove a book by title (prompts if omitted)
  find [author]                 - Find books by author (prompts if omitted)
  read [title]                  - Mark a book as read (prompts if omitted)
  help                          - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add(args)
    elif command == "remove":
        handle_remove(args)
    elif command == "find":
        handle_find(args)
    elif command == "read":
        handle_read(args)
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
