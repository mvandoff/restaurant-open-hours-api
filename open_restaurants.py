import csv
from pprint import pprint
import re
from typing import Union
from enum import Enum

# Day = Enum("Day", ["Sun", "Mon", "Tues", "Wed", "Thu", "Fri", "Sat"])
# ParsedHours = dict[Day, Union[tuple[int, int], None]]

dayIndexes = {
    "Mon": 0,
    "Tues": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}


def load_restaurant_data():
    days = [[], [], [], [], [], [], []]

    with open("restaurants.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            [name, all_hours] = row

            # Split the hours string on '/' or ',' and strip the whitespace
            hours_split = [x.strip() for x in re.split(r"[/,]+", all_hours)]

            for hours_segment in hours_split:
                hours_segment_list = hours_segment.split(" ")
                day_or_day_range = hours_segment_list[0]
                times = hours_segment_list[1:]

                day_range = day_or_day_range.split("-")

                start_day = dayIndexes[day_range[0]]
                end_day = dayIndexes[day_range[1]] if len(day_range) > 1 else start_day

                for i in range(start_day, end_day + 1):
                    days[i].append(
                        {
                            # Append a "*" to the name if the restaurant times are unknown for that day
                            "name": name if len(times) > 0 else name + "*",
                            "times": parse_and_serialize_times(times),
                        }
                    )

    pprint(days)


# Parses the times list and returns a tuple of (start_time, end_time)
def parse_and_serialize_times(times: list[str]) -> tuple[int, int]:
    if len(times) == 0:
        return (0, 1439)

    [start_time, start_am_pm, _, end_time, end_am_pm] = times

    start_time_hours_and_minutes = start_time.split(":")
    start_time_hours = (
        0
        if start_time_hours_and_minutes[0] == "12" and start_am_pm == "am"
        else int(start_time_hours_and_minutes[0])
    )
    start_time_minutes = (
        int(start_time_hours_and_minutes[1])
        if len(start_time_hours_and_minutes) > 1
        else 0
    )

    if start_am_pm == "pm":
        start_time_hours += 12

    end_time_hours_and_minutes = end_time.split(":")
    end_time_hours = (
        0
        if end_time_hours_and_minutes[0] == "12" and end_am_pm == "am"
        else int(end_time_hours_and_minutes[0])
    )
    end_time_minutes = (
        int(end_time_hours_and_minutes[1]) if len(end_time_hours_and_minutes) > 1 else 0
    )

    if end_am_pm == "pm":
        end_time_hours += 12

    return (
        start_time_hours * 60 + start_time_minutes,
        end_time_hours * 60 + end_time_minutes,
    )


load_restaurant_data()
