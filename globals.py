from .config import *

from datetime import datetime

DEBUG = 2


parseableData = [
    #defaults
    "title",
    "section",
    "group",
    "status",

    #other
    "subtasks",
    "event-date",
    "class",
    "event-time",
    "due-date",
    "due-time",
    "tags",
    "dates",
    "times"
]



def currentDate():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def currentTime():    
    now = datetime.now()
    return now.strftime("%H:%M")

def currentTime2():
    now = datetime.now()
    return now.strftime("%H:%M:%S")