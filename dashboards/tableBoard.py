

from .default import *
from app.widgets import TaskArray
from files.taskfiles import deleteTaskFile
from backend.boards import Table

from textual.app import Binding


class tableBoard(defaultDashboard, Table):

    

    def __init__(self, columns, title=None):
        Table.__init__(self,columns, title)
        defaultDashboard.__init__(self)
        
        self.boardClass = TaskArray

        super().__init__()

    def getBindings(self):
        self.BINDINGS = [
            Binding("space","addTask", "add task", priority=True),
            Binding("delete","deleteSelected", "delete", priority=True),
        ] + self.defaultDashboardBindings
        print("returning bindings")
        print(len(self.BINDINGS))
        return self.BINDINGS

    def getSelectedTaskAsString(self, x=None, y=None):
        x,y = self.getXY(x,y)
        
        taskPath =  self.columns[x].paths()[y]
        with open(taskPath,"r") as tp:
            taskString = tp.read()

        return taskString

    def getSelectedAsString(self, x =None, y = None):
        return self.getSelectedTaskAsString(x,y)
    
    
    def getMax(self):
        return [len(self.columns) - 1, [col.size() -1 for col in self.columns]]
    
    
    
    def action_deleteSelected(self):
        selectedTask = self.currentTask()
        
        selectedID = selectedTask["ID"]
        selectedTitle = selectedTask["title"]
        deleteTaskFile(selectedID)
        self.widgets.resetColumn()
        self.select()
        self.addLog(f"deleted task {selectedTitle}")

    def action_addTask(self):
        self.commandInputWidget.show_command(
            "taskAdd",
            self.widgets.getCurrentPath()
            )
