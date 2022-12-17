from datetime import datetime
from .database import db


class Vorstellung:
    ID = len(db.query("Vorstellungen")) + 1

    def __init__(self, name: str, date: datetime, verfuegbare_plaetze: int, plaetze_ingesamt: int):
        self.name = name
        self.date = date
        self.verfuegbare_plaetze = verfuegbare_plaetze
        self.plaetze_ingesamt = plaetze_ingesamt

    def __str__(self) -> str:
        return self.name + " " + self.date.strftime("%x %H:%M")

    # Store in database
    def save(self):
        return db.insert_one("Vorstellungen", self.to_dict())

    def to_dict(self) -> dict:
        return {
            "id": self.ID,
            "name": self.name,
            "datum": self.date.strftime("%x"),
            "uhrzeit": self.date.strftime("%X"),
            "verfuegbarePlaetze": self.verfuegbare_plaetze,
            "plaetzeInsgesamt": self.plaetze_ingesamt
        }



