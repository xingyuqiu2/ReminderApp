from typing import List
from datetime_wrapper import DateTimeWrapper
from abc import ABC, abstractmethod


class Recurrence(ABC):
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int) -> None:
        self.start_dt_wrapper = start_dt_wrapper
        self.interval = interval
        self.last_occur_dt_wrapper = None
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        pass

    def _check_and_record_recurrence(self, current_dt_wrapper: DateTimeWrapper, recur_condition_check: bool) -> bool:
        if current_dt_wrapper < self.start_dt_wrapper:
            return False
        if not self.last_occur_dt_wrapper and current_dt_wrapper == self.start_dt_wrapper:
            self.last_occur_dt_wrapper = current_dt_wrapper
            return True
        if self.last_occur_dt_wrapper and self.last_occur_dt_wrapper == current_dt_wrapper:
            return False
        if not recur_condition_check:
            return False
        self.last_occur_dt_wrapper = current_dt_wrapper
        return True

class Once(Recurrence):
    """
    Recurrence class representing occur only once.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int = 0) -> None:
        super().__init__(start_dt_wrapper, interval)

    def __repr__(self) -> str:
        return f"Once(Occur once on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        return super()._check_and_record_recurrence(current_dt_wrapper, False)

class Hour(Recurrence):
    """
    Recurrence class representing recurrence every certain number of hours.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int) -> None:
        super().__init__(start_dt_wrapper, interval)

    def __repr__(self) -> str:
        return f"Hour(Recur every {self.interval} hour starting on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        days, hours, minutes = current_dt_wrapper.get_diff_days_hours_minutes(self.start_dt_wrapper)
        interval_check = (days * 24 + hours) % self.interval == 0
        minute_check = minutes == 0
        recur_condition_check = interval_check and minute_check
        return super()._check_and_record_recurrence(current_dt_wrapper, recur_condition_check)

class Day(Recurrence):
    """
    Recurrence class representing recurrence every certain number of days.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int) -> None:
        super().__init__(start_dt_wrapper, interval)

    def __repr__(self) -> str:
        return f"Day(Recur every {self.interval} day starting on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        days, hours, minutes = current_dt_wrapper.get_diff_days_hours_minutes(self.start_dt_wrapper)
        interval_check = days % self.interval == 0
        hour_check = hours == 0
        minute_check = minutes == 0
        recur_condition_check = interval_check and hour_check and minute_check
        return super()._check_and_record_recurrence(current_dt_wrapper, recur_condition_check)

class Week(Recurrence):
    """
    Recurrence class representing recurrence every certain number of weeks.
    Sunday is defined to be the start weekday of a week.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int, weekdays: List[int]) -> None:
        super().__init__(start_dt_wrapper, interval)
        self.weekdays = weekdays

    def __repr__(self) -> str:
        return f"Week(Recur every {self.interval} week on {self.weekdays} weekdays starting on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        _, hours, minutes = current_dt_wrapper.get_diff_days_hours_minutes(self.start_dt_wrapper)
        interval_check = current_dt_wrapper.get_diff_weeks(self.start_dt_wrapper) % self.interval == 0
        weekday_check = current_dt_wrapper.weekday in self.weekdays
        hour_check = hours == 0
        minute_check = minutes == 0
        recur_condition_check = interval_check and weekday_check and hour_check and minute_check
        return super()._check_and_record_recurrence(current_dt_wrapper, recur_condition_check)

class Month(Recurrence):
    """
    Recurrence class representing recurrence every certain number of months.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int, days: List[int]) -> None:
        super().__init__(start_dt_wrapper, interval)
        self.days = days

    def __repr__(self) -> str:
        return f"Month(Recur every {self.interval} month on {self.days} days starting on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        interval_check = (current_dt_wrapper.month - self.start_dt_wrapper.month + 12 * (self.interval // 12)) % self.interval == 0
        day_check = current_dt_wrapper.day in self.days
        hour_check = self.start_dt_wrapper.hour == current_dt_wrapper.hour
        minute_check = self.start_dt_wrapper.minute == current_dt_wrapper.minute
        recur_condition_check = interval_check and day_check and hour_check and minute_check
        return super()._check_and_record_recurrence(current_dt_wrapper, recur_condition_check)

class Year(Recurrence):
    """
    Recurrence class representing recurrence every certain number of years.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int, months: List[int]) -> None:
        super().__init__(start_dt_wrapper, interval)
        self.months = months

    def __repr__(self) -> str:
        return f"Year(Recur every {self.interval} year on {self.months} months starting on {self.start_dt_wrapper})"

    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        interval_check = (current_dt_wrapper.year - self.start_dt_wrapper.year) % self.interval == 0
        month_check = current_dt_wrapper.month in self.months
        day_check = self.start_dt_wrapper.day == current_dt_wrapper.day
        hour_check = self.start_dt_wrapper.hour == current_dt_wrapper.hour
        minute_check = self.start_dt_wrapper.minute == current_dt_wrapper.minute
        recur_condition_check = interval_check and month_check and day_check and hour_check and minute_check
        return super()._check_and_record_recurrence(current_dt_wrapper, recur_condition_check)
