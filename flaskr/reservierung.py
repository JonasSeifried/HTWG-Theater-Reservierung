from flask import Blueprint, render_template, request, redirect, url_for
from .database import query
from .database import db
from .forms.admin.ReservierungsForm import ReservierungsForm
from .vorstellung import Vorstellung

bp = Blueprint("reservierung", __name__)


@bp.route('/reservierung', methods=["GET", "POST"])
@bp.route('/', methods=["GET", "POST"])
def reservieren():
    form = ReservierungsForm(request.form)
    if request.method == "POST":
        if form.validate():
            reservierung = Reservierung(form.email.data, form.vorstellung.data, form.anzahl_personen.data)
            # Todo Email schicken mit /verify?email=email&vorstellung=vorstellung&personen=anzahl_personen
            print(reservierung)
            return "worked"
        if form.vorstellung.data == 0:
            return render_template("reservierung/reservierung.html", form=form, vorstellung_error=True)
    return render_template("reservierung/reservierung.html", form=form)


@bp.route('/verify', methods=["GET"])
def reservierung_verify():
    email = request.args.get("email")
    try:
        vorstellung = int(request.args.get("vorstellung"))
        anzahl_personen = int(request.args.get("personen"))
    except ValueError:
        return redirect(url_for("reservierung.reservieren"))

    Reservierung(email, vorstellung, anzahl_personen)

    return f"email: {email}, vorstellung: {vorstellung}, personen: {anzahl_personen}"


class Reservierung:
    def __init__(self, email: str, vorstellungs_id: int, anzahl_personen: int):
        self.email = email
        self.vorstellungs_id = vorstellungs_id
        self.anzahl_personen = anzahl_personen

    def __str__(self):
        return f"email: {self.email}, v_ID: {self.vorstellungs_id}, personen: {self.anzahl_personen}"

    def verify(self):
        if query.add_verification_data(self.email,
                                       self.vorstellungs_id,
                                       self.anzahl_personen):
            return

    def save(self) -> bool:

        if db.insert_one("Reservierungen", self.to_dict()):
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "vorstellung": self.vorstellungs_id,
            "anzahlPersonen": self.anzahl_personen}
