
from .taskfiles import getPathTags



class Node:

    def __init__(self, name, chain):
        self.name = name
        self.chain =chain
        
        self.parent = None
        self.children =[]
    
    def display1(self):
        print(f"name: {self.name}")
        if self.parent:
            print(f"parent: {self.parent.name}")
        else:
            print(f"parent: {None}")
        print(f"children: {[child.name for child in self.children]}")
        print()
        for child in self.children:
            child.display1()
    
    def path(self):
        if self.name:
            if self.parent.name:
                return f"{self.parent.path()}/{self.name}"
            return self.name
    


class chain:
    def __init__(self):
        self.nodes = []
    def getTop(self):
        return [n for n in self.nodes if n.parent is None][0]
    
    def sortTopLevel(self):
        currentNodes = self.getTop().children
        allNodesSorted = []
        while currentNodes:
            nextNodes = []
            for i in currentNodes:
                allNodesSorted.append(i)
                nextNodes += i.children
            currentNodes = nextNodes
        return allNodesSorted
    
    def getFilteredBy(self,filterValue):
        nodes = self.sortTopLevel()
        for node in nodes:
            if node.name == filterValue or (node.name == filterValue.split("/")[-1] and node.path().endswith(filterValue)):
                return node




def buildChain(pathDict,chainObject = None,parentNode = None):
    topNode = False
    if chainObject is None:
        chainObject = chain()
        topNode = True
    
    (nodeTitle, children), = pathDict.items()
    currentNode = Node(nodeTitle, chainObject)
    chainObject.nodes.append(currentNode)
    currentNode.parent = parentNode
    
    if children:
        for child in children:
            currentNode.children.append(buildChain(child, chainObject, currentNode))
    if topNode:
        return chainObject
    else:
        return currentNode

def getPathTagNodes():
    x = getPathTags(allDict=True)
    x2 = {None:x}
    return buildChain(x2)
    
