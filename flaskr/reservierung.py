from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from .database import db
from .mailing import mail
from .forms.admin.ReservierungsForm import ReservierungsForm

bp = Blueprint("reservierung", __name__)


@bp.route('/reservierung', methods=["GET", "POST"])
@bp.route('/', methods=["GET", "POST"])
def reservieren():
    form = ReservierungsForm(request.form)
    if request.method == "POST":
        if form.validate():
            reservierung = Reservierung(form.email.data, form.vorstellung.data, form.anzahl_personen.data)
            if reservierung.start_verification():
                mail.send_verify(reservierung.email, reservierung.get_url())
                # Todo Email schicken mit /verify?email=email&vorstellung=vorstellung&personen=anzahl_personen
                return "worked email should be send now"
            return "Something didnt work"
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

    reservierung = Reservierung(email, vorstellung, anzahl_personen)
    if not reservierung.verify():
        return "Etwas ist schiefgelaufen, vielleicht ist dein Bestätigungslink abgelaufen!"

    # mail.send_Qrcode()
    return f"email: {email}, vorstellung: {vorstellung}, personen: {anzahl_personen}"


class Reservierung:
    def __init__(self, email: str, vorstellungs_id: int, anzahl_personen: int):
        self.email = email
        self.vorstellungs_id = vorstellungs_id
        self.anzahl_personen = anzahl_personen

    def __str__(self):
        return f"email: {self.email}, v_ID: {self.vorstellungs_id}, personen: {self.anzahl_personen}"

    def start_verification(self) -> bool:
        item = self.to_dict()
        item["tagAktiv"] = datetime.now().day
        print(item)
        if db.insert_one("Verifizierungen", item):
            return True
        return False

    def get_url(self):
        return f"http://127.0.0.1:5000/verify?email={self.email}&vorstellung={self.vorstellungs_id}&personen={self.anzahl_personen} "

    def verify(self) -> bool:
        res_data = db.query("Verifizierungen", self.to_dict())
        print(res_data)
        if res_data is None:
            return False
        if res_data["tagAktiv"] != datetime.now().day:
            return False
        if self.save():
            db.delete_one("Verifizierungen", self.to_dict())
            return True
        return False

    def save(self) -> bool:

        if db.insert_one("Reservierungen", self.to_dict()):
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "vorstellung": self.vorstellungs_id,
            "anzahlPersonen": self.anzahl_personen}
