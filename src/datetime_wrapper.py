from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing_extensions import Self
from typing import Tuple


FORMAT = "%Y-%m-%d %H:%M"

class DateTimeWrapper:
    def __init__(self, year: int = None, month: int = None, day: int = None, hour: int = None, minute: int = None) -> None:
        if all(val is not None for val in (year, month, day, hour, minute)):
            self.my_datetime = datetime(year, month, day, hour, minute)
        else:
            self.my_datetime = datetime.now()
        self.datetime_string = self.my_datetime.strftime(FORMAT)
    
    def __repr__(self) -> str:
        return self.datetime_string

    def __eq__(self, other):
        if isinstance(other, DateTimeWrapper):
            return self.my_datetime == other.my_datetime
        else:
            raise TypeError("Unsupported operand type. Can only compare DateTimeWrapper objects.")
    
    def __lt__(self, other: Self) -> bool:
        if isinstance(other, DateTimeWrapper):
            return self.my_datetime < other.my_datetime
        else:
            raise TypeError("Unsupported operand type. Can only compare DateTimeWrapper objects.")
    
    def __gt__(self, other: Self) -> bool:
        if isinstance(other, DateTimeWrapper):
            return self.my_datetime > other.my_datetime
        else:
            raise TypeError("Unsupported operand type. Can only compare DateTimeWrapper objects.")
    
    def get_diff_days_hours_minutes(self, other: Self) -> Tuple[int, int, int]:
        if self.my_datetime > other.my_datetime:
            td = self.my_datetime - other.my_datetime
        else:
            td = other.my_datetime - self.my_datetime
        return td.days, td.seconds//3600, (td.seconds//60)%60
    
    def get_diff_weeks(self, other: Self) -> int:
        if self.my_datetime > other.my_datetime:
            later_start_dt = self.my_datetime.date() - timedelta(days=self.weekday if self.weekday != 7 else 0)
            former_start_dt = other.my_datetime.date() - timedelta(days=other.weekday if other.weekday != 7 else 0)
        else:
            later_start_dt = other.my_datetime.date() - timedelta(days=other.weekday if other.weekday != 7 else 0)
            former_start_dt = self.my_datetime.date() - timedelta(days=self.weekday if self.weekday != 7 else 0)
        return (later_start_dt - former_start_dt).days // 7
    
    def increment(self, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0) -> None:
        self.my_datetime += timedelta(days=days, hours=hours, minutes=minutes)
        self.my_datetime += relativedelta(months=months)
        self.datetime_string = self.my_datetime.strftime(FORMAT)
    
    @property
    def year(self) -> int:
        return self.my_datetime.year
    
    @property
    def month(self) -> int:
        return self.my_datetime.month
    
    @property
    def day(self) -> int:
        return self.my_datetime.day
    
    @property
    def week(self) -> int:
        return self.my_datetime.isocalendar()[1]
    
    @property
    def weekday(self) -> int:
        return self.my_datetime.isoweekday()
    
    @property
    def hour(self) -> int:
        return self.my_datetime.hour
    
    @property
    def minute(self) -> int:
        return self.my_datetime.minute
