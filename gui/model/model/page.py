from .item import Item
import json

class Page(Item): 
    item_title = "Page"
    child_title = "Slot"
    def __init__(self, name, parent):
        super().__init__(name, parent)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)