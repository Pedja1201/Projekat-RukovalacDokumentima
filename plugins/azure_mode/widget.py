from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Qt
from PySide2.QtGui import QPalette, QColor

class AzureMode(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        app = QApplication
        azure_palette = QPalette()
        azure_palette.setColor(QPalette.Window, QColor(0, 127, 255))
        azure_palette.setColor(QPalette.WindowText, Qt.white)
        azure_palette.setColor(QPalette.Base, QColor(173, 216, 230))
        azure_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        azure_palette.setColor(QPalette.ToolTipBase, Qt.white)
        azure_palette.setColor(QPalette.ToolTipText, Qt.white)
        azure_palette.setColor(QPalette.Text, Qt.white)
        azure_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        azure_palette.setColor(QPalette.ButtonText, Qt.black)
        azure_palette.setColor(QPalette.BrightText, Qt.red)
        azure_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        azure_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        azure_palette.setColor(QPalette.HighlightedText, Qt.black)
        return app.setPalette(azure_palette)
