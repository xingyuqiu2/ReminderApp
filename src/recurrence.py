from typing import List
from datetime_wrapper import DateTimeWrapper
from abc import ABC, abstractmethod


class Recurrence(ABC):
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int) -> None:
        self.start_dt_wrapper = start_dt_wrapper
        self.interval = interval
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        pass

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
        return interval_check and minute_check

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
        return interval_check and hour_check and minute_check

class Week(Recurrence):
    """
    Recurrence class representing recurrence every certain number of weeks.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, interval: int, weekdays: List[int]) -> None:
        super().__init__(start_dt_wrapper, interval)
        self.weekdays = weekdays

    def __repr__(self) -> str:
        return f"Week(Recur every {self.interval} week on {self.weekdays} weekdays starting on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        # TODO
        days, hours, minutes = current_dt_wrapper.get_diff_days_hours_minutes(self.start_dt_wrapper)
        interval_check = (current_dt_wrapper.week - self.start_dt_wrapper.week) % self.interval == 0
        weekday_check = current_dt_wrapper.weekday in self.weekdays
        hour_check = hours == 0
        minute_check = minutes == 0
        return interval_check and weekday_check and hour_check and minute_check

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
        # TODO
        interval_check = (current_dt_wrapper.month - self.start_dt_wrapper.month) % self.interval == 0
        day_check = current_dt_wrapper.day in self.days
        hour_check = self.start_dt_wrapper.hour == current_dt_wrapper.hour
        minute_check = self.start_dt_wrapper.minute == current_dt_wrapper.minute
        return interval_check and day_check and hour_check and minute_check

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
        # TODO
        interval_check = (current_dt_wrapper.year - self.start_dt_wrapper.year) % self.interval == 0
        month_check = current_dt_wrapper.month in self.months
        day_check = self.start_dt_wrapper.day == current_dt_wrapper.day
        hour_check = self.start_dt_wrapper.hour == current_dt_wrapper.hour
        minute_check = self.start_dt_wrapper.minute == current_dt_wrapper.minute
        return interval_check and month_check and day_check and hour_check and minute_check

