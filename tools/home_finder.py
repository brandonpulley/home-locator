from dateutil.parser import parse
import datetime
import sys


SAMPLE_START_TIME = "5/29/2015 10:12:35"

SAMPLE_END_TIME = "5/30/2015 10:12:35"

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


def add_time_for_location(start_time: str, end_time: str):

    start_time_dt = parse(start_time)
    end_time_dt = parse(end_time)

    # first, check if start time starts before bounds

    new_time = end_time_dt - start_time_dt

    return new_time.total_seconds()
    # TODO: don't do this in this method
    # if is_visit_long_enough(new_time):
    #     print('more than 30 hours! - ', new_time)
    # else:
    #     print('less than 30 hours! - ', new_time)


def is_visit_long_enough(total_time_at_location):

    return total_time_at_location.total_seconds() > MINIMUM_SECONDS
