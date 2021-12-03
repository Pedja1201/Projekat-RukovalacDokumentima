from PySide2 import QtWidgets, QtCore
from .tree_xml import OpenXMLFile

class StructureDock(QtWidgets.QWidget):
    kliknut = QtCore.Signal(str) # Atribut klase koji nam omogucuje ispis ocitanog fajla u konzoli preko file_clicked metode
    widget_for=1234
    def __init__(self, iface):
        super().__init__(iface)

        self.iface = iface

        self.layout = QtWidgets.QVBoxLayout()
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath()))
        self.tree.clicked.connect(self.populate)

        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)
       

        
    # Metoda koja ispisuje path u terminalu klikom na fajl iz strukture dok.
    def populate(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        file = self.model.filePath(indexItem)

        if(QtCore.QFileInfo(file).fileName().split(".")[1] == "xml"):
            fileOpen = open(file, "r").read()
            OpenXMLFile(self.iface).XMLinTreeView(fileOpen, QtCore.QFileInfo(file).fileName())
            self.iface.list_view.show()
            self.iface.text_edit.setText("")
            self.iface.text_edit.hide()
