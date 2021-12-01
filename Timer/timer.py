"""
This module contains the timer class with context manager and the Timer decorator
"""
import time
import logging
from functools import wraps


def Timed(f):
    """Timer decorator"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        s = time.time()
        result = f(*args, **kwargs)
        e = time.time()
        print(f'Function {f}: {e - s} seconds')
        return result

    return wrapped


logging.getLogger().setLevel(logging.WARNING)


class Timer(object):
    timerResults = {}  # Timer dictionary to store last result
    d = "seconds"
    warn_threshold = 60  # seconds

    def __init__(self, msg):  # initialization function
        self._startTime = None
        self.msg = msg

    def __enter__(self):
        """Start a new timer"""
        logging.info('The timer has started...')
        self._startTime = time.perf_counter()
        return self

    def __exit__(self, *args):
        """ Stops the timer and prints the time taken"""
        time_taken = time.perf_counter() - self._startTime
        self.timerResults["seconds"] = time_taken
        self.timerResults["minutes"] = time_taken / 60
        self.timerResults["hours"] = time_taken / 3600
        logging.info(f'{self.msg}: {self.timerResults[Timer.d]} {Timer.d}')
        print(f'{self.msg}: {self.timerResults[Timer.d]} {Timer.d}')
        logging.info('The timer has ended.')
        if time_taken > 60:
            logging.warning("Time taken has exceeded 1 minute")

    def retrieveLastResult(self):
        """ Retrieves that time taken from the timer results dictionary"""
        return self.timerResults[Timer.d]

    @classmethod
    def configureDisplayType(cls, display=d):
        """changes and stores 'd' which is used to pull the required display type"""
        """ display format is 'seconds', 'minutes' or 'hours' """
        # display = input("Enter display format in seconds, minutes or hours: ")
        cls.d = display
