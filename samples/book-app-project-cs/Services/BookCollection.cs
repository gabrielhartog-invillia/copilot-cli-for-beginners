using System.Text.Json;
using BookApp.Models;

namespace BookApp.Services;

public class BookCollection
{
    private static readonly char[] ForbiddenInputChars = [';', '|', '&', '`', '$', '>', '<', '\n', '\r'];
    private readonly string _dataFile;
    private List<Book> _books = [];

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true
    };

    public BookCollection(string? dataFile = null)
    {
        _dataFile = dataFile ?? Path.Combine(AppContext.BaseDirectory, "data.json");
        LoadBooks();
    }

    public IReadOnlyList<Book> Books => _books;

    private void LoadBooks()
    {
        try
        {
            var json = File.ReadAllText(_dataFile);
            _books = JsonSerializer.Deserialize<List<Book>>(json, JsonOptions) ?? [];
        }
        catch (FileNotFoundException)
        {
            _books = [];
        }
        catch (JsonException)
        {
            Console.WriteLine("Warning: data.json is corrupted. Starting with empty collection.");
            _books = [];
        }
    }

    private void SaveBooks()
    {
        var json = JsonSerializer.Serialize(_books, JsonOptions);
        File.WriteAllText(_dataFile, json);
    }

    private static string ValidateTextInput(string value, string fieldName)
    {
        var cleanedValue = value.Trim();
        if (cleanedValue.Length > 200)
        {
            throw new ArgumentException($"{fieldName} is too long.", fieldName);
        }

        if (cleanedValue.IndexOfAny(ForbiddenInputChars) >= 0)
        {
            throw new ArgumentException($"{fieldName} contains forbidden characters.", fieldName);
        }

        return cleanedValue;
    }

    private static int ValidateYear(int year)
    {
        if (year < 0 || year > 9999)
        {
            throw new ArgumentOutOfRangeException(nameof(year), "Year must be between 0 and 9999.");
        }

        return year;
    }

    public Book AddBook(string title, string author, int year)
    {
        var book = new Book
        {
            Title = ValidateTextInput(title, nameof(title)),
            Author = ValidateTextInput(author, nameof(author)),
            Year = ValidateYear(year)
        };
        _books.Add(book);
        SaveBooks();
        return book;
    }

    public List<Book> ListBooks() => _books;

    public Book? FindBookByTitle(string title)
    {
        var safeTitle = ValidateTextInput(title, nameof(title));
        return _books.Find(b => b.Title.Equals(safeTitle, StringComparison.OrdinalIgnoreCase));
    }

    public bool MarkAsRead(string title)
    {
        var book = FindBookByTitle(title);
        if (book is null) return false;
        book.Read = true;
        SaveBooks();
        return true;
    }

    public bool RemoveBook(string title)
    {
        var safeTitle = ValidateTextInput(title, nameof(title));
        var book = FindBookByTitle(safeTitle);
        if (book is null) return false;
        _books.Remove(book);
        SaveBooks();
        return true;
    }

    public List<Book> FindByAuthor(string author)
    {
        var safeAuthor = ValidateTextInput(author, nameof(author));
        return _books
            .Where(b => b.Author.Equals(safeAuthor, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }
}
