import ssl

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


def get_database():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient("mongodb+srv://root:roottoor@htwg-theater-reservieru.bzwrqzs.mongodb.net/?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)

    return client['theater']
