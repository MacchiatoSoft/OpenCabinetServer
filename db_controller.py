'''Connects to PostGreSQL database in docker'''
from __future__ import annotations
from typing import Optional
from models import User
from uuid import uuid4
import time
import psycopg2


class DB_Cabinet:

    is_connected : bool = False
    conn : psycopg2.extensions.connection
    cur : psycopg2.extensions.cursor

    def __init__(self):
        self.init_conn()


    def get_conn(self):
        return psycopg2.connect(
            database="opencabinet",
            user="postgres",
            password="postgres",
            host="0.0.0.0"
        )

    def init_conn(self):
        while True:
            try:
                self.conn = self.get_conn()
                self.cur = self.conn.cursor()
                is_connected = True
            except Exception as e:
                print("Error connecting to DB")
                is_conencted = False
                time.sleep(5)
                continue

    # Close communication with db
    def close_conn(self):
        if self.is_connected:
            self.cur.close() 
            self.conn.close()
            is_connected=False

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

