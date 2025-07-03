import os
import pytest
from library.library import Library

@pytest.fixture
def lib():
    l = Library()
    l.add_book("1984", "George Orwell")
    l.add_book("Brave New World", "Aldous Huxley")
    l.register_member("Alice")
    l.register_member("Bob")
    return l

def test_add_and_search_books(lib):
    assert len(lib.books) == 2
    assert lib.find_book_id("1984") == [0]
    assert lib.search_books_by_author("George Orwell") == ["1984 by George Orwell"]

def test_register_and_find_members(lib):
    assert len(lib.members) == 2
    assert lib.find_member_id("Alice") == [0]

def test_borrow_and_return(lib):
    lib.borrow_book(0, 0)
    assert not lib.get_book_by_id(0).is_available
    assert len(lib.get_member_by_id(0).borrowed_books) == 1
    lib.return_book(0, 0)
    assert lib.get_book_by_id(0).is_available
    assert len(lib.get_member_by_id(0).borrowed_books) == 0

def test_persistence(tmp_path, lib):
    file_path = tmp_path / "lib.json"
    lib.borrow_book(0, 0)
    lib.save_to_file(str(file_path))
    loaded = Library.load_from_file(str(file_path))
    assert len(loaded.books) == 2
    assert not loaded.get_book_by_id(0).is_available
    assert loaded.get_member_by_id(0).borrowed_books[0].title == "1984"
    # Clean up
    if os.path.exists(file_path):
        os.remove(file_path) 