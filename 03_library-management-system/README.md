# Library Management System

A simple, modular library management system in Python. This project demonstrates object-oriented programming, modular code structure, type annotations, data persistence, and automated testing.

## Features
- Add, remove, and search for books
- Register and deregister library members
- Borrow and return books
- Search books by author
- Track loan history for each member
- Save and load library state to/from a JSON file
- Full type annotations
- Modular codebase
- Demo script showcasing all features
- Ready for automated testing

## Technologies
- Python 3.10+
- Standard library only (no external dependencies)
- Type annotations
- JSON for data persistence
- `pytest` for testing (see `tests/` directory)

## Usage
1. Clone the repository or copy the project files.
2. Run the demo script:
   ```bash
   python demo.py
   ```
   This will showcase adding books, registering members, borrowing/returning, searching, saving/loading, and printing loan history.

3. To use the library in your own scripts, import from the `library` package:
   ```python
   from library.library import Library
   ```

## Persistence
- The library state can be saved to and loaded from a JSON file using `save_to_file` and `load_from_file` methods.

## Tests
- Automated tests are located in the `tests/` directory.
- Run all tests with:
  ```bash
  pytest
  ```

## Project Structure
- `library/` - main package with modules: `book.py`, `member.py`, `library.py`
- `demo.py` - demo script
- `tests/` - automated tests (unit and integration)
- `README.md` - this file





