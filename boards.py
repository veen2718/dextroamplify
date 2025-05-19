from .taskfiles import *
from .tools import *
from textual.app import App

from textual.widgets import Static
from textual.containers import Horizontal

class Board:
    def __init__(
        self,
        name,
        content = []
    ):
        self.name=name
        self.content = content
    


class Text:
    def __init__(self,text):
        self.text = text
    def Text(self):
        return text

class Table:
    def __init__(self, columns,title=None):
        self.title = title
        self.columns = columns
    def toArray(self):
        arr = []
        for column in self.columns:
            col = [column.title]
            col += column.titles()
            arr.append(col)
        
        maxLength = max([len(i) for i in arr])

        arr2 = [col + [" "]*(maxLength-len(col)) for col in arr]
        return rotate(arr2)


class Column:
    def __init__(self, taskFunction,title=None):
        self.taskFunction = taskFunction
        self.title = title
    def paths(self,*args):
        return self.taskFunction(*args)
    def data(self, *args):
        paths = self.paths(*args)
        return [readTask(path) for path in paths]
    def titles(self, *args):
        return [data.get("title") for data in self.data(*args)]
    def size(self):
        return len(self.paths())
    
    def display(self):
        return Static(f"[b]{self.title}[/b]\n\n" + "\n\n".join(self.titles()),classes="column")
    
    def indexOf(self, ID):
        data = self.data()
        for i, v in enumerate(data):
            if v["ID"] == ID:
                return i
        return -1

    