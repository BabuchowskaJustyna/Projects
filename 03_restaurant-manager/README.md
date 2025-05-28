# **Restaurant Management System**

## **Overview**

Python-based restaurant management system using Object-Oriented Programming (OOP). The system
include two user interfaces:

1. **Waiter Interface**: For managing table seating, orders, reservations, and payments.
2. **Kitchen Interface**: For tracking and updating the status of dishes.

The system:

- Load menu from input files.
- Log order history to an output file in append mode.
- Use clear representation for the restaurant layout in the waiter amd kitchen interface.
- Implement error handling for invalid inputs.

---

1. **Restaurant Layout**:

	- The restaurant is represented as a rectangular grid of tables.
	- Each table has:

		- A unique ID.
		- A number of seats.
		- A status (`empty`, `taken`, or `reserved`).
		
2. **Menu**:

	- The menu is a list of dishes, where each dish includes:
		- Name.
		- Price.
		- Attributes like `gluten_free`, `vegan`, `vegetarian`, and `spice_level`.
	- The menu is stored in a JSON file and loaded at runtime - please use enclosed menu.json file.

3. **Orders**:

	- Each order is associated with a table and consists of a list of dishes.
	- The order tracks the status of each dish.
	- Completed orders are logged to a history file in append mode.

4. **Interfaces**:

	- **Waiter Interface**:
		- Display the restaurant layout showing table statuses. Example below:
		  ```plaintext
			 ------------------ Tables -----------------
			|#01  0/4  |#02 ----- |#03 ----- |#04 ----- |
			|#05 --R-- |#06 ----- |#07  0/6  |#08  0/4  |
			|#09 ----- |#10 ----- |#11  0/12 |#12  0/4  |
			 -------------------------------------------
		  ```
		- `#01  0/4` represents table #1 with 0 guests out of 4 total seats.
		- `#06 -----` represents a taken table.
		- `#05 --R--` represents a table that is reserved within the next hour.

	- **Kitchen Interface**:
		- Display orders with dish details and statuses. Example below:
		  ```plaintext
		  Order #1
		  - Spaghetti Bolognese: ToBePrepared
		  - Tomato Soup: CannotBePrepared  
		  Order #2
		  - Calzone: ToBePrepared 
		  - Lemonade: Completed
		  ```
