from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# সব txt ফাইল স্ক্যান করবে
TXT_FILES = ["1.txt", "2.txt", "3.txt"]


def search_data(query_type, query_value):
    for file_name in TXT_FILES:
        if not os.path.exists(file_name):
            continue

        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                # Demo format:
                # ID|FirstName|LastName|Phone|UserID|Username|Timestamp
                while len(parts) < 7:
                    parts.append("")

                data = {
                    "line_id": parts[0],
                    "first_name": parts[1],
                    "last_name": parts[2],
                    "phone": parts[3],
                    "user_id": parts[4],
                    "username": parts[5],
                    "timestamp": parts[6] if parts[6] else None,
                    "raw_line": line,
                    "source_file": file_name
                }

                # Search Logic
                if query_type == "phone" and data["phone"] == query_value:
                    return data

                elif query_type == "username" and data["username"].lower() == query_value.lower():
                    return data

                elif query_type == "userid" and data["user_id"] == query_value:
                    return data

    return None


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Demo Search API Running",
        "endpoints": {
            "phone": "/api/search?phone=8801700000001",
            "username": "/api/search?username=demo_user",
            "userid": "/api/search?userid=123456789"
        }
    })


@app.route("/api/search")
def api_search():
    phone = request.args.get("phone")
    username = request.args.get("username")
    userid = request.args.get("userid")

    result = None
    query = None

    if phone:
        query = phone
        result = search_data("phone", phone)

    elif username:
        query = username
        result = search_data("username", username)

    elif userid:
        query = userid
        result = search_data("userid", userid)

    else:
        return jsonify({
            "status": "error",
            "message": "Use phone, username or userid"
        }), 400

    if result:
        return jsonify({
            "status": "success",
            "query": query,
            "result": result
        })

    return jsonify({
        "status": "not_found",
        "query": query
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
