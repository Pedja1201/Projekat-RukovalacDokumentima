from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui


class TextEdit(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO: Dodati odredjene funkcije za text edit(Bold,font,size....)
        self._layout = QtWidgets.QVBoxLayout()
        self.text_edit = QtWidgets.QTextEdit(self)
        self.tool_bar = QtWidgets.QToolBar("Naslov", self)
    
        #ToolAkcije
        self.tool_actions = {
            "New file": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&New file"),
            "Save": QtWidgets.QAction(QtGui.QIcon("resources/icons/save.png"), "&Save"),
            "Undo": QtWidgets.QAction(QtGui.QIcon("resources/icons/undo.png"), "&Undo"),
            "Redo": QtWidgets.QAction(QtGui.QIcon("resources/icons/redo.png"), "&Redo"),
            "Delete": QtWidgets.QAction(QtGui.QIcon("resources/icons/delete.png"), "&Delete"),
        }


        #ToolBar
        self.tool_bar.addAction(self.tool_actions["New file"])
        self.tool_actions["New file"].setStatusTip("Otvori novi dokument!")
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.tool_actions["Save"])
        self.tool_actions["Save"].setStatusTip("Sačuvaj dokument!")
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.tool_actions["Undo"])
        self.tool_actions["Undo"].setStatusTip("Korak nazad!")
        self.tool_bar.addAction(self.tool_actions["Redo"])
        self.tool_actions["Redo"].setStatusTip("Ponovno vraćanje!")
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.tool_actions["Delete"])
        self.tool_actions["Delete"].setStatusTip("Obriši dokument!")

        #toolAkcije
        self.tool_actions["Undo"].triggered.connect(self.text_edit.undo)
        self.tool_actions["Redo"].triggered.connect(self.text_edit.redo)
        self.tool_actions["Delete"].triggered.connect(self.text_edit.deleteLater) #Pedja
        self.tool_actions["New file"].triggered.connect(self.on_open) #Pedja





        self._layout.addWidget(self.tool_bar)
        self._layout.addWidget(self.text_edit)
        
        self.setLayout(self._layout)
        # u layout dodati toolbar i menubar
        # sam widget koji je npr. textedit

    def on_open(self):
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open python file", ".", "Python Files (*.py)")
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            self.text_edit.setText(text_from_file)