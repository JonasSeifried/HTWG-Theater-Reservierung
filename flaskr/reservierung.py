from flask import Blueprint, render_template, request
from .database.query import store_reservierung, get_vorstellungen

bp = Blueprint("reservierung", __name__)


@bp.route('/reservierung', methods=["GET", "POST"])
@bp.route('/', methods=["GET", "POST"])
def reservieren():
    vorstellungen = ["test"]
    if request.method == "GET":
        return render_template("reservierung/reservierung.html", vorstellungen=get_vorstellungen())
        # render_template rendert eine html datei, weitere Parameter sind übergebene Variablen
    if request.method == "POST":
        form_data = request.form  # Dict der form antworten
        store_reservierung(form_data)
        return "worked"
