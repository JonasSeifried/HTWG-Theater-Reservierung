from flask import Blueprint, render_template, request

from flaskr.auth import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
def admin_homepage():
    return "wow"

@bp.route("/test")
@login_required
def test():
    return "test"
