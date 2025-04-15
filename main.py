from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
from datetime import datetime

from db_controller import db_cabinet
from session_controller import db_session

db_controller = db_cabinet()
session = db_session()
session.init_conn(db_controller)

#make this actually secure in the future
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost:5432/cabinet_session"
app.config['SESSION_TYPE'] = 'sqlalchemy'

db_session = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db_session

sess = Session(app)
cors = CORS(app, origins='*')

@app.route('/ping')
def ping():
    return "pong"
if __name__ == '__main__':
    app.run(debug=True, port=5000)