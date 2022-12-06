from datetime import datetime
from .database import query


class Vorstellung:
    ID = len(query.get_vorstellungen()) + 1

    def __init__(self, name: str, date: datetime, verfuegbare_plaetze: int):
        self.name = name
        self.date = date
        self.verfuegbare_plaetze = verfuegbare_plaetze

    # Vorstellung -> str
    def __str__(self):
        return self.name + " " + self.date.strftime("%x %H:%M")

    # Store in database
    def save(self):
        query.add_vorstellung(self.ID, self.name, self.date, self.verfuegbare_plaetze)



