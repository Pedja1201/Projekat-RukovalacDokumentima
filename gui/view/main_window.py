from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from ..view.strukture_dock import StructureDock
from ..model.document_model import DocumentModel
from ..model.document import Document
from ..model.page import Page
from os.path import abspath


# FIXME: Raspodeliti nadleznosti na druge view-ove.
class MainWindow(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Podesavanje prozora
        self.setWindowTitle("Rukovalac dokumentima")
        self.setWindowIcon(QtGui.QIcon("resources/icons/singi.jpg"))
        self.resize(640, 480)
    

        # Definisanje delova aplikacije
        self.menubar = QtWidgets.QMenuBar(self)
        self.file_menu = QtWidgets.QMenu("File")
        self.edit_menu = QtWidgets.QMenu("Edit")
        self.window_menu = QtWidgets.QMenu("Window")
        self.help_menu = QtWidgets.QMenu("Help")
        self.toolbar = QtWidgets.QToolBar("Toolbar", self)
        self.toolbar1 = QtWidgets.QToolBar(self)##Drugi toolbar
        self.central_widget = QtWidgets.QTextEdit(self)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.showMessage("Status Bar is Ready!")
        # self.project_dock = QtWidgets.QDockWidget("Struktura dokumenta", self)
        self.project_dock = StructureDock("Struktura dokumenta", self)

        # Akcije menija
        # TODO: Dodati i ostale akcije
        self.menu_actions = {
            "Open": QtWidgets.QAction(QtGui.QIcon("resources/icons/create_file.png"), "&Open"),
            "Save": QtWidgets.QAction(QtGui.QIcon("resources/icons/save.png"), "&Save"),
            "Print": QtWidgets.QAction(QtGui.QIcon("resources/icons/print.png"), "&Print"),
            "Undo": QtWidgets.QAction(QtGui.QIcon("resources/icons/undo.png"), "&Undo"),
            "Copy": QtWidgets.QAction(QtGui.QIcon("resources/icons/copy.png"), "&Copy"),
            "Paste": QtWidgets.QAction(QtGui.QIcon("resources/icons/paste.png"), "&Paste"),
            "Close": QtWidgets.QAction(QtGui.QIcon("resources/icons/end.png"), "&Close"),
            "about": QtWidgets.QAction(QtGui.QIcon("resources/icons/about.png"), "&About"),
        }
        #Akcije toolbara
        self.tool_actions = {
            "New file": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&New file"),
            "Save": QtWidgets.QAction(QtGui.QIcon("resources/icons/save.png"), "&Save"),
            "Undo": QtWidgets.QAction(QtGui.QIcon("resources/icons/undo.png"), "&Undo"),
            "Delete": QtWidgets.QAction(QtGui.QIcon("resources/icons/delete.png"), "&Delete"),
        }

        # Dodavanje elemenata na glavni prozor
        self._populate_main_window()

    def _populate_main_window(self):
        # populisanje menija
        self._populate_menus()
        self._populate_toolbar()
        # postavljanje widgeta na window
        self.setMenuBar(self.menubar)
        self.addToolBar(self.toolbar)
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolbar1)##Primer za drugi toolbar sa desne strane

        # populisanje textWidgeta u centralnom widgetu
        self._populate_text_widget()
        # postavljanje dock widgeta (mozemo ih imati proizvoljan broj)
        self._populate_project_dock()
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.statusbar)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.project_dock)
        # uvezivanje akcija
        self._bind_actions()
        self._bind_shortcuts()

    def _populate_project_dock(self):
        self.project_dock.tree.clicked.connect(self.read_file)
    #     self.project_dock.setWidget(QtWidgets.QTreeView(self.project_dock))
    #     # TODO: Primer za file system sadrzaj
    #     model = QtWidgets.QFileSystemModel()
    #     model.setRootPath(QtCore.QDir.currentPath())
    #     self.project_dock.widget().setModel(model)
    #     self.project_dock.widget().setRootIndex(model.index(QtCore.QDir.currentPath()))

    #FIXME: Najveci problem-Ucitavanje dokumenta iz struk
    def read_file(self, index):
        path = self.project_dock.model.filePath(index)
        with open(path) as f:
            text = (f.read())
            new_workspace = QtWidgets.QWidget(self.central_widget)
            self.central_widget.setText(new_workspace, path.split("/")[-1])
            new_workspace.show_text(text)

    def _populate_text_widget(self):
        """
            Populisati prilikom ucitavanja konteksta, kreirati sve tabove koji su bili otvoreni
            sa widgetima. Podesiti modele za svaki ucitani widget.

        """
        text_editor_wgt = QtWidgets.QTextEdit(self)
        self.setCentralWidget(text_editor_wgt)
    

    def _populate_menus(self):
        """
        Privatna metoda koja smesta menije u meni bar.
        """
        self.file_menu.addAction(self.menu_actions["Open"])
        self.file_menu.addAction(self.menu_actions["Save"])
        self.file_menu.addAction(self.menu_actions["Print"])
        self.menubar.addMenu(self.file_menu)

        self.edit_menu.addAction(self.menu_actions["Undo"])
        self.edit_menu.addAction(self.menu_actions["Copy"])
        self.edit_menu.addAction(self.menu_actions["Paste"])
        self.menubar.addMenu(self.edit_menu)

        self.window_menu.addAction(self.menu_actions["Close"])
        toggle_structure_dock_action = self.project_dock.toggleViewAction()
        toggle_toolbar_action = self.toolbar.toggleViewAction()
        self.menubar.addMenu(self.window_menu)
        self.window_menu.addAction(toggle_structure_dock_action)
        self.window_menu.addAction(toggle_toolbar_action)

        self.help_menu.addAction(self.menu_actions["about"])
        self.menubar.addMenu(self.help_menu)

    def _populate_toolbar(self):
        self.toolbar.addAction(self.tool_actions["New file"])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Save"])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Undo"])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Delete"])

        self.toolbar1.addAction(self.menu_actions["about"])

    def _set_models(self, models=[]):
        """
            Populise modele u tabove redom.
        """
        print(self.central_widget.count())
        for i in range(self.central_widget.count()):
            widget = self.central_widget.widget(i)
            widget.setModel(models[i])

    def _bind_actions(self):
        """
        Privatna metoda koja uvezuje reagovanje na dogadjaje.
        """
        self.menu_actions["about"].triggered.connect(self.about_action)
        self.menu_actions["Open"].triggered.connect(self.on_open)##Pedja dodao
        self.menu_actions["Undo"].triggered.connect(self.central_widget.undo)

        self.tool_actions["New file"].triggered.connect(self.on_open)##Pedja dodao
        self.tool_actions["Undo"].triggered.connect(self.central_widget.undo)
        self.tool_actions["Delete"].triggered.connect(self.central_widget.deleteLater) #Pedja

        self.menu_actions["Close"].triggered.connect(self.button_close) #Pedja
        self.menu_actions["Print"].triggered.connect(self.print) #Pedja

        self.menu_actions["Save"].triggered.connect(self.file_save) #Pedja


    def _bind_shortcuts(self):
        self.menu_actions["Open"].setShortcut('Ctrl+O')
        self.menu_actions["Close"].setShortcut('Ctrl+Q')
        self.menu_actions["Print"].setShortcut('Ctrl+P')
        self.menu_actions["Save"].setShortcut('Ctrl+S')
        self.menu_actions["Undo"].setShortcut('Ctrl+U')

    def print(self): ##Klikom na Print izbacuje dialog za stampanje
        self.printer = QPrinter(QPrinter.HighResolution)
        self.previewDialog = QPrintPreviewDialog(self.printer, self)

        self.previewDialog.paintRequested.connect(self.print_preview)
        self.previewDialog.exec_()

    def print_preview(self, printer): #Pomoc printu
        self.central_widget.print_(printer)

    #FIXME:Namestiti da klikom 'Yes' izadje iz cele app a ne samo iz dialoga
    def button_close(self): #Izbaci box dialog kad stisnemo Close.
        self.dlg = QtWidgets.QMessageBox(self)
        self.dlg.setWindowTitle("Upozorenje!")
        self.dlg.setText("Da li sigurno zelite da napustite aplikaciju?")
        self.dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.dlg.setIcon(QtWidgets.QMessageBox.Question)
        button = self.dlg.exec_()
        if button == QtWidgets.QMessageBox.Yes:
            print("Yes!")
        else:
            print("No!")
        
    
    def on_open(self): #Pedja dodao
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open python file", ".", "Python Files (*.py)")
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            self.central_widget.setText(text_from_file)

    #FIXME: Poterbno je omoguciti cuvanje text file
    def file_save(self): 
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def about_action(self):
        """
        Metoda koja prikazuje informacioni dijalog korisniku o aplikaciji.
        """
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "About Rukovalac dokumentima", "Autori: Studenti Univerziteta Singidunum, Centar Novi Sad.", parent = self)
        msg.addButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()