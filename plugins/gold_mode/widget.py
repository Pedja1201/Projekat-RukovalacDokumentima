from PySide2.QtWidgets import *
from PySide2.QtCore import Slot,Qt
from PySide2.QtGui import QPalette, QColor

class GoldMode(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        app = QApplication
        gold_palette = QPalette()
        gold_palette.setColor(QPalette.Window, QColor(255, 215, 0))
        gold_palette.setColor(QPalette.WindowText, Qt.white)
        gold_palette.setColor(QPalette.Base, QColor(255, 255, 224))
        gold_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        gold_palette.setColor(QPalette.ToolTipBase, Qt.white)
        gold_palette.setColor(QPalette.ToolTipText, Qt.white)
        gold_palette.setColor(QPalette.Text, Qt.black)
        gold_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        gold_palette.setColor(QPalette.ButtonText, Qt.black)
        gold_palette.setColor(QPalette.BrightText, Qt.red)
        gold_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        gold_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        gold_palette.setColor(QPalette.HighlightedText, Qt.black)
        return app.setPalette(gold_palette)
