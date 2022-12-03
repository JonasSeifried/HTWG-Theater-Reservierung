from flask import Blueprint, render_template, request
from .database.query import store_reservierung, get_vorstellungen
from .forms.admin.ReservierungsForm import ReservierungsForm

bp = Blueprint("reservierung", __name__)


@bp.route('/reservierung', methods=["GET", "POST"])
@bp.route('/', methods=["GET", "POST"])
def reservieren():
    form = ReservierungsForm(request.form)

    if request.method == "POST" and form.validate():
        email = form.email.data
        print(email)
        print(form.anzahl.data)
        print(form.email.data)
        return "worked"

    vorstellungen = []
    vorstellungen_raw = get_vorstellungen()
    for item in vorstellungen_raw:
        form.vorstellung.choices.append(item["name"] + " " + item["datum"] + " " + item["uhrzeit"])

    return render_template("reservierung/reservierung.html", form=form, vorstellungen=vorstellungen)
