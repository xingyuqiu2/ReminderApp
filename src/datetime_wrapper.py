from datetime import datetime
from typing_extensions import Self
from typing import Tuple


FORMAT = "%Y-%m-%d %H:%M"

class DateTimeWrapper:
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int) -> None:
        self.my_datetime = datetime(year, month, day, hour, minute)
        self.datetime_string = self.my_datetime.strftime(FORMAT)
    
    def __repr__(self) -> str:
        return self.datetime_string
    
    def get_diff_days_hours_minutes(self, other: Self) -> Tuple[int, int, int]:
        if self.my_datetime > other.my_datetime:
            td = self.my_datetime - other.my_datetime
        else:
            td = other.my_datetime - self.my_datetime
        return td.days, td.seconds//3600, (td.seconds//60)%60
    
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
