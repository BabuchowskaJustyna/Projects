from typing import Iterator


class Book:
    """
    Represents a book in the library.

    >>> b = Book("1984", "George Orwell")
    >>> b.title
    '1984'
    >>> b.is_available
    True
    """

    def __init__(self, title: str, author: str, book_id: int | None = None, is_available: bool = True) -> None:
        """
        Initializes the Book object.

        >>> b = Book("1984", "George Orwell")
        >>> b.book_id is None
        True
        >>> b.is_available
        True
        """
        self.title = title
        self.author = author
        self.book_id = book_id
        self.is_available = is_available

    def mark_as_borrowed(self):
        """
        Marks the book as borrowed if it's not available.

        >>> b = Book("1984", "George Orwell")
        >>> b.mark_as_borrowed()
        >>> b.is_available
        False
        >>> b.mark_as_borrowed()
        Traceback (most recent call last):
        ...
        ValueError: Book is already borrowed.
        """
        if self.is_available:
            self.is_available = False
        else:
            raise ValueError('Book is already borrowed.')

    def mark_as_returned(self):
        """
        Marks the book as returned if it was borrowed.

        >>> b = Book("1984", "George Orwell")
        >>> b.mark_as_borrowed()
        >>> b.mark_as_returned()
        >>> b.is_available
        True
        >>> b.mark_as_returned()
        Traceback (most recent call last):
        ...
        ValueError: Book is already available.
        """
        if self.is_available:
            raise ValueError('Book is already available.')
        else:
            self.is_available = True

    def __str__(self) -> str:
        """
        String representation of the book.

        >>> b = Book("Animal Farm", "George Orwell")
        >>> str(b)
        'Animal Farm by George Orwell'
        """
        return f'{self.title} by {self.author}'


