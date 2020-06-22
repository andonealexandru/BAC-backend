from flask import Flask, request
from flask_pymongo import PyMongo
from bitmap import BitMap
import base64

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/bac_test"
mongo = PyMongo(app)

@app.route("/upload", methods=['POST'])
def handle_request():
    img = request.get_json()
    mongo.db.images.insert(dict(img))
    img = dict(img)
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.b64decode(str(img["key"])))
    return "ok"
    
app.run(host="0.0.0.0", debug=False)
