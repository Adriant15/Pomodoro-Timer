# Pomodoro Timer

Simple servlet app created with Python and Python libraries.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a simple timer app that help the user implement the pomodoro technique, which is do tasks in 25 minute bursts. The app also keeps a log of what and when the task(s) were done if 25 minutes was used to perform said task(s). The app uses Python and Python libraries to implement the GUI and database management. A secondary script was written to generate a sample database file for testing and demonstrating the app.
	
## Technologies
Project is created with:

* ATOM 1.53.0
* Python 3.8

Python libraries used:

* Threading
* Datetime
* Tkinter
* Sqlite3
* Random
* Os
* Notebook
* Tree view
	
## Setup
To start .EXE file without sample database:

1. Navigate to "exe files" folder and run "PomodoroTimer.exe".

To start .EXE file with sample database:

1.	Navigate to "exe files" folder and run "GenerateSampleDatabase.exe".
2.	Verifiy that a file has been generated named "pomodoro.db".
3.	If required, move "pomodoro.db" file to the same directory as the "PomodoroTimer.exe" file.
4.	Run "PomodoroTimer.exe" and verify that there are data in the logger (from menu bar or CTRL+L from main app window).

To run app in command line or IDE (ie. ATOM):

1.	Install Python 3 or higher.
1.	Open command line interface of choice or open a terminal within ATOM.
2.	Download all scripts from the "scripts" folder to a local folder location.
2.	In the command line interface or terminal, changes the current directory to local folder location using -cd command.
3.	To run the app with sample database, run "GenerateSampleDatabase.py" before running "PomodoroTimer.py"

## App Features

<img src="https://raw.githubusercontent.com/Adriant15/Pomodoro-Timer/main/screenshots/timer_start.jpg" width=35% height=35%>  <img src="https://raw.githubusercontent.com/Adriant15/Pomodoro-Timer/main/screenshots/timer_resume.jpg" width=35% height=35%>

* User can specify the name of the task to focus on for the next 25 minutes.
* The timer has pause and end-early function. 
* Information about teach task is stored locally in sqlite3 database.

<img src="https://raw.githubusercontent.com/Adriant15/Pomodoro-Timer/main/screenshots/timer_logger.JPG" width=35% height=35%>

* The logger is build using Tkinter notebook with a tab representing a specific date and lists all the task(s) done with the app on that date.
* For debugging and/or demonstration, a separate python script and .exe file has been included to generate a sample sqlite3 database file.

## Source

This app is inspired by tutorial David Love "Python Tkinter By Example" 

Improvement implemented:

* Separation of sample script code into three scripts with more defined purpose and ease of debugging.
* Added scrolling to each tab of the logger.
* Main GUI window appear in the middle of computer screen. 
* Logger appear right of the main GUI window.
* Python script to generate sample database file for app debugging and/or demonstration.
* Additional comments to explain algorithms locally in code.

