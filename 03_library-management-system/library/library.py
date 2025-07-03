import json
from typing import List, Iterator, Optional
from .book import Book
from .member import Member

class Library:
    """
    Represents the library.
    """
    def __init__(self) -> None:
        """
        Initializes the library with empty lists of books and members.
        """
        self.books: List[Book] = []
        self.members: List[Member] = []
        self.id_counter_book: int = 0
        self.id_counter_member: int = 0

    def get_book_by_id(self, book_id: int) -> Book:
        """
        Retrieves a book by its ID, otherwise raises ValueError.
        """
        find_book = list(filter(lambda book: book.book_id == book_id, self.books))
        if find_book:
            return find_book[0]
        else:
            raise ValueError('Book not found.')

    def get_member_by_id(self, member_id: int) -> Member:
        """
        Retrieves a member by ID, otherwise raises ValueError.
        """
        find_member = list(filter(lambda member: member.member_id == member_id, self.members))
        if find_member:
            return find_member[0]
        else:
            raise ValueError('Member not found.')

    def add_book(self, title: str, author: str) -> None:
        """
        Adds a new book to the library and assigns a unique ID.
        """
        book_id = self.id_counter_book
        new_book = Book(title, author, book_id)
        self.books.append(new_book)
        self.id_counter_book += 1

    def remove_book(self, book_id: int) -> None:
        """
        Removes a book if it's not borrowed. Raises ValueError if borrowed.
        """
        book_to_remove: Book = self.get_book_by_id(book_id)
        if book_to_remove.is_available:
            self.books.remove(book_to_remove)
        else:
            raise ValueError('Cannot remove a borrowed book.')

    def register_member(self, name: str) -> None:
        """
        Registers a new library member and assigns a unique ID.
        """
        member_id = self.id_counter_member
        new_member = Member(name, member_id)
        self.members.append(new_member)
        self.id_counter_member += 1

    def deregister_member(self, member_id: int) -> None:
        """
        Deregisters a member if they have no borrowed books. Raises ValueError otherwise.
        """
        member_to_check: Member = self.get_member_by_id(member_id)
        if len(member_to_check.borrowed_books) == 0:
            self.members.remove(member_to_check)
        else:
            raise ValueError('Cannot deregister a member who still has borrowed books.')

    def borrow_book(self, member_id: int, book_id: int) -> None:
        """
        Lets a member borrow a book. Raises ValueError if unavailable or invalid ID.
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
        """
        try:
            member: Member = self.get_member_by_id(member_id)
            book: Book = self.get_book_by_id(book_id)
            if member and book:
                member.return_book(book)
        except ValueError:
            raise ValueError('Member does not have this book.')

    def list_available_books(self) -> List[str]:
        """
        Lists all available books in the library.
        """
        return [str(book) for book in self.books if book.is_available]

    def search_books_by_author(self, author: str) -> List[str]:
        """
        Returns a list of books by the given author.
        """
        return [str(book) for book in self.books if book.author == author]

    def find_member_id(self, name: str) -> List[Optional[int]]:
        """
        Finds all member IDs matching a given name.
        """
        members_search: Iterator[Member] = filter(lambda member: member.name == name, self.members)
        members_id: List[Optional[int]] = list(map(lambda members: members.member_id, members_search))
        return members_id

    def find_book_id(self, title: str) -> List[Optional[int]]:
        """
        Finds all book IDs matching a given title.
        """
        books_search: Iterator[Book] = filter(lambda book: book.title == title, self.books)
        books_id: List[Optional[int]] = list(map(lambda books: books.book_id, books_search))
        return books_id

    def save_to_file(self, path: str) -> None:
        """
        Saves the library state to a JSON file.
        """
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "book_id": book.book_id,
                    "is_available": book.is_available
                } for book in self.books
            ],
            "members": [
                {
                    "name": member.name,
                    "member_id": member.member_id,
                    "borrowed_books": [book.book_id for book in member.borrowed_books],
                    "loan_history": member.loan_history
                } for member in self.members
            ],
            "id_counter_book": self.id_counter_book,
            "id_counter_member": self.id_counter_member
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "Library":
        """
        Loads the library state from a JSON file.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        lib = cls()
        lib.id_counter_book = data.get("id_counter_book", 0)
        lib.id_counter_member = data.get("id_counter_member", 0)
        # Recreate books
        id_to_book = {}
        for book_data in data["books"]:
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                book_id=book_data["book_id"],
                is_available=book_data["is_available"]
            )
            lib.books.append(book)
            id_to_book[book.book_id] = book
        # Recreate members
        for member_data in data["members"]:
            member = Member(
                name=member_data["name"],
                member_id=member_data["member_id"]
            )
            # Assign borrowed books
            for book_id in member_data["borrowed_books"]:
                if book_id in id_to_book:
                    member.borrowed_books.append(id_to_book[book_id])
            # Assign loan history
            member.loan_history = member_data.get("loan_history", [])
            lib.members.append(member)
        return lib

    def __str__(self) -> str:
        """
        String representation of the library.
        """
        title = self.__class__.__name__
        books_repr = '\n'.join([
            f'- {str(book)} (ID: {book.book_id}) {"Available" if book.is_available else "Borrowed"}'
            for book in self.books
        ])
        members_repr = ''.join([f'- {str(member)}\n' for member in self.members]) or '---'
        return f'{title}\nbooks: {len(self.books)}\n{books_repr}\nmembers: {len(self.members)}\n{members_repr}'.strip() 