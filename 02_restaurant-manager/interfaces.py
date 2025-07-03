import logging
from abc import ABC, abstractmethod
from typing import List
from models import TableStatus, OrderStatus
from manager import OrderManager, Order

logger = logging.getLogger(__name__)

class Interface(ABC):
    """Abstrakcyjny interfejs do wyświetlania układu restauracji."""
    @abstractmethod
    def show_layout(self) -> str:
        ...

class WaiterInterface(Interface):
    """Interfejs kelnera do obsługi zamówień i stolików."""
    def __init__(self, order_manager: OrderManager) -> None:
        self.order_manager = order_manager

    def free_tables(self) -> str:
        filter_orders: List[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
        free_tables = '\n'.join([str(order.table).strip() for order in filter_orders])
        return f'Free tables are:\n{free_tables}'

    def seat_guests(self, guests_number: int, table_id: int) -> None:
        filter_orders: List[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
        try:
            filter_order: Order = list(filter(lambda order: order.table.table_id == table_id, filter_orders))[0]
            filter_order.table.add_guests(guests_number)
            logger.info(f'Number of guests: {guests_number}, assign to table: {table_id}, order_id: {filter_order.order_id}')
        except IndexError:
            raise ValueError('There is no free table with that id_number')

    def add_order(self, order: Order) -> None:
        self.order_manager.add_order(order)
        logger.info(f'Order with id: {order.order_id} is added.')

    def add_dish(self, table_id: int, dish_name: str) -> None:
        order_by_table: Order = self.order_manager.find_order(table_id)
        order_by_table.order_dish(dish_name)
        logger.info(f'Dish: {dish_name} add to order for table {table_id}.')

    def change_dish_order(self, table_id: int, ordered_dish: str, new_dish: str) -> None:
        order_by_table: Order = self.order_manager.find_order(table_id)
        order_by_table.change_dish_order(ordered_dish, new_dish)
        logger.info(f'Dish: {ordered_dish} was changed into {new_dish}.')

    def change_order(self, table_id: int, new_guests_number: int) -> None:
        order_for_update: Order = self.order_manager.find_order(table_id)
        if order_for_update.table.seats_number < new_guests_number:
            free_orders: List[Order] = self.order_manager.filter_orders(table_status=TableStatus.EMPTY)
            new_order: Order = [order for order in free_orders if order.table.seats_number >= new_guests_number][0]
            if new_order:
                new_order.table.guests = new_guests_number
                self.change_table_status(table_id, new_status=TableStatus.EMPTY)
                order_for_update.table.guests = 0
                order_for_update.ordered_dishes = []
                logger.info(f'Order from table {table_id} has now {new_guests_number} guests with assign new table number {new_order.table.table_id}. Table {table_id} is free now.')
            else:
                logger.warning(f'There is no free tables now for {new_guests_number} guests.')
        else:
            order_for_update.table.guests = new_guests_number
            logger.info(f'Order from table {table_id} has now {new_guests_number} guests')

    def cancel_order(self, table_id_remove: int) -> None:
        self.order_manager.remove_order(table_id_remove)
        logger.info(f'Order with table_id: {table_id_remove} is canceled.')

    def paid_table(self, table_id: int) -> None:
        paid_order: Order = self.order_manager.find_order(table_id)
        paid_order.add_to_history()
        self.order_manager.remove_order(table_id)
        logger.info(f'Table {table_id} is clear now and ready for new guests.')

    def change_table_status(self, table_id: int, new_status: TableStatus) -> None:
        order: Order = self.order_manager.find_order(table_id)
        order.table.status = new_status

    def show_layout(self) -> str:
        title = ' ------------------ Tables -----------------'
        row_tables = [f'|{str(order.table)}' for order in self.order_manager.orders]
        row_numbers = len(row_tables) + 1
        columns = 4
        row_divided = [''.join(row_tables[i:i + columns]) for i in range(0, row_numbers, 4)]
        end = ' -------------------------------------------'
        return f'{title}\n{'|\n'.join(row_divided)}{end}'

class KitchenInterface(Interface):
    """Interfejs kuchni do obsługi statusów dań."""
    def __init__(self, order_manager: OrderManager) -> None:
        self.order_manager = order_manager

    def update_dish_status(self, table_id: int, dish_name: str, new_status: OrderStatus) -> None:
        order: Order = self.order_manager.find_order(table_id)
        order.change_dish_status(dish_name=dish_name, status=new_status)
        logger.info(f'Status of dish: {dish_name} is updated into {new_status.value}')

    def filter_orders(self, status: OrderStatus) -> str:
        filtered_orders = self.order_manager.filter_orders(order_status=status)
        view_orders = '\n'.join([str(order).strip() for order in filtered_orders])
        return view_orders

    def show_layout(self) -> str:
        return str(self.order_manager) 