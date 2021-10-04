from .element import Element


class Page(Element):
    def __init__(self, title="", text="", page_number=1):
        super().__init__()
        self.title = title
        self.text = text
        self.page_number = page_number

    def add_child(self, child):
        """
        Dodaje tekst u ostatak definisanog teksta.
        :param child: novi tekst
        """
        self.text += child

    def remove_child(self, child):
        if child in self.text:
            result = self.text.split(child)
            self.text = result[0]+result[1]