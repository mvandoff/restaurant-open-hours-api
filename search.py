from datetime import datetime
from typing import Union, List
from IntervalTreeNode import IntervalTreeNode
from preprocess import RestaurantData


def get_open_restaurants(
    date_time: datetime, restaurant_data: RestaurantData
) -> list[str]:
    # Get the day of the week (0 is Monday, 6 is Sunday)
    day_of_week = date_time.weekday()
    # Get the number of minutes into the day
    minutes_into_day = date_time.hour * 60 + date_time.minute

    return (
        search_interval_tree(minutes_into_day, restaurant_data["trees"][day_of_week])
        + restaurant_data["unknown_times_restaurant_names"][day_of_week]
    )


def search_interval_tree(time: int, tree: Union[IntervalTreeNode, None]) -> list[str]:
    # Initialize a list to hold the names of restaurants open at the given time
    restaurants: List[str] = []

    # Base case: if the tree is None, return an empty list
    if tree is None:
        return restaurants

    # If the current time is within the range of the current node's time, add its names to the list
    if tree.val["times"][0] <= time <= tree.val["times"][1]:
        restaurants += tree.val["names"]

    # If there is a left child and its max end time is greater than or equal to the current time,
    # it means there might be open restaurants in the left subtree as well.
    if tree.left is not None and tree.left.max_end_time >= time:
        restaurants += search_interval_tree(time, tree.left)

    # Explore the right subtree regardless, as there might be restaurants opening later
    if tree.right is not None:
        restaurants += search_interval_tree(time, tree.right)

    return restaurants
