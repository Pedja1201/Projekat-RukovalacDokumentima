class Handler: # Ovde bi se jos mogle dodati i provere vezane za prosledjene metapodatke (da li su u ispravnom formatu i slicno), kao i dodatna logika kontrolera
    def __init__(self, metadata={}) -> None:
        self.metadata = metadata
