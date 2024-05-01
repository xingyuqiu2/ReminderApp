from typing import List
from datetime import datetime
from abc import ABC, abstractmethod


class Recurrence(ABC):
    def __init__(self, start_datetime: datetime, interval: int) -> None:
        self.start_datetime = start_datetime
        self.interval = interval
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def should_recur(self, current_datetime: datetime) -> bool:
        pass

class Hour(Recurrence):
    """
    Recurrence class representing recurrence every certain number of hours.
    """
    def __init__(self, start_datetime: datetime, interval: int) -> None:
        super().__init__(start_datetime, interval)

    def __repr__(self) -> str:
        return f"Hour(interval={self.interval})"
    
    def should_recur(self, current_datetime: datetime) -> bool:
        interval_check = (current_datetime.hour - self.start_datetime.hour) % self.interval == 0
        minute_check = self.start_datetime.minute == current_datetime.minute
        return interval_check and minute_check

class Day(Recurrence):
    """
    Recurrence class representing recurrence every certain number of days.
    """
    def __init__(self, start_datetime: datetime, interval: int) -> None:
        super().__init__(start_datetime, interval)

    def __repr__(self) -> str:
        return f"Day(interval={self.interval})"
    
    def should_recur(self, current_datetime: datetime) -> bool:
        interval_check = (current_datetime.day - self.start_datetime.day) % self.interval == 0
        hour_check = self.start_datetime.hour == current_datetime.hour
        minute_check = self.start_datetime.minute == current_datetime.minute
        return interval_check and hour_check and minute_check

class Week(Recurrence):
    """
    Recurrence class representing recurrence every certain number of weeks.
    """
    def __init__(self, start_datetime: datetime, interval: int, weekdays: List[int]) -> None:
        super().__init__(start_datetime, interval)
        self.weekdays = weekdays

    def __repr__(self) -> str:
        return f"Week(interval={self.interval}, weekdays={self.weekdays})"
    
    def should_recur(self, current_datetime: datetime) -> bool:
        interval_check = (current_datetime.week - self.start_datetime.week) % self.interval == 0
        weekday_check = current_datetime.weekday in self.weekdays
        hour_check = self.start_datetime.hour == current_datetime.hour
        minute_check = self.start_datetime.minute == current_datetime.minute
        return interval_check and weekday_check and hour_check and minute_check

class Month(Recurrence):
    """
    Recurrence class representing recurrence every certain number of months.
    """
    def __init__(self, start_datetime: datetime, interval: int, days: List[int]) -> None:
        super().__init__(start_datetime, interval)
        self.days = days

    def __repr__(self) -> str:
        return f"Month(interval={self.interval}, days={self.days})"
    
    def should_recur(self, current_datetime: datetime) -> bool:
        interval_check = (current_datetime.month - self.start_datetime.month) % self.interval == 0
        day_check = current_datetime.day in self.days
        hour_check = self.start_datetime.hour == current_datetime.hour
        minute_check = self.start_datetime.minute == current_datetime.minute
        return interval_check and day_check and hour_check and minute_check

class Year(Recurrence):
    """
    Recurrence class representing recurrence every certain number of years.
    """
    def __init__(self, start_datetime: datetime, interval: int, months: List[int]) -> None:
        super().__init__(start_datetime, interval)
        self.months = months

    def __repr__(self) -> str:
        return f"Year(interval={self.interval}, months={self.months})"

    def should_recur(self, current_datetime: datetime) -> bool:
        interval_check = (current_datetime.year - self.start_datetime.year) % self.interval == 0
        month_check = current_datetime.month in self.months
        day_check = self.start_datetime.day == current_datetime.day
        hour_check = self.start_datetime.hour == current_datetime.hour
        minute_check = self.start_datetime.minute == current_datetime.minute
        return interval_check and month_check and day_check and hour_check and minute_check

