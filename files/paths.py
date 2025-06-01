
from .taskfiles import getPathTags



class Node:

    def __init__(self, name, chain):
        self.name = name
        self.chain =chain
        # print(self.name)
        
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
    


class chain:
    def __init__(self):
        self.nodes = []
    def getTop(self):
        return [n for n in self.nodes if n.parent is None][0]

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

