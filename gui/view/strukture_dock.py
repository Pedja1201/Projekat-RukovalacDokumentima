from PySide2 import QtWidgets, QtCore


class StructureDock(QtWidgets.QDockWidget):
    kliknut = QtCore.Signal(str) # Atribut klase koji nam omogucuje ispis ocitanog fajla u konzoli preko file_clicked metode

    def __init__(self, title, parent):
        super().__init__(title, parent)

        # document_path = QtCore.QDir.currentPath()
        # document_path = document_path[:document_path.rfind('/')] + '/Dokument'

        self.model = QtWidgets.QFileSystemModel()
        self.main_window = parent
        # skip = ["*.json"]
        
        self.model.setRootPath(QtCore.QDir.currentPath())
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)
        # self.model.setNameFilters(skip)
        self.model.setNameFilterDisables(False)


        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath()+"/Dokument"))
        self.tree.clicked.connect(self.file_clicked)
        self.setWidget(self.tree)

        
    # Metoda koja ispisuje path u terminalu klikom na fajl iz strukture dok.
    def file_clicked(self, index):
        print(self.model.filePath(index))
        path = self.model.filePath(index)
        self.kliknut.emit(path)#Ne moze da emituje path bez kliknut signala
        #Uzima path i u main windowu otvara novi file sa datim path-om.

    def set_root_path(self, path):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
