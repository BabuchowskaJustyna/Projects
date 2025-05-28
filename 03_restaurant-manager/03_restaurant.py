import os.path
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import json


class TableStatus(Enum):
    EMPTY = 'empty'
    TAKEN = 'taken'
    RESERVED = 'reserved'


class OrderStatus(Enum):
    TO_BE_PREPARED = 'ToBePrepared'
    CANNOT_BE_PREPARED = 'CannotBePrepared'
    PREPARING = 'Preparing'
    COMPLETED = 'Completed'


class Interface(ABC):
    @abstractmethod
    def show_layout(self):
        ...


class Table:
    """
    >>> table = Table(seats_number=4, status=TableStatus.TAKEN)
    >>> table2 = Table(seats_number=4, status=TableStatus.TAKEN, guests=6)
    Traceback (most recent call last):
    ...
    ValueError: Please chose bigger table to many guests.
    >>> table2 = Table(seats_number=4)
    >>> table2.guests
    0
    >>> Table.reset_id_counter()
    """
    _id_counter = 1

    def __init__(self, seats_number: int, status: TableStatus = TableStatus.EMPTY, guests: int = 0) -> None:
        self.seats_number = seats_number
        self.status = status
        self.guests = guests
        self.table_id = self.get_id()

    @property
    def guests(self):
        return self._guests

    @guests.setter
    def guests(self, value: int) -> None:
        if value < 0:
            raise ValueError('Number of guests can not be lower than 0.')
        elif self.seats_number < value:
            raise ValueError('Please chose bigger table to many guests.')
        else:
            self._guests = value

    def add_guests(self, number: int) -> None:
        self.guests += number
        self.status = TableStatus.TAKEN

    @classmethod
    def get_id(cls) -> int:
        id_number = cls._id_counter
        cls._id_counter += 1
        return id_number

    @classmethod
    def reset_id_counter(cls) -> None:
        cls._id_counter = 1

    def change_table_status(self, new_status: TableStatus) -> None:
        self.status = new_status

    def __str__(self) -> str:
        if self.status == TableStatus.EMPTY:
            status_repr = f'{self.guests:>2}/{self.seats_number}  '
        elif self.status == TableStatus.TAKEN:
            status_repr = '----- '
        else:
            status_repr = '--R-- '
        return f'#{self.table_id:02d} {status_repr}'


class Dish:
    """
    >>> dish = Dish(name="Spaghetti bolognese", price=30.0)
    >>> dish.to_dict()
    {'name': 'Spaghetti Bolognese', 'price': 30.0, 'gluten_free': False, 'vegan': False, 'vegetarian': False, 'spice_level': 0}
    >>> dish.update_dish_params(price=35.5, gluten_free=True)
    >>> dish.to_dict()
    {'name': 'Spaghetti Bolognese', 'price': 35.5, 'gluten_free': True, 'vegan': False, 'vegetarian': False, 'spice_level': 0}
    """

    def __init__(self, name: str, price: float, gluten_free=False, vegan=False,
                 vegetarian=False, spice_level=0, id_number: int | None = None):
        self.name = name.title()
        self.price = price
        self.gluten_free = gluten_free
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.spice_level = spice_level
        self.id_number = id_number
        self.status: OrderStatus = OrderStatus.TO_BE_PREPARED

    @property
    def spice_level(self):
        return self._spice_level

    @spice_level.setter
    def spice_level(self, value: int):
        if value not in [0, 1, 2, 3]:
            raise ValueError('Spice level needs to be 0, 1, 2 or 3!')
        else:
            self._spice_level = value

    def update_dish_params(self, **kwargs) -> None:
        """
        Update the dish parameters if it has such attributes
        """
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    def to_dict(self):
        return {'name': self.name, 'price': self.price, 'gluten_free': self.gluten_free, 'vegan': self.vegan,
                'vegetarian': self.vegetarian, 'spice_level': self.spice_level}

    def __str__(self):
        return f'- {self.name}: {self.status.value}'


