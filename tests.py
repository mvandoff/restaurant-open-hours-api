import unittest
from datetime import datetime
from preprocess import load_restaurant_data
from query import get_open_restaurants

# Finds restaurants open after midnight


# Tests the get_open_restaurants function
class TestGetOpenRestaurants(unittest.TestCase):
    def test_get_open_restaurants(self):
        """
        Returns a list of open restaurants
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-20 18:00:00"  # Saturday, everything open
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertEqual(len(response), 5)

    def test_get_open_restaurants_empty(self):
        """
        Returns an empty list when no restaurants are open
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-20 9:00:00"  # Saturday, everything closed
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertEqual(len(response), 0)


if __name__ == "__main__":
    unittest.main()
