
class Board:
    def __init__(
        self,
        name,
        content = []
    ):
        self.name=name
        self.content = content
    
    # def board(self):
    #     data = []
    #     for func in self.columnFuncs:
    #         data.append(func())
    #     return data


class Text:
    def __init__(self,text):
        self.text = text
    def Text(self):
        return text

class Table:
    def __init__(self, *columns,title=None):
        self.title = title

class Column:
    def __init__(self, taskFunction,title=None):
        self.taskFunction = taskFunction
        self.title = title
    def data(self,*args):
        return self.taskFunction(*args)

boards = {
    "testBoard":[
        
    ]
}
    