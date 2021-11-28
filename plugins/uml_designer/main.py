from plugin_framework.extension import Extension
from .widget.uml_widget import UmlWidget


class Main(Extension):
    def __init__(self, specification):
        super().__init__(specification)

    def activate(self):
        self.do_something()

    def deactivate(self):
        return super().deactivate()

    def do_something(self):
        print("Hello world!")

    def get_widget(self,parent=None):
        return UmlWidget(parent), None, None
