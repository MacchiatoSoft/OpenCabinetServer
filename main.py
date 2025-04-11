from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from OpenCabinetServer.db_controller import DB_Cabinet

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
alc =  SQLAlchemy(app)

@app.route('/ping')
def ping():
    return "pong"

"""
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Missing or invalid JSON"}), 400
    
    errorjson = []

    username = data.get("username")
    password = data.get("password")

    if not username:
        errorjson.append("Missing 'username' field")
    if not password:
        errorjson.append("Missing 'password field")

    if len(errorjson) > 0:
        return jsonify({"error":errorjson}), 400
    else:

        user = db.get_user_full(username, password)
        if user is not None:
            session['user'] = user
            return jsonify({"status":True})
        else:
            return jsonify({"error": "Invalid username or password"}), 400
"""
if __name__ == '__main__':
    app.run()