from plugin_framework.extension import Extension
from plugins.table.view import View
from gui.view.main_window import MainWindow


class Main(Extension):
    def __init__(self, specification):
        super().__init__(specification)
        self.main_window = MainWindow
        #self.view = View(self.main_window)

    def activate(self):
        self.do_something()

    def deactivate(self):
        return super().deactivate()

    def do_something(self):
        print("Hello world!")

    def get_widget(self, parent=None):
        #return View(self.main_window), None, None
        return View(parent = None), None, None


