
from backend.cache import *
buildTaskCache()

from .widgets import *
from .styles import CSS

from backend.cache import taskCache
from backend.filters import *

from dashboards.tableBoard import tableBoard

from files.task import *
from files.taskfiles import *
from data.config import *
from data.data import boards, keyBindings

from veenTools.jsonFunctions import *

from textual.app import App,Binding
from textual.widgets import Static, Header, Footer

from json import dumps
from types import MethodType

    



class KanbanApp(App):

    def __init__(self,tabs = boards):
        print("initializing")
        self.tabs =tabs
        self.tabIndex = 0
        self.Logs = ""

        super().__init__()
    # BINDINGS =[]
    def tabSet(self, n=0,draw=True):
        print("tab setting")
        self.tabIndex = (self.tabIndex + n) % len(self.tabs)
        self.tab = self.tabs[self.tabIndex] 
        self.tab.app = self
        self.tab.resetPosition()
        # self.tab.setMax()
        self.syncActions(keyBindings)
        self.tab.composeWidgets()

        # self.BINDINGS = self.tab.getBindings()
        # print(self.BINDINGS)
        # self.reBind()
        if draw:
            self.tab.reDraw()


    CSS = CSS
    BINDINGS = keyBindings


 

    def reBind(self):
        previousBindings = getattr(self, "_current_bindings",[])
        for binding in previousBindings:
            self.unbind(binding.key, binding.action)
        
        self._current_bindings =self.tab.getBindings()
        for binding in self._current_bindings:
            self.bind(
                binding.key,
                binding.action,
                description=binding.description,
                show=binding.show,
                priority=binding.priority,

            )
    
    def syncActions(self, all_bindings = keyBindings):
        current =self.tab.getBindings()
        current_actions = {b.action for b in current}
        all_actions = {b.action for b in all_bindings}

        def make_method(
            action_name: str,
            present: set[str],
        ):
            def _method(self, *args, **kwargs):
                if action_name in present:
                    handler = getattr(self.tab, f"action_{action_name}", None)
                    if handler: 
                        return handler(*args, **kwargs)
            _method.__name__ = f"action_{action_name}"
            return _method
        for name in all_actions:
            func = make_method(name, current_actions)
            setattr(self,f"action_{name}", MethodType(func, self))
            




    def compose(self):
        self.tabSet(draw=False)
        print("composing!")
        print(self.BINDINGS)
        for widgetObject in self.tab.composeWidgets():
            yield widgetObject

        self.tab.select()
        self.set_focus(None)
    
  


    
app = KanbanApp()

if __name__ == "__main__":
    app.run()