from abc import ABC, abstractmethod


class Element(ABC):
    """
    Korenska klasa za sve ostale klase modela.
    Omogucava jednostavnije kreiranje i manipulisanje hijerarhijom modela.
    """
    def __init__(self, children=list()):
        self.children = children

    @abstractmethod
    def add_child(self, child):
        raise NotImplementedError()

    @abstractmethod
    def remove_child(self, child):
        raise NotImplementedError()