class MenuItem:
    """
    >>> menu = MenuItem()
    >>> menu.add_dish(name="Spaghetti Bolognese", price=30.50, spice_level=2)
    >>> menu.add_dish(name="Garlic Bread", price=15.2, spice_level=0)
    >>> menu.dishes[0].id_number
    1
    >>> menu.dishes[1].id_number
    2
    >>> menu.add_dish(name="Bread", price=5.0, spice_level=10)
    Traceback (most recent call last):
    ...
    ValueError: Spice level needs to be 0, 1, 2 or 3!
    >>> menu.add_dish(name="Garlic Bread", price=5.0, spice_level=0)
    Traceback (most recent call last):
    ...
    ValueError: Dish already exist in menu, please use update_dish_params
    >>> print(menu)
    - Spaghetti Bolognese
    - Garlic Bread
    >>> menu.remove_dish('Pizza Margherita')
    Traceback (most recent call last):
    ...
    ValueError: Dish with that name does not exist.
    >>> menu.add_dish(name="Pizza Margherita", price=15.0)
    >>> print(menu)
    - Spaghetti Bolognese
    - Garlic Bread
    - Pizza Margherita
    >>> menu.remove_dish('Pizza Margherita')
    >>> print(menu)
    - Spaghetti Bolognese
    - Garlic Bread
    >>> menu.update_dish_params('Spaghetti Bolognese', price=25.50)
    >>> menu.save_to_file('test.json')
    >>> _ = menu.load_from_file()
    >>> menu.dishes[0].name
    'Spaghetti Bolognese'
    >>> menu.dishes[2].id_number
    3
    """

    def __init__(self):
        self.dishes = []
        self.id_counter = 1

    def add_dish(self, name: str, price: float, gluten_free=False, vegan=False, vegetarian=False, spice_level=0):
        if any(dish.name == name for dish in self.dishes):
            raise ValueError('Dish already exist in menu, please use update_dish_params')
        else:
            dish_id = self.id_counter
            dish: Dish = Dish(name=name, price=price, gluten_free=gluten_free, vegan=vegan,
                              vegetarian=vegetarian, spice_level=spice_level, id_number=dish_id)
            self.dishes.append(dish)
            self.id_counter += 1

    def find_dish(self, dish_name: str) -> Dish:
        try:
            return [dish for dish in self.dishes if dish.name == dish_name][0]
        except IndexError:
            raise ValueError('Dish with that name does not exist.')

    def remove_dish(self, dish_name: str) -> None:
        dish_to_rem = self.find_dish(dish_name)
        if dish_to_rem:
            self.dishes.remove(dish_to_rem)

    def update_dish_params(self, dish_name: str, **kwargs) -> None:
        """
        Update dish parameters if exist and has that attribute.
        """
        update_dish: Dish = self.find_dish(dish_name)
        if update_dish:
            update_dish.update_dish_params(**kwargs)

    def save_to_file(self, file_name: str) -> None:
        """
        Save to json file.
        """
        with open(file_name, 'w') as file:
            dishes = [dish.to_dict() for dish in self.dishes]
            json.dump(dishes, file, indent=4)

    def load_from_file(self, file_name: str = 'menu.json'):
        """
        Load menu from input files.
        """
        self.dishes = []
        self.id_counter = 1
        try:
            with open(file_name, 'r') as file:
                menu = json.load(file)
            [self.add_dish(**dish) for dish in menu]
        except (FileNotFoundError, json.JSONDecodeError):
            raise RuntimeError('Error during running file.')
        return self

    def __str__(self) -> str:
        return ''.join([f'- {dish.name}\n' for dish in self.dishes]).strip()


