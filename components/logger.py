import datetime as dt
from time import time


class Logger:
    @staticmethod
    def Log(logMessage: str):

        f = open("log.txt", "w")
        date = dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d %H:%M:%S')
        logMessage = logMessage + date
        f.write(logMessage)
        f.close()
