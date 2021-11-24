from PySide2 import QtCore, QtGui, QtWidgets

class FindDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        findLabel = QtWidgets.QLabel("Enter the name of a contact:")
        self.lineEdit = QtWidgets.QLineEdit()

        self.findButton = QtWidgets.QPushButton("&Find")
        self.findText = ''

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(findLabel)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.findButton)

        self.setLayout(layout)
        self.setWindowTitle("Find a Contact")

        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()

        if not text:
            QtWidgets.QMessageBox.information(self, "Empty Field",
                    "Please enter a name.")
            return

        self.findText = text
        self.lineEdit.clear()
        self.hide()

    def getFindText(self):
        return self.findText