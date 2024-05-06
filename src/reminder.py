from recurrence import Recurrence, CLASS_NAME_TO_CONSTRUCTOR
from datetime_wrapper import DateTimeWrapper
from typing import Dict, List
from typing_extensions import Self
from uuid import uuid4


class Reminder:
    def __init__(self, id: str, title: str, message: str, recurrence: Recurrence) -> None:
        self.id: str = id
        self.title: str = title
        self.message: str = message
        self.recurrence: Recurrence = recurrence
    
    def __eq__(self, other):
        if isinstance(other, Reminder):
            return self.recurrence.next_recur_dt_wrapper == other.recurrence.next_recur_dt_wrapper
        else:
            raise TypeError("Unsupported operand type. Can only compare Reminder objects.")
    
    def __lt__(self, other: Self) -> bool:
        if isinstance(other, Reminder):
            return self.recurrence.next_recur_dt_wrapper < other.recurrence.next_recur_dt_wrapper
        else:
            raise TypeError("Unsupported operand type. Can only compare Reminder objects.")
    
    def __gt__(self, other: Self) -> bool:
        if isinstance(other, Reminder):
            return self.recurrence.next_recur_dt_wrapper > other.recurrence.next_recur_dt_wrapper
        else:
            raise TypeError("Unsupported operand type. Can only compare Reminder objects.")

    def should_remind_now(self) -> bool:
        current_dt_wrapper: DateTimeWrapper = DateTimeWrapper()
        return self.recurrence.should_recur(current_dt_wrapper)
    
    def task_finished(self) -> bool:
        return self.recurrence.is_finished()


class ReminderManager:
    def __init__(self) -> None:
        self.reminders: Dict[str, Reminder] = {}

    def add_reminder(self, title: str, message: str, recurrence_type: str, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, interval: int = 1, list: List[int] = None) -> None:
        id = uuid4()
        recurrence_class = CLASS_NAME_TO_CONSTRUCTOR[recurrence_type]
        if recurrence_type == "Once":
            recurrence = recurrence_class(start_dt_wrapper)
        elif recurrence_type == "Hour" or recurrence_type == "Day":
            recurrence = recurrence_class(start_dt_wrapper, end_dt_wrapper, interval)
        else:
            recurrence = recurrence_class(start_dt_wrapper, end_dt_wrapper, interval, list)
        reminder = Reminder(id, title, message, recurrence)
        self.reminders[id] = reminder
        self.reminders = dict(sorted(self.reminders.items(), key=lambda item: item[1]))

    def remove_reminder(self, reminder_id: str) -> None:
        del self.reminders[reminder_id]

    def get_due_reminders(self) -> List[Reminder]:
        due_reminders: List[Reminder] = []
        for reminder in self.reminders.values():
            if reminder.should_remind_now():
                due_reminders.append(reminder)
        return due_reminders
    
    def remove_finished_reminders(self) -> None:
        for reminder in self.reminders.values():
            if reminder.task_finished():
                self.remove_reminder(reminder.id)
    