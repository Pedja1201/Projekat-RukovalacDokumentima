from .content import Content
from .item import Item
import json

class Document(Item): 
    item_title = "Document"
    child_title = "Content"
    def __init__ (self, name, parent):
        super(). __init__ (name, parent)
        
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    