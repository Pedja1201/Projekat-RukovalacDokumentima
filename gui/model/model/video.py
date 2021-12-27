from .item import Item

# Ovo verovatno ne treba ovako
# Klasa text bi trebala da pokazuje na text widget

class Video(Item): 
    item_title = "Video"
    file_path = None
    def __init__(self, name, parent):
        super().__init__(name, parent)

