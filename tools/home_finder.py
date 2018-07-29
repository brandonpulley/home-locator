from dateutil.parser import parse
import datetime
import sys


EARLY_HOUR_BOUND = 8
LATE_HOUR_BOUND = 20
MINIMUM_SECONDS = 108000

ARRIVAL_TIME = 'arrival_time'
DEPARTURE_TIME = 'departure_time'
LATITUDE = 'lat'
LONGITUDE = 'lon'

TOTAL_TIME = 'total_time'


def get_home_location(visits: []):
    my_locations = {}

    current_top = None

    for visit in visits:
        # normalizing lat/lon to easily find when the same location is visited
        key = _normalize_location(visit.get(LATITUDE), visit.get(LONGITUDE))

        if key in my_locations:
            # back at the same location!
            this_locations_current_total_time = my_locations[key]
        else:
            # default starting value - 0 seconds total time
            this_locations_current_total_time = 0

        # add this visit's total number of seconds
        this_locations_current_total_time += add_time_for_location(
            visit.get(ARRIVAL_TIME),
            visit.get(DEPARTURE_TIME)
        )

        my_locations[key] = this_locations_current_total_time
        keep_current_top = current_top and \
                           my_locations[current_top] > \
                           this_locations_current_total_time
        if not keep_current_top:
            current_top = key

    # TODO: Calculate current top stuff

    return my_locations


def _normalize_location(lat: float, lon: float):
    """
    Round the latitude and longitude to 3 decimal places and return
    a concatenated string
    :param lat: latitude as a float
    :param lon: longitude as a float
    :return: concatenated string of longitude and latitude
    """
    latitude = "{0:.3f}".format(round(lat, 3))
    longitude = "{0:.3f}".format(round(lon, 3))
    return latitude + ":" + longitude


def add_time_for_location(start_st: str, end_st: str):

    start_time_dt = parse(start_st)
    end_time_dt = parse(end_st)

    time_total_seconds = 0

    # first, check if start time starts before bounds
    if start_time_dt.hour < EARLY_HOUR_BOUND or \
            start_time_dt.hour > LATE_HOUR_BOUND:
        current_time = start_time_dt
    elif end_time_dt.day == start_time_dt.day and end_time_dt.hour < LATE_HOUR_BOUND:
        # same day, both start and end out of bounds. Add no time
        return 0
    else:
        # if start time is out of bounds, but end_time isn't, start at 8 pm
        current_time = datetime.datetime(start_time_dt.year,
                                         start_time_dt.month,
                                         start_time_dt.day,
                                         LATE_HOUR_BOUND)

    while current_time < end_time_dt:
        print('current_time:: ', current_time)
        current_time, time_total_seconds = _daily_bounds_check(
            current_time,
            end_time_dt,
            time_total_seconds)

    sys.stdout.flush()
    return time_total_seconds


def _get_next_datetime(current_time, day_offset, hour):
    current_time = current_time + datetime.timedelta(days=day_offset)
    return datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        hour
    )


def _daily_bounds_check(current_time, end_time_dt, time_total_seconds):

    # check: start_time after 8 PM and end_time after 8 AM next day
    if current_time.hour >= LATE_HOUR_BOUND and \
            end_time_dt.day > current_time.day \
            and end_time_dt.hour > EARLY_HOUR_BOUND:

        tomorrow_morning_bounds = _get_next_datetime(
            current_time, 1, EARLY_HOUR_BOUND)
        time_total_seconds += (tomorrow_morning_bounds -
                               current_time).total_seconds()

        # add 12 hours, update current_time, and continue
        current_time = _get_next_datetime(current_time, 1, LATE_HOUR_BOUND)

    # check: start_time after 8 PM and end_time before 8 AM next day
    elif current_time.hour >= LATE_HOUR_BOUND and \
            ((end_time_dt.day == current_time.day + 1
              and end_time_dt.hour < EARLY_HOUR_BOUND)
             or end_time_dt.day == current_time.day):

        time_total_seconds += (end_time_dt - current_time).total_seconds()
        current_time = _get_next_datetime(current_time, 1, LATE_HOUR_BOUND)

    # check: start_time before 8 AM and end_time after 8 AM today day
    elif current_time.hour < EARLY_HOUR_BOUND and \
            (end_time_dt.day > current_time.day
             or end_time_dt.hour > EARLY_HOUR_BOUND):
        this_morning_bounds = _get_next_datetime(current_time, 0, EARLY_HOUR_BOUND)
        time_total_seconds += (this_morning_bounds -
                               current_time).total_seconds()

        current_time = _get_next_datetime(current_time, 0, LATE_HOUR_BOUND)

    # check: start before 8 AM and end before 8 AM same day
    elif current_time.hour < EARLY_HOUR_BOUND \
            and end_time_dt.day == current_time.day \
            and end_time_dt.hour < EARLY_HOUR_BOUND:
        time_total_seconds += (end_time_dt -
                               current_time).total_seconds()

        current_time = _get_next_datetime(current_time, 0, LATE_HOUR_BOUND)

    return current_time, time_total_seconds


def is_visit_long_enough(total_time_at_location):

    return total_time_at_location.total_seconds() > MINIMUM_SECONDS
