
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

from textual.app import App,Binding
from textual.widgets import Static, Header, Footer
from textual.reactive import reactive

from json import dumps


    



class KanbanApp(App):

    def __init__(self,tabs = boards):
        self.userX = 0
        self.userY=0
        self.tabs =tabs
        self.tabIndex = 0
        self.tab = tabs[self.tabIndex]

        self.xMax = len(self.tab.columns) - 1
        self.yMax = [col.size() -1 for col in self.tab.columns]
        self.Logs = ""



        super().__init__()
    
    def resetConstants(self):
        self.tab = self.tabs[self.tabIndex]
        self.userX = 0
        self.userY = 0
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
        Binding("up","moveUp","move up", priority=True),
        Binding("down","moveDown","move down", priority=True),
        Binding("colon","enter_command","Command prompt"),
        Binding("tab", "nextTab", "Next Dashboard",priority=True),
        Binding("shift+tab", "prevTab", "Previous Dashboard",priority=True),
]


    def addLog(self, logMsg):
        self.Logs += "\n" + logMsg
        self.logStatic.refresh()

    def getXY(self, x,y):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)
        return x,y

    



    def select(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.select()
    
    def deSelect(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.deSelect()



    def getSelectedTaskAsString(self, x=None, y=None):
        x,y = self.getXY(x,y)
        
        taskPath =  self.tab.columns[x].paths()[y]
        with open(taskPath,"r") as tp:
            taskString = tp.read()

        return taskString

    

    

    def currentWidget(self):
        return self.widgets.get(self.userX, self.realY())
    
    def focusCurrentWidget(self):
        self.set_focus(self.currentWidget())








    def action_moveRight(self):
        self.deSelect()
        if 0 <= self.userX < self.xMax:
            self.userX += 1
        else:
            self.userX = 0
        self.afterMove()
    
    def action_moveLeft(self):
        self.deSelect()
        if 0 < self.userX <= self.xMax:
            self.userX -= 1
        else:
            self.userX = self.xMax
        self.afterMove()

    
    def action_moveUp(self):
        self.deSelect()
        if 0 < self.userY:
            self.userY = self.realY() - 1
        else:
            self.userY = self.yMax[self.userX]
        self.afterMove()
    
    def action_moveDown(self):
        self.deSelect()
        if self.userY < self.yMax[self.userX]:
            self.userY = self.realY() + 1
        else:
            self.userY = 0
        self.afterMove()
 
    def afterMove(self):
        self.select()
        self.updateTaskInfo()
        self.focusCurrentWidget()

    def action_nextTab(self):
        print("next tab")
        self.tabIndex = (self.tabIndex + 1) % len(self.tabs)
        self.resetConstants()
        self.refresh(recompose=True)
        self.focusCurrentWidget()
        self.addLog(f"switched to tab {self.tabIndex}")

    def action_prevTab(self):
        print("prev tab")
        self.tabIndex = (self.tabIndex - 1) % len(self.tabs)
        self.resetConstants()
        self.refresh(recompose=True)
        self.focusCurrentWidget()
        self.addLog(f"switched to tab {self.tabIndex}")

    def action_enter_command(self):
        self.commandInputWidget.remove_class("hidden")
        self.set_focus(self.commandInputWidget)
        self.ft.add_class("hidden")
    

    
            
    def hide_command(self):
        self.commandInputWidget.blur()
        self.commandInputWidget.add_class("hidden")
        self.focusCurrentWidget()
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
        
        self.taskDataStatic = Static(self.getSelectedTaskAsString(),markup=False,classes="taskInfo")
        self.logStatic = Static(self.Logs, classes="log")
        self.sideBar = Vertical(self.taskDataStatic, self.logStatic, classes="sideBar")
        self.widgets = TaskArray(self.tab, self.sideBar)



        self.commandInputWidget = CommandInput(classes="commandPrompt hidden")
        self.ft = Footer(id="footer", classes="footer")

        self.select()
        yield Header(classes="header")
        yield self.widgets
        yield self.commandInputWidget
        yield self.ft

        self.set_focus(None)
    
    
app = KanbanApp()

if __name__ == "__main__":
    app.run()