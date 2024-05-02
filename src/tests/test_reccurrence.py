import pytest
from datetime_wrapper import DateTimeWrapper
from recurrence import Day, Hour, Week, Month, Year


class TestRecurrence:
    @pytest.fixture
    def start_dt_wrapper(self):
        return DateTimeWrapper(2022, 1, 1, 10, 30)

    @pytest.mark.parametrize(
        "recurrence_class, interval, args, expected_repr",
        [
            (Hour, 2, [], "Hour(Recur every 2 hour starting on 2022-01-01 10:30)"),
            (Day, 3, [], "Day(Recur every 3 day starting on 2022-01-01 10:30)"),
            (Week, 1, [[1, 3, 5]], "Week(Recur every 1 week on [1, 3, 5] weekdays starting on 2022-01-01 10:30)"),
            (Week, 1, [[4]], "Week(Recur every 1 week on [4] weekdays starting on 2022-01-01 10:30)"),
            (Month, 4, [[1, 15]], "Month(Recur every 4 month on [1, 15] days starting on 2022-01-01 10:30)"),
            (Year, 1, [[1, 6]], "Year(Recur every 1 year on [1, 6] months starting on 2022-01-01 10:30)"),
        ],
    )
    def test_repr(self, start_dt_wrapper, recurrence_class, interval, args, expected_repr):
        recurrence = recurrence_class(start_dt_wrapper, interval, *args)
        assert repr(recurrence) == expected_repr

    @pytest.mark.parametrize(
        "recurrence_class, interval, args, cur_dt_wrapper, expected_should_recur",
        [
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 12, 30), True),
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 11, 30), False),
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 12, 29), False),
            (Day, 2, [], DateTimeWrapper(2022, 1, 3, 10, 30), True),
            (Day, 2, [], DateTimeWrapper(2022, 1, 4, 10, 30), False),
            (Week, 1, [[1, 3, 5]], DateTimeWrapper(2022, 1, 8, 10, 30), True),
            (Week, 1, [[1, 3, 5]], DateTimeWrapper(2022, 1, 9, 10, 30), False),
            (Month, 1, [[1, 15]], DateTimeWrapper(2022, 2, 1, 10, 30), True),
            (Month, 1, [[1, 15]], DateTimeWrapper(2022, 2, 2, 10, 30), False),
            (Year, 1, [[1, 6]], DateTimeWrapper(2023, 1, 1, 10, 30), True),
            (Year, 1, [[1, 6]], DateTimeWrapper(2023, 1, 2, 10, 30), False),
        ],
    )
    def test_should_recur(
        self, start_dt_wrapper, recurrence_class, interval, args, cur_dt_wrapper, expected_should_recur
    ):
        recurrence = recurrence_class(start_dt_wrapper, interval, *args)
        assert recurrence.should_recur(cur_dt_wrapper) == expected_should_recur
