import pytest
from datetime_wrapper import DateTimeWrapper


@pytest.mark.parametrize(
    "dt_wrapper, expected_datetime_string",
    [
        (DateTimeWrapper(2022, 1, 1, 10, 30), "2022-01-01 10:30"),
        (DateTimeWrapper(2023, 12, 31, 23, 59), "2023-12-31 23:59"),
    ],
)
def test_init(dt_wrapper, expected_datetime_string):
    assert repr(dt_wrapper) == expected_datetime_string

@pytest.mark.parametrize(
    "dt_wrapper, expected_year, expected_month, expected_day, expected_week, expected_weekday, expected_hour, expected_minute",
    [
        (DateTimeWrapper(2022, 1, 1, 10, 30), 2022, 1, 1, 52, 6, 10, 30),
        (DateTimeWrapper(2023, 12, 31, 23, 59), 2023, 12, 31, 52, 7, 23, 59),
    ],
)
def test_properties(dt_wrapper, expected_year, expected_month, expected_day, expected_week, expected_weekday, expected_hour, expected_minute):
    assert dt_wrapper.year == expected_year
    assert dt_wrapper.month == expected_month
    assert dt_wrapper.day == expected_day
    assert dt_wrapper.week == expected_week
    assert dt_wrapper.weekday == expected_weekday
    assert dt_wrapper.hour == expected_hour
    assert dt_wrapper.minute == expected_minute

@pytest.mark.parametrize(
    "dt_wrapper1, dt_wrapper2, expected_diff",
    [
        (DateTimeWrapper(2022, 1, 1, 10, 30), DateTimeWrapper(2023, 12, 31, 23, 59), (729, 13, 29)),
        (DateTimeWrapper(2023, 12, 31, 23, 59), DateTimeWrapper(2022, 1, 1, 10, 30), (729, 13, 29)),
    ],
)
def test_get_diff_days_hours_minutes(dt_wrapper1, dt_wrapper2, expected_diff):
    assert dt_wrapper1.get_diff_days_hours_minutes(dt_wrapper2) == expected_diff
