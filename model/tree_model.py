from PySide2 import QtCore, QtGui, QtWidgets
from .document import Document
from .content import Content
from .page import Page
from .slot import Slot
from .text import Text
from .image import Image
from .table import Table
from .video import Video

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, workspace, parent=None):
        super().__init__(parent)
        self.workspace = workspace 
        self.all_items = []
        self.icons = {
            "Collection": QtGui.QIcon("resources\icons\search.png"),
            "Document": QtGui.QIcon("resources\icons\paste.png"),
            "Content": QtGui.QIcon("resources\icons\create_file.png"),
            "Page": QtGui.QIcon("resources\icons\copy.png"),
            "Slot": QtGui.QIcon("resources\icons\save.png"),
            "Video": QtGui.QIcon("resources\icons\save.png"),
            "Image": QtGui.QIcon("resources\icons\down.png"),
            "Text": QtGui.QIcon("resources\icons\copy.png"),
            "Table": QtGui.QIcon("resources\icons\icons8-grid-2-64.png")
        }
        self.dodavanje = 2

    
    def get_item(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.workspace

    
    def columnCount(self, parent):
        return 2

    
    def data(self, index, role):
        if not index.isValid():
            return None
        item = self.get_item(index)
        self.all_items.append(item)
        if (index.column() == 0) and (role == QtCore.Qt.DecorationRole):
            return self.icons.get(item.item_title)
        if (index.column() == 0 ) and (role == QtCore.Qt.DisplayRole):
            return item.name

        elif (index.column() == 1) and (role == QtCore.Qt.DisplayRole):
            return item.title
    
    #def return_children(self, index):
     #   item = self.get_item(index)
     #   dete_item = item.child()
     #   self.all_items.append(item)
     #   return item.name
        

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled 

    
    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "Name"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Type"

    
    def index(self, row, column, parent):
        parent_item = self.get_item(parent)
        if hasattr(parent_item, 'elements'):
            if (row >= 0) and (row < len(parent_item.elements)) and parent_item.elements[row]:
                return self.createIndex(row, column, parent_item.elements[row])
            else:
                return QtCore.QModelIndex()
        else:
            return QtCore.QModelIndex()
    

    
    def parent(self, child):
        if child.isValid():
            child_item = self.get_item(child)
            if hasattr(child_item, 'parent'):
                parent_item = child_item.parent
                if parent_item and (parent_item != self.workspace) and parent_item.parent:
                    return self.createIndex(parent_item.parent.elements.index(parent_item), 0, parent_item)
            else:
                return self.createIndex(child_item.index(child_item), 0, child_item)
                    
            return QtCore.QModelIndex()
            
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        item = self.get_item(index)
        if value == " ":
            return False

        if role == QtCore.Qt.EditRole:
            item.name = value
            return True
        
        return False

    
    def rowCount(self, parent):
        item = self.get_item(parent)
        if hasattr(item, 'elements'):
            return len(item.elements)
        else:
            return 0

    
    
    def removeRow(self, row, parent):
        if not parent.isValid():
            parent = self.workspace
            
        else:
            parent = parent.internalPointer()
            
        parent.removeChild(row)
        return True

    
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def create_slika(self, title, parent, index):
        if title == "Slot":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            image = Image(broj_elemenata + "." +  " Slika", parent)
            print("Napravljena slika")
            return image
    
    def create_text(self, title, parent, index):
        if title == "Slot":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            text = Text(broj_elemenata + "." +  " Tekst", parent)
            print("Napravljena tekst")
            return text

    def create_child(self, title, parent, index):
        if title == "Document":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            document = Document((broj_elemenata + "." + " Dokument"), parent)
            print("Napravljen dokument")
            return document

        elif title == "Content":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            content = Content(broj_elemenata + "." +  " Content", parent)
            print("Napravljen content")
            return content
        
        elif title == "Page":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            page = Page(broj_elemenata + "." +  " Page", parent)
            print("Napravljen page")
            return page
        
        elif title == "Slot":
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            slot = Slot(broj_elemenata + "." +  " Slot", parent)
            print("Napravljen slot")
            return slot
    
        else:
            ime = self.get_item(index)
            broj_elemenata = str(1 + len(ime.elements))
            text = Text(broj_elemenata + "." +  " Tekst", parent)
            print("Napravljen tekst")
            return text
        
    def create_child2(self, title, parent, index):
        if title == "Document":
            ime = self.get_item(index)
            broj_elemenata = str(self.dodavanje + len(ime.elements))
            self.dodavanje += 1
            document = Document((broj_elemenata + "." + " Dokument"), parent)
            
            return document

        elif title == "Content":
            ime = self.get_item(index)
            broj_elemenata = str(2 + len(ime.elements))
            content = Content(broj_elemenata + "." +  " Content", parent)
           #print("Napravljen content")
            return content
        
        elif title == "Page":
            ime = self.get_item(index)
            broj_elemenata = str(2 + len(ime.elements))
            page = Page(broj_elemenata + "." +  " Page", parent)
            print("Napravljen page")
            return page
        
        elif title == "Slot":
            ime = self.get_item(index)
            broj_elemenata = str(2 + len(ime.elements))
            slot = Slot(broj_elemenata + "." +  " Slot", parent)
            print("Napravljen slot")
            return slot
    
        else:
            ime = self.get_item(index)
            broj_elemenata = str(2 + len(ime.elements))
            text = Text(broj_elemenata + "." +  " Tekst", parent)
            
            print("Napravljen tekst")
            return text
        
    
    