class Order:
    """
    >>> order1 = Order(table=Table(seats_number=4, status=TableStatus.TAKEN, guests=2))
    >>> order2 = Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=6))
    Traceback (most recent call last):
    ...
    ValueError: Please chose bigger table to many guests.
    >>> order2 = Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=1))
    >>> order2.order_id
    2
    >>> order1.order_dish("Pizza Margherita")
    >>> order1.order_dish("Tomato Soup")
    >>> order2.order_dish("Caesar Salad")
    >>> order2.order_dish("Lemonade")
    >>> order2.change_dish_status(dish_name="Lemonade", status=OrderStatus.CANNOT_BE_PREPARED)
    >>> order2.order_id
    2
    >>> order2.order_dish("test")
    Traceback (most recent call last):
    ...
    ValueError: Dish with that name does not exist.
    >>> order1.change_dish_status(dish_name="Pizza Margherita", status=OrderStatus.PREPARING)
    >>> order2.change_dish_status(dish_name="Lemonade", status=OrderStatus.COMPLETED)
    >>> print(order2)
    Order #2
    - Caesar Salad: ToBePrepared
    - Lemonade: Completed
    >>> order1.change_dish_status(dish_name="Test")
    Traceback (most recent call last):
    ...
    ValueError: Dish with that name does not exist.
    >>> order2.change_dish_order(ordered_dish='Caesar Salad', new_dish='Tomato Soup')
    >>> print(order2)
    Order #2
    - Lemonade: Completed
    - Tomato Soup: ToBePrepared
    >>> file_name = 'test.csv'
    >>> order1.add_to_history(file_name=file_name)
    >>> order2.add_to_history(file_name=file_name)
    >>> Order.reset_id_counter()
    >>> Table.reset_id_counter()
    """
    _menu: MenuItem = MenuItem().load_from_file()
    _id_counter = 1

    def __init__(self, table: Table) -> None:
        self.table = table
        self.ordered_dishes: list[Dish] = []
        self.order_id = self.get_id()
        self.completion_time = ''

    @classmethod
    def get_id(cls) -> int:
        id_number = cls._id_counter
        cls._id_counter += 1
        return id_number

    @classmethod
    def reset_id_counter(cls) -> None:
        cls._id_counter = 1

    @classmethod
    def get_menu(cls) -> MenuItem:
        return cls._menu

    def order_dish(self, dish_name: str, status: OrderStatus = OrderStatus.TO_BE_PREPARED) -> None:
        ordered_dish = self.get_menu().find_dish(dish_name)
        if self.table.status == TableStatus.RESERVED:
            self.table.status = TableStatus.TAKEN
        ordered_dish.status = status
        self.ordered_dishes.append(ordered_dish)

    def change_dish_status(self, dish_name: str, status: OrderStatus = OrderStatus.PREPARING) -> None:
        update_dishes = list(filter(lambda dish: dish.name == dish_name, self.ordered_dishes))[:]
        if update_dishes:
            for update_dish in update_dishes:
                update_dish.status = status
        else:
            raise ValueError('Dish with that name does not exist.')

    def change_dish_order(self, ordered_dish: str, new_dish: str) -> None:
        dish_to_update: Dish = self.get_menu().find_dish(ordered_dish)
        self.ordered_dishes = [dish for dish in self.ordered_dishes if dish != dish_to_update]
        self.order_dish(dish_name=new_dish)

    def filter_dish_status(self, status: OrderStatus) -> list[Dish]:
        return [dish for dish in self.ordered_dishes if dish.status == status]

    def add_to_history(self, file_name='order_history.csv') -> None:
        """Add to history order that is competed"""
        if_exist = os.path.exists(file_name)
        self.completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = 'Order ID,Table ID,Menu Item Id,Status,Price,Timestamp\n'
        with open(file_name, 'a') as file:
            if not if_exist:
                file.write(title)
            for dish in self.ordered_dishes:
                file.write(f'{self.order_id}, {self.table.table_id}, {dish.id_number}, {dish.status.value}, '
                           f'{dish.price:.2f} {self.completion_time}\n')

    def __str__(self):
        order_dishes = '\n'.join([str(dish) for dish in self.ordered_dishes])
        return f'Order #{self.order_id}\n{order_dishes}'


