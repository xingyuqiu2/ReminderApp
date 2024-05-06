from datetime_wrapper import DateTimeWrapper
from datetime import datetime, timedelta
import bisect
import calendar

a = datetime(2020, 1, 1, 10, 30)
b = datetime(2022, 1, 1, 12, 29)
start = DateTimeWrapper(2020, 1, 1, 10, 30)
cur = DateTimeWrapper(2022, 1, 1, 12, 29)

print(cur.get_diff_days_hours_minutes(start))
print(start.get_diff_days_hours_minutes(cur))
td = b - a
print(td.seconds//3600)
print((td.seconds//60)%60)

print(DateTimeWrapper(2023, 12, 31, 23, 59).week)
print(DateTimeWrapper(2023, 12, 31, 23, 59).weekday)
print(DateTimeWrapper(2022, 3, 1, 9, 30) == DateTimeWrapper(2022, 3, 1, 9, 30))

weekdays = [2,4,1,3,6]
weekdays = sorted(weekdays)
if 7 in weekdays:
    weekdays = [7] + weekdays[:-1]
print(weekdays)

a = bisect.bisect_left([2,4,6,8,9], 10)
print(a)
print(calendar.monthrange(2023, 3)[1])

d = datetime(2020, 1, 1, 10, 30)
d += timedelta(minutes=-1)
print(d)
print(datetime(2020, 1, 1, 10, 29) < datetime(2020, 1, 1, 10, 30))