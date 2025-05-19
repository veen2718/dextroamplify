
from .cache import *
buildTaskCache()

from .cache import taskCache

from .task import *
from .taskfiles import *
from .filters import *
from tools.jsonFunctions import *
from .config import *
from .data import *
from .widgets import *
from .styles import CSS

from textual import on
from textual.app import App,Binding
from textual.widgets import Static, Header, Footer, Input
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
# from textual.screen import set_focus

from json import dumps


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
        self.tab = self.tabs[self.tabIndex]

        self.xMax = len(self.tab.columns) - 1
        self.yMax = [col.size() -1 for col in self.tab.columns]


    def realY(self,x= None):
        if x is None:
            x = self.userX
        yMaxCol = self.yMax[x]
        if self.userY > yMaxCol:
            return yMaxCol
        return self.userY


    CSS = CSS


    BINDINGS = [
        Binding("right","moveRight","move right"),
        Binding("left","moveLeft","move left"),
        Binding("up","moveUp","move up"),
        Binding("down","moveDown","move down"),
        Binding("colon","enter_command","Command prompt"),
        Binding("esc","escaped","Escape"),
        Binding("tab", "nextTab", "Next Dashboard",priority=True),
        Binding("shift+tab", "prevTab", "Previous Dashboard",priority=True),
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
    
    def getXY(self, x,y):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)
        return x,y

    
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




    def select(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.add_class("selected")
        self.refreshStatic(staticWidget)
    
    def deSelect(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.remove_class("selected")
        self.refreshStatic(staticWidget)



    def getSelectedTaskAsString(self, x=None, y=None):
        x,y = self.getXY(x,y)
        
        taskPath =  self.tab.columns[x].paths()[y]
        with open(taskPath,"r") as tp:
            taskString = tp.read()

        return taskString

    

    
    def staticCol(self, colX):
        drawnCol = self.DrawCol(colX)
        staticTexts = [TaskStatic(text,classes="text") for text in drawnCol]
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
            self.updateTaskInfo()
    
    def action_moveLeft(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if 0 < self.userX <= self.xMax:
            self.userX -= 1
            self.select()
            self.deSelect(self.userX+1)
            self.updateTaskInfo()
    
    def action_moveUp(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if 0 < self.userY:
            self.userY = self.realY() - 1
            self.select()
            self.deSelect(y=self.userY+1)
            self.updateTaskInfo()
    
    def action_moveDown(self):
        print(f"pos: {self.userX,self.userY,self.realY()}")
        if self.userY < self.yMax[self.userX]: 
            self.userY += 1
            self.select()
            self.deSelect(y = self.userY -1)
            self.updateTaskInfo()
    
    def action_nextTab(self):
        print("next tab")
        self.tabIndex = (self.tabIndex + 1) % len(self.tabs)
        self.resetConstants()
        self.refresh(recompose=True)

    def action_prevTab(self):
        print("prev tab")
        self.tabIndex = (self.tabIndex - 1) % len(self.tabs)
        self.resetConstants()
        self.refresh(recompose=True)

    def action_enter_command(self):
        self.commandInputWidget.remove_class("hidden")
        self.set_focus(self.commandInputWidget)
        self.ft.add_class("hidden")
    

    def action_escaped(self):
        self.hide_command()
    
            
    def hide_command(self):
        self.commandInputWidget.blur()
        self.commandInputWidget.add_class("hidden")
        self.set_focus(None)
        self.ft.remove_class("hidden")


    def updateWidget(self, x=None, y=None):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)

        self.call_later(self.widgets.get(x,y).update, self.drawText(x,y))
    
    def updateTaskInfo(self):
        self.call_later(self.taskDataStatic.update, self.getSelectedTaskAsString())

    def refreshStatic(self,stWidget):
        self.call_later(stWidget.refresh)


    def compose(self):
        print(f"composing {self.tabIndex}")
        
        self.widgets = staticArray(self.staticCols())
        self.taskDataStatic = Static(self.getSelectedTaskAsString(),classes="taskInfo")
        verticals = [Vertical(*stCol, classes="column") for stCol in self.widgets.getColumns()] + [self.taskDataStatic]

        self.commandInputWidget = CommandInput(classes="commandPrompt hidden")
        self.ft = Footer(id="footer")

        self.select()
        yield Header()
        yield Horizontal(*verticals)
        yield self.commandInputWidget
        yield self.ft

        self.set_focus(None)
    
    
app = KanbanApp()

if __name__ == "__main__":
    app.run()