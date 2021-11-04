from plugin_framework.extension import Extension
from plugin_framework.plugin_specification import PluginSpecification
import json

from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Qt
from PySide2.QtGui import QPalette, QColor


class Main(Extension):
    def __init__(self, specification):
        super().__init__(specification)
        

    QApplication.setStyle('Fusion')
    def activate(self):
        #return super().activate()
        app = QApplication
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        return app.setPalette(dark_palette)


    def deactivate(self):
        #return super().deactivate()
        app = QApplication
        default_palette = QPalette
        return app.setPalette(default_palette)
