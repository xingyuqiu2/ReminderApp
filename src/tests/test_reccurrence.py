import pytest
from datetime_wrapper import DateTimeWrapper
from recurrence import Once, Day, Hour, Week, Month, Year


class TestRecurrence:
    @pytest.fixture
    def start_dt_wrapper(self):
        return DateTimeWrapper(2022, 1, 1, 10, 30)

    @pytest.mark.parametrize(
        "recurrence_class, interval, args, expected_repr",
        [
            (Once, -1, [], "Once(Occur once on 2022-01-01 10:30)"),
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
            (Once, 0, [], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Once, 1, [], DateTimeWrapper(2022, 1, 1, 10, 31), False),
            (Once, 1, [], DateTimeWrapper(2022, 1, 2, 10, 31), False),
            (Once, 1, [], DateTimeWrapper(2021, 1, 1, 10, 31), False),
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 12, 30), True),
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 11, 30), False),
            (Hour, 2, [], DateTimeWrapper(2022, 1, 1, 12, 29), False),
            (Day, 2, [], DateTimeWrapper(2022, 1, 3, 10, 30), True),
            (Day, 2, [], DateTimeWrapper(2022, 1, 4, 10, 30), False),
            (Day, 31, [], DateTimeWrapper(2022, 2, 1, 10, 30), True),
            (Day, 31, [], DateTimeWrapper(2022, 2, 1, 11, 30), False),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 1, 8, 10, 30), True),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 1, 17, 10, 30), True),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 2, 2, 10, 30), True),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 1, 9, 10, 30), False),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2022, 2, 1, 10, 30), False),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2021, 12, 29, 10, 30), False),
            (Week, 1, [[1, 3, 6]], DateTimeWrapper(2021, 12, 27, 10, 30), False),
            (Week, 2, [[6, 7]], DateTimeWrapper(2022, 1, 2, 10, 30), False),
            (Week, 2, [[6, 7]], DateTimeWrapper(2022, 1, 8, 10, 30), False),
            (Week, 2, [[6, 7]], DateTimeWrapper(2022, 1, 9, 10, 30), True),
            (Week, 2, [[6, 7]], DateTimeWrapper(2022, 1, 29, 10, 30), True),
            (Week, 3, [[3]], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Week, 3, [[3]], DateTimeWrapper(2022, 2, 2, 10, 30), False),
            (Week, 3, [[3]], DateTimeWrapper(2022, 2, 9, 10, 30), True),
            (Week, 3, [[3]], DateTimeWrapper(2022, 2, 9, 11, 30), False),
            (Week, 12, [[5]], DateTimeWrapper(2022, 3, 25, 10, 30), True),
            (Week, 22, [[5]], DateTimeWrapper(2022, 6, 3, 10, 30), True),
            (Week, 50, [[5]], DateTimeWrapper(2022, 12, 16, 10, 30), True),
            (Week, 55, [[5]], DateTimeWrapper(2023, 1, 20, 10, 30), True),
            (Month, 1, [[1, 15]], DateTimeWrapper(2022, 2, 1, 10, 30), True),
            (Month, 1, [[1, 15]], DateTimeWrapper(2022, 2, 2, 10, 30), False),
            (Month, 4, [[10, 31]], DateTimeWrapper(2022, 5, 31, 10, 30), True),
            (Month, 4, [[10, 31]], DateTimeWrapper(2022, 9, 10, 10, 30), True),
            (Month, 4, [[10, 31]], DateTimeWrapper(2022, 9, 30, 10, 30), False),
            (Month, 4, [[10, 31]], DateTimeWrapper(2022, 10, 1, 10, 30), False),
            (Month, 12, [[3]], DateTimeWrapper(2023, 1, 3, 10, 30), True),
            (Month, 15, [[3]], DateTimeWrapper(2023, 4, 3, 10, 30), True),
            (Month, 24, [[3]], DateTimeWrapper(2024, 1, 3, 10, 30), True),
            (Month, 27, [[3]], DateTimeWrapper(2024, 4, 3, 10, 30), True),
            (Year, 1, [[1, 6]], DateTimeWrapper(2023, 1, 1, 10, 30), True),
            (Year, 1, [[1, 6]], DateTimeWrapper(2023, 1, 2, 10, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Year, 3, [[5, 6]], DateTimeWrapper(2022, 5, 1, 10, 30), True),
            (Year, 3, [[5, 6]], DateTimeWrapper(2022, 5, 2, 10, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2022, 5, 1, 9, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2022, 5, 1, 9, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2023, 1, 1, 10, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2023, 5, 1, 10, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2025, 1, 1, 10, 30), False),
            (Year, 3, [[5, 6]], DateTimeWrapper(2025, 5, 1, 10, 30), True),
        ],
    )
    def test_should_recur(
        self, start_dt_wrapper, recurrence_class, interval, args, cur_dt_wrapper, expected_should_recur
    ):
        recurrence = recurrence_class(start_dt_wrapper, interval, *args)
        assert recurrence.should_recur(cur_dt_wrapper) == expected_should_recur

    @pytest.fixture
    def recurrence_every_two_weeks(self):
        return Week(DateTimeWrapper(2022, 3, 1, 9, 30), 2, [2, 4])
    
    @pytest.mark.parametrize(
        "cur_dt_wrapper, expected_should_recur",
        [
            (DateTimeWrapper(2022, 3, 1, 9, 30), False),
            (DateTimeWrapper(2022, 3, 1, 9, 30), False),
            (DateTimeWrapper(2022, 3, 15, 9, 30), False),
            (DateTimeWrapper(2022, 3, 15, 9, 30), False),
            (DateTimeWrapper(2022, 3, 16, 9, 30), False),
            (DateTimeWrapper(2022, 3, 17, 9, 30), False),
        ],
    )
    def test_should_recur_when_call_twice_on_same_dt(
        self, recurrence_every_two_weeks, cur_dt_wrapper, expected_should_recur
    ):
        recurrence_every_two_weeks.should_recur(cur_dt_wrapper)
        assert recurrence_every_two_weeks.should_recur(cur_dt_wrapper) == expected_should_recur
