"""Generate Sample Database for Pomodoro Timer App

This script creates sample sqlite3 data for demostration and testing of the
pomodoro timer app. By default, the sqlite3 database file generated will be named
"pomodoro.db". It will check if a local database file of the same name exists
and this script will backup the existing database file and rename with the date
of backup (for example:"pomodoro.db" -> "pomodoro_backup(12-29-2020).db")

By default, no changes in the PomodoroTimer.py code will need to be modified
to connect to this database in runQuery().

Laste edited: 2020-12-29
"""

import sqlite3
import random
import datetime
import os

class SampleDatabase():
    def __init__(self):
        create_tables="CREATE TABLE pomodoro (task text, finished integer, date text)"
        SampleDatabase.runQuery(create_tables)

    def createData(self):
        task_sql = "INSERT INTO pomodoro VALUES (?, ?, ?)"
        sampleDate = [23, 24, 25]
        for sampledate in sampleDate:
            currentDate = datetime.datetime(2020,12,sampledate, 8, 30, 0, 342380)
            for x in range(1,11):
                task_text = "Sample Task " + str(x)
                finished_int = random.randint(0, 1)
                data = (task_text, finished_int, currentDate)
                self.runQuery(task_sql, data)
                currentDate = currentDate + datetime.timedelta(hours = 1)

    def viewDB(self):
        results = self.runQuery("SELECT * FROM pomodoro", None, True)
        for line in results:
            print(line)

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
        
if __name__ == "__main__":

    """if "pomodoro.db" already exists, back it up by by renaming it with backup date extension"""

    if os.path.isfile("pomodoro.db"):
        backup_file_name = "pomodoro_backup(" + datetime.datetime.now().strftime("%m-%d-%Y") + ").db"
        os.rename(os.path.join(os.getcwd(), "pomodoro.db"), os.path.join(os.getcwd(), backup_file_name))

    #Method used for viewing database during debugging
    #sample.viewDB()

    sample = SampleDatabase()
    sample.createData()
