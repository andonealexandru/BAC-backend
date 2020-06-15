from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

@app.route("/home")
def hello():
    client = MongoClient("localhost", 27017)
    db = client['marinel']
    coll = db['user']

    result = ""

    for doc in coll.find():
        for key, value in doc.items():
            result = result + str(key) + " : " + str(value) + "\n"
    return result