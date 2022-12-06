from flask import Blueprint, render_template, request
from .database import query
from .forms.admin.ReservierungsForm import ReservierungsForm
from .vorstellung import Vorstellung

bp = Blueprint("reservierung", __name__)


@bp.route('/reservierung', methods=["GET", "POST"])
@bp.route('/', methods=["GET", "POST"])
def reservieren():
    form = ReservierungsForm(request.form)
    if request.method == "POST":
        if form.validate():
            reservierung = Reservierung(form.email, form.vorstellung, form.anzahl_personen, form.discount)
            print(form.vorstellung.data)
            return "worked"
        if form.vorstellung.data == 0:
            return render_template("reservierung/reservierung.html", form=form, vorstellung_error=True)
    return render_template("reservierung/reservierung.html", form=form)


class Reservierung:
    def __init__(self, email: str, vorstellungs_id: int, anzahl_personen: int, discount: bool):
        self.email = email
        self.vorstellungs_id = vorstellungs_id
        self.anzahl_personen = anzahl_personen
        self.discount = discount

    def save(self):
        if query.add_reservierung(self.email,
                                  self.vorstellungs_id,
                                  self.anzahl_personen,
                                  self.discount):
            return
        print("Error")
