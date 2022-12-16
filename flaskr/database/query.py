import json
from datetime import datetime
from pymongo import errors

from bson import json_util
from bson.objectid import ObjectId
from .db import get_database


def parse_json(data):
    return json.loads(json_util.dumps(data))


def add_reservierung(email: str, vorstellungs_id: int, anzahl_personen: int) -> bool:
    db = get_database()
    item = {
        "email": email,
        "vorstellung": vorstellungs_id,
        "anzahlPersonen": anzahl_personen
    }
    try:
        db["Reservierungen"].insert_one(item)
    except errors.DuplicateKeyError as e:
        print(e)
        return False
    return True

def add_verification_data(email: str, vorstellungs_id: int, anzahl_personen: int) -> bool:
    db = get_database()
    item = {
        "email": email,
        "vorstellung": vorstellungs_id,
        "anzahlPersonen": anzahl_personen,
        "day": datetime.day,

    }
    try:
        db["Verification"].insert_one(item)
    except errors.DuplicateKeyError as e:
        print(e)
        return False
    return True



def get_reservierung_by_email(email: str):
    db = get_database()


def add_vorstellung(v_id: int, name: str, date: datetime, verfuegbare_plaetze: int):
    db = get_database()
    item = {
        "id": v_id,
        "name": name,
        "datum": date.strftime("%x"),
        "uhrzeit": date.strftime("%X"),
        "verfuegbarePlaetze": verfuegbare_plaetze
    }
    db["Vorstellungen"].insert_one(item)


def get_vorstellungen():
    db = get_database()
    return parse_json(list(db["Vorstellungen"].find()))


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
