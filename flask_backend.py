from flask import Flask, request
from flask_pymongo import PyMongo
# from bitmap import BitMap
import base64
import requests
from mainWordSegmentation import send_words_to_nn

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/dpit_database"
app.config['MONGO_DBNAME'] = "dpit_database"
mongo = PyMongo(app)


@app.route("/", methods=['GET'])
def test():
    return "ok ok"


@app.route("/add_history", methods=['POST'])
def handle_add():
    history = request.get_json()
    history = dict(history)
    doc = mongo.db.user.find_one({"email": history["email"]})
    print(history["email"])
    print(type(doc))
    mongo.db.user.delete_one({"email": history["email"]})
    doc["history"].append(history["history"])
    mongo.db.user.insert_one(doc)
    return "ok"


@app.route("/upload", methods=['POST'])
def handle_request():
    img = request.get_json()
    img = dict(img)
    with open("data/imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(str(img["key"])))
    string = send_words_to_nn()
    print(string)
    return string


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
        'lang': code_data["lang"],
        'time_limit': 5,
        'memory_limit': 262144,
    }

    if code_data["input"] != "":
        data['input'] = code_data['input']

    r = requests.post(RUN_URL, data=data)
    print(str(r.json()))
    return r.json()


@app.route("/signin", methods=['POST', 'GET'])
def handle_signin():
    email = request.get_json()
    email = dict(email)["email"]
    email_col = mongo.db['user']
    a = email_col.find_one({'email': email})

    if a is None:
        # mongo.db.user.insert_one({"email": email, "history": []})
        print("sal")
    return "Am virusi in calculator"


@app.route("/retrieve_history", methods=['POST', 'GET'])
def retrieve_history():
    email = request.get_json()
    email = dict(email)["email"]
    existing_user = mongo.db.user.find_one({"email": email})
    print(type(existing_user["history"]))
    return str(existing_user["history"])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
