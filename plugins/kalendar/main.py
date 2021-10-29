from plugin_framework.extension import Extension
from plugin_framework.plugin_specification import PluginSpecification
import json
from PySide2 import QtWidgets


class Main(Extension):
    def __init__(self, specification,iface):
        super().__init__(specification,iface)

        self.widget = QtWidgets.QCalendarWidget(iface.central_widget)
        # self.name = specification.name
        # self.version = specification.version
        # self.core_version = specification.core_version
        # self.description = specification.description
        # self.category =  specification.category
        # self.licence =  specification.licence
        # self.web_page = specification.web_page
        print("INIT TEST")

    # FIXME: implementacija apstraktnih metoda
    def activate(self):
        print("Activated")
        self.iface.add_widget(self.widget)

    def deactivate(self):
        print("Deactivated")
        self.iface.remove_widget(self.widget)
