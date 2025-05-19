from textual.widgets import Static, Input


class TaskStatic(Static, can_focus=True):
    test = 0

class CommandInput(Input):
    can_focus =True

    def on_key(self, event):
        if event.key == "escape":
            self.value = ""
            self.app.hide_command()
            event.stop()