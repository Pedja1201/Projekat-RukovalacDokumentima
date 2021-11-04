from plugin_framework.extension import Extension
# from plugin_framework.plugin_specification import PluginSpecification
import json
from PySide2 import QtWidgets


class Main(Extension):
    def __init__(self, specification):
        super().__init__(specification)

    def activate(self):
        self.do_something()

    def deactivate(self):
        return super().deactivate()

    def do_something(self):
        print("Hello world!")

    def get_widget(self, parent=None):
        return QtWidgets.QCalendarWidget(), None, None

 


        


# def __init__(self, specification):
#         super().__init__(specification)

#     def activate(self):
#         self.do_something()

#     def do_something(self):
#         print("Hello world from second plugin!")

#     def get_widget(self, parent=None):
#         return QtWidgets.QCalendarWidget(), None, None
