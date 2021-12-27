from .item import Item
import json

class Content(Item): 
    item_title = "Content"
    child_title = "Page"
    def __init__(self, name, parent):
        super().__init__(name, parent)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)