from backend.utils import cutText, reducedText, displayableText
from files.task import makeTask

from textual.widgets import Static, Input
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.scroll_view import ScrollView
from textual.strip import Strip
from textual.widget import Widget
from textual.app import RenderResult
from textual.message import Message
from rich.segment import Segment
from rich.text import Text


import time

class TaskStatic(Static):
    can_focus =True

    def innerWidth(self):
        inner_region = self.content_region
        inner = inner_region.width
        return inner
    
    def __init__(
            self,
            text: str,
            *,
            id = None,
            classes = None,
        ):
        self.text = text 
        self.selected = False
        super().__init__(text, id=id, classes=classes)
    
    
    def _wrap_text(self):
        if not self.selected:
            x =self.innerWidth()
            print(f"innerwidth {x}")
            newText = reducedText(self.text,x)
            print(newText, self.text,x)
            self.update(newText)
            return newText
    

    def render(self) -> RenderResult:
        x = self.innerWidth()
        
        if not self.selected:
            x2= reducedText(self.text, x)
            return x2   
        return displayableText(self.text, x)

    def select(self):
        self.add_class("selected")
        self.selected = True
        self.update(self.text)
        self.refresh()
    
    def deSelect(self):
        self.remove_class("selected")
        self.selected = False
        self._wrap_text()
        self.refresh()



class CommandInput(Input):
    can_focus =True
    mode = "hidden"
    taskPath = None

    def __init__(
        self,
        *,
        id = None,
        classes = None,
    ):
        self.tab = self.app.tab
        super().__init__(id=id,classes=classes)

    class Command(Message):
        def __init__(self, sender, value: str) -> None:
            super().__init__(sender)
            self.value = value

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if command:
            if self.mode == "command":
                self.tab.addLog(f"Command: {command}")
            elif self.mode == "taskAdd":
                self.tab.addLog(f"adding task {command} to {self.taskPath}")
                newTask = makeTask(
                    command,
                    {"path-tags":[self.taskPath]},
                    makeFile=True
                )
                self.tab.widgets.get().addTask(newTask)
                
        self.value = ""
        self.hide_command()


    def on_key(self, event):
        if event.key == "escape":
            self.value = ""
            self.hide_command()
            event.stop()
    
    def hide_command(self):
        self.blur()
        self.add_class("hidden")
        self.tab.focusCurrentWidget()
        self.tab.select()
        self.tab.ft.remove_class("hidden")
        self.mode = "hidden"
    
    def show_command(self,newMode="command",taskPath = None):
        self.mode = newMode
        self.remove_class("hidden")
        self.app.set_focus(self)
        self.tab.ft.add_class("hidden")
        if newMode == "taskAdd":
            self.add_class("taskAdd")
            self.taskPath = taskPath



class TaskArray(Horizontal):
    def __init__(self, tab,sideBar):
        self.columns = [TaskColumn(col) for col in tab.columns]
        self.tab = tab
        self.sideBar = sideBar

        super().__init__(*(self.columns + [sideBar]), classes="dashboard")
    
    def get(self, x=None,y=None):
        if x is None:
            x = self.tab.userX
        if y is None:
            return self.columns[x]
        return self.columns[x].get(y)
    
    def getCurrentPath(self):
        x, y = self.tab.getXY()
        tabName = self.tab.title
        colName = self.columns[x].title
        return f"{tabName}/{colName}"
    
    def resetColumn(self,x=None):
        if x is None:
            x, y = self.tab.getXY()
        self.columns[x].resetContent()

class TaskColumn(Vertical):

    def __init__(self,col):
        self.col = col
        self.title = col.title
        self.titleWidget = Static(f"[b]{self.title}[/b]",classes="title")
        self.contentWidget = TaskColumnContent(col.titles())
        super().__init__(
            self.titleWidget,
            self.contentWidget,
            classes="outerColumn"
        )
        self.tab = self.app.tab
    
    def get(self, colY=None):
        return self.contentWidget.get(colY)
    
    def addTask(self, newTask):
        self.contentWidget.addTask(newTask, self.col)
    
    def resetContent(self):
        self.contentWidget.reset()




class TaskColumnContent(VerticalScroll):
    def __init__(self,colData):
        self.content = colData
        self.staticContent = [TaskStatic(text, classes="text") for text in colData]
        super().__init__(*self.staticContent,classes="column")
        self.tab = self.app.tab
    
    def get(self, colY=None):
        if colY is None:
            return self.staticContent
        else:
            return self.staticContent[colY]
    
    def addTask(self, newTask, col):
        x, y = self.tab.getXY()
        self.content = col.titles()
        newID = newTask.get("ID")
        newIndex = col.indexOf(newID)
        self.reset(x, newIndex)

    
    def syncData(self):
        parent = self.parent
        grandParent = parent.parent
        parentSiblings = list(grandParent.children)
        selfIndex = parentSiblings.index(parent)
        self.content = self.tab.get(selfIndex).titles()


    def reset(self, x=None, y=None):
        self.syncData()
        x, y = self.tab.getXY(x, y)
        self.call_later(self.remove_children,selector="*")
        self.staticContent = [TaskStatic(text, classes="text") for text in self.content]
        self.call_later(self.mount, *self.staticContent)
        self.tab.resetConstants(x, y)



