from threading import Timer
import time
import threading
from datetime import datetime, timedelta


class Scheduler():
    def __init__(self, target):
        self.is_running = False
        self.__should_continue = False
        self.__target = target
        self.__thread = None
        self.__time_roller = DateTimeRoller()

    def start(self, interval, minutes, hours=None):
        self.__interval = interval
        now = datetime.now()
        then = self.__time_roller.get_time(now, minutes, hours)
        sleep_time = (then - now).total_seconds()

        if not self.__should_continue and not self.is_running:
            self.__should_continue = True
            self.__start_timer(sleep_time)
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def stop(self):
        if self.__thread is not None:
            self.__should_continue = False # Just in case thread is running and cancel fails.
            self.__thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

    def __run(self):
        self.is_running = True
        self.__target()
        self.is_running = False
        self.__start_timer(self.__interval)

    def __start_timer(self, interval):
        if self.__should_continue: # Code could have been running when cancel was called.
            self.__thread = Timer(interval, self.__run)
            self.__thread.start()


class DateTimeRoller:
    def get_time(self, now, minutes, hours=None):
        s_hour = now.hour
        s_minute = now.minute

        if hours == None:
            if minutes > s_minute:
                min_delta = minutes - s_minute
                return now + timedelta(minutes=min_delta)
            else:
                return (now + timedelta(hours=1)).replace(minute=minutes)
        else:
            if hours > s_hour:
                hour_delta = hours - s_hour
                return (now + timedelta(hours=hour_delta)).replace(minute=minutes)
            else:
                return (now + timedelta(days=1)).replace(minute=minutes, hour=hours)
