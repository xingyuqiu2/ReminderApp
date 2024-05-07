from datetime_wrapper import DateTimeWrapper
from typing import List, Any, Tuple
import sqlite3


DB_NAME = "reminder_db"

class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_NAME)
        self.__create_table()

    def __create_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datetime_wrappers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                hour INTEGER,
                minute INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                reminder_id TEXT PRIMARY KEY,
                title TEXT,
                message TEXT,
                recurrence_type TEXT,
                start_dt_wrapper_id INTEGER,
                end_dt_wrapper_id INTEGER,
                next_recur_dt_wrapper_id INTEGER,
                interval INTEGER,
                list TEXT,
                FOREIGN KEY (start_dt_wrapper_id) REFERENCES datetime_wrappers(id),
                FOREIGN KEY (end_dt_wrapper_id) REFERENCES datetime_wrappers(id),
                FOREIGN KEY (next_recur_dt_wrapper_id) REFERENCES datetime_wrappers(id)
            )
        ''')
        self.conn.commit()

    def add_reminder(self, reminder_id, title, message, recurrence_type, start_dt_wrapper, end_dt_wrapper=None, next_recur_dt_wrapper=None, interval=1, list=None):
        start_dt_wrapper_id = self.__add_datetime_wrapper(start_dt_wrapper.year, start_dt_wrapper.month, start_dt_wrapper.day, start_dt_wrapper.hour, start_dt_wrapper.minute)
        end_dt_wrapper_id = self.__add_datetime_wrapper(end_dt_wrapper.year, end_dt_wrapper.month, end_dt_wrapper.day, end_dt_wrapper.hour, end_dt_wrapper.minute) if end_dt_wrapper else None
        next_recur_dt_wrapper_id = self.__add_datetime_wrapper(next_recur_dt_wrapper.year, next_recur_dt_wrapper.month, next_recur_dt_wrapper.day, next_recur_dt_wrapper.hour, next_recur_dt_wrapper.minute) if next_recur_dt_wrapper else start_dt_wrapper_id
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (reminder_id, title, message, recurrence_type, start_dt_wrapper_id, end_dt_wrapper_id, next_recur_dt_wrapper_id, interval, list)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (reminder_id, title, message, recurrence_type, start_dt_wrapper_id, end_dt_wrapper_id, next_recur_dt_wrapper_id, interval, self.__list_of_int_to_str(list)))
        self.conn.commit()
    
    def __add_datetime_wrapper(self, year: int, month: int, day: int, hour: int, minute: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO datetime_wrappers (year, month, day, hour, minute)
            VALUES (?, ?, ?, ?, ?)
        ''', (year, month, day, hour, minute))
        self.conn.commit()
        return cursor.lastrowid  # Return the id of the inserted row

    def get_all_reminders(self) -> List[Any]:
        cursor = self.conn.cursor()
        cursor.execute('''
                       SELECT reminders.reminder_id, reminders.title, reminders.message, reminders.recurrence_type, 
                              reminders.interval, reminders.list,
                              start.year AS start_year, start.month AS start_month, start.day AS start_day, 
                              start.hour AS start_hour, start.minute AS start_minute,
                              end.year AS end_year, end.month AS end_month, end.day AS end_day, 
                              end.hour AS end_hour, end.minute AS end_minute,
                              next.year AS next_year, next.month AS next_month, next.day AS next_day, 
                              next.hour AS next_hour, next.minute AS next_minute
                        FROM reminders
                        LEFT JOIN datetime_wrappers AS start ON reminders.start_dt_wrapper_id = start.id
                        LEFT JOIN datetime_wrappers AS end ON reminders.end_dt_wrapper_id = end.id
                        LEFT JOIN datetime_wrappers AS next ON reminders.next_recur_dt_wrapper_id = next.id
                       ''')
        return cursor.fetchall()

    def remove_reminder(self, reminder_id) -> None:
        result_tuple = self.__get_dt_wrapper_id_by_reminder_id(reminder_id)
        if result_tuple:
            (start_dt_wrapper_id, end_dt_wrapper_id, next_recur_dt_wrapper_id) = result_tuple

            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM reminders WHERE reminder_id = ?', (reminder_id,))
            self.__remove_datetime_wrapper(start_dt_wrapper_id)
            self.__remove_datetime_wrapper(end_dt_wrapper_id)
            self.__remove_datetime_wrapper(next_recur_dt_wrapper_id)
            self.conn.commit()
    
    def __remove_datetime_wrapper(self, id) -> None:
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM datetime_wrappers WHERE id = ?', (id,))
        self.conn.commit()

    def update_reminder(self, reminder_id: str, title: str = None, message: str = None, recurrence_type: str = None, 
                        start_dt_wrapper: DateTimeWrapper = None, end_dt_wrapper: DateTimeWrapper = None, next_recur_dt_wrapper: DateTimeWrapper = None, 
                        interval: int = None, list: List[int] = None) -> None:
        cursor = self.conn.cursor()
        update_query = 'UPDATE reminders SET '
        update_values = []

        result_tuple = self.__get_dt_wrapper_id_by_reminder_id(reminder_id)
        if result_tuple:
            (start_dt_wrapper_id, end_dt_wrapper_id, next_recur_dt_wrapper_id) = result_tuple

        if title:
            update_query += 'title = ?, '
            update_values.append(title)
        if message:
            update_query += 'message = ?, '
            update_values.append(message)
        if recurrence_type:
            update_query += 'recurrence_type = ?, '
            update_values.append(recurrence_type)
        if start_dt_wrapper:
            self.__remove_datetime_wrapper(start_dt_wrapper_id)
            start_dt_wrapper_id = self.__add_datetime_wrapper(start_dt_wrapper.year, start_dt_wrapper.month, start_dt_wrapper.day, start_dt_wrapper.hour, start_dt_wrapper.minute)
            update_query += 'start_dt_wrapper_id = ?, '
            update_values.append(start_dt_wrapper_id)
        if end_dt_wrapper:
            self.__remove_datetime_wrapper(end_dt_wrapper_id)
            end_dt_wrapper_id = self.__add_datetime_wrapper(end_dt_wrapper.year, end_dt_wrapper.month, end_dt_wrapper.day, end_dt_wrapper.hour, end_dt_wrapper.minute)
            update_query += 'end_dt_wrapper_id = ?, '
            update_values.append(end_dt_wrapper_id)
        if next_recur_dt_wrapper:
            self.__remove_datetime_wrapper(next_recur_dt_wrapper_id)
            next_recur_dt_wrapper_id = self.__add_datetime_wrapper(next_recur_dt_wrapper.year, next_recur_dt_wrapper.month, next_recur_dt_wrapper.day, next_recur_dt_wrapper.hour, next_recur_dt_wrapper.minute)
            update_query += 'next_recur_dt_wrapper_id = ?, '
            update_values.append(next_recur_dt_wrapper_id)
        if interval:
            update_query += 'interval = ?, '
            update_values.append(interval)
        if list:
            update_query += 'list = ?, '
            update_values.append(self.__list_of_int_to_str(list))

        # Remove the last comma and space from the query string
        update_query = update_query[:-2]

        # Add the WHERE clause to update only the specified reminder
        update_query += ' WHERE reminder_id = ?'
        update_values.append(reminder_id)

        cursor.execute(update_query, update_values)
        self.conn.commit()
    
    def __get_dt_wrapper_id_by_reminder_id(self, reminder_id: str) -> Tuple[int, int, int]:
        cursor = self.conn.cursor()
        cursor.execute('''
                       SELECT reminders.start_dt_wrapper_id, 
                              reminders.end_dt_wrapper_id, 
                              reminders.next_recur_dt_wrapper_id
                        FROM reminders
                        WHERE reminders.reminder_id = ?
                       ''', (reminder_id,))
        result_list = cursor.fetchall()
        if result_list:
            return result_list[0]
        return None
    
    def __list_of_int_to_str(self, list: List[int]) -> str:
        return ','.join(map(str, list or []))

    def close(self):
        self.conn.close()
    