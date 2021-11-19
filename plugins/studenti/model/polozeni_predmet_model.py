from PySide2 import QtCore

class PolozeniPredmetModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.polozeni_predmeti = []
        

    def get_element(self, index):
        return self.polozeni_predmeti[index.row()]

    def rowCount(self, index):
        return len(self.polozeni_predmeti)

    def columnCount(self, index):
        return 3

    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        predmet = self.get_element(index)
        if index.column() == 0 and role == QtCore.Qt.DisplayRole:
            return predmet.naziv
        elif index.column() == 1 and role == QtCore.Qt.DisplayRole:
            return predmet.silabus
        elif index.column() == 2 and role == QtCore.Qt.DisplayRole:
            return predmet.ocena
        return None

    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if section == 0 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Naziv"
        elif section == 1 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Silabus"
        elif section == 2 and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Ocena"
        return None

    #Metode za editTable model
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        predmet = self.get_element(index)
        if value == "":
            return False
        if index.column() == 0 and role == QtCore.Qt.EditRole:
            predmet.naziv = value
            return True
        elif index.column() == 1 and role == QtCore.Qt.EditRole:
            predmet.silabus = value
            return True
        elif index.column() == 2 and role == QtCore.Qt.EditRole:
            predmet.ocena = value
            return True
        return False


    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable
