from wtforms import Form, BooleanField, StringField, SelectField, validators

from flaskr.database import db


def get_vorstellungen():
    vorstellungen = []
    for item in db.query("Vorstellungen"):
        vorstellungen.append((item["id"], item["name"] + " " + item["datum"] + " " + item["uhrzeit"]))
    return vorstellungen


class ReservierungsForm(Form):
    email = StringField('Email', [
        validators.Length(min=6, max=35),
        validators.DataRequired(),
    ])
    vorstellung = SelectField("Vorstellung", [
        validators.none_of(values=[0])],
                              coerce=int,
                              choices=[(0, "Vorstellung auswählen"), *get_vorstellungen()])

    anzahl_personen = SelectField("Anzahl", choices=[1, 2, 3, 4, 5, 6])

    discount = BooleanField('Reservierung ermäßigt')
