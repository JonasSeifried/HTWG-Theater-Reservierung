from wtforms import Form, BooleanField, StringField, SelectField, validators


class ReservierungsForm(Form):
    email = StringField('Email', [
        validators.Length(min=6, max=35),
        validators.DataRequired(),
    ])
    vorstellung = SelectField("Vorstellung", [
        validators.DataRequired()],
        choices=["Vorstellung", "testtest", "test3"])

    anzahl = SelectField("Anzahl", choices=[1, 2, 3, 4, 5, 6])

    ist_ermaessigt = BooleanField('Reservierung ermäßigt')
