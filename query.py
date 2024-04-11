from datetime import datetime
from typing import Union
from IntervalTreeNode import IntervalTreeNode
from preprocess import RestaurantData, load_restaurant_data


def get_open_restaurants(
    date_time: datetime, restaurant_data: RestaurantData
) -> list[str]:
    # Get the day of the week (0 is Monday, 6 is Sunday)
    day_of_week = date_time.weekday()
    # Get the number of minutes into the day
    minutes_into_day = date_time.hour * 60 + date_time.minute

    return (
        search_interval_tree(
            minutes_into_day, restaurant_data["trees"][day_of_week], []
        )
        + restaurant_data["unknown_times_restaurant_names"][day_of_week]
    )


def search_interval_tree(
    time: int, tree: Union[IntervalTreeNode, None], restaurants: list[str]
) -> list[str]:
    if tree is None:
        return restaurants

    if tree.val["times"][0] <= time <= tree.val["times"][1]:
        restaurants += tree.val["names"]

    if tree.left is not None and tree.left.max_end_time >= time:
        search_interval_tree(time, tree.left, restaurants)

    if tree.right is not None:
        search_interval_tree(time, tree.right, restaurants)

    return restaurants
