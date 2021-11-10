from PySide2 import QtWidgets
from plugin_framework.extension import Extension
from PySide2 import QtWidgets
from .widget import TextEdit

class Main(Extension):
    def __init__(self, specification):
        super().__init__(specification)

    def activate(self):
        print("Activated")
        self.plugin_specification.add_widget(self.get_widget)

    def deactivate(self):
        print("Deactivated")
        self.plugin_specification.remove_widget(self.get_widget)

    def do_something(self):
        print("Hello world!")

    def get_widget(self, parent=None):
        return TextEdit(parent), None, None






# from plugin_framework.extension import Extension
# from .widget import TextEdit

# class Plugin(Extension):
#     def __init__(self, specification, iface):
#         """
#         :param iface: main_window aplikacije
#         """
#         super().__init__(specification, iface)
#         self.widget = TextEdit(iface.central_widget)
#         print("INIT TEST")

#     # FIXME: implementacija apstraktnih metoda
#     def activate(self):
#         print("Activated")
#         self.iface.add_widget(self.widget)

#     def deactivate(self):
#         print("Deactivated")
#         self.iface.remove_widget(self.widget)


                
