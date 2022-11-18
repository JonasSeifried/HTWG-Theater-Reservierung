from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


def get_database():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient("mongodb+srv://root:roottoor@htwg-theater-reservieru.bzwrqzs.mongodb.net/?retryWrites=true&w=majority")

    return client['theater']
