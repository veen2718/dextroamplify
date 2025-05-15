from .task import *
from .taskfiles import *
from .filters import *
from tools.jsonFunctions import *
from .config import *


import curses
from textual.app import App
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive


class staticColumn:
    def __init__(self,title, content):
        self.title = title
        self.content = content
    def get(self, y):
        return self.content[y]
    def column(self):
        return [self.title] +self.content

class staticArray:
    def __init__(self,columns):
        self.columns = columns
    def get(self, x,y=None):
        if y is None:
            return self.columns[x]
        return self.columns[x].get(y)
    def getColumns(self):
        return [col.column() for col in self.columns]
    



class KanbanApp(App):
    userX = reactive(0)
    userY = reactive(0)
    userMode = reactive(0)

    def __init__(self,tabs = boards):
        self.tabs =tabs
        self.tabIndex = 0
        self.tab = tabs[self.tabIndex]

        self.xMax = len(self.tab.columns) - 1
        self.yMax = [col.size() -1 for col in self.tab.columns]



        super().__init__()
    
    def resetConstants(self):
        self.tab = tabs[self.tabIndex]

        self.xMax = len(self.tab.columns) - 1
        self.yMax = [col.size() -1 for col in self.tab.columns]


    def realY(self,x= None):
        if x is None:
            x = self.userX
        yMaxCol = self.yMax[x]
        if self.userY > yMaxCol:
            return yMaxCol
        return self.userY


    CSS = """
        .column {
            border: round $accent;
            padding: 1;
            width: 1fr;
        }
        .text {
            # padding-top: 1;
            border: round green;
        }

        # .de-selected {
        #     white-space: nowrap;
        #     overflow: hidden;
        #     text-overflow: ellipsis;
        # }

        .selected {
            border: round deepskyblue;
            background: #DDB8B8;   
        }
    """

    BINDINGS = [
        ("right","moveRight","move right"),
        ("left","moveLeft","move left"),
        ("up","moveUp","move up"),
        ("down","moveDown","move down"),
    ]


    def drawn(self):
        print("drawing")
        drawnOutputs = [] 
        for colX, col in enumerate(self.tab.columns):
            drawnOutputs.append(self.DrawCol(colX))
            # print(outputString)
        return drawnOutputs
    
    def staticCols(self):
        print("static")
        staticOutputs = []
        for colX, col in enumerate(self.tab.columns):
            staticOutputs.append(self.staticCol(colX))
        return staticOutputs
    
    def drawCol(self,x): 
        cols =self.drawn()
        return cols[x]
    
    def DrawCol(self,colX):
        col = self.tab.columns[colX]
        t = col.title
        outputs = [f"[b]{t}[/b]"]

        for colY, taskTitle in enumerate(col.titles()):
            outputs.append(self.drawText(colX, colY))
        return outputs

    def drawText(self, colX, colY) :
        taskTitle = self.tab.columns[colX].titles()[colY]
        return taskTitle
        # if (colX, colY) == (self.userX, self.realY()):
        #     print(colX, colY, "highlighting", taskTitle)
        #     return f"[reverse]{taskTitle}[/reverse]"
        # else:
        #     return taskTitle

    def select(self, x=None, y=None):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)

        staticWidget = self.widgets.get(x,y)
        # staticWidget.remove_class("de-selected")
        staticWidget.add_class("selected")
        self.refreshStatic(staticWidget)
    
    def deSelect(self, x=None, y=None):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)

        staticWidget = self.widgets.get(x,y)
        staticWidget.remove_class("selected")
        # staticWidget.add_class("de-selected")
        self.refreshStatic(staticWidget)


    
    def staticCol(self, colX):
        drawnCol = self.DrawCol(colX)
        staticTexts = [Static(text,classes="text") for text in drawnCol]
        staticTitle = staticTexts[0]
        staticContent = staticTexts[1:]
        return staticColumn(staticTitle,staticContent)


    def action_moveRight(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if 0 <= self.userX < self.xMax:
            self.userX += 1
            print("X incremented by 1")
            self.select()
            self.deSelect(self.userX -1)
    
    def action_moveLeft(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if 0 < self.userX <= self.xMax:
            self.userX -= 1
            self.select()
            self.deSelect(self.userX+1)
            # self.updateWidget()
            # self.updateWidget(self.userX+1)
    
    def action_moveUp(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if 0 < self.userY:
            self.userY = self.realY() - 1
            self.select()
            self.deSelect(y=self.userY+1)
            # self.updateWidget()
            # self.updateWidget(y=self.userY +1)
    
    def action_moveDown(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if self.userY < self.yMax[self.userX]: 
            self.userY += 1
            self.select()
            self.deSelect(y = self.userY -1)
            # self.updateWidget()
            # self.updateWidget(y=self.userY - 1)
    

    def updateWidget(self, x=None, y=None):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)

        self.call_later(self.widgets.get(x,y).update, self.drawText(x,y))

    def refreshStatic(self,stWidget):
        self.call_later(stWidget.refresh)


    def compose(self):
        self.console.log("test")
        #  yield Horizontal(                   q    # 6. This puts widgets side-by-side
        #     Static("To Do", classes="column"),  # 7. Add a widget with a class name
        #     Static("Doing", classes="column"),
        #     Static("Done", classes="column")
        # )
        
        # print(cols)
        
        self.widgets = staticArray(self.staticCols())
        verticals = [Vertical(*stCol, classes="column") for stCol in self.widgets.getColumns()]

        # self.widgets = [Static(col, classes="column") for col in cols]
        self.select()
        yield Horizontal(*verticals)
    




app = KanbanApp()