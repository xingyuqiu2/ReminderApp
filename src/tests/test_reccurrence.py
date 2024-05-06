import pytest
from datetime_wrapper import DateTimeWrapper
from recurrence import Once, Day, Hour, Week, Month
import copy


class TestRecurrence:
    @pytest.fixture
    def start_dt_wrapper(self):
        return DateTimeWrapper(2022, 1, 1, 10, 30)

    @pytest.mark.parametrize(
        "recurrence_class, args, expected_repr",
        [
            (Once, [], "Once(Occur once on 2022-01-01 10:30)"),
            (Hour, [None, 2], "Hour(Recur every 2 hour starting on 2022-01-01 10:30 ending on None)"),
            (Hour, [DateTimeWrapper(2022, 9, 9, 14, 30), 2], "Hour(Recur every 2 hour starting on 2022-01-01 10:30 ending on 2022-09-09 14:30)"),
            (Day, [None, 3], "Day(Recur every 3 day starting on 2022-01-01 10:30 ending on None)"),
            (Day, [DateTimeWrapper(2022, 9, 9, 14, 30), 3], "Day(Recur every 3 day starting on 2022-01-01 10:30 ending on 2022-09-09 14:30)"),
            (Week, [None, 1, [1, 3, 5]], "Week(Recur every 1 week on [1, 3, 5] weekdays starting on 2022-01-01 10:30 ending on None)"),
            (Week, [DateTimeWrapper(2022, 9, 9, 14, 30), 1, [1, 3, 5]], "Week(Recur every 1 week on [1, 3, 5] weekdays starting on 2022-01-01 10:30 ending on 2022-09-09 14:30)"),
            (Week, [None, 1, [4]], "Week(Recur every 1 week on [4] weekdays starting on 2022-01-01 10:30 ending on None)"),
            (Month, [None, 4, [1, 15]], "Month(Recur every 4 month on [1, 15] days starting on 2022-01-01 10:30 ending on None)"),
            (Month, [DateTimeWrapper(2022, 9, 9, 14, 30), 4, [1, 15]], "Month(Recur every 4 month on [1, 15] days starting on 2022-01-01 10:30 ending on 2022-09-09 14:30)"),
        ],
    )
    def test_repr(self, start_dt_wrapper, recurrence_class, args, expected_repr):
        recurrence = recurrence_class(start_dt_wrapper, *args)
        assert repr(recurrence) == expected_repr

    @pytest.mark.parametrize(
        "recurrence_class, args, cur_dt_wrapper, expected_should_recur",
        [
            (Once, [], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Once, [], DateTimeWrapper(2021, 12, 31, 10, 30), False),
            (Hour, [None, 2], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Hour, [None, 2], DateTimeWrapper(2021, 12, 31, 10, 30), False),
            (Day, [None, 2], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Day, [None, 2], DateTimeWrapper(2021, 12, 31, 10, 30), False),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2021, 12, 31, 10, 30), False),
            (Month, [None, 2, [3, 15]], DateTimeWrapper(2022, 1, 1, 10, 30), True),
            (Month, [None, 2, [3, 15]], DateTimeWrapper(2021, 12, 31, 10, 30), False),
        ],
    )

    def test_should_recur_when_occur_for_the_first_time(
        self, start_dt_wrapper, recurrence_class, args, cur_dt_wrapper, expected_should_recur
    ):
        recurrence = recurrence_class(start_dt_wrapper, *args)
        assert recurrence.should_recur(cur_dt_wrapper) == expected_should_recur

    @pytest.mark.parametrize(
        "recurrence_class, args, cur_dt_wrapper, expected_should_recur",
        [
            (Once, [], DateTimeWrapper(2022, 1, 1, 10, 32), False),
            (Once, [], DateTimeWrapper(2022, 1, 2, 10, 32), False),
            (Hour, [None, 2], DateTimeWrapper(2022, 1, 1, 12, 30), True),
            (Hour, [None, 2], DateTimeWrapper(2022, 1, 1, 11, 30), False),
            (Hour, [None, 2], DateTimeWrapper(2022, 1, 1, 12, 29), False),
            (Day, [None, 2], DateTimeWrapper(2022, 1, 3, 10, 30), True),
            (Day, [None, 2], DateTimeWrapper(2022, 1, 4, 10, 30), False),
            (Day, [None, 31], DateTimeWrapper(2022, 2, 1, 10, 30), True),
            (Day, [None, 31], DateTimeWrapper(2022, 2, 1, 11, 30), False),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 1, 8, 10, 30), True),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 1, 17, 10, 30), True),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 2, 2, 10, 30), True),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 1, 9, 10, 30), False),
            (Week, [None, 1, [1, 3, 6]], DateTimeWrapper(2022, 2, 1, 10, 30), False),
            (Week, [None, 2, [6, 7]], DateTimeWrapper(2022, 1, 2, 10, 30), True),
            (Week, [None, 2, [6, 7]], DateTimeWrapper(2022, 1, 8, 10, 30), False),
            (Week, [None, 2, [6, 7]], DateTimeWrapper(2022, 1, 9, 10, 30), False),
            (Week, [None, 2, [6, 7]], DateTimeWrapper(2022, 1, 16, 10, 30), True),
            (Week, [None, 2, [6, 7]], DateTimeWrapper(2022, 1, 29, 10, 30), True),
            (Week, [None, 3, [3]], DateTimeWrapper(2022, 2, 2, 10, 30), False),
            (Week, [None, 3, [3]], DateTimeWrapper(2022, 2, 9, 10, 30), True),
            (Week, [None, 3, [3]], DateTimeWrapper(2022, 2, 9, 11, 30), False),
            (Week, [None, 12, [5]], DateTimeWrapper(2022, 3, 25, 10, 30), True),
            (Week, [None, 22, [5]], DateTimeWrapper(2022, 6, 3, 10, 30), True),
            (Week, [None, 50, [5]], DateTimeWrapper(2022, 12, 16, 10, 30), True),
            (Week, [None, 55, [5]], DateTimeWrapper(2023, 1, 20, 10, 30), True),
            (Month, [None, 1, [31]], DateTimeWrapper(2022, 2, 28, 10, 30), False),
            (Month, [None, 2, [1, 15]], DateTimeWrapper(2022, 3, 1, 10, 30), True),
            (Month, [None, 2, [1, 15]], DateTimeWrapper(2022, 2, 2, 10, 30), False),
            (Month, [None, 4, [10, 31]], DateTimeWrapper(2022, 5, 31, 10, 30), True),
            (Month, [None, 4, [10, 31]], DateTimeWrapper(2022, 9, 10, 10, 30), True),
            (Month, [None, 4, [10, 31]], DateTimeWrapper(2022, 9, 30, 10, 30), False),
            (Month, [None, 4, [10, 31]], DateTimeWrapper(2022, 10, 1, 10, 30), False),
            (Month, [None, 12, [3]], DateTimeWrapper(2023, 1, 3, 10, 30), True),
            (Month, [None, 15, [3]], DateTimeWrapper(2023, 4, 3, 10, 30), True),
            (Month, [None, 24, [3]], DateTimeWrapper(2024, 1, 3, 10, 30), True),
            (Month, [None, 27, [3]], DateTimeWrapper(2024, 4, 3, 10, 30), True),
        ],
    )
    def test_should_recur_when_occur_for_more_then_once(
        self, start_dt_wrapper, recurrence_class, args, cur_dt_wrapper, expected_should_recur
    ):
        recurrence = recurrence_class(start_dt_wrapper, *args)
        prev_dt_wrapper = copy.deepcopy(cur_dt_wrapper)
        prev_dt_wrapper.increment(minutes=-1)
        assert recurrence.should_recur(prev_dt_wrapper) == True
        print(recurrence.next_recur_dt_wrapper)
        assert recurrence.should_recur(cur_dt_wrapper) == expected_should_recur

    @pytest.fixture
    def recurrence_every_two_weeks(self):
        return Week(DateTimeWrapper(2022, 3, 1, 9, 30), None, 2, [2, 4])
    
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
