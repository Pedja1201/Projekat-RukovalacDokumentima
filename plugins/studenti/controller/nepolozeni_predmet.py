from .predmet import Predmet

class NepolozeniPredmet(Predmet):
    def __init__(self, naziv, silabus = "", broj_polaganja = 1):
        super().__init__(naziv, silabus = silabus)
        self.broj_polaganja = broj_polaganja