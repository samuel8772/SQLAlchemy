# 📚 Articles Database (Python + SQL)

This project models a simple publishing system using Python classes and SQLite for database storage. It includes object relationships and basic ORM-style methods to manage data about authors, books, and publications.

## 📦 Project Structure

```
code-challenge/
├── lib/
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       ├── author.py
│       ├── book.py
│       └── publication.py
├── tests/
│   ├── test_author.py
│   ├── test_book.py
│   └── test_publication.py
├── README.md
└── requirements.txt
```

## 🧠 Features

- Create and manage **Authors** with book relationships
- Add **Books** linked to Authors and Publications
- Define **Publications** with metadata like founding year, genre, and city
- Run unit tests with `pytest` to verify behavior
- Handles basic validations (e.g., author name must be a string)

## 🛠️ Technologies

- Python 3.8+
- SQLite (optional if persistence is added)
- `pytest` for testing

## 🧪 Running Tests

Make sure you're in the project root directory:

```bash
# Set Python path and run tests
PYTHONPATH=. pytest
```

## ✅ Example Usage

```python
from lib.models.author import Author
from lib.models.book import Book
from lib.models.publication import Publication

author = Author("George Orwell")
pub = Publication("Penguin Books", 1935, "Fiction", "London")

book = Book("1984", author, pub, 328)
author.add_book(book)

print(author.books())         # [<Book title=1984>]
print(author)                 # <Author name=George Orwell>
print(pub)                    # <Publication name=Penguin Books>
```

## 💡 Learning Objectives

This project demonstrates your ability to:

- Design object relationships in Python
- Implement encapsulation and data validation
- Write clear `__repr__` methods for debugging
- Use test-driven development with `pytest`

## 👨‍💻 Author

**Samuel Kamau Karobia**  
Email: [kamauskk005@gmail.com](mailto:kamauskk005@gmail.com)

---

Happy coding! 🚀
