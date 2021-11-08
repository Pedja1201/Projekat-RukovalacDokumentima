from plugin_framework.extension import Extension
from plugin_framework.plugin_specification import PluginSpecification
import json
from .widget import PluginMode

from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Qt
from PySide2.QtGui import QPalette, QColor


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
        return PluginMode(parent), None, None