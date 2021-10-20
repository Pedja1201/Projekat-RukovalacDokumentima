from PySide2 import QtWidgets, QtGui, QtCore

##TODO: povezana je tabela,resi klase!!!

class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        self.create_tab_widget()

        
        self.main_text = QtWidgets.QTextEdit()
        self.main_layout.addWidget(self.main_text)

        table1 = self.create_table(5, 5)
        subtable1 = self.create_table(4, 4)
        subtable2 = self.create_table(3, 3)

        self.tab_widget.addTab(subtable1, QtGui.QIcon("resources/icons/icons8-grid-2-64.png"), "Table 1")
        self.tab_widget.addTab(subtable2, QtGui.QIcon("resources/icons/icons8-grid-2-64.png"), "Table 2")

        self.main_layout.addWidget(table1)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)
    

    def create_table(self, rows, columns):
        table_widget = QtWidgets.QTableWidget(rows, columns, self)

        for i in range(rows):
            for j in range(columns):
                table_widget.setItem(i, j, QtWidgets.QTableWidgetItem("Celija " + str(i) + str(j)))
        labels = []
        for i in range(columns):
            labels.append("Kolona" + str(i))
        table_widget.setHorizontalHeaderLabels(labels)
        return table_widget


    
    def create_tab_widget(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def show_text(self, text):
        self.main_text.setText(text)

    