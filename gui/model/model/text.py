from .item import Item

# Ovo verovatno ne treba ovako
# Klasa text bi trebala da pokazuje na text widget

class Text(Item): 
    item_title = "Text"
    file_path = None
    def __init__(self, name, parent):
        super().__init__(name, parent)

