from data.globals import *
from backend.cache import taskCache
from .taskfiles import readTask

from veenTools.yamlFrontmatter import *

from datetime import datetime
from pathvalidate import sanitize_filename

def makeTask(name,data=dict(),makeFile=False):
    currentDateTime =datetime.now()
    ID = sanitize_filename(f"{name}{currentDateTime.strftime("%Y%m%d%H%M%S")}")
    taskData = {
        "ID":ID,
        "title":name,
        "created-time":currentTime2(),
        "created-date":currentDate(),
        } | data
    if makeFile:
        filePath = f"{filesPath}/{ID}.md"
        writeFrontmatter(filePath,taskData)
        taskCache[filePath] = taskData


    return taskData

class taskObject:

    def __init__(self, taskPath):
        self.path = taskPath
        self.data = readTask(taskPath)
    
    def get(self,x):
        return self.data.get(x)

    def isTerminal(self):
        children = getChildrenOf(self.get("title"))
    