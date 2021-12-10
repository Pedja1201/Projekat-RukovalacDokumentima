from PySide2 import QtCore, QtGui, QtWidgets, QtXml

class XmlTree(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(XmlTree, self).__init__(parent)

        self.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setHeaderLabels(("Title", "Name"))

        self.domDocument = QtXml.QDomDocument()

        self.domElementForItem = {}

        self.folderIcon = QtGui.QIcon("resources/icons/file.png")
        self.documentIcon = QtGui.QIcon("resources/icons/doc.png")


    def read(self, device):
        ok, errorStr, errorLine, errorColumn = self.domDocument.setContent(device, True)
        if not ok:
            QtWidgets.QMessageBox.information(self.window(), "Documents",
                    "Parse error at line %d, column %d:\n%s" % (errorLine, errorColumn, errorStr))
            return False

        root = self.domDocument.documentElement()
        if root.tagName() != 'xbel':
            QtWidgets.QMessageBox.information(self.window(), "Documents",
                    "The file is not an XBEL file.")
            return False
        
        elif root.hasAttribute('version') and root.attribute('version') != '1.0':
            QtWidgets.QMessageBox.information(self.window(), "Documents",
                    "The file is not an XBEL version 1.0 file.")
            return False
            

        self.clear()

        # It might not be connected.
        try:
            self.itemChanged.disconnect(self.updateDomElement)
        except:
            pass

        child = root.firstChildElement('root')
        while not child.isNull():
            self.parseFolderElement(child)
            child = child.nextSiblingElement('root')

        self.itemChanged.connect(self.updateDomElement)

        return True

    def write(self, device):
        indentSize = 4

        out = QtCore.QTextStream(device)
        self.domDocument.save(out, indentSize)
        return True

    def updateDomElement(self, item, column):
        element = self.domElementForItem.get(id(item))
        if not element.isNull():
            if column == 0:
                oldTitleElement = element.firstChildElement('dir')
                newTitleElement = self.domDocument.createElement('dir')

                newTitleText = self.domDocument.createTextNode(item.text(0))
                newTitleElement.appendChild(newTitleText)

                element.replaceChild(newTitleElement, oldTitleElement)
            else:
                if element.tagName() == 'document':
                    element.setAttribute('name', item.text(1))

    def parseFolderElement(self, element, parentItem=None):
        item = self.createItem(element, parentItem)

        title = element.firstChildElement('name').text()
        if not title:
            title = "Collection"

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setIcon(0, self.folderIcon)
        item.setText(0, title)

        dir = (element.attribute('name') != 'Collection')
        self.setItemExpanded(item, not dir)

        child = element.firstChildElement()
        while not child.isNull():
            if child.tagName() == 'dir':
                self.parseFolderElement(child, item)
            elif child.tagName() == 'document':
                childItem = self.createItem(child, item)

                title = child.firstChildElement('name').text()
                if not title:
                    title = "Documents"

                childItem.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                childItem.setIcon(0, self.documentIcon)
                childItem.setText(0, title)
                childItem.setText(1, child.attribute('name'))
            elif child.tagName() == 'separator':
                childItem = self.createItem(child, item)
                childItem.setFlags(item.flags() & ~(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
                childItem.setText(0, 30 * "\xb7")

            child = child.nextSiblingElement()

    def createItem(self, element, parentItem=None):
        item = QtWidgets.QTreeWidgetItem()

        if parentItem is not None:
            item = QtWidgets.QTreeWidgetItem(parentItem)
        else:
            item = QtWidgets.QTreeWidgetItem(self)

        self.domElementForItem[id(item)] = element
        return item