from reminder import ReminderManager
from datetime_wrapper import DateTimeWrapper
import time


TIME_CHECK_INTERVAL_SECONDS: float = 10

def app():
    reminder_manager: ReminderManager = ReminderManager()
    reminder_manager.show_all_reminders()
    reminder_manager.add_reminder(title="hi", message="test message", recurrence_type="Once",
                                  start_dt_wrapper=DateTimeWrapper(2024, 3, 9, 12, 00))
    while (True):
        reminder_manager.notify_due_reminders()
        time.sleep(TIME_CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    app()
