import csv
import re
from pprint import pprint
from datetime import datetime, timedelta

from IntervalTreeNode import build_interval_tree_from_sorted_list
from data_types import ParsedRestaurant

dayIndexes = {"Mon": 0, "Tues": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

# TODO: Dont add restaurants that are closed for the entire day to the tree


def load_restaurant_data(path_to_csv: str):
    days: list[list[ParsedRestaurant]] = [[], [], [], [], [], [], []]

    with open(path_to_csv, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            [name, all_hours] = row

            # Split the hours string on '/' or ',' and strip the whitespace
            hours_split = [x.strip() for x in re.split(r"[/,]+", all_hours)]

            # Parse the hours
            for hours_segment in hours_split:
                hours_segment_list = hours_segment.split(" ")
                day_or_day_range = hours_segment_list[0]
                times = hours_segment_list[1:]

                day_range = day_or_day_range.split("-")

                start_day = dayIndexes[day_range[0]]
                end_day = dayIndexes[day_range[1]] if len(day_range) > 1 else start_day

                for day_index in range(start_day, end_day + 1):
                    # TODO: Handle restaurants that are closed for the entire day and remove this
                    if len(times) == 0:
                        days[day_index].append(
                            {
                                "names": [name + "*"],
                                "times": (0, 1439),
                            }
                        )
                        continue

                    start_datetime, end_datetime = parse_times(times)

                    start_minutes = minutes_between(
                        datetime.strptime("12:00 am", "%I:%M %p"),
                        start_datetime,
                    )
                    end_minutes = minutes_between(start_datetime, end_datetime)

                    days[day_index].append(
                        {
                            # Append a "*" to the name if the restaurant times are unknown for that day
                            "names": [name],
                            "times": (
                                (
                                    start_minutes,
                                    start_minutes + end_minutes,
                                )
                            ),
                        }
                    )

                    # Some restaurants are open past midnight, so we need to add them to the next day
                    if end_datetime < start_datetime:
                        days[(day_index + 1) % 7].append(
                            {
                                "names": [name],
                                "times": (
                                    0,
                                    minutes_between(
                                        datetime.strptime("12:00 am", "%I:%M %p"),
                                        end_datetime,
                                    ),
                                ),
                            }
                        )

    # Sort the lists of restaurants by their start times
    for day in days:
        day.sort(key=lambda x: x["times"][0])

    # Merge any restaurants with the same start and end times
    for day in days:
        day_index = 0
        while day_index < len(day) - 1:
            if day[day_index]["times"] == day[day_index + 1]["times"]:
                day[day_index]["names"] += day[day_index + 1]["names"]
                del day[day_index + 1]
            else:
                day_index += 1

    # Build an interval tree for each day
    return [build_interval_tree_from_sorted_list(day) for day in days]


def minutes_between(start_datetime: datetime, end_datetime: datetime) -> int:
    """
    Calculates the number of minutes between two times.
    If the end time is earlier than the start time, assume it's the next day.
    """
    # Check if the end time is earlier than the start time (e.g., past midnight scenario)
    if end_datetime < start_datetime:
        # Correctly handle the next day adjustment
        end_datetime += timedelta(days=1)

    time_diff = end_datetime - start_datetime
    minutes = int(time_diff.total_seconds() // 60)
    return minutes


def parse_times(times: list[str]) -> tuple[datetime, datetime]:
    [start_time, start_am_pm, _, end_time, end_am_pm] = times

    start_time_hours_and_minutes = start_time.split(":")

    start_datetime = datetime.strptime(
        f"{start_time_hours_and_minutes[0]}:{'00' if len(start_time_hours_and_minutes) == 1 else start_time_hours_and_minutes[1]} {start_am_pm.upper()}",
        "%I:%M %p",
    )

    end_time_hours_and_minutes = end_time.split(":")
    end_datetime = datetime.strptime(
        f"{end_time_hours_and_minutes[0]}:{'00' if len(end_time_hours_and_minutes) == 1 else end_time_hours_and_minutes[1]} {end_am_pm.upper()}",
        "%I:%M %p",
    )

    return (start_datetime, end_datetime)


trees = load_restaurant_data("restaurants.csv")
