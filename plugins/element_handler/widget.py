from .handler_list import HandlerList
from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui

class ElementHandler(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self.tool_bar = QtWidgets.QToolBar("Element-Handler", self)
    
        #ToolAkcije
        self.tool_actions = {
            "Open": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&Open")#,
        }

        #ToolBar
        self.tool_bar.addAction(self.tool_actions["Open"])
        self.tool_actions["Open"].setStatusTip("Otvori novi sadrzaj!")
        self.tool_actions["Open"].triggered.connect(self.on_open)

        self._layout.addWidget(self.tool_bar)        
        self.setLayout(self._layout)

    def on_open(self):
        content_name = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        handler_list = HandlerList(content_name)
        handler_list.handler_list[0].handle()