class OrderManager:
    """
    >>> order1 = Order(table=Table(seats_number=4, status=TableStatus.TAKEN, guests=2))
    >>> order1.order_dish('Spaghetti Bolognese')
    >>> order1.order_dish('Tomato Soup')
    >>> order1.change_dish_status('Tomato Soup', status=OrderStatus.CANNOT_BE_PREPARED)
    >>> order2 = Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=1))
    >>> order2.order_dish('Calzone')
    >>> order2.order_dish('Lemonade')
    >>> order2.change_dish_status('Lemonade', status=OrderStatus.COMPLETED)
    >>> order3 = Order(table=Table(seats_number=6, status=TableStatus.TAKEN, guests=6))
    >>> order4 = Order(table=Table(seats_number=4, status=TableStatus.RESERVED, guests=4))
    >>> order_manager = OrderManager(orders=[order1, order2, order3])
    >>> order_manager.add_order(order4)
    >>> len(order_manager.orders)
    4
    >>> order_manager.remove_order(3)
    >>> len(order_manager.orders)
    4
    >>> print(order_manager)
    Order #1
    - Spaghetti Bolognese: ToBePrepared
    - Tomato Soup: CannotBePrepared
    Order #2
    - Calzone: ToBePrepared
    - Lemonade: Completed
    Order #3
    Order #4
    >>> Table.reset_id_counter()
    >>> Order.reset_id_counter()
    """

    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders or []

    def add_order(self, order: Order) -> None:
        if isinstance(order, Order):
            self.orders.append(order)
        else:
            raise AttributeError('You can add only instance of class Order.')

    def remove_order(self, table_id: int) -> None:
        order = self.find_order(table_id)
        if order:
            order.ordered_dishes = []
            order.table.status = TableStatus.EMPTY

    def filter_orders(self, table_status=None, order_status=None) -> list[Order]:
        filtered_orders = self.orders
        if table_status is not None:
            filtered_orders = [order for order in filtered_orders if order.table.status == table_status]
        if order_status is not None:
            filtered_orders = [order for order in filtered_orders if order.filter_dish_status(order_status)]
        return filtered_orders

    def find_order(self, table_id: int) -> Order:
        """
        Find order by table id number.
        """
        order_by_table = list(filter(lambda order: order.table.table_id == table_id, self.orders))[0]
        if order_by_table:
            return order_by_table
        else:
            raise ValueError('There is no table with that id_number')

    def __str__(self) -> str:
        return '\n'.join([str(order).strip() for order in self.orders])


