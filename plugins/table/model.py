from PySide2 import QtCore


class Model(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, metadata={}, db_data=[]):
        super().__init__(parent)
        self.metadata = metadata
        self.db_data = db_data


    def get_element(self, index):
        return self.db_data[index.row()]

    def rowCount(self, index):
        return len(self.db_data)

    def columnCount(self, index):
        return len(self.metadata["columns"])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        item = self.get_element(index)

        for c in range(len(self.metadata["columns"])):
            if index.column() == c and role == QtCore.Qt.DisplayRole:
                return item[c]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        for c in range(len(self.metadata["columns"])):
            if section == c and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.metadata["columns"][c]
