from typing import List
from datetime_wrapper import DateTimeWrapper
from abc import ABC, abstractmethod
import calendar
import bisect
import copy


class Recurrence(ABC):
    def __init__(self, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper, interval: int) -> None:
        self.start_dt_wrapper: DateTimeWrapper = copy.deepcopy(start_dt_wrapper)
        self.end_dt_wrapper: DateTimeWrapper = copy.deepcopy(end_dt_wrapper)
        self.interval: int = interval
        self.next_recur_dt_wrapper: DateTimeWrapper = copy.deepcopy(start_dt_wrapper)
        self.finished: bool = False
    
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        pass

    def _check_recurrence_and_update(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        if self.finished:   # when recurrence task is already done
            return False
        outdated_recurrence = False
        while self.next_recur_dt_wrapper < current_dt_wrapper:  # stored next recurrence time is outdated, update first
            self._set_next_recurrence_dt_wrapper()
            outdated_recurrence = True
        if not outdated_recurrence and current_dt_wrapper < self.next_recur_dt_wrapper:    # have not reach the time yet
            return False
        if self.next_recur_dt_wrapper == current_dt_wrapper:    # reach the next recurence time, update the next recurrence time
            self._set_next_recurrence_dt_wrapper()
        if self.end_dt_wrapper and self.next_recur_dt_wrapper > self.end_dt_wrapper:    # reach the end time, recurrence task is done
            self.finished = True
        return True

    def is_finished(self):
        return self.finished
    
    # @property
    # def next_recur_dt_wrapper(self) -> DateTimeWrapper:
    #     return self.next_recur_dt_wrapper
    
    # @next_recur_dt_wrapper.setter
    # def next_recur_dt_wrapper(self, dt_wrapper: DateTimeWrapper) -> None:
    #     self.next_recur_dt_wrapper = dt_wrapper


class Once(Recurrence):
    """
    Recurrence class representing occur only once.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper) -> None:
        super().__init__(start_dt_wrapper, start_dt_wrapper, 0)

    def __repr__(self) -> str:
        return f"Once(Occur once on {self.start_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        if self.finished:
            return False
        if current_dt_wrapper < self.next_recur_dt_wrapper:    # have not reach the time yet
            return False
        # reach the next occurence time
        self.finished = True
        return True

class Hour(Recurrence):
    """
    Recurrence class representing recurrence every certain number of hours.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, interval: int = 1) -> None:
        super().__init__(start_dt_wrapper, end_dt_wrapper, interval)

    def __repr__(self) -> str:
        return f"Hour(Recur every {self.interval} hour starting on {self.start_dt_wrapper} ending on {self.end_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        return super()._check_recurrence_and_update(current_dt_wrapper)
    
    def _set_next_recurrence_dt_wrapper(self):
        self.next_recur_dt_wrapper.increment(hours=self.interval)

class Day(Recurrence):
    """
    Recurrence class representing recurrence every certain number of days.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, interval: int = 1) -> None:
        super().__init__(start_dt_wrapper, end_dt_wrapper, interval)

    def __repr__(self) -> str:
        return f"Day(Recur every {self.interval} day starting on {self.start_dt_wrapper} ending on {self.end_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        return super()._check_recurrence_and_update(current_dt_wrapper)
    
    def _set_next_recurrence_dt_wrapper(self):
        self.next_recur_dt_wrapper.increment(days=self.interval)

class Week(Recurrence):
    """
    Recurrence class representing recurrence every certain number of weeks.
    Sunday is defined to be the start weekday of a week.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, interval: int = 1, weekdays: List[int] = None) -> None:
        super().__init__(start_dt_wrapper, end_dt_wrapper, interval)
        self.weekdays = sorted(weekdays) if weekdays else [start_dt_wrapper.weekday]

    def __repr__(self) -> str:
        return f"Week(Recur every {self.interval} week on {self.weekdays} weekdays starting on {self.start_dt_wrapper} ending on {self.end_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        return super()._check_recurrence_and_update(current_dt_wrapper)
    
    def _set_next_recurrence_dt_wrapper(self):
        weekday = self.next_recur_dt_wrapper.weekday
        same_week = True    # whether the next recurrence time is in the same week

        # check whether the next recurrence time is in the same week
        # find the next_weekday if yes
        # set same_week to False if no
        if weekday not in self.weekdays:  # next_recur_dt_wrapper is not in the list of weekdays, happens when weekday of start_dt_wrapper is not in the list
            next_idx = bisect.bisect_left(self.weekdays, weekday)
            if next_idx == len(self.weekdays):
                same_week = False
            else:
                next_weekday = self.weekdays[next_idx]
        else:
            idx = self.weekdays.index(weekday)
            if idx == len(self.weekdays) - 1:   # reach the end the week
                same_week = False
            else:
                next_weekday = self.weekdays[idx + 1]

        # update the next recurrence time
        if not same_week:    # not in the same week
            delta_days = ((self.interval - 1) * 7) + (7 - weekday + self.weekdays[0])
        else:   # in the same week
            delta_days = (next_weekday - weekday + 7) % 7
        self.next_recur_dt_wrapper.increment(days=delta_days)

class Month(Recurrence):
    """
    Recurrence class representing recurrence every certain number of months.
    """
    def __init__(self, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, interval: int = 1, days: List[int] = None) -> None:
        super().__init__(start_dt_wrapper, end_dt_wrapper, interval)
        self.days = sorted(days) if days else [start_dt_wrapper.day]

    def __repr__(self) -> str:
        return f"Month(Recur every {self.interval} month on {self.days} days starting on {self.start_dt_wrapper} ending on {self.end_dt_wrapper})"
    
    def should_recur(self, current_dt_wrapper: DateTimeWrapper) -> bool:
        return super()._check_recurrence_and_update(current_dt_wrapper)
    
    def _set_next_recurrence_dt_wrapper(self):
        day = self.next_recur_dt_wrapper.day
        same_month = True    # whether the next recurrence time is in the same month

        # check whether the next recurrence time is in the same month
        # find the next_day if yes
        # set same_month to False if no
        if day not in self.days:  # next_recur_dt_wrapper is not in the list of days, happens when day of start_dt_wrapper is not in the list
            next_idx = bisect.bisect_left(self.days, day)
            if next_idx == len(self.days):
                same_month = False
            else:
                next_day = self.days[next_idx]
        else:
            idx = self.days.index(day)
            if idx == len(self.days) - 1:   # reach the end the month
                same_month = False
            else:
                next_day = self.days[idx + 1]

        # update the next recurrence time
        if not same_month or next_day > calendar.monthrange(self.next_recur_dt_wrapper.year, self.next_recur_dt_wrapper.month)[1]:    # not in the same month, or the next day doesn't exist in the current month
            self.next_recur_dt_wrapper.increment(days=-day+1)
            self.next_recur_dt_wrapper.increment(months=self.interval)
            self.next_recur_dt_wrapper.increment(days=self.days[0] - 1)
        else:   # in the same month
            delta_days = next_day - day
            self.next_recur_dt_wrapper.increment(days=delta_days)

CLASS_NAME_TO_CONSTRUCTOR = {
    "Once": Once,
    "Hour": Hour,
    "Day": Day,
    "Week": Week,
    "Month": Month,
}
