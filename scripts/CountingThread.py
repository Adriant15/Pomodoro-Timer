"""Counting Thread

This script creates a seperate thread to count down a specific amount of time.
This scripts depends on instantiating class (master) to provide method implementation
for finish() and update_time_remaining() methods.

Laste edited: 2020-12-24
"""

import threading
import datetime

class CountingThread(threading.Thread):

    def __init__(self, master, start_time, end_time):
        super().__init__()
        self.master = master
        self.start_time = start_time
        self.end_time = end_time

        self.end_now = False
        self.paused = False
        self.force_quit = False

    def run(self):
        """Continously run main loop until count down timer is paused, time ends or force stops.

        If timer is paused, the while loops without performing any operation.
        If count down time ends/completes, the finish method, to be implmented by the class initiator, is called.
        If count down is force quit, this thread object is deleted.
        """

        while True:
            if not self.paused and not self.end_now and not self.force_quit:
                self.main_loop()
                if datetime.datetime.now() >= self.end_time:
                    if not self.force_quit:
                        self.master.finish()
                        break
            elif self.end_now:
                self.master.finish()
                break
            elif self.force_quit:
                del self.master.worker
                return
            else:
                continue
        return

    def main_loop(self):
        now = datetime.datetime.now()
        if now < self.end_time:
            time_difference = self.end_time - now
            mins, secs = divmod(time_difference.seconds, 60)    #returns tuple
            time_string = "{:02d}:{:02d}".format(mins, secs)
            if not self.force_quit:
                self.master.update_time_remaining(time_string)
