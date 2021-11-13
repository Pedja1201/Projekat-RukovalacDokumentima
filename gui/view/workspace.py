from PySide2 import QtWidgets, QtGui, QtCore

##TODO: povezana je tabela,resi klase!!!

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        # self.create_tab_widget()

        
        self.main_text = QtWidgets.QTextEdit()
        self.main_layout.addWidget(self.main_text)

    
        # self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)
    


    
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def show_text(self, text):
        self.main_text.setText(text)

    