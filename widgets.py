from textual.widgets import Static, Input
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


