from PySide2.QtWidgets import QMainWindow

from plugins.image_viewer.widget import ImageViewer
from plugins.paint.widget import Paint


class ImageEditor(QMainWindow): # dodati image_viewer i paint u dependency. Dodati ovo u model
    def __init__(self):
        super(ImageEditor, self).__init__()
        self.image_viewer = ImageViewer()
        self.paint_window = Paint() #  'window' je metoda klase QMainWindow, zato se ovde zove paint_window
