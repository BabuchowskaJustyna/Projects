from typing import Optional, List, Tuple
from datetime import datetime
from .book import Book

class Member:
    """
    Represents a library member.
    """
    def __init__(self, name: str, member_id: Optional[int] = None) -> None:
        """
        Initializes the Member object.
        """
        self.name: str = name
        self.member_id: Optional[int] = member_id
        self.borrowed_books: List[Book] = []
        self.loan_history: List[Tuple[int, str, str]] = []  # (book_id, action, timestamp)

    def borrow_book(self, book: Book) -> None:
        """
        Borrows a book if available, otherwise raises ValueError.
        """
        if isinstance(book, Book) and book.is_available:
            book.mark_as_borrowed()
            self.borrowed_books.append(book)
            self.loan_history.append((book.book_id, 'borrowed', datetime.now().isoformat()))
        else:
            raise ValueError('Book is not available.')

    def return_book(self, book: Book) -> None:
        """
        Returns a borrowed book.
        """
        if isinstance(book, Book) and not book.is_available:
            book.mark_as_returned()
            self.borrowed_books.remove(book)
            self.loan_history.append((book.book_id, 'returned', datetime.now().isoformat()))
        else:
            raise ValueError('This book is not marked as borrowed.')

    def set_id(self, new_id: int) -> None:
        """
        Sets the member ID.
        """
        if self.member_id is not None:
            raise ValueError('Member has id.')
        else:
            self.member_id = new_id

    def __str__(self) -> str:
        """
        String representation of the member.
        """
        return f'{self.name} [ID: {self.member_id}] Borrowed books: {len(self.borrowed_books)}\n' 