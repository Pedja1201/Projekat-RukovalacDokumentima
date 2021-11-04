from abc import ABC
from plugin_framework.plugin import Plugin

class Extension(Plugin, ABC):
    def __init__(self, plugin_specification):
        self.plugin_specification = plugin_specification
        # self.iface = iface

    @property
    def _id(self):
        """
        Property za dobavljanje imena iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("id", "")

    @_id.setter
    def _id(self, value):
        self.plugin_specification["id"] = value

    @property
    def name(self):
        """
        Property za dobavljanje imena iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("name", "")

    @name.setter
    def name(self, value):
        self.plugin_specification["name"] = value
    
    @property
    def authors(self):
        """
        Property za dobavljanje autora iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("authors", "")

    @authors.setter
    def authors(self, value):
        self.plugin_specification["authors"] = value
    
    @property
    def version(self):
        """
        Property za dobavljanje verzije iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("version", "1.0.0")

    @version.setter
    def version(self, value):
        self.plugin_specification["version"] = value

    @property
    def core_version(self):
        """
        Property za dobavljanje verzije iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("core_version", "1.0.0")
    
    @core_version.setter
    def core_version(self, value):
        self.plugin_specification["core_version"] = value
    
    @property
    def category(self):
        """
        Property za dobavljanje kategorije iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("category", "podaci")

    @category.setter
    def category(self, value):
        self.plugin_specification["category"] = value


    @property
    def licence(self):
        """
        Property za dobavljanje licence iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("licence", "MIT")

    @licence.setter
    def licence(self, value):
        self.plugin_specification["licence"] = value

    @property
    def description(self):
        """
        Property za dobavljanje opisa iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("description", "")
    
    @description.setter
    def description(self, value):
        self.plugin_specification["description"] = value

    @property
    def web_page(self):
        """
        Property za dobavljanje webPage iz metapodataka specifikacije.
        """
        return self.plugin_specification.get("web_page", "")
    
    @web_page.setter
    def web_page(self, value):
        self.plugin_specification["web_page"] = value

    def get_widget(self, parent=None):
        """
        Ova metoda treba da vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        Treba da vrati widget, toolbar, menu. Ukoliko su ne postoji dodatni toolbar ili meni, potrebno je za njih
        vratiti None.
        """
        raise NotImplementedError("Ova metoda metoda mora biti realizovana u podklasi!")
    