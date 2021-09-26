# Realizacija interfejsa preko apstraktne klase
from abc import ABC, abstractmethod


class ComponentInterface(ABC):
    @abstractmethod
    def get_actions(self):
        raise NotImplementedError("Not implemented!")

    @abstractmethod
    def get_menu(self):
        raise NotImplementedError("Not implemented!")

    @abstractmethod
    def get_toolbar(self):
        raise NotImplementedError("Not implemented!")

    @abstractmethod
    def get_widget(self):
        raise NotImplementedError("Not implemented!")