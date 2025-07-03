"""
main.py - Przykładowe uruchomienie systemu restauracyjnego

Uruchom: python main.py
"""
import logging
from models import Table, TableStatus
from manager import Order, OrderManager
from interfaces import WaiterInterface, KitchenInterface

def main():
    logging.basicConfig(level=logging.INFO)
    # Tworzenie przykładowych stolików i zamówień
    tables = [Table(seats_number=4), Table(seats_number=2, status=TableStatus.RESERVED, guests=1), Table(seats_number=6, status=TableStatus.TAKEN, guests=6)]
    orders = [Order(table=t) for t in tables]
    order_manager = OrderManager(orders=orders)
    waiter = WaiterInterface(order_manager=order_manager)
    kitchen = KitchenInterface(order_manager=order_manager)

    print(waiter.free_tables())
    waiter.seat_guests(guests_number=4, table_id=1)
    waiter.add_dish(table_id=1, dish_name='Spaghetti Bolognese')
    waiter.add_dish(table_id=1, dish_name='Tomato Soup')
    print(kitchen.show_layout())
    kitchen.update_dish_status(table_id=1, dish_name='Tomato Soup', new_status=2)  # OrderStatus.CANNOT_BE_PREPARED
    print(kitchen.filter_orders(status=2))  # OrderStatus.CANNOT_BE_PREPARED

if __name__ == "__main__":
    main() 