import sys
from books import BookCollection
from history import HistoryLog
from history_export import export_to_csv


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

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_edit():
    print("\nEdit a Book\n")
    title = input("Title of the book to edit: ").strip()
    print("Leave blank to keep current value.")
    author = input("New author: ").strip()
    year_str = input("New year: ").strip()

    fields = {}
    if author:
        fields["author"] = author
    if year_str:
        try:
            fields["year"] = int(year_str)
        except ValueError:
            print("Invalid year. Skipping.")

    if not fields:
        print("No changes provided.")
        return

    result = collection.edit_book(title, **fields)
    if result:
        print("\nBook updated successfully.\n")
    else:
        print("\nBook not found.\n")


def handle_history(args):
    history = HistoryLog()

    if args and args[0] == "clear":
        confirm = input("Are you sure you want to clear history? [y/N] ").strip().lower()
        if confirm == "y":
            history.clear()
            print("History cleared.")
        else:
            print("Cancelled.")
        return

    filter_type = None
    filter_book = None
    export_format = None

    i = 0
    while i < len(args):
        if args[i] == "--filter" and i + 1 < len(args):
            filter_type = args[i + 1]
            i += 2
        elif args[i] == "--book" and i + 1 < len(args):
            filter_book = args[i + 1]
            i += 2
        elif args[i] == "--export" and i + 1 < len(args):
            export_format = args[i + 1]
            i += 2
        else:
            i += 1

    events = history.load()

    if filter_type:
        events = [e for e in events if e.get("event") == filter_type]
    if filter_book:
        events = [e for e in events if e.get("title", "").lower() == filter_book.lower()]

    if export_format == "csv":
        export_to_csv(events, "history_export.csv")
        print("History exported to history_export.csv")
        return

    if not events:
        print("No history found.")
        return

    print("\nHistory:\n")
    for e in events:
        changes_str = ""
        if e.get("changes"):
            parts = [f"{k}: \"{v['before']}\" → \"{v['after']}\"" for k, v in e["changes"].items()]
            changes_str = " — " + ", ".join(parts)
        print(f"[{e['timestamp']}] {e['event']}: \"{e['title']}\"{changes_str}")
    print()


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  edit     - Edit a book's details
  history  - Show history of changes
             --filter added|edited|deleted
             --book "Title"
             --export csv
             clear  (clears the history log)
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "edit":
        handle_edit()
    elif command == "history":
        handle_history(sys.argv[2:])
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
