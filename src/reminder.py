from recurrence import Recurrence, CLASS_NAME_TO_CONSTRUCTOR
from datetime_wrapper import DateTimeWrapper
from typing import Dict, List
from typing_extensions import Self
from uuid import uuid4
from db import DB
import atexit


class Reminder:
    def __init__(self, reminder_id: str, title: str, message: str, recurrence_type: str, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, next_recur_dt_wrapper: DateTimeWrapper = None, interval: int = 1, list: List[int] = None) -> None:
        self.reminder_id: str = reminder_id
        self.title: str = title
        self.message: str = message

        recurrence_class = CLASS_NAME_TO_CONSTRUCTOR[recurrence_type]
        if recurrence_type == "Once":
            recurrence = recurrence_class(start_dt_wrapper)
        elif recurrence_type == "Hour" or recurrence_type == "Day":
            recurrence = recurrence_class(start_dt_wrapper, end_dt_wrapper, interval)
            if next_recur_dt_wrapper:
                recurrence.next_recur_dt_wrapper = next_recur_dt_wrapper
        else:
            recurrence = recurrence_class(start_dt_wrapper, end_dt_wrapper, interval, list)
            if next_recur_dt_wrapper:
                recurrence.next_recur_dt_wrapper = next_recur_dt_wrapper

        self.recurrence: Recurrence = recurrence
        self.next_recur_dt_wrapper: DateTimeWrapper = self.recurrence.next_recur_dt_wrapper
    
    def __repr__(self) -> str:
        return f"Reminder(title={self.title}, message={self.message}, recur_datetime={self.next_recur_dt_wrapper}, Recurrence={self.recurrence})"
    
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
        res = self.recurrence.should_recur(current_dt_wrapper)
        self.next_recur_dt_wrapper: DateTimeWrapper = self.recurrence.next_recur_dt_wrapper
        return res
    
    def notify(self) -> None:
        print('''
              tile = {},
              message = {},
              next recurrence time = {}
              '''.format(self.title, self.message, self.recurrence.next_recur_dt_wrapper))
    
    def task_finished(self) -> bool:
        return self.recurrence.is_finished()


class ReminderManager:
    def __init__(self) -> None:
        self.reminders: Dict[str, Reminder] = {}
        self.db: DB = DB()
        self.__fetch_reminders_data_from_db()
        atexit.register(self.on_exit)

    def add_reminder(self, title: str, message: str, recurrence_type: str, start_dt_wrapper: DateTimeWrapper, end_dt_wrapper: DateTimeWrapper = None, next_recur_dt_wrapper: DateTimeWrapper = None, interval: int = 1, list: List[int] = None) -> None:
        reminder_id = str(uuid4())
        reminder = Reminder(
            reminder_id,
            title, 
            message, 
            recurrence_type, 
            start_dt_wrapper, 
            end_dt_wrapper,
            next_recur_dt_wrapper,
            interval, 
            list
        )
        self.reminders[reminder_id] = reminder
        self.reminders = dict(sorted(self.reminders.items(), key=lambda item: item[1]))
        self.db.add_reminder(reminder_id, title, message, recurrence_type, start_dt_wrapper, end_dt_wrapper, next_recur_dt_wrapper, interval, list)

    def remove_reminder(self, reminder_id: str) -> None:
        del self.reminders[reminder_id]
        self.db.remove_reminder(reminder_id)
    
    def notify_due_reminders(self) -> None:
        reminders: List[Reminder] = self.__get_due_reminders()
        for reminder in reminders:
            reminder.notify()
        self.__remove_finished_reminders()

    def __get_due_reminders(self) -> List[Reminder]:
        due_reminders: List[Reminder] = []
        for reminder_id, reminder in self.reminders.items():
            if reminder.should_remind_now():
                due_reminders.append(reminder)
                self.db.update_reminder(reminder_id=reminder_id, next_recur_dt_wrapper=reminder.next_recur_dt_wrapper)
        return due_reminders
    
    def __remove_finished_reminders(self) -> None:
        reminders_list = list(self.reminders.values())
        for reminder in reminders_list:
            if reminder.task_finished():
                self.remove_reminder(reminder.reminder_id)
    
    def __fetch_reminders_data_from_db(self) -> List[Reminder]:
        reminders_data = self.db.get_all_reminders()
        reminders = self.__create_reminders(reminders_data)
        for reminder in reminders:
            self.reminders[reminder.reminder_id] = reminder
        self.reminders = dict(sorted(self.reminders.items(), key=lambda item: item[1]))

    def __create_reminders(self, reminders_data):
        created_reminders = []
        for reminder_data in reminders_data:
            start_dt_wrapper = DateTimeWrapper(
                reminder_data[6], 
                reminder_data[7], 
                reminder_data[8], 
                reminder_data[9], 
                reminder_data[10]
            )

            if reminder_data[11] is not None:
                end_dt_wrapper = DateTimeWrapper(
                    reminder_data[11], 
                    reminder_data[12], 
                    reminder_data[13], 
                    reminder_data[14], 
                    reminder_data[15]
                )
            else:
                end_dt_wrapper = None
            
            next_recur_dt_wrapper = DateTimeWrapper(
                reminder_data[16], 
                reminder_data[17], 
                reminder_data[18], 
                reminder_data[19], 
                reminder_data[20]
            )

            reminder = Reminder(
                reminder_data[0],
                reminder_data[1], 
                reminder_data[2], 
                reminder_data[3], 
                start_dt_wrapper, 
                end_dt_wrapper,
                next_recur_dt_wrapper,
                reminder_data[4], 
                self.__convert_str_to_list(reminder_data[5])
            )
            created_reminders.append(reminder)
        return created_reminders
    
    def __convert_str_to_list(self, list_int_str: str) -> List[int]:
        return [int(x) for x in list_int_str.split(',')] if list_int_str else []
    
    def show_all_reminders(self):
        print("Stored Reminders: ")
        for reminder_id, reminder in self.reminders.items():
            print(reminder_id, reminder)

    def on_exit(self):
        self.show_all_reminders()
        self.db.close()
    