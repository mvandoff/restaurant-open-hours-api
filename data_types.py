from typing import TypedDict


ParsedRestaurant = TypedDict(
    "ParsedRestaurant", {"names": list[str], "times": tuple[int, int]}
)
