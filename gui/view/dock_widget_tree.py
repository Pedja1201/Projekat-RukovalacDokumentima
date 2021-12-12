from PySide2 import QtWidgets, QtCore
from ..model.tree_xml import XmlTree
from PySide2 import QtCore, QtGui, QtWidgets, QtXml
# from PyQt5.QtCore import pyqtSignal


class DockWidget(QtWidgets.QMainWindow):
    kliknut = QtCore.Signal(str)
    def __init__(self, parent=None):
        super(DockWidget, self).__init__(parent)

        self.xmlTree = XmlTree()
        self.setCentralWidget(self.xmlTree)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("Document Collection")
        self.resize(480, 320)

#         self.xmlTree.clicked.connect(self.file_clicked)


#     def file_clicked(self, index):
#         print(self.xmlTree.filePath(index))
#         print(self.xmlTree.fileName(index))
#         path = self.xmlTree.filePath(index)
#         self.kliknut.emit(path)

    def open(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                "Open Document File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Document Collection",
                    "Cannot read file %s:\n%s." % (fileName, inFile.errorString()))
            return

        if self.xmlTree.read(inFile):
            self.statusBar().showMessage("File loaded", 2000)

    def saveAs(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save Document File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        outFile = QtCore.QFile(fileName)
        if not outFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Document Collection",
                    "Cannot write file %s:\n%s." % (fileName, outFile.errorString()))
            return

        if self.xmlTree.write(outFile):
            self.statusBar().showMessage("File saved", 2000)

    def about(self):
       QtWidgets.QMessageBox.about(self, "About Document",
            "The <b>Document Collection</b> example demonstrates how to use Qt's "
            "Document classes to read and write XML documents.")

    def createActions(self):
        self.openAct = QtWidgets.QAction(QtGui.QIcon("resources/icons/xml.jpg"),"&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveAsAct = QtWidgets.QAction(QtGui.QIcon("resources/icons/snimi.png"),"&Save As...", self, shortcut="Ctrl+S",
                triggered=self.saveAs)

        self.exitAct = QtWidgets.QAction(QtGui.QIcon("resources/icons/exit.jpg"),"E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtWidgets.QAction(QtGui.QIcon("resources/icons/search.png"),"&About", self, triggered=self.about)

        self.aboutQtAct = QtWidgets.QAction(QtGui.QIcon("resources/icons/qt.png"),"About &Qt", self,
                triggered=QtWidgets.QApplication.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

