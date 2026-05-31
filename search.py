from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "API Working"
    })

@app.route("/api/search")
def search():
    return jsonify({
        "status": "success",
        "message": "Search endpoint working"
    })
