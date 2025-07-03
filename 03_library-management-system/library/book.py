from typing import Optional

class Book:
    """
    Represents a book in the library.
    """
    def __init__(self, title: str, author: str, book_id: Optional[int] = None, is_available: bool = True) -> None:
        """
        Initializes the Book object.
        """
        self.title: str = title
        self.author: str = author
        self.book_id: Optional[int] = book_id
        self.is_available: bool = is_available

    def mark_as_borrowed(self) -> None:
        """
        Marks the book as borrowed if it's available.
        """
        if self.is_available:
            self.is_available = False
        else:
            raise ValueError('Book is already borrowed.')

    def mark_as_returned(self) -> None:
        """
        Marks the book as returned if it was borrowed.
        """
        if self.is_available:
            raise ValueError('Book is already available.')
        else:
            self.is_available = True

    def __str__(self) -> str:
        """
        String representation of the book.
        """
        return f'{self.title} by {self.author}' 