class Member:
    """
    Represents a library member.

    >>> m = Member("Alice", 0)
    >>> m.name
    'Alice'
    >>> m.borrowed_books
    []
    """

    def __init__(self, name: str, member_id: int | None = None) -> None:
        """
        Initializes the Member object.

        >>> m = Member("Alice", 1)
        >>> m.member_id
        1
        >>> m.borrowed_books
        []
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books: list[Book] = []

    def borrow_book(self, book: Book) -> None:
        """
        Borrows a book if available, otherwise raises ValueError.

        >>> b = Book("1984", "George Orwell")
        >>> m = Member("Bob")
        >>> m.borrow_book(b)
        >>> b.is_available
        False
        >>> len(m.borrowed_books)
        1
        >>> m.borrow_book(b)  # Book already borrowed
        Traceback (most recent call last):
        ...
        ValueError: Book is not available.
        """
        if isinstance(book, Book) and book.is_available:
            book.mark_as_borrowed()
            self.borrowed_books.append(book)
        else:
            raise ValueError('Book is not available.')

    def return_book(self, book: Book) -> None:
        """
        Returns a borrowed book.

        >>> b = Book("1984", "George Orwell")
        >>> m = Member("Bob")
        >>> m.borrow_book(b)
        >>> m.return_book(b)
        >>> b.is_available
        True
        >>> m.return_book(b)
        Traceback (most recent call last):
        ...
        ValueError: This book is not marked as borrowed.
        """
        if isinstance(book, Book) and not book.is_available:
            book.mark_as_returned()
            self.borrowed_books.remove(book)
        else:
            raise ValueError('This book is not marked as borrowed.')

    def set_id(self, new_id: int) -> None:
        """
        Sets the member ID.

        >>> m = Member("Charlie")
        >>> m.set_id(5)
        >>> m.member_id
        5
        >>> m.set_id(6)
        Traceback (most recent call last):
        ...
        ValueError: Member has id.
        """
        if self.member_id:
            raise ValueError('Member has id.')
        else:
            self.member_id = new_id

    def __str__(self) -> str:
        """
        String representation of the member.

        >>> m = Member("Diane", 1)
        >>> str(m).split('\\n')[0]
        'Diane [ID: 1] Borrowed books: 0'
        """
        return f'{self.name} [ID: {self.member_id}] Borrowed books: {len(self.borrowed_books)}\n'


class Library:
    """
    Represents the library.

    >>> lib = Library()
    >>> len(lib.books)
    0
    >>> len(lib.members)
    0
    """

    def __init__(self) -> None:
        """
        Initializes the library with empty lists of books and members.
        """
        self.books: list[Book] = []
        self.members: list[Member] = []
        self.id_counter_book = 0
        self.id_counter_member = 0

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Retrieves a book by its ID, otherwise raises ValueError.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> b = lib.get_book_by_id(0)
        >>> b.title
        '1984'
        >>> lib.get_book_by_id(999)
        Traceback (most recent call last):
        ...
        ValueError: Book not found.
        """
        find_book = list(filter(lambda book: book.book_id == book_id, self.books))
        if find_book:
            return find_book[0]
        else:
            raise ValueError('Book not found.')

    def get_member_by_id(self, member_id: int) -> Member:
        """
        Retrieves a member by ID, otherwise raises ValueError.

        >>> lib = Library()
        >>> lib.register_member("Alice")
        >>> m = lib.get_member_by_id(0)
        >>> m.name
        'Alice'
        >>> lib.get_member_by_id(999)
        Traceback (most recent call last):
        ...
        ValueError: Member not found.
        """
        find_member = list(filter(lambda member: member.member_id == member_id, self.members))
        if find_member:
            return find_member[0]
        else:
            raise ValueError('Member not found.')

    def add_book(self, title: str, author: str) -> None:
        """
        Adds a new book to the library and assigns a unique ID.

        >>> lib = Library()
        >>> lib.add_book("Brave New World", "Aldous Huxley")
        >>> lib.books[0].title
        'Brave New World'
        """
        book_id = self.id_counter_book
        new_book = Book(title, author, book_id)
        self.books.append(new_book)
        self.id_counter_book += 1

    def remove_book(self, book_id: int) -> None:
        """
        Removes a book if it's not borrowed. Raises ValueError if borrowed.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.remove_book(0)
        >>> len(lib.books)
        0
        >>> lib.add_book("To Kill a Mockingbird", "Harper Lee")
        >>> lib.register_member("Sam")
        >>> lib.borrow_book(0, 1)
        >>> lib.remove_book(1)
        Traceback (most recent call last):
        ...
        ValueError: Cannot remove a borrowed book.
        """
        book_to_remove: Book = self.get_book_by_id(book_id)
        if book_to_remove.is_available:
            self.books.remove(book_to_remove)
        else:
            raise ValueError('Cannot remove a borrowed book.')

    def register_member(self, name: str) -> None:
        """
        Registers a new library member and assigns a unique ID.

        >>> lib = Library()
        >>> lib.register_member("Zed")
        >>> lib.members[0].name
        'Zed'
        """
        member_id = self.id_counter_member
        new_member = Member(name, member_id)
        self.members.append(new_member)
        self.id_counter_member += 1

    def deregister_member(self, member_id: int) -> None:
        """
        Deregisters a member if they have no borrowed books. Raises ValueError otherwise.

        >>> lib = Library()
        >>> lib.register_member("Zed")
        >>> lib.deregister_member(member_id=0)
        >>> len(lib.members)
        0
        >>> lib.register_member("Kelly")
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.borrow_book(book_id=0, member_id=1)
        >>> lib.deregister_member(1)
        Traceback (most recent call last):
        ...
        ValueError: Cannot deregister a member who still has borrowed books.
        """
        member_to_check: Member = self.get_member_by_id(member_id)
        if len(member_to_check.borrowed_books) == 0:
            self.members.remove(member_to_check)
        else:
            raise ValueError('Cannot deregister a member who still has borrowed books.')

    def borrow_book(self, member_id: int, book_id: int) -> None:
        """
        Lets a member borrow a book. Raises ValueError if unavailable or invalid ID.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.register_member("Alice")
        >>> lib.borrow_book(0, 0)
        >>> lib.borrow_book(0, 99)
        Traceback (most recent call last):
        ...
        ValueError: Book not found.
        """
        try:
            member: Member = self.get_member_by_id(member_id)
            book: Book = self.get_book_by_id(book_id)
            if member and book:
                member.borrow_book(book)
        except ValueError:
            raise ValueError('Book not found.')

    def return_book(self, member_id: int, book_id: int) -> None:
        """
        Lets a member return a borrowed book. Raises ValueError if the book isn't borrowed by that member.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.register_member("Alice")
        >>> lib.borrow_book(member_id=0, book_id=0)
        >>> lib.return_book(member_id=0, book_id=0)
        >>> len(lib.members[0].borrowed_books)
        0
        >>> lib.return_book(0, 0)
        Traceback (most recent call last):
        ...
        ValueError: Member does not have this book.
        """
        try:
            member: Member = self.get_member_by_id(member_id)
            book: Book = self.get_book_by_id(book_id)
            if member and book:
                member.return_book(book)
        except ValueError:
            raise ValueError('Member does not have this book.')

    def list_available_books(self) -> list[str | None]:
        """
        Lists all available books in the library.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.add_book("Brave New World", "Aldous Huxley")
        >>> lib.register_member("Alice")
        >>> lib.borrow_book(member_id=0, book_id=0)
        >>> lib.list_available_books()
        ['Brave New World by Aldous Huxley']
        """
        return [str(book) for book in self.books if book.is_available]

    def find_member_id(self, name: str) -> list[int | None]:
        """
        Finds all member IDs matching a given name.

        >>> lib = Library()
        >>> lib.register_member("Alice")
        >>> lib.register_member("Alice")
        >>> lib.find_member_id("Alice")
        [0, 1]
        >>> lib.find_member_id("Unknown")
        []
        """
        members_search: Iterator[Member] = filter(lambda member: member.name == name, self.members)
        members_id: list[int | None] = list(map(lambda members: members.member_id, members_search))
        return members_id

    def find_book_id(self, title: str) -> list[int | None]:
        """
        Finds all book IDs matching a given title.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.add_book("1984", "George Orwell")
        >>> lib.find_book_id("1984")
        [0, 1]
        >>> lib.find_book_id("NotHere")
        []
        """
        books_search: Iterator[Book] = filter(lambda book: book.title == title, self.books)
        books_id: list[int | None] = list(map(lambda books: books.book_id, books_search))
        return books_id

    def __str__(self) -> str:
        """
        String representation of the library.

        >>> lib = Library()
        >>> lib.add_book("1984", "George Orwell")
        >>> print(lib)
        Library
        books: 1
        - 1984 by George Orwell (ID: 0) Available
        members: 0
        ---
        >>> lib.register_member("Alice")
        >>> print(lib)
        Library
        books: 1
        - 1984 by George Orwell (ID: 0) Available
        members: 1
        - Alice [ID: 0] Borrowed books: 0
        >>> lib.borrow_book(member_id=0, book_id=0)
        >>> print(lib)
        Library
        books: 1
        - 1984 by George Orwell (ID: 0) Borrowed
        members: 1
        - Alice [ID: 0] Borrowed books: 1
        """
        title = self.__class__.__name__
        books_repr = '\n'.join([f'- {str(book)} (ID: {book.book_id}) {''.join(['Available' if book.is_available else 'Borrowed'])}' for book in self.books])
        members_repr = ''.join([f'- {str(member)}\n' for member in self.members]) or '---'
        return f'{title}\nbooks: {len(self.books)}\n{books_repr}\nmembers: {len(self.members)}\n{members_repr}'.strip()
