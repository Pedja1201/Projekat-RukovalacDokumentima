import subprocess
from PySide2 import QtWidgets
from PySide2.QtWidgets import  QFileDialog, QWidget
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PySide2.QtCore import QFileInfo

 # Obzirom na ogranicenja Qt-a (otvaranje eksternih procesa u okviru same aplikacije nije u potpunosti podrzano), rad na ovom pluginu je odlozen.

class MultiOmniOpener(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self.tool_bar = QtWidgets.QToolBar("Multi Omni-Opener", self)
        
        #ToolAkcije
        self.tool_actions = {
            "Add": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&Add")#,
        }

        #ToolBar
        self.tool_bar.addAction(self.tool_actions["Add"])
        self.tool_actions["Add"].setStatusTip("Dodajte novi sadrzaj")
        self.tool_actions["Add"].triggered.connect(self.on_open)

        self._layout.addWidget(self.tool_bar)        
        self.setLayout(self._layout)

    def on_open(self):
        content_name = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        subprocess.Popen([content_name], shell=True)
        windowIdStr = subprocess.check_output(['sh', '-c', """xwininfo -int | sed -ne 's/^.*Window id: \\([0-9]\\+\\).*$/\\1/p'"""]).decode('utf-8')
        windowId = int(windowIdStr)
        self.slot = QtGui.QWindow.fromWinId(windowId)
        self.container = QWidget.createWindowContainer(self.slot, self._layout)
        self._layout.addWidget(self.container)
        self.setLayout(self._layout)