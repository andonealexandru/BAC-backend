import stripe
from flask import Flask, request
from flask_pymongo import PyMongo
from PIL import Image
# from bitmap import BitMap
import numpy as np
import codecs
import base64
import cv2
import requests
from mainWordSegmentation import send_words_to_nn

app = Flask(__name__)
app.config[
    'MONGO_URI'] = "mongodb+srv://mirela:parola1234@dpitcluster.t2xz8.mongodb.net/DPIT_TEST?retryWrites=true&w=majority"
app.config['MONGO_DBNAME'] = "DPIT_TEST"
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

    message = base64.b64decode(img["key"])

    npimg = np.fromstring(message, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    string = send_words_to_nn(img)
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
        mongo.db.user.insert_one({"email": email, "accountType": "basic", "history": []})
        print("basic")
        return "basic"
    else:
        print(a["accountType"])
        return a["accountType"]


@app.route("/retrieve_history", methods=['POST', 'GET'])
def retrieve_history():
    email = request.get_json()
    email = dict(email)["email"]
    existing_user = mongo.db.user.find_one({"email": email})
    print(type(existing_user["history"]))
    return str(existing_user["history"])

@app.route("/get_payment_secret", methods=['GET'])
def get_client_secret():
    stripe.api_key = 'sk_test_51HNFe4AqwyEMhL7IEvRyQbiM6ppsxllw24cjEptBZWdUbpQav04q0Lc6OTYelnGazW4vYPp3lEYshhcwu2cDj9Fe00uVwgw2Qo'

    intent = stripe.PaymentIntent.create(
        amount=500,
        currency='usd',
    )
    client_secret = intent.client_secret
    return client_secret

@app.route("/got_premium", methods=['POST'])
def handle_premium():
    email = request.get_json()
    email = dict(email)["email"]
    existing_user = mongo.db.user.find_one({"email": email})
    mongo.db.user.delete_one({"email": email})
    existing_user["accountType"] = "premium"
    mongo.db.user.insert_one(existing_user)
    return "yay?"

if __name__ == "__main__":
    app.run(host='0.0.0.0')