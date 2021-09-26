from datetime import datetime
from .element import Element


class Document(Element):
    def __init__(self, name="", author=""):
        super().__init__()
        self.name = name
        self.author = author
        self.created = datetime.now()

    def add_child(self, child):
        # TODO: Mozda proveriti da li je stranica, ako samo stranice
        # mogu da se nalaze u dokumentu
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_page_by_page_number(self, page_number):
        """
        Uklanja stranicu iz dokumenta na osnovu njenog broja.
        Podrazumevamo da korisnik pocinje brojanje strana od 1.
        Stranice gledamo kao redni broj u dokumentu, a ne redni broj
        koji je zapisan na samoj stranici (njen atribut)
        """
        del self.children[page_number-1]