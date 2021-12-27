from .content import Content
from .item import Item

class Collection(Item): 
    item_title = "Collection"
    child_title = "Document"
    def __init__ (self, name, parent):
        super(). __init__ (name, parent)

    