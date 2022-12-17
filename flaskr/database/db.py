import certifi
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient, errors
from bson import json_util
import json


def get_database():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(
        "mongodb+srv://root:roottoor@htwg-theater-reservieru.bzwrqzs.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where())

    return client['theater']


def query(table: str, search_filter: dict = None, *, only_first: bool = False) -> list | dict | None:
    """
    Queries items from the given table with an optional filter
    If option query_only_first is True,
    then only it only returns first item found


    :returns:
    found items as list of dictionaries | found item as dictionary | None if none found
    """

    db = get_database()

    if search_filter is None:
        if only_first:
            data = db[table].find_one()
            return parse_json(data) if data is not None else None
        data = db[table].find()
        if data is None:
            return None
        data = parse_json(data)
        return data[0] if len(data) == 1 else data

    if only_first:
        data = db[table].find_one(search_filter)
        return parse_json(data) if data is not None else None
    data = db[table].find(search_filter)
    if data is None:
        return None
    data = parse_json(data)
    return data[0] if len(data) == 1 else data


def insert_one(table: str, item: dict) -> bool:
    """
    Inserts an item into the given table

    :return: True if successful, False if failed
    """

    db = get_database()
    try:
        db[table].insert_one(item)
    except errors.DuplicateKeyError as e:
        print(e)
        return False

    return True


def parse_json(data):
    return json.loads(json_util.dumps(data))


# Testing
if __name__ == '__main__':
    print(query("Mitarbeiter", only_first=True))
