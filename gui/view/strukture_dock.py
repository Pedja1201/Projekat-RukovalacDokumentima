from PySide2 import QtWidgets, QtCore

class StructureDock(QtWidgets.QDockWidget):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.model = QtWidgets.QFileSystemModel()
        self.main_window = parent
        skip = ["*.json"]
        
        self.model.setRootPath(QtCore.QDir.currentPath())
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllEntries)
        self.model.setNameFilters(skip)
        self.model.setNameFilterDisables(False)


        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath() + "/"))
        
        self.setWidget(self.tree)
        #self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath()))
        self.tree.clicked.connect(self.file_clicked)

        

    def file_clicked(self, index):
        self.file_path = self.model.filePath(index)
        self.data_filepath = self.file_path.replace(".json")
        print(self.data_filepath)
        if(self.main_window.is_db_workspace == True): 
            self.main_window.set_workspace()
        self.main_window.open_new_file(self.data_filepath)
        #Uzima path i u main windowu otvara novi file sa datim path-om.

    def set_root_path(self, path):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
