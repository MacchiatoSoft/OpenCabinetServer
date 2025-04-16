import os
from typing import Any, Optional
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
from datetime import datetime, timedelta

from werkzeug import datastructures

from db_controller import db_cabinet
from session_controller import db_session

from models import User, DrawerPointer
import traceback

db_controller = db_cabinet()
db_session_controller = db_session()
db_session_controller.init_conn(db_controller)



#make this actually secure in the future
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost:5432/cabinet_session"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Initialize SQLAlchemy
db_session = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db_session

# Initialize Flask-Session
sess : Session = Session(app)
cors = CORS(app, origins='*')

@app.route('/ping')
def ping():
    return "pong"

@app.route('/drawers', methods=['GET'])
def get_drawers():
    try:
        #verify user is logged in
        if(session.get('USER')):
            drawer_pointers : Optional[list[DrawerPointer]] = db_controller.get_drawer_pointers()
            if(drawer_pointers is not None):
                # return list of drawer pointers
                return jsonify({
                    "success": True,
                    "data": [d.toJSON() for d in drawer_pointers]
                }), 200
            else:      
                # no drawers in db
                return jsonify({
                    "success": False,
                    "message": "No drawers",
                    "error_code": "NO_DRAWERS"
                }), 404
        else:
            # Authentication failed
            return jsonify({
                "success": False,
                "message": "Invalid credentials",
                "error_code": "INVALID_CREDENTIALS"
            }), 401
        
    except Exception as e:
        print("get drawers error", e)
        # Handle unexpected errors
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "SERVER_ERROR"
        }), 500
    
@app.route('/logout', methods=['POST'])
def logout():
    try:
        #check if user has a session
        if(session.get('USER')):
            session.clear()
            return jsonify({
                "success": True,
                "message": "Logged Out"
            }), 200
        else:
            #user has no session
            return jsonify({
                "success": False,
                "message": "User not logged in",
                "error_code":"USER_NOT_LOGGED_IN"
            }), 403 
    except Exception as e:
        print("logout error", e)
        # Handle unexpected errors
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "SERVER_ERROR"
        }), 500
    
@app.route('/signup', methods=['POST'])
def signup():
    try:
        username : Optional[str] = request.form.get('username')
        password : Optional[str] = request.form.get('password')

        if(username is None or password is None):
            data_check = check_login_form(username, password)
            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "error_code": data_check
            }), 400
        else:
            is_success = db_controller.add_user(str(username), str(password))
            print(is_success)
            if(is_success):
                user_db_data = db_controller.get_user_full(str(username), str(password))
                if user_db_data is not None:
                    session['USER'] = user_db_data.id
                    return jsonify({
                        "success": True,
                        "message": "Signed Up"
                    }), 200
                else:
                    raise Exception
            else:
                return jsonify({
                    "success": False,
                    "message": "Username already exists",
                    "error_code":"USERNAME_TAKEN"
                }), 409
    except Exception as e:
        print(f"signup fail: {traceback.print_exc()}")
        # Handle unexpected errors
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "SERVER_ERROR"
        }), 500


    
@app.route('/login', methods=['POST'])
def login():
    try:
        username : Optional[str] = request.form.get('username')
        password : Optional[str] = request.form.get('password')

        if(username is None or password is None):
            
            data_check = check_login_form(username, password)
            return jsonify({
                "success": False,
                "message": "Missing required fields",
                "error_code": data_check
            }), 400
        else:
            # Get user from database
            user_db_data : Optional[User]= db_controller.get_user_full(username, password)
            
            # Check if user exists and credentials match
            if user_db_data is not None:
                # Store user ID in session
                session["USER"] = user_db_data.id
                return jsonify({
                    "success": True,
                    "message": "Login successful",
                }), 200
            else:
                # Authentication failed
                return jsonify({
                    "success": False,
                    "message": "Invalid credentials",
                    "error_code": "INVALID_CREDENTIALS"
                }), 401
        
    except Exception as e:
        print("login error", e)
        # Handle unexpected errors
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "SERVER_ERROR"
        }), 500
    
def check_login_form(username:Optional[str], password:Optional[str]) -> str:
    missing_fields = []
    
    if not username:
        missing_fields.append('username')
    if not password:
        missing_fields.append('password')

    error_code = None
    if 'username' in missing_fields and 'password' not in missing_fields:
        error_code = "MISSING_USERNAME"
    elif 'username' not in missing_fields and 'password' in missing_fields:
        error_code = "MISSING_PASSWORD"
    elif 'username' not in missing_fields and 'password' not in missing_fields:
        error_code = "MISSING_ALL_CREDENTIALS"
    else:
        error_code = "MISSING_CREDENTIALS"

    return error_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)