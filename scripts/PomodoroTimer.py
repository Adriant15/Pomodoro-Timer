"""Pomodoro Timer

This script creates a Pomodoro timer app and gui interface. The user will input
the name of a task he/she will concentrate for 25 minutes. The timer will count
down for 25 minutes and alert the user when the time is up and to take a short
break before the next task. This app includes a logger that keeps track of task(s)
performed for everyday this app is used.

Laste edited: 2020-12-24
"""

import sqlite3
import os
import time
import datetime
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from CountingThread import CountingThread
from LogWindow import LogWindow

class Timer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")

        """Center window on screen"""

        self.logWindow_width = 600
        self.logWIndow_height = 300

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        xLeft = int((screen_width/2) - (self.logWindow_width/2))
        yTop = int((screen_height/2) - (self.logWIndow_height/2))

        self.geometry(str(self.logWindow_width) + "x" + str(self.logWIndow_height) + "+" + str(xLeft) + "+" + str(yTop))
        self.resizable(width = 0, height = 0)

        """TTK Style"""

        style = ttk.Style()
        style.configure("TLabel", foreground = "black", background = "lightgrey", font = (None, 16), anchor = "center")
        style.configure("B.TLabel", font = (None, 40))
        style.configure("B.TButton", foreground = "black", background = "lightgrey", font = (None, 16), anchor = "center")
        style.configure("TEntry", foregound = "black", background = "white")

        """Timer GUI"""

        self.main_frame = tk.Frame(self, width = 500, height = 300, bg = "lightgrey")

        self.task_name_label = ttk.Label(self.main_frame, text = "Task Name:")
        self.task_name_entry = ttk.Entry(self.main_frame, font = (None, 16))

        self.start_button = ttk.Button(self.main_frame, text = "Start", command = self.start, style = "B.TButton")

        self.time_remaining_var = tk.StringVar(self.main_frame)
        self.time_remaining_var.set("25:00")
        self.time_remaining_label = ttk.Label(self.main_frame, textvar = self.time_remaining_var, style = "B.TLabel")

        self.pause_button = ttk.Button(self.main_frame, text = "Pause", command = self.pause, state = "disabled", style = "B.TButton")

        self.main_frame.pack(fill = tk.BOTH, expand = True)

        self.task_name_label.pack(fill = tk.X, pady = 15)
        self.task_name_entry.pack(fill = tk.X, padx = 50, pady = (0,20))
        self.start_button.pack(fill = tk.X, padx = 50)
        self.time_remaining_label.pack(fill = tk.X, pady = 15)
        self.pause_button.pack(fill = tk.X, padx = 50)

        """Menu for Log GUI"""

        self.menubar = tk.Menu(self, bg = "lightgrey", fg = "black")
        self.log_menu = tk.Menu(self.menubar, tearoff = 0, bg = "lightgrey", fg = "black")
        self.log_menu.add_command(label = "View Log", command = self.show_log_window, accelerator = "Ctrl+L")

        #create "Log" to menubar
        self.menubar.add_cascade(label = "Log", menu = self.log_menu)
        self.configure(menu = self.menubar)

        """Windows options"""

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)    #bind destory methon to window close
        self.task_name_entry.focus_set()
        self.bind("<Control-l>", self.show_log_window)

    #Defines start and end time and create a new coutdown timer instance.
    def setup_worker(self):
        now = datetime.datetime.now()
        in_25_mins = now + datetime.timedelta(minutes = 25)
        worker = CountingThread(self, now, in_25_mins)
        self.worker = worker

    """Start countdown timer thread and create one if object has not been created

    If this timer object instance does not have a countdown timer object attribute
    ("worker"), it calls setup_worker() to create it. This app does allow empty or
    duplicate task to be entered, so error message will be display in either cases.

    Once countdown timer object attribute is verified to exists, this method configures
    the starting states and displays for the GUI buttons, values and entry. Information
    about the current task is logged in sqlite3 databases through add_new_task()
    """

    def start(self):
        if not hasattr(self, "worker"):      #assign CountingThread object to worker object
            self.setup_worker()

        if not self.task_name_entry.get():
            msg.showerror("No Task", "Please enter a task name")
            return

        if self.task_is_duplicate():
            msg.showerror("Task Duplicate", "You have already performed this task today. Please enter a different task name")
            return

        self.task_name_entry.configure(state = "disabled")
        self.start_button.configure(text = "Finish", command = self.finish_early)
        self.time_remaining_var.set("25:00")
        self.pause_button.configure(state = "normal")
        self.task_finished_early = False
        self.add_new_task()
        self.worker.start()       #starts the thread

    """Pauses the countdown clock and keep track start and end time

    Whenever the pause button is pressed, the boolean state is flipped. If the
    boolean variable "paused" is true, the pause button will display "Resume" and
    will set the start_time to the current date time.

    When the app is resume, the button text will display "Pause". In addition,
    the total pause time is calculated by difference between the start_time (the time
    when the pause button was first pressed) and current time. This time difference
    is added to the end_time target.
    """

    def pause(self):
        self.worker.paused = not self.worker.paused

        if self.worker.paused:
            self.pause_button.configure(text = "Resume")
            self.worker.start_time = datetime.datetime.now()
        else:
            self.pause_button.configure(text = "Pause")
            end_timedelta = datetime.datetime.now() - self.worker.start_time
            self.worker.end_time = self.worker.end_time + datetime.timedelta(seconds = end_timedelta.seconds)

    """Defines Finish button action when task is completed before 25 minutes

    If a task is completed early, the start button text is reset to "Start". The
    task_finished_early boolean is set to true and will display in the logger. The
    end_now boolean is set to true, which will cause while loop in the CountingThread.py
    object to break after calling finish() located in PomodoroTimer.py.
    """

    def finish_early(self):
        self.start_button.configure(text = "Start", command = self.start)
        self.task_finished_early = True
        self.worker.end_now = True

    """Defines GUI state/display when a task is complete before/after 25 minutes

    All GUI entry, variable and buttons are reset to original state/value. If the
    full 25 minutes was used for a task, the mark_finished_task() is called to
    set the "finished" value to 1/True.

    At the end of the method, the instance of CountingThread object is deleted.
    Message is thrown to notify user that 25 minutes has elasped.
    """

    def finish(self):
        self.task_name_entry.configure(state = "normal")
        self.time_remaining_var.set("25:00")
        self.pause_button.configure(text = "Pause", state = "disabled")
        self.start_button.configure(text = "Start", command = self.start)

        if not self.task_finished_early:
                self.mark_finished_task()

        del self.worker
        msg.showinfo("Promodoro Finished", "Task Finished. Take a 5 minute break!")

    """Update the countdown timer to display elasped time.

    Takes current time (time_string) from CountingThread object and update the
    time_remaining_var. Calling update_idletasks will forces the app to refresh
    its display. Without this the timer may occasionally appear to miss seconds.
    """

    def update_time_remaining(self, time_string):
        self.time_remaining_var.set(time_string)
        self.update_idletasks()

    """Take current task and add a new row entry into the logger database

    The database consist of three values: task text, finished integer and date
    text. The task text is takend from the entry field. The finished integer
    defines if the task was finished early (value = 0/False) or full 25 minutes
    duration was used (value = 1/True). date text is variable value of
    task_started_time stored in PomodoroTimer object.

    The prepared statement will update database with the above three values. The
    prepared statement and values are passed to runQuery function to execute.
    """

    def add_new_task(self):
        task_name = self.task_name_entry.get()
        self.task_started_time = datetime.datetime.now()
        add_task_sql = "INSERT INTO pomodoro VALUES (?, 0, ?)"
        self.runQuery(add_task_sql, (task_name, self.task_started_time))

    """Update the database to reflect if full 25 minutes duration was used for a task

    The database consist of three values: task text, finished integer and date
    text. The task text is takend from the entry field. The finished integer
    defines if the task was finished early (value = 0/False) or worked on during
    the 25 minutes duration (value = 1/True). In this case, the finished integer
    will be set to 1. date text is variable value of task_started_time stored in
    PomodoroTimer object.

    The prepared statement will update database with the above three values. The
    prepared statement and values are passed to runQuery function to execute.
    """

    def mark_finished_task(self):
        task_name = self.task_name_entry.get()
        add_task_sql = "UPDATE pomodoro SET finished  =  ? WHERE task  =  ? and date  =  ?"
        self.runQuery(add_task_sql, ("1", task_name, self.task_started_time))

    def show_log_window(self, event = None):
        LogWindow(self)

    """Destory CountingThread object when GUI window is closed

    If PomodoroTimer still has instance of CountingThread object, the instance will
    be deleted. After 100 ms, the safel_destory() calls itself to verify that the
    CountingThread object is deleted and if this is so, the GUI window is closed.
    """

    def safe_destroy(self):
        if hasattr(self, "worker"):
            self.worker.force_quit = True
            self.after(100, self.safe_destroy)
        else:
            self.destroy()

    """Run sql query to get a list of unique datetime from database"""

    def get_unique_dates(self):
        dates_sql = "SELECT DISTINCT date FROM pomodoro ORDER BY date DESC"
        dates = self.runQuery(dates_sql, None, True)
        return dates

    """Run sql query to get all tasks performed on specific date"""

    def get_tasks_by_date(self, date):
        tasks_sql = "SELECT * FROM pomodoro WHERE date LIKE ?"
        date_like = date + "%"
        data = (date_like,)
        tasks = self.runQuery(tasks_sql, data, True)
        return tasks

    """Run sql query to delete a task from a specific date"""

    def delete_task(self, task_name, task_date):
        delete_task_sql = "DELETE FROM pomodoro WHERE task = ? AND date LIKE ?"
        task_date_like = task_date + "%"
        data = (task_name, task_date_like)
        self.runQuery(delete_task_sql, data)

    """Check if the a duplicate task is being entered

    This app does not allow duplicate task name for a specific date. A unique name
    for each task will ensure that the app only delete one task at a time.

    The prepared statement attempts to get a task from the database from the
    current date. The returned value is a string. If the task already exists, the
    len() of the return value will be non-zero number, which considered to be True.
    If an empty string is returned, this is considerd to be False.
    """

    def task_is_duplicate(self):
        task_name = self.task_name_entry.get()
        today = datetime.datetime.now().date()
        task_exisits_sql = "SELECT task FROM pomodoro WHERE task = ? AND date LIKE ?"
        today_like = str(today) + "%"
        data = (task_name, today_like)
        tasks = self.runQuery(task_exisits_sql, data, True)
        return len(tasks)

    """Static method to connect to sqlite3 database and run sql queries

    The method has three arguments. The "sql" parameter is the sql query in string.
    the "data" paramter tells the method if the sql query is prepared statement.
    By default, it is set to None/False. The third parameter "receive" tells the
    method if there's a return for the the sql query.
    """

    @staticmethod
    def runQuery(sql, data = None, receive = False):
        conn  =  sqlite3.connect("pomodoro.db")
        cursor  =  conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    """Static method to create table is sqlite3 database on startup"""

    @staticmethod
    def firstTimeDB():
        create_tables  =  "CREATE TABLE pomodoro (task text, finished integer, date text)"
        Timer.runQuery(create_tables)

"""Create and start instance of this class (Timer) and create database if needed"""

if __name__ == "__main__":
    timer = Timer()

    if not os.path.isfile("pomodoro.db"):
        timer.firstTimeDB()

    timer.mainloop()
