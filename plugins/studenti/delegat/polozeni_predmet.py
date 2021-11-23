from .predmet import Predmet

class PolozeniPredmet(Predmet):
    def __init__(self, naziv, silabus = "", ocena = 6):
        super().__init__(naziv, silabus = silabus)
        self.ocena = ocena
