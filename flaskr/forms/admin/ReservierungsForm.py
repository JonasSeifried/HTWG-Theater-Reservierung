from wtforms import Form, BooleanField, StringField, SelectField, validators


class ReservierungsForm(Form):
    email = StringField('Email', [
        validators.DataRequired()
    ])
    vorstellung = SelectField("Vorstellung",
                              choices=[],
                              validators=[validators.DataRequired()],
                              render_kw={"class": "form-select me-1", "style": "width: fit-content"})

    anzahl = SelectField("Anzahl",
                         choices=[1, 2, 3, 4, 5, 6],
                         render_kw={"class": "form-select me-1", "style": "max-width: fit-content"})

    ist_ermaessigt = BooleanField('Reservierung ermäßigt', default=False)
