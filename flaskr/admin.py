from flask import Blueprint, render_template, request

from flaskr.auth import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
def admin_overview():
    return render_template("admin/admin_overview.html")


@bp.route("/test")
@login_required
def test():
    return "test"


@bp.route("/veranstaltungen", methods=["POST", "GET"])
def veranstaltungen():
    return render_template("admin/admin_veranstaltungen.html")
