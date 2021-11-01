from PySide2 import QtWidgets
from plugin_framework.extension import Extension
from plugin_framework.plugin_specification import PluginSpecification
from .widget import TextEdit
import json

class Main(Extension):
    def __init__(self, specification, iface):
        """
        :param iface: main_window aplikacije
        """
        super().__init__(specification,iface)
        self.widget = TextEdit(iface.central_widget)
        if self.specification is None:
            self._load_specification("plugins/text_edit/spec.json")

    # TODO: dodati metode specificne za komponentu
    def _load_specification(self, path):
        # FIXME: sta ako putanja ne postoji (nedostaje datoteka) os.path.exists
        with open(path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            self.specification = PluginSpecification(data["_id"], data["name"], data["authors"],
                data["version"], data["core_version"], data["category"],
                data["licence"], data["description"], data["web_page"],  data["dependencies"])



    # FIXME: implementacija apstraktnih metoda
    def activate(self):
        print("Activated")
        self.iface.add_widget(self.widget)

    def deactivate(self):
        print("Deactivated")
        self.iface.remove_widget(self.widget)






# from plugin_framework.extension import Extension
# from .widget import TextEdit

# class Plugin(Extension):
#     def __init__(self, specification, iface):
#         """
#         :param iface: main_window aplikacije
#         """
#         super().__init__(specification, iface)
#         self.widget = TextEdit(iface.central_widget)
#         print("INIT TEST")

#     # FIXME: implementacija apstraktnih metoda
#     def activate(self):
#         print("Activated")
#         self.iface.add_widget(self.widget)

#     def deactivate(self):
#         print("Deactivated")
#         self.iface.remove_widget(self.widget)


                
