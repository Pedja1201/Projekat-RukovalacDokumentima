from PySide2 import QtCore

class StudentModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.students = []

        #Pomocna metoda
    def get_element(self, index):
        return self.students[index.row()]

    def rowCount(self, index): #Broj redova
        return len(self.students)

    def columnCount(self, index): #Broj kolona(Onoliko koliko nam treba=[2])
        return 2

    
    def data(self, index, role = QtCore.Qt.DisplayRole): 
        student = self.get_element(index)
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return student.broj_indeksa
        elif index.column() == 1 and role == QtCore.Qt.DisplayRole:
            return student.ime_prezime
        return None

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if section == 0 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Broj indeksa"
        elif section == 1 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Ime i prezime"
        return None

    #Metode za editTable model
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        student = self.get_element(index)
        if value == "":
            return False
        if index.column() == 0 and role == QtCore.Qt.EditRole:
            student.broj_indeksa = value
            return True
        elif index.column() == 1 and role == QtCore.Qt.EditRole:
            student.ime_prezime = value
            return True
        return False


    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable
