import unittest
from models import Table, TableStatus, Dish

class TestTable(unittest.TestCase):
    def test_add_guests(self):
        table = Table(seats_number=4)
        table.add_guests(2)
        self.assertEqual(table.guests, 2)
        self.assertEqual(table.status, TableStatus.TAKEN)

    def test_guests_overflow(self):
        table = Table(seats_number=2)
        with self.assertRaises(ValueError):
            table.guests = 3

class TestDish(unittest.TestCase):
    def test_dish_creation(self):
        dish = Dish(name="Pizza", price=20.0)
        self.assertEqual(dish.name, "Pizza")
        self.assertEqual(dish.price, 20.0)
        self.assertFalse(dish.gluten_free)

    def test_spice_level(self):
        dish = Dish(name="Spicy", price=25.0, spice_level=2)
        self.assertEqual(dish.spice_level, 2)
        with self.assertRaises(ValueError):
            dish.spice_level = 5

if __name__ == "__main__":
    unittest.main() 