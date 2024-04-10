from __future__ import annotations
from pprint import pprint
from typing import Union

from data_types import ParsedRestaurant


class IntervalTreeNode:
    def __init__(
        self,
        val: ParsedRestaurant,
        max_end_time: int,
        left: Union[IntervalTreeNode, None] = None,
        right: Union[IntervalTreeNode, None] = None,
    ):
        self.val = val
        self.max_end_time = max_end_time
        self.left = left
        self.right = right


def build_interval_tree_from_sorted_list(
    l: list[ParsedRestaurant], start: int = 0, end: Union[int, None] = None
) -> Union[IntervalTreeNode, None]:

    if end is None:
        end = len(l)

    if start >= end:
        return None

    mid = (start + end) // 2

    return IntervalTreeNode(
        val=l[mid],
        max_end_time=max(l[i]["times"][1] for i in range(start, end)),
        left=build_interval_tree_from_sorted_list(l, start, mid),
        right=build_interval_tree_from_sorted_list(l, mid + 1, end),
    )