class WaiterInterface(Interface):
    """
    >>> order1 = Order(table=Table(seats_number=4))
    >>> order2 = Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=1))
    >>> order3 = Order(table=Table(seats_number=6, status=TableStatus.TAKEN, guests=6))
    >>> order4 = Order(table=Table(seats_number=1))
    >>> order5 = Order(table=Table(seats_number=5))
    >>> order_manager = OrderManager(orders=[order1, order2, order3, order4])
    >>> waiter_interface = WaiterInterface(order_manager=order_manager)
    >>> print(waiter_interface.free_tables())
    Free tables are:
    #01  0/4
    #04  0/1
    >>> waiter_interface.seat_guests(guests_number=4, table_id=1)
    Number of guests: 4, assign to table: 1, order_id: 1
    >>> try:
    ...     waiter_interface.seat_guests(guests_number=4, table_id=2)
    ... except ValueError as e:
    ...     print(e)
    There is no free table with that id_number
    >>> waiter_interface.change_table_status(table_id=2, new_status=TableStatus.EMPTY)
    >>> waiter_interface.seat_guests(guests_number=1, table_id=2)
    Number of guests: 1, assign to table: 2, order_id: 2
    >>> waiter_interface.seat_guests(guests_number=4, table_id=4)
    Traceback (most recent call last):
    ...
    ValueError: Please chose bigger table to many guests.
    >>> waiter_interface.seat_guests(guests_number=1, table_id=4)
    Number of guests: 1, assign to table: 4, order_id: 4
    >>> waiter_interface.add_order(order5)
    Order with id: 5 is added.
    >>> order6 = Order(table=Table(seats_number=3))
    >>> waiter_interface.add_order(order6)
    Order with id: 6 is added.
    >>> print(waiter_interface.free_tables())
    Free tables are:
    #05  0/5
    #06  0/3
    >>> waiter_interface.seat_guests(guests_number=3, table_id=6)
    Number of guests: 3, assign to table: 6, order_id: 6
    >>> waiter_interface.change_order(table_id=6, new_guests_number=2)
    Order from table 6 has now 2 guests
    >>> waiter_interface.order_manager.find_order(6).table.guests
    2
    >>> waiter_interface.change_order(table_id=6, new_guests_number=5)
    Order from table 6 has now 5 guests with assign new table number 5. Table 6 is free now.
    >>> waiter_interface.cancel_order(table_id_remove=5)
    Order with table_id: 5 is canceled.
    >>> waiter_interface.add_dish(table_id=1, dish_name='Spaghetti Bolognese')
    Dish: Spaghetti Bolognese add to order for table 1.
    >>> waiter_interface.change_dish_order(table_id=1, ordered_dish='Spaghetti Bolognese', new_dish='Tomato Soup')
    Dish: Spaghetti Bolognese was changed into Tomato Soup.
    >>> waiter_interface.paid_table(table_id=1)
    Table 1 is clear now and ready for new guests.
    >>> waiter_interface.order_manager.find_order(1).table.status == TableStatus.EMPTY
    True
    >>> try:
    ...     waiter_interface.seat_guests(guests_number=8, table_id=3)
    ... except ValueError as e:
    ...     print(e)
    There is no free table with that id_number
    >>> waiter_interface.add_order(order=Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=1)))
    Order with id: 7 is added.
    >>> for _ in range(5):
    ...     waiter_interface.add_order(order=Order(table=Table(seats_number=4)))
    Order with id: 8 is added.
    Order with id: 9 is added.
    Order with id: 10 is added.
    Order with id: 11 is added.
    Order with id: 12 is added.
    >>> print(waiter_interface.show_layout())
     ------------------ Tables -----------------
    |#01  4/4  |#02 ----- |#03 ----- |#04 ----- |
    |#05  5/5  |#06  0/3  |#07 --R-- |#08  0/4  |
    |#09  0/4  |#10  0/4  |#11  0/4  |#12  0/4  |
     -------------------------------------------
    >>> Order.reset_id_counter()
    >>> Table.reset_id_counter()
    """

    def __init__(self, order_manager: OrderManager) -> None:
        self.order_manager = order_manager

    """
    Display the restaurant layout showing table statuses.
    """

    def free_tables(self) -> str:
        filter_orders: list[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
        free_tables = '\n'.join([str(order.table).strip() for order in filter_orders])
        return f'Free tables are:\n{free_tables}'

    def seat_guests(self, guests_number: int, table_id: int) -> None:
        filter_orders: list[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
        try:
            filter_order: Order = list(filter(lambda order: order.table.table_id == table_id, filter_orders))[0]
            filter_order.table.add_guests(guests_number)
            print(f'Number of guests: {guests_number}, assign to table: {table_id}, order_id: {filter_order.order_id}')
        except IndexError:
            raise ValueError('There is no free table with that id_number')

    def add_order(self, order: Order) -> None:
        self.order_manager.add_order(order)
        print(f'Order with id: {order.order_id} is added.')

    def add_dish(self, table_id: int, dish_name: str) -> None:
        order_by_table: Order = self.order_manager.find_order(table_id)
        order_by_table.order_dish(dish_name)
        print(f'Dish: {dish_name} add to order for table {table_id}.')

    def change_dish_order(self, table_id: int, ordered_dish: str, new_dish: str) -> None:
        order_by_table: Order = self.order_manager.find_order(table_id)
        order_by_table.change_dish_order(ordered_dish, new_dish)
        print(f'Dish: {ordered_dish} was changed into {new_dish}.')

    def change_order(self, table_id: int, new_guests_number: int) -> None:
        """
        Change number of guests, if bigger than seats number change table from free.
        """
        order_for_update: Order = self.order_manager.find_order(table_id)
        if order_for_update.table.seats_number < new_guests_number:
            free_orders: list[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
            new_order: Order = [order for order in free_orders if order.table.seats_number >= new_guests_number][0]
            if new_order:
                new_order.table.guests = new_guests_number
                self.change_table_status(table_id, new_status=TableStatus.EMPTY)
                order_for_update.table.guests = 0
                order_for_update.ordered_dishes = []
                print(f'Order from table {table_id} has now {new_guests_number} guests with assign '
                      f'new table number {new_order.table.table_id}. Table {table_id} is free now.')
            else:
                print(f'There is no free tables now for {new_guests_number} guests.')
        else:
            order_for_update.table.guests = new_guests_number
            print(f'Order from table {table_id} has now {new_guests_number} guests')

    def cancel_order(self, table_id_remove: int) -> None:
        self.order_manager.remove_order(table_id_remove)
        print(f'Order with table_id: {table_id_remove} is canceled.')

    def paid_table(self, table_id: int) -> None:
        """
        Mark tables as paid and clear them for new guests
        """
        paid_order: Order = self.order_manager.find_order(table_id)
        paid_order.add_to_history()
        self.order_manager.remove_order(table_id)
        print(f'Table {table_id} is clear now and ready for new guests.')

    def change_table_status(self, table_id: int, new_status: TableStatus) -> None:
        order: Order = self.order_manager.find_order(table_id)
        order.table.status = new_status

    def show_layout(self) -> str:
        title = ' ------------------ Tables -----------------'
        row_tables = [f'|{str(order.table)}' for order in self.order_manager.orders]
        row_numbers = len(row_tables) + 1
        columns = 4  # nie dajemy jako parametr w funkcji, bo stała
        row_divided = [''.join(row_tables[i:i + columns]) for i in range(0, row_numbers, 4)]

        end = ' -------------------------------------------'
        return f'{title}\n{'|\n'.join(row_divided)}{end}'


class KitchenInterface(Interface):
    """
    >>> order1 = Order(table=Table(seats_number=4, status=TableStatus.TAKEN, guests=2))
    >>> order2 = Order(table=Table(seats_number=2, status=TableStatus.RESERVED, guests=1))
    >>> order_manager = OrderManager(orders=[order1, order2])
    >>> waiter_interface = WaiterInterface(order_manager=order_manager)
    >>> waiter_interface.add_dish(table_id=1, dish_name='Spaghetti Bolognese')
    Dish: Spaghetti Bolognese add to order for table 1.
    >>> waiter_interface.add_dish(table_id=1, dish_name='Tomato Soup')
    Dish: Tomato Soup add to order for table 1.
    >>> waiter_interface.add_dish(table_id=2, dish_name='Calzone')
    Dish: Calzone add to order for table 2.
    >>> waiter_interface.add_dish(table_id=2, dish_name='Lemonade')
    Dish: Lemonade add to order for table 2.
    >>> kitchen_interface = KitchenInterface(order_manager=order_manager)
    >>> kitchen_interface.update_dish_status(table_id=1, dish_name='Tomato Soup', new_status=OrderStatus.CANNOT_BE_PREPARED)
    Status of dish: Tomato Soup is updated into CannotBePrepared
    >>> kitchen_interface.update_dish_status(table_id=2, dish_name='Lemonade', new_status=OrderStatus.COMPLETED)
    Status of dish: Lemonade is updated into Completed
    >>> print(kitchen_interface.show_layout())
    Order #1
    - Spaghetti Bolognese: ToBePrepared
    - Tomato Soup: CannotBePrepared
    Order #2
    - Calzone: ToBePrepared
    - Lemonade: Completed
    >>> print(kitchen_interface.filter_orders(status=OrderStatus.COMPLETED))
    Order #2
    - Calzone: ToBePrepared
    - Lemonade: Completed
    >>> Order.reset_id_counter()
    >>> Table.reset_id_counter()
    """

    def __init__(self, order_manager: OrderManager) -> None:
        self.order_manager = order_manager

    """
    Display orders with dish details and statuses
    """

    def update_dish_status(self, table_id: int, dish_name: str, new_status: OrderStatus) -> None:
        order: Order = self.order_manager.find_order(table_id)
        order.change_dish_status(dish_name=dish_name, status=new_status)
        print(f'Status of dish: {dish_name} is updated into {new_status.value}')

    def filter_orders(self, status: OrderStatus) -> str:
        """
        Filters orders with dishes with a specified status.
        """
        filtered_orders = self.order_manager.filter_orders(order_status=status)
        view_orders = '\n'.join([str(order).strip() for order in filtered_orders])
        return view_orders

    def show_layout(self) -> str:
        return str(self.order_manager)
