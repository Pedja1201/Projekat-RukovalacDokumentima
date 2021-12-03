from os import name
import xml.etree.ElementTree as et
from PySide2 import QtGui
from xml.dom import minidom

from PySide2.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QDialog

class OpenXMLFile(QDialog):

    def init(self, parent=None):
        super().init(parent)

        self.parent = parent #MainWindow

        self.treeWidget = QTreeWidget()

        self.parent.project_dock.setWidget(self.treeWidget)

        self.treeWidget.itemClicked.connect(self.onItemClicked)

    def XMLinTreeView(self, file):
        fileOpen = et.fromstring(file)
        tree = QTreeWidgetItem([fileOpen.attrib.get("name")])
        self.treeWidget.addTopLevelItem(tree)

        def displayTree(tree,childs):
            for child in childs:
                branch = QTreeWidgetItem([child.attrib.get("name")])
                branch.setIcon(0, QtGui.QIcon("resources/icons/close.png"))

                tree.addChild(branch)
                tree.setIcon(0, QtGui.QIcon("resources/icons/undo.png"))

                displayTree(branch, child)

        displayTree(tree, fileOpen)

    def onItemClicked(self):
        item = self.treeWidget.currentItem()
        print(self.getParentPath(item))

        
    def getParentPath(self, item):
        def getParent(item, outstring):
            if item.parent() is None:
                return outstring
            outstring = item.parent().text(0) +  "/" + outstring
            return getParent(item.parent(), outstring)

        output = getParent(item, item.text(0))
        return output