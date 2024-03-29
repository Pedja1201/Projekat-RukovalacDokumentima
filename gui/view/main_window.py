import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from gui.view.dock_widget_tree import DockWidget  #Beta klasa za otvaranje xml kolekcije dokumenata.
from ..view.strukture_dock import StructureDock
from ..model.document_model import DocumentModel
from ..model.document import Document
from ..model.page import Page
from os.path import abspath
from gui.view.dialogs.plugin_dialog import PluginDialog
from .workspace import WorkspaceWidget ##Ovom klasom bi resili problem tipiziranja 
                                                #dokumenata tako sto bi je prosledili u 
                                                #read_file da otvara svaki dokument u poseban tabWidget.


# FIXME: Raspodeliti nadleznosti na druge view-ove.
class MainWindow(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor.
    """
    def __init__(self, ps, parent=None):
        super().__init__(parent)
        # Podesavanje prozora
        self.setWindowTitle("Rukovalac dokumentima")
        self.setWindowIcon(QtGui.QIcon("resources/icons/singi.jpg"))
        self.resize(800, 600)
    

        # Definisanje delova aplikacije
        self.menubar = QtWidgets.QMenuBar(self)
        self.file_menu = QtWidgets.QMenu("File")
        self.edit_menu = QtWidgets.QMenu("Edit")
        self.window_menu = QtWidgets.QMenu("Window")
        self.help_menu = QtWidgets.QMenu("Help")
        self.plugin_menu = QtWidgets.QMenu("Plugins")
        self.toolbar = QtWidgets.QToolBar("Toolbar", self)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) ##Pazi na conflict
        self.toolbar1 = QtWidgets.QToolBar(self)##Drugi toolbar
        self.central_widget = QtWidgets.QTabWidget(self)### Zbog tipa mozemo promeniti u QTabWidget
        self.workspace = WorkspaceWidget(self) #Workspace - Promenljiva za prikaz tabova
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.showMessage("Status Bar is Ready!")
        self.project_dock = StructureDock("Struktura dokumenta", self)
        self.xml_dock = QtWidgets.QDockWidget("Documents",self) #FIXME: Otvaranje xml strukture u workspace
        self.plugin_service = ps

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
            "plugin_settings": QtWidgets.QAction(QtGui.QIcon("resources/icons/puzzle.png"), "&Plugin settings")
        }
        #Akcije toolbara
        self.tool_actions = {
            "New file": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&New file"),
            "Save": QtWidgets.QAction(QtGui.QIcon("resources/icons/save.png"), "&Save"),
            "Undo": QtWidgets.QAction(QtGui.QIcon("resources/icons/undo.png"), "&Undo"),
            "Redo": QtWidgets.QAction(QtGui.QIcon("resources/icons/redo.png"), "&Redo"),
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
        self.setCentralWidget(self.central_widget)
        #Workspace - Nova promenljiva workspace za prikaz i uklanjanje tabova
        self.central_widget.addTab(self.workspace, "Welcome Page")  
        self.central_widget.setTabsClosable(True)
        self.central_widget.tabCloseRequested.connect(self.delete_tab)

        self.setStatusBar(self.statusbar)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.project_dock)
        self.add_dock_widget() #Novi DockWidget za xml kolekciju
        # uvezivanje akcija
        self._bind_actions()
        self._bind_shortcuts()

        #Dodavanje dock widzeta (xml varijanta)
    def add_dock_widget(self):#metoda za dodavanje u widgeta, u main.py je plugin_registry i tamo se stavi taj id od vidzeta i poziva kao ostali
        self.widgets = DockWidget(self)
        self.xml_dock.setWidget(self.widgets)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.xml_dock)
        self.widgets.kliknut.connect(self.read_file)

    

    def read_file(self, index):
        path = self.project_dock.model.filePath(index)
        with open(path) as f:
            text = (f.read())                                       #Workspace
            new_workspace = WorkspaceWidget(self.central_widget)
            # self.central_widget.addTab(new_workspace, path.split("/")[-1])
            self.central_widget.addTab(new_workspace, "Page"+ "/" + path.split("/")[-1])
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
        self.menu_actions["Open"].setStatusTip("Otvorite novi dokument!")
        self.file_menu.addAction(self.menu_actions["Save"])
        self.menu_actions["Save"].setStatusTip("Sačuvaj dokument!")
        self.file_menu.addAction(self.menu_actions["Print"])
        self.menu_actions["Print"].setStatusTip("Štampanje dokumenata!")
        self.menubar.addMenu(self.file_menu)

        self.edit_menu.addAction(self.menu_actions["Undo"])
        self.menu_actions["Undo"].setStatusTip("Korak nazad!")
        self.edit_menu.addAction(self.menu_actions["Copy"])
        self.menu_actions["Copy"].setStatusTip("Kopiraj dokument!")
        self.edit_menu.addAction(self.menu_actions["Paste"])
        self.menu_actions["Paste"].setStatusTip("Nalepi dokument!")
        self.menubar.addMenu(self.edit_menu)



        self.window_menu.addAction(self.menu_actions["Close"])
        self.menu_actions["Close"].setStatusTip("Da li ste sigurni da želite izlazak?")
        toggle_structure_dock_action1 = self.project_dock.toggleViewAction()
        toggle_structure_dock_action2 = self.xml_dock.toggleViewAction()
        toggle_toolbar_action = self.toolbar.toggleViewAction()
        self.menubar.addMenu(self.window_menu)
        self.window_menu.addAction(toggle_structure_dock_action1)
        self.window_menu.addAction(toggle_structure_dock_action2)
        self.window_menu.addAction(toggle_toolbar_action)

        self.help_menu.addAction(self.menu_actions["about"])
        self.menu_actions["about"].setStatusTip("Poruka o nama!")
        self.menubar.addMenu(self.help_menu)
        # self.file_menu.addAction(self.menu_actions["plugin_settings"])
        #self.tools_menu.addAction(self.action_dict["plugin_settings"])

        self.plugin_menu.addAction(self.menu_actions["plugin_settings"])
        self.menu_actions["plugin_settings"].setStatusTip("Otvorite plugin servis!")
        self.menubar.addMenu(self.plugin_menu)

    def _populate_toolbar(self):
        self.toolbar.addAction(self.tool_actions["New file"])
        self.tool_actions["New file"].setStatusTip("Otvori novi dokument!")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Save"])
        self.tool_actions["Save"].setStatusTip("Sačuvaj dokument!")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Undo"])
        self.tool_actions["Undo"].setStatusTip("Korak nazad!")
        self.toolbar.addAction(self.tool_actions["Redo"])
        self.tool_actions["Redo"].setStatusTip("Ponovno vraćanje!")
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_actions["Delete"])
        self.tool_actions["Delete"].setStatusTip("Obriši dokument!")

        self.toolbar1.addAction(self.menu_actions["about"])    
        self.menu_actions["about"].setStatusTip("Poruka o nama!")


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
        self.menu_actions["Undo"].triggered.connect(self.workspace.main_text.undo)
        self.menu_actions["Copy"].triggered.connect(self.workspace.main_text.copy)
        self.menu_actions["Paste"].triggered.connect(self.workspace.main_text.paste)

        self.tool_actions["New file"].triggered.connect(self.on_open)##Pedja dodao
        self.tool_actions["Save"].triggered.connect(self.file_save) #Pedja
        self.tool_actions["Undo"].triggered.connect(self.workspace.main_text.undo)
        self.tool_actions["Redo"].triggered.connect(self.workspace.main_text.redo)
        self.tool_actions["Delete"].triggered.connect(self.central_widget.deleteLater) #Pedja

        self.menu_actions["Close"].triggered.connect(self.button_close) #Pedja
        self.menu_actions["Print"].triggered.connect(self.print) #Pedja

        self.menu_actions["Save"].triggered.connect(self.file_save) #Pedja

        self.project_dock.tree.clicked.connect(self.read_file)#Prikaz dokumenta iz strukture dok.
        # self.xml_dock.xmletree.clicked.connect(self.read_file)#Prikaz dokumenta iz strukture dok.
        self.menu_actions["plugin_settings"].triggered.connect(self.on_open_plugin_settings_dialog)


    def _bind_shortcuts(self):
        self.menu_actions["Open"].setShortcut('Ctrl+O')
        self.menu_actions["Close"].setShortcut('Ctrl+Q')
        self.menu_actions["Print"].setShortcut('Ctrl+P')
        self.menu_actions["Save"].setShortcut('Ctrl+S')
        self.menu_actions["Undo"].setShortcut('Ctrl+Z')
        self.tool_actions["Redo"].setShortcut('Ctrl+Y')
        self.menu_actions["plugin_settings"].setShortcut('Ctrl+E') # E kao Extension, posto je Ctrl+P (kao Plugin) zauzeto za Print

    def on_open_plugin_settings_dialog(self):
        dialog = PluginDialog("Plugin settings", self, self.plugin_service)
        dialog.exec_()



    def print(self): ##Klikom na Print izbacuje dialog za stampanje
        self.printer = QPrinter(QPrinter.HighResolution)
        self.previewDialog = QPrintPreviewDialog(self.printer, self)

        self.previewDialog.paintRequested.connect(self.print_preview)
        self.previewDialog.exec_()

    def print_preview(self, printer): #Pomoc printu
        self.workspace.main_text.print_(printer)

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
            sys.exit()
        else:
            print("No!")
        
    
    def on_open(self): #Pedja dodao
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open document", ".")
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            new_workspace = WorkspaceWidget(self.central_widget)
            self.central_widget.addTab(new_workspace, file_name[-1])
            new_workspace.show_text(text_from_file)

    #FIXME: Poterbno je omoguciti cuvanje text file
    #DONE: Omoguceno cuvanje text file-a
    def file_save(self): # Izbacuje: TypeError: expected str, bytes or os.PathLike object, not tuple
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save')[0]
        print(name) # ovaj print je prosao samo prilikom prvog pokretanja i ispisao je tuple: ('', '')
        # kod svakog narednog pokretanja ga preskace, ali dolazi do file = open(name,'w')
        file = open(name + ".rudok",'w') #Bez extenzije jer biramo sami kako cemo sacuvati (Default = *.txt)
        text = self.workspace.main_text.toPlainText() #Dolazak skroz do unosenja teksta i njegove klase.
        print(text)
        file.write(text)
        file.close()

    def about_action(self):
        """
        Metoda koja prikazuje informacioni dijalog korisniku o aplikaciji.
        """
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "About Rukovalac dokumentima", "Autori: Studenti Univerziteta Singidunum, Centar Novi Sad.", parent = self)
        msg.addButton(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        
    def set_central_widget(self, name: str):
        """
        Podesava centralni widget glavnog prozora, na osnovu simboličkog imena se dobija plugin
        koji će se smestiti u centralni deo glavnog prozora.

        :param symbolic_name: Simbolicko ime plugina koji želimo da instanciramo.
        """
        # try:

        plugin = self.plugin_service.get_by_name(name)
        widgets = plugin.get_widget()
        # self.central_widget.addTab(widgets[0], name.split("/")[-1])
        self.central_widget.addTab(widgets[0],  "Page" + "/" + name.split("/")[-1])
        if widgets[1] is not None:
            self.toolbar.addSeparator()
            self.toolbar.addActions(widgets[1].actions())
        self.menubar.addMenu(widgets[2]) if widgets[2] is not None else None
        # except IndexError:
        #     print("Ne postoji ni jedan plugin sa zadatim simboličkim imenom!")

    ##Workspace
    def delete_tab(self,index):
        self.central_widget.removeTab(index)