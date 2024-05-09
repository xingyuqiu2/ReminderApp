import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime_wrapper import DateTimeWrapper


TEXT_ENTRY_WIDTH = 50
TIME_ENTRY_WIDTH = 20

class AddReminderWindow(tk.Toplevel):
    def __init__(self, parent, app_instance, reminder_manager):
        super().__init__(parent)
        self.reminder_manager = reminder_manager
        self.title("Add Reminder")

        self.title_entry = tk.Entry(self, width=TEXT_ENTRY_WIDTH)
        self.message_entry = tk.Entry(self, width=TEXT_ENTRY_WIDTH)
        self.year_entry = tk.Entry(self, width=TIME_ENTRY_WIDTH)
        self.month_entry = tk.Entry(self, width=TIME_ENTRY_WIDTH)
        self.day_entry = tk.Entry(self, width=TIME_ENTRY_WIDTH)
        self.hour_entry = tk.Entry(self, width=TIME_ENTRY_WIDTH)
        self.minute_entry = tk.Entry(self, width=TIME_ENTRY_WIDTH)

        label_entry_pairs = [
            ("Title:", self.title_entry),
            ("Message:", self.message_entry),
            ("Year:", self.year_entry),
            ("Month:", self.month_entry),
            ("Day:", self.day_entry),
            ("Hour:", self.hour_entry),
            ("Minute:", self.minute_entry)
        ]

        for i, (label, entry) in enumerate(label_entry_pairs):
            tk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry.grid(row=i, column=1, padx=5, pady=5)

        self.recurrence_label = tk.Label(self, text="Recurrence Type:")
        self.recurrence_label.grid(row=7, column=0, padx=5, pady=5)
        self.recurrence_type = tk.StringVar()
        self.recurrence_type_picker = ttk.Combobox(self, textvariable=self.recurrence_type)
        self.recurrence_type_picker["values"] = ["Once", "Hour", "Day", "Week", "Month"]
        self.recurrence_type_picker.current(0)
        self.recurrence_type_picker.grid(row=7, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self, text="Add Reminder", command=self.add_reminder)
        self.add_button.grid(row=8, column=1, padx=5, pady=5)

        self.app_instance = app_instance

    def add_reminder(self):
        title = self.title_entry.get()
        message = self.message_entry.get()
        year_str = self.year_entry.get()
        month_str = self.month_entry.get()
        day_str = self.day_entry.get()
        hour_str = self.hour_entry.get()
        minute_str = self.minute_entry.get()
        recurrence_type = self.recurrence_type.get()

        try:
            start_dt_wrapper = DateTimeWrapper(int(year_str), int(month_str), int(day_str), int(hour_str), int(minute_str))
        except ValueError:
            messagebox.showwarning("Invalid Time", "Please enter time in the correct format")
            return

        reminder_id = self.reminder_manager.add_reminder(title, message, recurrence_type, start_dt_wrapper, None, None, 1, None)
        self.app_instance.add_reminder((reminder_id, title, message, start_dt_wrapper))
        self.destroy()

class ReminderAppView:
    def __init__(self, master, reminder_manager):
        self.master = master
        self.master.title("Reminder App")
        
        self.reminder_manager = reminder_manager
        self.reminders = self.reminder_manager.get_all_reminders()

        self.reminder_listbox = tk.Listbox(master, width=50, height=15)
        self.reminder_listbox.pack(pady=10)

        self.add_button = tk.Button(master, text="Add Reminder", command=self.open_add_window)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(master, text="Delete Reminder", command=self.remove_reminder)
        self.delete_button.pack(pady=5)

        self.update_reminder_list()

    def open_add_window(self):
        add_window = AddReminderWindow(self.master, self, self.reminder_manager)

    def add_reminder(self, reminder):
        self.reminders.append(reminder)
        self.update_reminder_list()

    def remove_reminder(self):
        try:
            selected_index = self.reminder_listbox.curselection()[0]
            reminder_id, _, _, _ = self.reminders[selected_index]
            self.reminder_manager.remove_reminder(reminder_id)
            del self.reminders[selected_index]
            self.update_reminder_list()
        except IndexError:
            messagebox.showwarning("Warning", "No reminder selected.")

    def update_reminder_list(self):
        self.reminder_listbox.delete(0, tk.END)
        for reminder in self.reminders:
            reminder_id, title, message, next_recur_dtwrapper = reminder
            self.reminder_listbox.insert(tk.END, f"{title} ({next_recur_dtwrapper}): {message}")
