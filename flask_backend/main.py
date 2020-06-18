from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def handle_request():
    return "Flask server working"

app.run(host="0.0.0.0")
