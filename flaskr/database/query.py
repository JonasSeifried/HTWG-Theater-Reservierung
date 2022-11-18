import json

from bson import json_util
from bson.objectid import ObjectId
from .db import get_database


def get_vorstellungen():
    db = get_database()
    vorstellungen = db["Vorstellungen"].find()
    vor_arr = []
    for item in vorstellungen:
        vor_arr.append(item)
    return parse_json(vor_arr)


def store_reservierung(values):
    db = get_database()
    email = values.get("email")
    datum, uhrzeit = values.get("vorstellung").split(" ")
    anzahl = values.get("anzahl")
    item = {
        "email": email,
        "datum": datum,
        "uhrzeit": uhrzeit,
        "anzahlPersonen": int(anzahl)
    }
    db["Reservierungen"].insert_one(item)


def parse_json(data):
    return json.loads(json_util.dumps(data))


# Admin Queries


def get_user_by_name(username):
    db = get_database()
    user = db["Mitarbeiter"].find_one({"username": username})
    if user is None:
        return None
    return parse_json(user)


def get_user_by_id(user_id):
    db = get_database()
    user = db["Mitarbeiter"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        return None
    return parse_json(user)


def add_user(username, password):
    if get_user_by_name(username):
        return False
    db = get_database()
    item = {
        "username": username,
        "password": password
    }
    db["Mitarbeiter"].insert_one(item)
    return True


