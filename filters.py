from .globals import *
from .taskfiles import *
from .boards import *

def byPathTag(*pathTags,title=None):
    allPaths = getAllTaskPaths()
    filteredPaths = []
    for path in allPaths:
        taskData = readTask(path)
        if any(pathTag in taskData.get("path-tags",[]) for pathTag in pathTags):
            filteredPaths.append(path)
    return filteredPaths,title


def hasPathTag(*pathTags):
    allPaths = getAllTaskPaths()
    filteredPaths = []
    for path in allPaths:
        taskData = readTask(path)
        taskDataPathTags = taskData.get("path-tags",[])
        match = False
        for taskDataPathTag in taskDataPathTags:
            for pathTag in pathTags:
                if pathTag in taskDataPathTag:
                    match = True
        if match:
            filteredPaths.append(path)
    return filteredPaths

def filter(dataDict):
    allPaths = getAllTaskPaths()
    filteredPaths = []
    for path in allPaths:
        taskData = readTask(path)
        if dataDict.items() <= taskData.items():
            filteredPaths.append(path)
    return filteredPaths



def standard(basePathTag,*pathTagsInput):
    pathTags = [i for i in pathTagsInput] #cloning to avoid errors
    if not pathTags:
        pass
    return Table(
        columns = [
            Column(
                lambda: byPathTag(f"{basePathTag}/{pathTag}")
            )
            for pathTag in pathTags
        ],
        title=basePathTag
    )
    
