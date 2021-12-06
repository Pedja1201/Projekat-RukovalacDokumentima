from PySide2 import QtWidgets
from PySide2.QtWidgets import  QFileDialog
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PySide2.QtCore import QFileInfo

class TextEditService(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self.text_edit = QtWidgets.QTextEdit(self)
        self.tool_bar = QtWidgets.QToolBar("Naslov", self)
    
        #ToolAkcije
        self.tool_actions = {
            "New file": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&New file"),
            "Save": QtWidgets.QAction(QtGui.QIcon("resources/icons/save.png"), "&Save"),
            "Undo": QtWidgets.QAction(QtGui.QIcon("resources/icons/undo.png"), "&Undo"),
            "Redo": QtWidgets.QAction(QtGui.QIcon("resources/icons/redo.png"), "&Redo"),
            "Font": QtWidgets.QAction(QtGui.QIcon("resources/icons/font.png"), "&Font"),
            "Delete": QtWidgets.QAction(QtGui.QIcon("resources/icons/delete.png"), "&Delete"),
            "Export PDF": QtWidgets.QAction(QtGui.QIcon("resources/icons/pdf.png"), "&Export PDF")
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
        self.tool_bar.addAction(self.tool_actions["Font"])
        self.tool_actions["Font"].setStatusTip("Prikaz tekstualnog stila!")
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.tool_actions["Delete"])
        self.tool_actions["Delete"].setStatusTip("Obriši dokument!")
        self.tool_bar.addAction(self.tool_actions["Export PDF"])
        self.tool_actions["Export PDF"].setStatusTip("Napravi PDF dokument!")

        #toolAkcije
        self.tool_actions["Undo"].triggered.connect(self.text_edit.undo)
        self.tool_actions["Redo"].triggered.connect(self.text_edit.redo)
        self.tool_actions["Delete"].triggered.connect(self.text_edit.deleteLater)
        self.tool_actions["New file"].triggered.connect(self.handle)
        self.tool_actions["Font"].triggered.connect(self.font_dialog)
        self.tool_actions["Save"].triggered.connect(self.file_save)
        self.tool_actions["Export PDF"].triggered.connect(self.pdf_export)




        self._layout.addWidget(self.tool_bar)
        self._layout.addWidget(self.text_edit)
        
        self.setLayout(self._layout)

    def handle(self):
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self)
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            self.text_edit.setText(text_from_file)

    def font_dialog(self):
        (ok, font) = QtWidgets.QFontDialog.getFont()
 
        if ok:
            self.text_edit.setFont(font)

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save')[0]
        print(name)
        file = open(name + ".txt",'w')
        text = self.text_edit.toPlainText()
        print(text)
        file.write(text)
        file.close()

    
    def pdf_export(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf); All files")
 
        if fn != '':
 
            if QFileInfo(fn).suffix() == "": fn += '.pdf'
 
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.text_edit.document().print_(printer)