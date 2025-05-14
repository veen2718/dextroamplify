from tools.yamlFrontmatter import *
from .globals import *

import os
from pathlib import Path

def getTaskData(taskPath):
    if not os.path.exists(taskPath):
        print(f"non-existent path given:\n{taskPath}\ninput() used to pause program")
        input()
        return ""
    data,md = readFrontmatter(taskPath)
    return data

def getParseableData(pathSection):
    if filesPath not in pathSection:
        taskPath = os.path.join(filesPath, pathSection)
    else:
        taskPath = pathSection
    taskPathObject = Path(taskPath)
    taskPathParts = taskPathObject.parts
    taskPathParent = taskPathObject.parent
    relativePath = Path(*taskPathParts[3:])
    relativeParent = relativePath.parent

    if not os.path.exists(taskPath):
        print(f"non-existent path given:\n{taskPath}\ninput() used to pause program")
        input()
        return ""
    
    data, md = readFrontmatter(taskPath)
    parsedData = dict()
    
    for parseableKey in parseableData:
        parsedValue = data.get(parseableKey)
        if parsedValue:
            parsedData[parseableKey] = parsedValue
    
    
    
    parsedData["hasLink"] = True
    parsedData["folderPath"] = str(taskPathParent)
    parsedData["filePath"] = str(taskPathObject)
    parsedData["link"] = f"[[{str(relativeParent)}|{parsedData["title"]}]]"
    return parsedData