from PySide2 import QtWidgets


class TextEdit(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO: dodati meni
        # TODO: toolbar
        self._layout = QtWidgets.QVBoxLayout()
        self.text_edit = QtWidgets.QTextEdit(self)
        self.tool_bar = QtWidgets.QToolBar("Naslov", self)

        self._layout.addWidget(self.tool_bar)
        self._layout.addWidget(self.text_edit)
        
        self.setLayout(self._layout)
        # u layout dodati toolbar i menubar
        # sam widget koji je npr. textedit
