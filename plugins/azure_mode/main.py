from plugin_framework.extension import Extension
from plugin_framework.plugin_specification import PluginSpecification
import json
from .widget import AzureMode

from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Qt
from PySide2.QtGui import QPalette, QColor


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
        return AzureMode(parent), None, None
