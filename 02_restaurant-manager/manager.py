import os
import logging
from datetime import datetime
from typing import List
from models import Table, Dish, MenuItem, TableStatus, OrderStatus

logger = logging.getLogger(__name__)

class Order:
    """Reprezentuje zamówienie dla danego stolika."""
    _menu: MenuItem = MenuItem().load_from_file()
    _id_counter = 1

    def __init__(self, table: Table) -> None:
        self.table = table
        self.ordered_dishes: List[Dish] = []
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

    def filter_dish_status(self, status: OrderStatus) -> List[Dish]:
        return [dish for dish in self.ordered_dishes if dish.status == status]

    def add_to_history(self, file_name: str = 'order_history.csv') -> None:
        if_exist = os.path.exists(file_name)
        self.completion_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = 'Order ID,Table ID,Menu Item Id,Status,Price,Timestamp\n'
        with open(file_name, 'a') as file:
            if not if_exist:
                file.write(title)
            for dish in self.ordered_dishes:
                file.write(f'{self.order_id}, {self.table.table_id}, {dish.id_number}, {dish.status.value}, '
                           f'{dish.price:.2f} {self.completion_time}\n')

    def __str__(self) -> str:
        order_dishes = '\n'.join([str(dish) for dish in self.ordered_dishes])
        return f'Order #{self.order_id}\n{order_dishes}'

class OrderManager:
    """Zarządza wszystkimi zamówieniami w restauracji."""
    def __init__(self, orders: List[Order]) -> None:
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

    def filter_orders(self, table_status: TableStatus = None, order_status: OrderStatus = None) -> List[Order]:
        filtered_orders = self.orders
        if table_status is not None:
            filtered_orders = [order for order in filtered_orders if order.table.status == table_status]
        if order_status is not None:
            filtered_orders = [order for order in filtered_orders if order.filter_dish_status(order_status)]
        return filtered_orders

    def find_order(self, table_id: int) -> Order:
        order_by_table = list(filter(lambda order: order.table.table_id == table_id, self.orders))[0]
        if order_by_table:
            return order_by_table
        else:
            raise ValueError('There is no table with that id_number')

    def __str__(self) -> str:
        return '\n'.join([str(order).strip() for order in self.orders]) 