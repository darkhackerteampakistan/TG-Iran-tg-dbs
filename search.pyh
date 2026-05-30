from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 1.txt থেকে 57.txt পর্যন্ত auto load
TXT_FILES = [f"{i}.txt" for i in range(1, 58)]


def parse_line(line, source_file):
    """
    Demo format:
    ID|FirstName|LastName|Phone|UserID|Username|Timestamp
    """

    parts = line.strip().split("|")

    # কম field থাকলে auto fill
    while len(parts) < 7:
        parts.append("")

    return {
        "line_id": parts[0].strip(),
        "first_name": parts[1].strip(),
        "last_name": parts[2].strip(),
        "phone": parts[3].strip(),
        "user_id": parts[4].strip(),
        "username": parts[5].strip(),
        "timestamp": parts[6].strip() if parts[6].strip() else None,
        "source_file": source_file,
        "raw_line": line.strip()
    }


def search_data(query_type, query_value):
    query_value = query_value.strip()

    for file_name in TXT_FILES:

        # file না থাকলে skip
        if not os.path.exists(file_name):
            continue

        try:
            with open(file_name, "r", encoding="utf-8", errors="ignore") as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    data = parse_line(line, file_name)

                    # Phone Search
                    if query_type == "phone":
                        if data["phone"] == query_value:
                            return data

                    # Username Search
                    elif query_type == "username":
                        if (
                            data["username"]
                            and data["username"].lower()
                            == query_value.lower()
                        ):
                            return data

                    # User ID Search
                    elif query_type == "userid":
                        if data["user_id"] == query_value:
                            return data

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    return None


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Demo Search API Running",
        "files_scanning": "1.txt → 57.txt",
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

    query = None
    result = None
    query_type = None

    # Priority
    if phone:
        query = phone
        query_type = "phone"

    elif username:
        query = username
        query_type = "username"

    elif userid:
        query = userid
        query_type = "userid"

    else:
        return jsonify({
            "status": "error",
            "message": "Use phone, username or userid parameter",
            "example": {
                "phone": "/api/search?phone=8801700000001",
                "username": "/api/search?username=demo_user",
                "userid": "/api/search?userid=123456789"
            }
        }), 400

    result = search_data(query_type, query)

    if result:
        return jsonify({
            "status": "success",
            "query_type": query_type,
            "query": query,
            "result": result
        }), 200

    return jsonify({
        "status": "not_found",
        "query_type": query_type,
        "query": query
    }), 404


# Local Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
