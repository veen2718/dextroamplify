from .config import *
from .tools import *
import os
from tools.yamlFrontmatter import *

def buildTaskCache():
    global taskCache
    taskCache = {}
    for path in getAllTaskPathsLocal():
        taskCache[path] = readTaskLocal(path)

def readTaskLocal(path):
    path = makeToFile(path)
    yaml, md = readFrontmatter(path)
    return yaml

def getAllTaskPathsLocal(filesPath=filesPath):
    allTaskPaths = []
    for dirPath, dirNames, fileNames in os.walk(filesPath):
        for file in fileNames:
            if file.endswith(".md"):
                filePath = os.path.join(dirPath, file)
                yaml, md = readFrontmatter(filePath)
                if yaml:
                    allTaskPaths.append(filePath)
    return allTaskPaths