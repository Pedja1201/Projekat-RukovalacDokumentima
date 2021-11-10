from PySide2 import QtCore, QtGui

class Item(object): 
    item_title = "Item"
    child_title = "Child title"
    def __init__(self, name, parent=None, item_data = None):
        self.name = name
        self.parent = parent
        self.item_data = item_data
        self.elements = [] 

    @property 
    def title(self):
        return self.item_title

    @property 
    def child_title(self):
        return self.child_title
    
    def appendChild(self, item): 
        self.elements.append(item)

    def add_child(self, child, position = -1): 
        child.parent = self
        if position < 0:
            position = len(self.elements)
        self.elements.insert(position, child)

    def remove_child(self, child): 
        if child in self.elements:
            index = self.elements.index(child)
            del self.elements[index]
        
            return index
    
    def removeChildren(self, position, count): 
        if position < 0 or position + count > len(self.elements):
            return False
        
        for row in range(count):
            self.elements.pop(position)
        return True


        
    def removeChild(self, position): 
        if position < 0 or position > len(self.elements):
            return False
        del self.elements[position]
        #child = self.elements.pop(position)
        #child.parent = None
        return True

    def to_dict(self):
        self.lista = []
        for i in self.elements:
            self.lista.append(i.name)
        return {
            "name": self.name,
            "parent": self.parent.name,
            "title": self.title,
            "elements": self.lista
        }

    def child(self, row): 
        return self.elements[row]
    
    def childCount(self): 
        return len(self.elements)

    def columnCount(self):  
        return len(self.item_data)
    
    def data(self, column): 
        try:
            return self.item_data[column]
        except IndexError:
            return None
    
    def parent(self): 
        return self.parent

    def row(self): 
        if self.parent:
            return self.parent.elements.index(self)
        
        return 0