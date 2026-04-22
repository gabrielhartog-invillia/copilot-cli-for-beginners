const fs = require("fs");
const path = require("path");

const DATA_FILE = path.join(__dirname, "data.json");
const FORBIDDEN_INPUT_CHARS = /[;|&`$><\n\r]/;

class Book {
  constructor(title, author, year, read = false) {
    this.title = title;
    this.author = author;
    this.year = year;
    this.read = read;
  }
}

class BookCollection {
  constructor(dataFile) {
    this.dataFile = dataFile || DATA_FILE;
    this.books = [];
    this.loadBooks();
  }

  loadBooks() {
    try {
      const raw = fs.readFileSync(this.dataFile, "utf-8");
      const data = JSON.parse(raw);
      this.books = data.map((b) => new Book(b.title, b.author, b.year, b.read));
    } catch (err) {
      if (err.code === "ENOENT") {
        this.books = [];
      } else if (err instanceof SyntaxError) {
        console.log("Warning: data.json is corrupted. Starting with empty collection.");
        this.books = [];
      } else {
        throw err;
      }
    }
  }

  saveBooks() {
    const data = this.books.map((b) => ({
      title: b.title,
      author: b.author,
      year: b.year,
      read: b.read,
    }));
    fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
  }

  static validateTextInput(value, fieldName) {
    if (typeof value !== "string") {
      throw new Error(`${fieldName} must be a string.`);
    }

    const cleanedValue = value.trim();
    if (cleanedValue.length > 200) {
      throw new Error(`${fieldName} is too long.`);
    }
    if (FORBIDDEN_INPUT_CHARS.test(cleanedValue)) {
      throw new Error(`${fieldName} contains forbidden characters.`);
    }

    return cleanedValue;
  }

  static validateYear(year) {
    if (!Number.isInteger(year)) {
      throw new Error("Year must be an integer.");
    }
    if (year < 0 || year > 9999) {
      throw new Error("Year must be between 0 and 9999.");
    }
    return year;
  }

  addBook(title, author, year) {
    const safeTitle = BookCollection.validateTextInput(title, "Title");
    const safeAuthor = BookCollection.validateTextInput(author, "Author");
    const safeYear = BookCollection.validateYear(year);
    const book = new Book(safeTitle, safeAuthor, safeYear);
    this.books.push(book);
    this.saveBooks();
    return book;
  }

  listBooks() {
    return this.books;
  }

  findBookByTitle(title) {
    const safeTitle = BookCollection.validateTextInput(title, "Title");
    return this.books.find((b) => b.title.toLowerCase() === safeTitle.toLowerCase()) || null;
  }

  markAsRead(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      book.read = true;
      this.saveBooks();
      return true;
    }
    return false;
  }

  removeBook(title) {
    const book = this.findBookByTitle(title);
    if (book) {
      this.books = this.books.filter((b) => b !== book);
      this.saveBooks();
      return true;
    }
    return false;
  }

  findByAuthor(author) {
    const safeAuthor = BookCollection.validateTextInput(author, "Author");
    return this.books.filter((b) => b.author.toLowerCase() === safeAuthor.toLowerCase());
  }
}

module.exports = { Book, BookCollection, DATA_FILE };
