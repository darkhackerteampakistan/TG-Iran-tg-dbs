from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# 1.txt → 57.txt
TXT_FILES = [f"{i}.txt" for i in range(1, 58)]


def convert_timestamp(ts):
    try:
        if not ts:
            return None

        ts = int(ts)
        dt = datetime.fromtimestamp(ts / 1000)

        return {
            "unix": str(ts),
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%I:%M:%S %p"),
            "full": dt.strftime("%Y-%m-%d %I:%M:%S %p")
        }
    except:
        return None


def parse_line(line):
    parts = line.strip().split("|")

    while len(parts) < 7:
        parts.append("")

    return {
        "first_name": parts[1].strip(),
        "last_name": parts[2].strip(),

        "user_id": parts[4].strip(),
        "username": parts[5].strip(),

        "phone": parts[3].strip(),

        "timestamp": convert_timestamp(parts[6].strip())
    }


def search_data(query_type, query_value):

    query_value = query_value.strip()

    for file_name in TXT_FILES:

        if not os.path.exists(file_name):
            continue

        try:
            with open(file_name, "r", encoding="utf-8", errors="ignore") as f:

                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    data = parse_line(line)

                    if query_type == "phone":
                        if data["phone"] == query_value:
                            return data

                    elif query_type == "username":
                        if data["username"].lower() == query_value.lower():
                            return data

                    elif query_type == "userid":
                        if data["user_id"] == query_value:
                            return data

        except Exception:
            continue

    return None


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Demo Search API",
        "search_params": [
            "phone",
            "username",
            "userid"
        ]
    })


@app.route("/api/search")
def api_search():

    phone = request.args.get("phone")
    username = request.args.get("username")
    userid = request.args.get("userid")

    if phone:
        query = phone
        qtype = "phone"

    elif username:
        query = username
        qtype = "username"

    elif userid:
        query = userid
        qtype = "userid"

    else:
        return jsonify({
            "status": "error",
            "message": "Use phone, username or userid"
        }), 400

    result = search_data(qtype, query)

    if result:
        return jsonify({
            "status": "success",
            "query": query,
            "query_type": qtype,
            "result": result
        })

    return jsonify({
        "status": "not_found",
        "query": query,
        "query_type": qtype
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
