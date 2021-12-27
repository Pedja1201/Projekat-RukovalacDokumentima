from .item import Item
import json

class Slot(Item): 
    item_title = "Slot"
    child_title = "Text", "Video", "Table", "Image"
    def __init__(self, name, parent):
        super().__init__(name, parent)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)