import unittest
from datetime import datetime
from preprocess import load_restaurant_data
from query import get_open_restaurants


# Tests the get_open_restaurants function
class TestGetOpenRestaurants(unittest.TestCase):
    def test_get_open_restaurants_all_open(self):
        """
        Returns every restaurant when all are open
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-21 18:00:00"  # Sunday, everything open
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertEqual(len(response), 6)

    def test_get_open_restaurants_empty(self):
        """
        Returns an empty list when no restaurants are open
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-20 9:00:00"  # Saturday, everything closed
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertEqual(len(response), 0)

    def test_get_open_restaurants_some_closed(self):
        """
        Returns a list of open restaurants when some are closed
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-15 12:00:00"  # Monday, Garland and Bonchon closed
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertEqual(len(response), 4)

    def test_get_open_restaurants_unknown_hours(self):
        """
        Returns a list of open restaurants when some have unknown hours.
        Restaurants with unknown hours should have a "*" appended to their name.
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-15 12:00:00"
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        response = get_open_restaurants(date_time, day_trees)
        self.assertTrue("Beasley's Chicken + Honey*" in response)

    def test_get_open_restaurants_after_midnight(self):
        """
        Returns a list of open restaurants when the time is after midnight
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-20 23:30:00"  # Saturday, Bonchon open until 1:30am

        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        response = get_open_restaurants(date_time, day_trees)

        self.assertTrue("Bonchon" in response)

    def test_get_open_restaurants_after_midnight_next_day(self):
        """
        Returns a list of open restaurants when the time is after midnight and the restaurant closes the next day
        """
        day_trees = load_restaurant_data("tests/tests_get_open_restaurants.csv")
        date_time_str = "2024-04-21 1:00:00"

        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        response = get_open_restaurants(date_time, day_trees)
        print("response", response)
        self.assertTrue("Bonchon" in response)


if __name__ == "__main__":
    unittest.main()
