"""Log Window

This script creates a notebook with each tab representing a date when task(s)
was done using the Pomodoro timer. Each task stored in each tab is presented as
a tree view with the following headings: "Name", "Full 25 Minutes", "Time".

The instantiating class (master) must provide implmenation for get_unique_dates(),
get_tasks_by_date() and delete_task() method.

Laste edited: 2020-12-24
"""

import tkinter as tk
from tkinter import messagebox as msg
from tkinter import *

class LogWindow(tk.Toplevel):
    def  __init__(self, master):
        super().__init__()     #intit for tk.Toplevel

        self.title("Log")

        """Center log window next to main window on the right"""

        logWindow_width = 600
        logWIndow_height = 200

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        xLeft = int((screen_width/2) - (logWindow_width/2)) + 600
        yTop = int((screen_height/2) - (logWIndow_height/2))

        self.geometry(str(logWindow_width) + "x" + str(logWIndow_height) + "+" + str(xLeft) + "+" + str(yTop))
        self.resizable(width = 0, height = 0)

        #creates tabbed interface inside window
        self.notebook = ttk.Notebook(self)

        #define a dictionary in a "list" called a literal.
        self.tab_trees  =  {}

        style = ttk.Style()
        style.configure("Treeview", font=(None,12))
        style.configure("Treeview.Heading", font=(None, 14))

        """get_unique_dates() returns a list of unique datetime.

        example return: '2020-12-20 20:46:54.584119'. For log, we just want the date portion.
        """

        dates = self.master.get_unique_dates()

        """Formate unique dates to only get the date portion

        Enumerate(dates) addes a counter "index" to iterable
        the for loop replaces each item in dates list with just the firstportion of the date and time

        split() returns a list with the date and tiem splitted: ['2020-12-20', '20:46:54.584119']
        Get only the date portion .split()[0]
        """

        for index, date in enumerate(dates):
            dates[index] = date[0].split()[0]

        #turn dates list into a set to get the unique items and sort in descending order
        dates = sorted(set(dates), reverse = True)

        """Populate each tab with all tasks from a specific date and then add tab to notebook

        A list of task is returned by instantiating class (master) get_tasks_by_date() method. The
        returned attibutes are assigned to the headings of the treeview. Double clicking on a task
        is will trigger deletion method to remove task.
        """

        for date in dates:
            tab = tk.Frame(self.notebook)

            columns = ("name", "finished", "time")

            tree = ttk.Treeview(tab, columns = columns, show = "headings")

            tree.heading("name", text = "Name")
            tree.heading("finished", text = "Full 25 Minutes")
            tree.heading("time", text = "Time")

            tree.column("name", anchor = "center")
            tree.column("finished", anchor = "center")
            tree.column("time", anchor = "center")

            tasks = self.master.get_tasks_by_date(date)

            for task_name, task_finished, task_date in tasks:
                task_finished_text = "Yes" if task_finished else "No"
                task_time = task_date.split()[1]
                task_time_pieces = task_time.split(":")
                #Display only hours and minutes of task time
                task_time_pretty = "{}:{}".format(task_time_pieces[0], task_time_pieces[1])
                tree.insert("", tk.END, values = (task_name, task_finished_text, task_time_pretty))

            tree.pack(side = 'left', fill = tk.BOTH, expand = 1)

            scroll_bar = ttk.Scrollbar(tree, orient = "vertical", command = tree.yview, )
            scroll_bar.pack(side = 'right', fill='y')

            tree.configure(yscrollcommand = scroll_bar.set)

            #binds double-click to open delete task pane
            tree.bind("<Double-Button-1>", self.confirm_delete)

            #for index "date" in list tab_tress, store tree object
            self.tab_trees[date]  =  tree

            self.notebook.add(tab, text = date)

        self.notebook.pack(fill = tk.BOTH, expand = 1)

    """Delete selected task in tree view

    Deletes task from tree view and from databsed through instantiating class (master) delete_task()
    """

    def confirm_delete(self, event = None):
        #get tab label as a text and store in current_tab
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        tree = self.tab_trees[current_tab]
        selected_item_id = tree.selection()

        #tree.item returns a dictionary.
        #"values" holds row's list of task_name, task_finished_text, and task_time_pretty
        selected_item = tree.item(selected_item_id)

        #get first item in tree object, which is task_name
        if msg.askyesno("Delete Item?", "Delete" + selected_item["values"][0] + "?", parent = self):
            task_name = selected_item["values"][0]
            task_time = selected_item["values"][2]

            #join list containing current_tabl and task_time with a " "
            task_date = " ".join([current_tab, task_time])
            self.master.delete_task(task_name, task_date)
            tree.delete(selected_item_id)
