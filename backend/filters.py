if __name__ == "__main__":
    from .cache import buildTaskCache
    buildTaskCache()
from backend.cache import taskCache

from data.globals import *
from files.taskfiles import *
from backend.boards import *
from files.task import *
from dashboards.tableBoard import tableBoard

def byPathTag(*pathTags):
    # print("byPathTag1", pathTags)
    allPaths = getAllTaskPaths()
    filteredPaths = []
    for path in allPaths:
        taskData = readTask(path)
        if any(pathTag in taskData.get("path-tags",[]) for pathTag in pathTags):
            filteredPaths.append(path)
    # print("byPathTag2", filteredPaths)
    return filteredPaths


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



def standardTable(basePathTag,*pathTagsInput):
    pathTags = [i for i in pathTagsInput] #cloning to avoid errors
    if not pathTags:
        pathTags = getChildrenOf(basePathTag, endsOnly=True)
    return tableBoard([
            Column(
                lambda pathTag=pathTag: byPathTag(f"{basePathTag}/{pathTag}"),
                title=pathTag
            )
            for pathTag in pathTags
        ], title=basePathTag)
    

if __name__ == "__main__": 
    x = getChildrenOf("Keyboarding")
    print(x)
    print(getPathTags())
    print(getPathTagsPaths())