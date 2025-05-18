from .cache import taskCache

from .globals import *
from tools.yamlFrontmatter import *
from tools.listtools import *
from tools.jsonFunctions import *
from .tools import *
from .config import *

import os
import re

def getAllTaskPaths(filesPath=filesPath):
    return taskCache.keys()

def readTask(path):
    return taskCache[path]

def writeTask(path, data):
    path = makeToFile(path)
    writeFrontmatter(path, data)
    taskCache[path] = data

def deleteTaskFile(ID):
    path = shortPath(makeToFile(ID))
    newPath = dataPath(f".trash/tasks/{path}")
    path = dataPath(pathJoin("tasks",path))
    os.rename(path,newPath)
    taskCache.pop(path, None)
    print(f"deleted {path}\nnewpath: {newPath}")

    
    
    

def getPathTags(allDict = False):
    allPaths = getAllTaskPaths()
    allTasks = [readTask(path) for path in allPaths]
    allPathTags = [taskData.get("path-tags",[]) for taskData in allTasks]
    
    allPathTags = [item for innerList in allPathTags for item in innerList]
    allTagPaths0 = [pathTag.split("/") for pathTag in allPathTags]

    def recursiveSort(allTagPaths):
        x = max([len(tagPath) for tagPath in allTagPaths])
        if not allTagPaths or not any(tagPath for tagPath in allTagPaths):
            return []
        
        pathBases = []
        for tagPath in allTagPaths:
            if tagPath:
                pathBases.append(tagPath[0])
        pathBases = clearDuplicates(pathBases)
        newTagPaths = [
            {pathBase:recursiveSort([
                tagPath[1:] for tagPath in allTagPaths if tagPath and tagPath[0] == pathBase
            ])} for pathBase in pathBases
        ]
        if not newTagPaths or not any(x for x in newTagPaths):
            return []
        if allDict:
            return newTagPaths
        newTagPaths2 = [list(tagPath)[0] if len(tagPath) == 1 and not list(tagPath.values())[0] else tagPath for tagPath in newTagPaths]

        return newTagPaths2
    
    allTagPaths1 = recursiveSort(allTagPaths0)
    return allTagPaths1


    
def getPathTagsPaths(tagChildren=getPathTags()):
    newTagChildren = []
    for tagChild in tagChildren:
        if type(tagChild) == dict:
            tagChildName, tagGrandchildren = dictElement(tagChild)
            newTagChildren += [f"{tagChildName}/{tagGrandchildName}" for tagGrandchildName in getPathTagsPaths(tagGrandchildren)]
        elif type(tagChild == str):
            newTagChildren.append(tagChild)
    return newTagChildren


def getChildrenOf(parentTask, endsOnly = False):
    allPaths = [path.split("/") for path in getPathTagsPaths()]
    relevantPaths = [path for path in allPaths if parentTask in path]
    # print(relevantPaths)
    relevantPaths2 =[]
    for path in relevantPaths:
        i = path.index(parentTask)
        relevantPaths2.append(path[:i+2])
    relevantPaths3 = []
    for path in relevantPaths2:
        if path not in relevantPaths3:
            relevantPaths3.append(path)
    if endsOnly:
        return [pathList[-1] for pathList in relevantPaths3]
    return relevantPaths3


    