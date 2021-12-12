import subprocess
from PySide2 import QtGui, QtWidgets
from plugins.table.controller import Handler
from plugins.table.model import Model

class View(QtWidgets.QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self._layout = QtWidgets.QVBoxLayout()
            self.tool_bar = QtWidgets.QToolBar("Table", self)
    
            #ToolAkcije
            self.tool_actions = {
                "Open": QtWidgets.QAction(QtGui.QIcon("resources/icons/file.png"), "&Open")#,
            }

            #ToolBar
            self.tool_bar.addAction(self.tool_actions["Open"])
            self.tool_actions["Open"].setStatusTip("Otvorite tabelu")
            self.tool_actions["Open"].triggered.connect(self.on_open)

            self._layout.addWidget(self.tool_bar)        
            self.setLayout(self._layout)

        def on_open(self):
            content_name = QtWidgets.QFileDialog.getOpenFileName(self)[0]
            subprocess.Popen([content_name], shell=True)
            
            
    # def __init__(self, parent, metadata={}):
    #     super().__init__(parent)
    #     self.metadata = metadata
    #     self.main_layout = QtWidgets.QVBoxLayout()
    #     self.tab_widget = None
    #     self.handler = Handler(self.metadata)
    #     self.create_tab_widget()

    #     self.table1 = QtWidgets.QTableView(self.tab_widget)
         
    #     self.main_layout.addWidget(self.table1)
    #     self.main_layout.addWidget(self.tab_widget)
    #     self.setLayout(self.main_layout)
    #     self.change_model()
        
    # def change_model(self, table_index=0):
    #     data = self.handler.get_all(self.metadata["tables"][table_index]["name"])
    #     model = Model(self, self.metadata["tables"][table_index], data)
    #     self.table1.setModel(model)

    # def create_tab_widget(self):
    #     self.tab_widget = QtWidgets.QTabWidget(self)
    #     self.tab_widget.setTabsClosable(True)
    #     self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    # def delete_tab(self, index):
    #     self.tab_widget.removeTab(index)

        
