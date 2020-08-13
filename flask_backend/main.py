from flask import Flask, request
from flask_pymongo import PyMongo
# from bitmap import BitMap
import base64
import requests

# trebuie sa inseram userul nou la sign in daca nu e deja existent

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/dpit_databse"
mongo = PyMongo(app)


@app.route("/add_history", methods=['POST'])
def handle_add():
    history = request.get_json()
    history = dict(history)
    doc = mongo.db.user.find_one({"email":history["email"]})
    mongo.db.user.remove({"email":history["email"]})
    doc["history"].append(history["history"])
    mongo.db.user.insert_one(doc)
    return "ok"



@app.route("/upload", methods=['POST', 'GET'])
def handle_request():
    img = request.get_json()
    img = dict(img)
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(str(img["key"])))
    return "ok"


@app.route("/compile", methods=['POST'])
def handle_compile():
    code_data = request.get_json()
    code_data = dict(code_data)

    RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
    CLIENT_SECRET = '90cc525c23f99059c05da47bf9ea1de8d8a74304'
    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': code_data["source"],
        # 'input': input,
        'lang': code_data["lang"],
        'time_limit': 5,
        'memory_limit': 262144,
    }

    r = requests.post(RUN_URL, data=data)
    return r.json()


@app.route("/signin", methods=['POST', 'GET'])
def handle_signin():
    email = request.get_json()
    email = dict(email)["email"]
    existing_user = mongo.db.user.find_one({"email": email})
    print(existing_user)
    if existing_user == None:
        mongo.db.user.insert_one({"email": email, "history":[]})
        print("sal")
    return "Am virusi in calculator"


app.run(host='0.0.0.0', debug=False)
