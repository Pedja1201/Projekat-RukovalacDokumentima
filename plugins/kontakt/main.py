from plugin_framework.extension import Extension
from .widgets.contacts_widget import ContactsWidget
from plugin_framework.plugin_specification import PluginSpecification
# import json

class Main(Extension):
    def __init__(self, specification):
        """
        Inicijalizator imenik plugina.

        :param spec: specifikacija metapodataka o pluginu.
        :type spec: dict
        """
        super().__init__(specification)

    def get_widget(self, parent=None):
        """
        Ova metoda vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        
        :param parent: bi trebao da bude widget u koji će se smestiti ovaj koji naš plugin omogućava.
        :returns: QWidget, QToolbar, QMenu
        """
        return ContactsWidget(parent), None, None

    # FIXME: implementacija apstraktnih metoda
    def activate(self):
        print("Activated")
        self.iface.add_widget(self.widget)

    def deactivate(self):
        print("Deactivated")
        self.iface.remove_widget(self.widget)
