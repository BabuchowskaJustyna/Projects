import logging
from enum import Enum
from typing import List, Optional

logger = logging.getLogger(__name__)

class TableStatus(Enum):
    """Status pojedynczego stolika w restauracji."""
    EMPTY = 'empty'
    TAKEN = 'taken'
    RESERVED = 'reserved'

class OrderStatus(Enum):
    """Status pojedynczego dania w zamówieniu."""
    TO_BE_PREPARED = 'ToBePrepared'
    CANNOT_BE_PREPARED = 'CannotBePrepared'
    PREPARING = 'Preparing'
    COMPLETED = 'Completed'

class Table:
    """Reprezentuje stolik w restauracji."""
    _id_counter = 1

    def __init__(self, seats_number: int, status: TableStatus = TableStatus.EMPTY, guests: int = 0) -> None:
        self.seats_number = seats_number
        self.status = status
        self.guests = guests
        self.table_id = self.get_id()

    @property
    def guests(self) -> int:
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
    """Reprezentuje pojedyncze danie w menu."""
    def __init__(self, name: str, price: float, gluten_free: bool = False, vegan: bool = False,
                 vegetarian: bool = False, spice_level: int = 0, id_number: Optional[int] = None):
        self.name = name.title()
        self.price = price
        self.gluten_free = gluten_free
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.spice_level = spice_level
        self.id_number = id_number
        self.status: OrderStatus = OrderStatus.TO_BE_PREPARED

    @property
    def spice_level(self) -> int:
        return self._spice_level

    @spice_level.setter
    def spice_level(self, value: int) -> None:
        if value not in [0, 1, 2, 3]:
            raise ValueError('Spice level needs to be 0, 1, 2 or 3!')
        else:
            self._spice_level = value

    def update_dish_params(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    def to_dict(self) -> dict:
        return {'name': self.name, 'price': self.price, 'gluten_free': self.gluten_free, 'vegan': self.vegan,
                'vegetarian': self.vegetarian, 'spice_level': self.spice_level}

    def __str__(self) -> str:
        return f'- {self.name}: {self.status.value}'

class MenuItem:
    """Reprezentuje menu restauracji."""
    def __init__(self):
        self.dishes: List[Dish] = []
        self.id_counter = 1

    def add_dish(self, name: str, price: float, gluten_free: bool = False, vegan: bool = False, vegetarian: bool = False, spice_level: int = 0) -> None:
        if any(dish.name == name for dish in self.dishes):
            raise ValueError('Dish already exist in menu, please use update_dish_params')
        else:
            dish_id = self.id_counter
            dish = Dish(name=name, price=price, gluten_free=gluten_free, vegan=vegan,
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
        update_dish = self.find_dish(dish_name)
        if update_dish:
            update_dish.update_dish_params(**kwargs)

    def save_to_file(self, file_name: str) -> None:
        import json
        with open(file_name, 'w') as file:
            dishes = [dish.to_dict() for dish in self.dishes]
            json.dump(dishes, file, indent=4)

    def load_from_file(self, file_name: str = 'menu.json'):
        import json
        self.dishes = []
        self.id_counter = 1
        try:
            with open(file_name, 'r') as file:
                menu = json.load(file)
            [self.add_dish(**dish) for dish in menu]
        except (FileNotFoundError, json.JSONDecodeError):
            logger.error('Error during running file.')
            raise RuntimeError('Error during running file.')
        return self

    def __str__(self) -> str:
        return ''.join([f'- {dish.name}\n' for dish in self.dishes]).strip() 