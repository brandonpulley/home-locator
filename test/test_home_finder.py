from tools.home_finder import add_time_for_location


START_TIME_1 = "5/29/2015 9:12:35"
END_TIME_1 = "5/30/2015 9:12:35"
TOTAL_SECONDS_1 = 12 * 60 * 60

START_TIME_2 = "5/29/2015 9:12:35"
END_TIME_2 = "5/29/2015 22:12:35"
TOTAL_SECONDS_2 = 2 * 60 * 60 + 12 * 60 + 35


def test_bounds():
    assert add_time_for_location(START_TIME_1, END_TIME_1) == TOTAL_SECONDS_1
    assert add_time_for_location(START_TIME_2, END_TIME_2) == TOTAL_SECONDS_2
