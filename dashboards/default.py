from app.widgets import CommandInput

from textual.app import Binding
from textual.widgets import Static, Header, Footer
from textual.containers import Vertical





class defaultMovement:
    def __init__(self):
        self.userX=0
        self.userY=0

    def resetPosition(self,newX = 0, newY = 0):
        self.userX = newX
        self.userY = newY
        self.xMax, self.yMax = self.getMax()

    
    def realY(self,x= None):
        if x is None:
            x = self.userX
        yMaxCol = self.yMax[x]
        if self.userY > yMaxCol:
            return yMaxCol
        return self.userY
        
    def getXY(self, x=None,y=None):
        if x is None:
            x = self.userX
        if y is None:
            y = self.realY(x)
        return x,y

    movementBindings = [
        Binding("right","moveRight","move right"),
        Binding("left","moveLeft","move left"),
        Binding("up","moveUp","move up", priority=True),
        Binding("down","moveDown","move down", priority=True),
    ]
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
    
    def setMax(self):
        self.xMax, self.yMax = self.getMax()

class defaultSelection:
    
        
    def currentTask(self):
        x, y = self.getXY()
        return self.get(x, y)

    def currentWidget(self):
        return self.widgets.get(self.userX, self.realY())
    
    def focusCurrentWidget(self):
        self.app.set_focus(self.currentWidget())

    def select(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.select()
    
    def deSelect(self, x=None, y=None):
        x,y = self.getXY(x,y)

        staticWidget = self.widgets.get(x,y)
        staticWidget.deSelect()
    

class defaultInterfacer:
    # def updateWidget(self, x=None, y=None):
    #     if x is None:
    #         x = self.userX
    #     if y is None:
    #         y = self.realY(x)

    #     self.call_later(self.widgets.get(x,y).update, self.drawText(x,y))
    
    def updateTaskInfo(self):
        self.app.call_later(self.taskDataStatic.update, self.getSelectedAsString())

    def refreshStatic(self,stWidget):
        self.app.call_later(stWidget.refresh)

class defaultCommand:
    commandBindings =[
        Binding("colon","enter_command","Command prompt"),
    ]

    def action_enter_command(self):
        self.commandInputWidget.show_command()

class defaultTabManager:
    
    def action_nextTab(self):
        print("next tab")
        # self.tabIndex = (self.tabIndex + 1) % len(self.tabs)
        # self.tab = self.tabs[self.tabIndex]
        # self.tab.reDraw()
        self.app.tabSet(1)
        self.addLog(f"switched to tab {self.app.tabIndex}")

    def action_prevTab(self):
        print("prev tab")
        # self.tabIndex = (self.tabIndex - 1) % len(self.tabs)
        self.app.tabSet(-1)
        # self.reDraw()
        self.addLog(f"switched to tab {self.app.tabIndex}")


class defaultDashboard(
    defaultMovement,
    defaultSelection,
    defaultInterfacer,
    defaultCommand,
    defaultTabManager
):
    baseBindings = [
        Binding("tab", "nextTab", "Next Dashboard",priority=True),
        Binding("shift+tab", "prevTab", "Previous Dashboard",priority=True),
    ]

    def __init__(self):
        self.logs = ""

        defaultMovement.__init__(self)
        defaultSelection.__init__(self)
        defaultInterfacer.__init__(self)
        defaultCommand.__init__(self)
        defaultTabManager.__init__(self)

        self.defaultDashboardBindings = self.baseBindings +self.movementBindings + self.commandBindings
        self.setMax()
        # self.composeWidgets()
    
    def composeWidgets(self):

        self.taskDataStatic = Static(self.getSelectedAsString(),markup=False,classes="taskInfo")
        self.logStatic = Static(self.app.Logs, classes="log")
        self.sidebar = Vertical(self.taskDataStatic, self.logStatic, classes="sideBar")


        self.widgets = self.boardClass(self, self.sidebar)

        self.commandInputWidget = CommandInput(classes="commandPrompt hidden")
        self.ft = Footer(id="footer", classes="footer")

        return [
            Header(classes="header"),
            self.widgets,
            self.commandInputWidget,
            self.ft
        ]
        
    def addLog(self, logMsg):
        print("logging", logMsg)
        self.app.Logs += "\n" + logMsg
        self.logStatic.update(self.app.Logs)
        self.logStatic.refresh()
        print("refreshed")
    def afterMove(self):
        self.select()
        self.updateTaskInfo()
        self.focusCurrentWidget()
    def resetConstants(self, newX = 0, newY = 0):
        self.app.tab = self.app.tabs[self.app.tabIndex]
        self.resetPosition(newX, newY)
        self.app.BINDINGS = self.getBindings()
    
    def reDraw(self):
        self.resetConstants()
        self.app.refresh(recompose=True)
        self.focusCurrentWidget()
