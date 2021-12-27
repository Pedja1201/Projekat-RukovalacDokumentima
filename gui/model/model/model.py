import logging
import os
from PySide2.QtCore import Qt, Slot, QModelIndex, QAbstractListModel, QAbstractTableModel, QAbstractItemModel
from PySide2.QtWidgets import QMessageBox
from config import INVALID_CHARS, TOOL_OUTPUT_DIR
from helpers import rename_dir

class MinimalTableModel(QAbstractTableModel):
    """Table model for outlining simple tabular data.

    Attributes:
        parent (QMainWindow): the parent widget, usually an instance of TreeViewForm
    """

    def __init__(self, parent=None):
        """Initialize class"""
        super().__init__(parent)
        self._parent = parent
        self._main_data = list()  # DisplayRole and EditRole
        self.default_flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        self.header = list()  # DisplayRole and EditRole
        self.aux_header = list()  # All the other roles, each entry in the list is a dict

    def clear(self):
        """Clear all data in model."""
        self.beginResetModel()
        self._main_data = list()
        self.endResetModel()


    def flags(self, index):
        """Return index flags."""
        if not index.isValid():
            return Qt.NoItemFlags
        return self.default_flags


    def rowCount(self, parent=QModelIndex()):
        """Number of rows in the model."""
        return len(self._main_data)


    def columnCount(self, parent=QModelIndex()):
        """Number of columns in the model."""
        try:
            return len(self._main_data[0])
        except IndexError:
            return len(self.header)


    def headerData(self, section, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        """Get headers."""
        if role != Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                try:
                    return self.aux_header[section][role]
                except IndexError:
                    return None
                except KeyError:
                    return None
            return None
        if orientation == Qt.Horizontal:
            try:
                return self.header[section]
            except IndexError:
                return None
        if orientation == Qt.Vertical:
            return section + 1


    def set_horizontal_header_labels(self, labels):
        """Set horizontal header labels."""
        if not labels:
            return
        self.header = labels
        self.aux_header = [{} for _ in range(len(labels))]
        self.headerDataChanged.emit(Qt.Horizontal, 0, len(labels) - 1)


    def insert_horizontal_header_labels(self, section, labels):
        """Insert horizontal header labels at the given section."""
        if not labels:
            return
        for j, value in enumerate(labels):
            if section + j >= self.columnCount():
                self.header.append(value)
                self.aux_header.append({})
            else:
                self.header.insert(section + j, value)
                self.aux_header.insert(section + j, {})
        self.headerDataChanged.emit(Qt.Horizontal, section, section + len(labels) - 1)


    def horizontal_header_labels(self):
        return self.header


    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        """Sets the data for the given role and section in the header
        with the specified orientation to the value supplied.
        """
        if orientation != Qt.Horizontal:
            return False
        if role != Qt.EditRole:
            try:
                self.aux_header[section][role] = value
                self.headerDataChanged.emit(orientation, section, section)
                return True
            except IndexError:
                return False
        try:
            self.header[section] = value
            self.headerDataChanged.emit(orientation, section, section)
            return True
        except IndexError:
            return False


    def data(self, index, role=Qt.DisplayRole):
        """Returns the data stored under the given role for the item referred to by the index.

        Args:
            index (QModelIndex): Index of item
            role (int): Data role

        Returns:
            Item data for given role.
        """
        if not index.isValid():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        try:
            return self._main_data[index.row()][index.column()]
        except IndexError:
            logging.error("Cannot access model data at index %s", index)
            return None


    def row_data(self, row, role=Qt.DisplayRole):
        """Returns the data stored under the given role for the given row.

        Args:
            row (int): Item row
            role (int): Data role

        Returns:
            Row data for given role.
        """
        if not 0 <= row < self.rowCount():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        return self._main_data[row]


    def column_data(self, column, role=Qt.DisplayRole):
        """Returns the data stored under the given role for the given column.

        Args:
            column (int): Item column
            role (int): Data role

        Returns:
            Column data for given role.
        """
        if not 0 <= column < self.columnCount():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        return [self._main_data[row][column] for row in range(self.rowCount())]


    def model_data(self, role=Qt.DisplayRole):
        """Returns the data stored under the given role in the entire model.

        Args:
            role (int): Data role

        Returns:
            Model data for given role.
        """
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._main_data
        return [self.row_data(row, role) for row in range(self.rowCount())]


    def setData(self, index, value, role=Qt.EditRole):
        """Set data in model."""
        if not index.isValid():
            return False
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return False
        return self.batch_set_data([index], [value])


    def batch_set_data(self, indexes, data):
        """Batch set data for indexes."""
        if not indexes:
            return False
        if len(indexes) != len(data):
            return False
        for k, index in enumerate(indexes):
            if not index.isValid():
                continue
            self._main_data[index.row()][index.column()] = data[k]
        # Find square envelope of indexes to emit dataChanged
        top = min(ind.row() for ind in indexes)
        bottom = max(ind.row() for ind in indexes)
        left = min(ind.column() for ind in indexes)
        right = max(ind.column() for ind in indexes)
        self.dataChanged.emit(self.index(top, left), self.index(bottom, right), [Qt.EditRole, Qt.DisplayRole])
        return True


    def insertRows(self, row, count, parent=QModelIndex()):
        """Inserts count rows into the model before the given row.
        Items in the new row will be children of the item represented
        by the parent model index.

        Args:
            row (int): Row number where new rows are inserted
            count (int): Number of inserted rows
            parent (QModelIndex): Parent index

        Returns:
            True if rows were inserted successfully, False otherwise
        """
        if row < 0 or row > self.rowCount():
            return False
        if count < 1:
            return False
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            if self.columnCount() == 0:
                new_main_row = [None]
            else:
                new_main_row = [None for j in range(self.columnCount())]
            # Notice if insert index > rowCount(), new object is inserted to end
            self._main_data.insert(row + i, new_main_row)
        self.endInsertRows()
        return True


    def insertColumns(self, column, count, parent=QModelIndex()):
        """Inserts count columns into the model before the given column.
        Items in the new column will be children of the item represented
        by the parent model index.

        Args:
            column (int): Column number where new columns are inserted
            count (int): Number of inserted columns
            parent (QModelIndex): Parent index

        Returns:
            True if columns were inserted successfully, False otherwise
        """
        if column < 0 or column > self.columnCount():
            return False
        if count < 1:
            return False
        self.beginInsertColumns(parent, column, column + count - 1)
        for j in range(count):
            for i in range(self.rowCount()):
                self._main_data[i].insert(column + j, None)
        self.endInsertColumns()
        return True


    def removeRows(self, row, count, parent=QModelIndex()):
        """Removes count rows starting with the given row under parent.

        Args:
            row (int): Row number where to start removing rows
            count (int): Number of removed rows
            parent (QModelIndex): Parent index

        Returns:
            True if rows were removed successfully, False otherwise
        """
        if row < 0 or row + count - 1 >= self.rowCount():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in reversed(range(row, row + count)):
            self._main_data.pop(i)
        self.endRemoveRows()
        return True


    def removeColumns(self, column, count, parent=QModelIndex()):
        """Removes count columns starting with the given column under parent.

        Args:
            column (int): Column number where to start removing columns
            count (int): Number of removed columns
            parent (QModelIndex): Parent index

        Returns:
            True if columns were removed successfully, False otherwise
        """
        if column < 0 or column >= self.columnCount():
            return False
        if not count == 1:
            logging.error("Remove 1 column at a time")
            return False
        self.beginRemoveColumns(parent, column, column)
        # for loop all rows and remove the column from each
        removing_last_column = False
        if self.columnCount() == 1:
            removing_last_column = True
        for r in self._main_data:
            r.pop(column)
        if removing_last_column:
            self._main_data = []
        # logging.debug("{0} removed from column:{1}".format(removed_column, column))
        self.endRemoveColumns()
        return True


    def reset_model(self, main_data=None):
        """Reset model."""
        if main_data is None:
            main_data = list()
        self.beginResetModel()
        self._main_data = main_data
        self.endResetModel()



class EmptyRowModel(MinimalTableModel):
    """A table model with a last empty row."""

    def __init__(self, parent=None):
        """Init class."""
        super().__init__(parent)
        self.default_row = {}  # A row of default values to put in any newly inserted row
        self.force_default = False  # Whether or not default values are editable
        self.dataChanged.connect(self._handle_data_changed)
        self.rowsRemoved.connect(self._handle_rows_removed)
        self.rowsInserted.connect(self._handle_rows_inserted)

    def flags(self, index):
        """Return default flags except if forcing defaults."""
        if not index.isValid():
            return Qt.NoItemFlags
        if self.force_default:
            try:
                name = self.header[index.column()]
                if name in self.default_row:
                    return self.default_flags & ~Qt.ItemIsEditable
            except IndexError:
                pass
        return self.default_flags


    def set_default_row(self, **kwargs):
        """Set default row data."""
        self.default_row = kwargs


    def clear(self):
        super().clear()
        self.insertRows(self.rowCount(), 1, QModelIndex())


    def reset_model(self, data):
        super().reset_model(data)
        self.insertRows(self.rowCount(), 1, QModelIndex())


    @Slot("QModelIndex", "QModelIndex", "QVector", name="_handle_data_changed")
    def _handle_data_changed(self, top_left, bottom_right, roles=None):
        """Insert a new last empty row in case the previous one has been filled
        with any data other than the defaults."""
        if roles is None:
            roles = list()
        if roles and Qt.EditRole not in roles:
            return
        last_row = self.rowCount() - 1
        for column in range(self.columnCount()):
            try:
                name = self.header[column]
            except IndexError:
                name = None
            data = self._main_data[last_row][column]
            default = self.default_row.get(name)
            if not data and not default:
                continue
            if data != default:
                self.insertRows(self.rowCount(), 1)
                break


    @Slot("QModelIndex", "int", "int", name="_handle_rows_removed")
    def _handle_rows_removed(self, parent, first, last):
        """Insert a new empty row in case it's been removed."""
        last_row = self.rowCount()
        if last_row in range(first, last + 1):
            self.insertRows(self.rowCount(), 1)


    @Slot("QModelIndex", "int", "int", name="_handle_rows_inserted")
    def _handle_rows_inserted(self, parent, first, last):
        """Handle rowsInserted signal."""
        self.set_rows_to_default(first, last)


    def set_rows_to_default(self, first, last):
        """Set default data in newly inserted rows."""
        left = None
        right = None
        for column in range(self.columnCount()):
            try:
                name = self.header[column]
            except IndexError:
                name = None
            default = self.default_row.get(name)
            if left is None:
                left = column
            right = column
            for row in range(first, last + 1):
                self._main_data[row][column] = default
        if left is None:
            return
        top_left = self.index(first, left)
        bottom_right = self.index(last, right)
        self.dataChanged.emit(top_left, bottom_right)



class HybridTableModel(MinimalTableModel):
    """A model that concatenates two models,
    one for existing items and another one for new items.
    """

    def __init__(self, parent=None):
        """Init class."""
        super().__init__(parent)
        self._parent = parent
        self.existing_item_model = MinimalTableModel(self)
        self.new_item_model = EmptyRowModel(self)

    def flags(self, index):
        """Return flags for given index.
        Depending on the index's row we will land on one of the two models.
        """
        row = index.row()
        column = index.column()
        if row < self.existing_item_model.rowCount():
            return self.existing_item_model.index(row, column).flags()
        row -= self.existing_item_model.rowCount()
        return self.new_item_model.index(row, column).flags()


    def data(self, index, role=Qt.DisplayRole):
        """Return data for given index and role.
        Depending on the index's row we will land on one of the two models.
        """
        row = index.row()
        column = index.column()
        if row < self.existing_item_model.rowCount():
            return self.existing_item_model.index(row, column).data(role)
        row -= self.existing_item_model.rowCount()
        return self.new_item_model.index(row, column).data(role)


    def rowCount(self, parent=QModelIndex()):
        """Return the sum of rows in the two models.
        """
        return self.existing_item_model.rowCount() + self.new_item_model.rowCount()


    def batch_set_data(self, indexes, data):
        """Batch set data for indexes.
        Distribute indexes and data among the two models
        and call batch_set_data on each of them."""
        if not indexes:
            return False
        if len(indexes) != len(data):
            return False
        existing_model_indexes = []
        existing_model_data = []
        new_model_indexes = []
        new_model_data = []
        for k, index in enumerate(indexes):
            if not index.isValid():
                continue
            row = index.row()
            column = index.column()
            if row < self.existing_item_model.rowCount():
                existing_model_indexes.append(self.existing_item_model.index(row, column))
                existing_model_data.append(data[k])
            else:
                row -= self.existing_item_model.rowCount()
                new_model_indexes.append(self.new_item_model.index(row, column))
                new_model_data.append(data[k])
        self.existing_item_model.batch_set_data(existing_model_indexes, existing_model_data)
        self.new_item_model.batch_set_data(new_model_indexes, new_model_data)
        # Find square envelope of indexes to emit dataChanged
        top = min(ind.row() for ind in indexes)
        bottom = max(ind.row() for ind in indexes)
        left = min(ind.column() for ind in indexes)
        right = max(ind.column() for ind in indexes)
        self.dataChanged.emit(self.index(top, left), self.index(bottom, right))
        return True


    def insertRows(self, row, count, parent=QModelIndex()):
        """Find the right sub-model (or the empty model) and call insertRows on it."""
        if row < self.existing_item_model.rowCount():
            self.rowsInserted.emit()
            return self.existing_item_model.insertRows(row, count)
        row -= self.existing_item_model.rowCount()
        return self.new_item_model.insertRows(row, count)


    def removeRows(self, row, count, parent=QModelIndex()):
        """Find the right sub-models (or empty model) and call removeRows on them."""
        if row < 0 or row + count - 1 >= self.rowCount():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        if row < self.existing_item_model.rowCount():
            # split count across models
            existing_count = min(count, self.existing_item_model.rowCount() - row)
            self.existing_item_model.removeRows(row, existing_count)
            new_count = count - existing_count
            if new_count > 0:
                self.new_item_model.removeRows(row, new_count)
        else:
            row -= self.existing_item_model.rowCount()
            self.new_item_model.removeRows(row, count)
        self.endRemoveRows()
        return True


    def set_horizontal_header_labels(self, labels):
        super().set_horizontal_header_labels(labels)
        self.new_item_model.set_horizontal_header_labels(labels)


    def reset_model(self, data):
        """Reset model data."""
        self.beginResetModel()
        self.existing_item_model.reset_model(data)
        self.new_item_model.clear()
        self.new_item_model.rowsInserted.connect(self._handle_new_item_model_rows_inserted)
        self.endResetModel()


    @Slot("QModelIndex", "int", "int", name="_handle_new_item_model_rows_inserted")
    def _handle_new_item_model_rows_inserted(self, parent, first, last):
        offset = self.existing_item_model.rowCount()
        self.rowsInserted.emit(QModelIndex(), offset + first, offset + last)



class DatapackageResourcesModel(MinimalTableModel):
    """A model of datapackage resource data, used by SpineDatapackageWidget.

    Attributes:
        parent (SpineDatapackageWidget)
    """

    def __init__(self, parent):
        """Initialize class"""
        super().__init__(parent)

    def reset_model(self, resources):
        self.clear()
        self.set_horizontal_header_labels(["name", "source"])
        data = list()
        for resource in resources:
            name = resource.name
            source = os.path.basename(resource.source)
            data.append([name, source])
        super().reset_model(data)


    def flags(self, index):
        if index.column() == 1:
            return ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        return super().flags(index)



class DatapackageFieldsModel(MinimalTableModel):
    """A model of datapackage field data, used by SpineDatapackageWidget.

    Attributes:
        parent (SpineDatapackageWidget)
    """

    def __init__(self, parent):
        """Initialize class"""
        super().__init__(parent)

    def reset_model(self, schema):
        self.clear()
        self.set_horizontal_header_labels(["name", "type", "primary key?"])
        data = list()
        for field in schema.fields:
            name = field.name
            type_ = field.type
            primary_key = name in schema.primary_key
            data.append([name, type_, primary_key])
        super().reset_model(data)



class DatapackageForeignKeysModel(EmptyRowModel):
    """A model of datapackage foreign key data, used by SpineDatapackageWidget.

    Attributes:
        parent (SpineDatapackageWidget)
    """

    def __init__(self, parent):
        """Initialize class"""
        super().__init__(parent)
        self._parent = parent

    def reset_model(self, foreign_keys):
        self.clear()
        self.set_horizontal_header_labels(["fields", "reference resource", "reference fields", ""])
        data = list()
        for foreign_key in foreign_keys:
            fields = ",".join(foreign_key['fields'])
            reference_resource = foreign_key['reference']['resource']
            reference_fields = ",".join(foreign_key['reference']['fields'])
            data.append([fields, reference_resource, reference_fields, None])
        super().reset_model(data)

class TableModel(QAbstractItemModel):

    def __init__(self, headers=None, data=None):
        super(TableModel, self).__init__()
        if headers is None:
            headers = list()
        if data is None:
            data = list()
        self._data = data
        self._headers = headers
    def parent(self, child=None):
        return QModelIndex()

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, parent)

    def set_data(self, data, headers):
        if data and len(data[0]) != len(headers):
            raise ValueError("'data[0]' must be same length as 'headers'")
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount(), self.columnCount())
        self.dataChanged.emit(top_left, bottom_right)

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

    def row(self, index):
        if index.isValid():
            return self._data[index.row()]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
