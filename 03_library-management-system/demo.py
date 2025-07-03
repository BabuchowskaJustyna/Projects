from library.library import Library

# Demo script for the Library Management System
if __name__ == "__main__":
    print("--- Library Management System Demo ---")
    lib = Library()

    # Add books
    lib.add_book("1984", "George Orwell")
    lib.add_book("Brave New World", "Aldous Huxley")
    lib.add_book("Animal Farm", "George Orwell")

    # Register members
    lib.register_member("Alice")
    lib.register_member("Bob")

    # Borrow and return books
    lib.borrow_book(0, 0)  # Alice borrows 1984
    lib.borrow_book(1, 1)  # Bob borrows Brave New World
    lib.return_book(0, 0)  # Alice returns 1984

    # Search by author
    print("\nBooks by George Orwell:")
    print(lib.search_books_by_author("George Orwell"))

    # List available books
    print("\nAvailable books:")
    print(lib.list_available_books())

    # Print library state
    print("\nCurrent library state:")
    print(lib)

    # Show loan history for Alice
    alice = lib.get_member_by_id(0)
    print("\nAlice's loan history:")
    for entry in alice.loan_history:
        print(entry)

    # Save and load library state
    lib.save_to_file("library_state.json")
    print("\nLibrary state saved to 'library_state.json'.")
    loaded_lib = Library.load_from_file("library_state.json")
    print("\nLoaded library state:")
    print(loaded_lib) 