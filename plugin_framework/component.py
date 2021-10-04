from abc import ABC, abstractmethod
from plugin_framework.component_interface import ComponentInterface
from plugin_framework.component_specification import ComponentSpecification
from PySide2.QtWidgets import QMenu, QToolBar, QWidget



class Component(ComponentInterface, ABC):
    def __init__(self, actions, menu : QMenu, toolbar : QToolBar, widget : QWidget, 
        specification : ComponentSpecification):
        self.actions = actions # realizovati kao recnik/lista
        self.menu = menu
        self.toolbar = toolbar
        self.widget = widget
        self.specification = specification

    def get_actions(self):
        return self.actions

    def get_menu(self):
        return self.menu

    def get_toolbar(self):
        return self.toolbar

    def get_widget(self):
        return self.widget

    @abstractmethod
    def _load_specification(self, path):
        raise NotImplementedError("Not implemented!")