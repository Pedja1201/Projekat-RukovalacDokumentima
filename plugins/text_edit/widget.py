from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon, QFont

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
            "Font": QtWidgets.QAction(QtGui.QIcon("resources/icons/font.png"), "&Font"),
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
        self.tool_bar.addAction(self.tool_actions["Font"])

        #toolAkcije
        self.tool_actions["Undo"].triggered.connect(self.text_edit.undo)
        self.tool_actions["Redo"].triggered.connect(self.text_edit.redo)
        self.tool_actions["Delete"].triggered.connect(self.text_edit.deleteLater) #Pedja
        self.tool_actions["New file"].triggered.connect(self.on_open) #Pedja
        self.tool_actions["Font"].triggered.connect(self.font_dialog) #Pedja
        self.tool_actions["Save"].triggered.connect(self.file_save)




        self._layout.addWidget(self.tool_bar)
        self._layout.addWidget(self.text_edit)
        
        self.setLayout(self._layout)
        # u layout dodati toolbar i menubar
        # sam widget koji je npr. textedit

    def on_open(self):
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open python file", ".")
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            self.text_edit.setText(text_from_file)

    def font_dialog(self):
        (ok, font) = QtWidgets.QFontDialog.getFont()
 
        if ok:
            self.text_edit.setFont(font)

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save')[0]
        print(name) # ovaj print je prosao samo prilikom prvog pokretanja i ispisao je tuple: ('', '')
        file = open(name + ".txt",'w')
        text = self.text_edit.toPlainText()
        print(text)
        file.write(text)
        file.close()