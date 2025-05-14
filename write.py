from tools.yamlFrontmatter import *
from .globals import *
from tools.jsonFunctions import *

def updateTask(path,newData):
    oldData, md = readFrontmatter(path)
    writeFrontmatter(path, oldData | newData)

def deleteTaskProperty(path, property):
    oldData, md = readFrontmatter(path)
    if oldData.get(property):
        del oldData[property]
        writeFrontmatter(path, oldData)
    else:
        print(f"property {property} not found in the task file")
