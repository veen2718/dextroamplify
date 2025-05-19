from textual.widgets import Static, Input
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.scroll_view import ScrollView
from textual.strip import Strip
from rich.segment import Segment

class TaskStatic(Static, can_focus=True):
    test = 0

class CommandInput(Input):
    can_focus =True

    def on_key(self, event):
        if event.key == "escape":
            self.value = ""
            self.app.hide_command()
            event.stop()



class TaskArray(Horizontal):
    def __init__(self, tab,taskDataStatic):
        self.columns = [TaskColumn(col) for col in tab.columns] 

        super().__init__(*(self.columns + [taskDataStatic]), classes="dashboard")
    def get(self, x,y=None):
        if y is None:
            return self.columns[x]
        return self.columns[x].get(y)

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
    
    def get(self, colY=None):
        return self.contentWidget.get(colY)




class TaskColumnContent(VerticalScroll):
    def __init__(self,colData):
        self.content = colData
        self.staticContent = [TaskStatic(text, classes="text") for text in colData]
        super().__init__(*self.staticContent,classes="column")
    
    def get(self, colY=None):
        if colY is None:
            return self.staticContent
        else:
            return self.staticContent[colY]
