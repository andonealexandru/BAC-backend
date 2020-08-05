from flask import Flask, request
from flask_pymongo import PyMongo
# from bitmap import BitMap
import base64
import requests

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/Test_Db"
mongo = PyMongo(app)
db = mongo.db
users_col = mongo.db["Users"]
print("MongoDB Database:", mongo.db)


@app.route("/", methods=['GET'])
def test():
    return "ok ok"


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
    print(email)
    existing_user = users_col.find_one({"email": email})
    if existing_user is None:
        users_col.insert_one({"email": email})
    return "Am virusi in calculator"


app.run(host='0.0.0.0', debug=False)
