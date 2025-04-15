'''Connects to PostGreSQL database in docker'''
from __future__ import annotations
from typing import Optional
from models import User
from uuid import uuid4
import time
import psycopg2


class db_cabinet:

    is_connected : bool = False
    conn : psycopg2.extensions.connection
    cur : psycopg2.extensions.cursor

    def __init__(self):
        self.init_conn()

    def create_session_db(self):
        self.conn.autocommit=True
        self.cur.execute("CREATE DATABASE cabinet_session")
        self.conn.autocommit=False

    def get_conn(self):
        print("Connecting")
        return psycopg2.connect(
            database="cabinet",
            user="admin",
            password="admin",
            host="localhost",
            port=5432
        )

    def init_conn(self):
        while not self.is_connected:
            try:
                self.conn = self.get_conn()
                self.cur = self.conn.cursor()
                self.is_connected = True
                print("Connected")
            except Exception as e:
                print("Error connecting to DB")
                self.is_connected = False
                time.sleep(5)
                continue

    # Close communication with db
    def close_conn(self):
        if self.is_connected:
            self.cur.close() 
            self.conn.close()
            self.is_connected=False

    def get_user_full(self, username:str, password:str) -> User | None:
            if self.is_connected:
                query = "SELECT u.user_id u.user_name, u.password FROM main.users u WHERE u.user_name = %s; and u.password = %s LIMIT 1"
                data = (username, password)
                self.cur.execute(query, data)
                result = self.cur.fetchone()
                if result != None:
                    return User(result[0], result[1], result[2])
                else:
                    return None
            else:
                return None

