from .globals import *

def makeToFile(path): #takes either a filename or ID, if filename it returns it, otherwise it adds .md 
    if not path.endswith(".md"):
        path = path + ".md"
    return path

def makeToID(path):
    if path.endswith(".md"):
        return path[:-3]

def shortPath(path):
    for startOfPath in [filesPath + "/",trashPath + "/"]:
        if path.startswith(startOfPath):
            return(path.replace(startOfPath,""))
        else:
            return path


def dataPath(pathEnd):
    if pathEnd.startswith(pathStart):
        return pathEnd
    return pathJoin(pathStart,pathEnd)

def pathJoin(pathA,pathB):
    path0, path1 = pathA, pathB
    if path0.endswith("/"):
        path0 = path0[:len(path0)-1]
    if path1.startswith("/"):
        path1 = path1[1:]
    return f"{path0}/{path1}"


def dictElement(dictionary):
    key, value = next(iter(dictionary.items()))
    return key,  value

def clearDuplicates(arr):
    newArr = []
    for element in arr:
        if element not in newArr:
            newArr.append(element)
    return newArr

def rotate(arr):
    newArr = []
    maxLength = max([len(i) for i in arr])

    for i in range(maxLength):
        row = []
        for col in arr:
            row.append(col[i])
        newArr.append(row)
    return newArr