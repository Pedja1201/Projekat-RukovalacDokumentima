

from .handler import Handler
from ..text_edit_service.widget import TextEditService
from ..image_viewer_service.widget import ImageViewerService
from plugins.image_viewer_service import widget # izgleda da je ovaj import automatski dodat iz nekog razloga


class HandlerList():
    def __init__(self, input):
        self.input = input
        self.text_handler = Handler(widget = TextEditService(None), input = self.input)
        self.image_handler = Handler(widget = ImageViewerService(None), input = self.input)

        self.text_handler.successor = self.image_handler

        self.handler_list = list()
        self.handler_list.append(self.text_handler)
        self.handler_list.append(self.image_handler)

    def setListOrder(self): # dodavanje u listu bi se moglo vrsiti ovde odredjenim redosledom
        pass
        