'''Connects to PostGreSQL database in docker'''
from __future__ import annotations
from typing import Optional, cast
from models import User, DrawerPointer
from uuid import uuid4
import time
import psycopg2
from psycopg2.extras import DictCursor, DictRow
from typing import Optional

class db_cabinet:

    is_connected : bool = False
    conn : psycopg2.extensions.connection
    cur : psycopg2.extensions.cursor

    def __init__(self):
        self.init_conn()

    def create_session_db(self):
        try:
            self.conn.autocommit=True
            self.cur.execute("CREATE DATABASE cabinet_session")
        except psycopg2.errors.DuplicateDatabase as e:
            print("Database already Exists")
            self.conn.autocommit=False

    def get_conn(self):
        print("Connecting")
        return psycopg2.connect(
            database="cabinet",
            user="admin",
            password="admin",
            host="localhost",
            port=5432,
            cursor_factory=DictCursor
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

    def get_user_full(self, username:str, password:str) -> Optional[User]:
            if self.is_connected:
                query = "SELECT u.user_id, u.user_name, u.password FROM main.users u WHERE u.user_name = %s AND u.password = %s LIMIT 1"
                data = (username, password)
                self.cur.execute(query, data)
                result : DictRow= cast(DictRow, self.cur.fetchone())
                if result:
                    return User(result['user_id'], result['user_name'], result['password'])
            else:
                print(f"Not Connected to db")

    def check_user_exists(self, username:str) -> bool:
            if self.is_connected:
                query = "SELECT * FROM main.users u WHERE u.user_name = %s"
                data = (username,)
                self.cur.execute(query, data)
                result : DictRow= cast(DictRow, self.cur.fetchall())
                if len(result)>0:
                    return True
                else:
                    return False
            else:
                raise Exception

    def add_user(self, username:str, password:str) -> bool:
        try:
            if self.is_connected:
                if self.check_user_exists(username):
                    # User already exists, don't insert
                    return False

                # User doesn't exist, safe to insert
                query = "INSERT INTO main.users(user_name, password) VALUES (%s, %s)"
                data = (username, password)
                self.cur.execute(query, data)
                self.conn.commit()
                return True
            else:
                raise Exception("Not connected to DB")
        except Exception as e:
            print(f"add_user error: {e}")
            raise
    
    #gets all drawers
    def get_drawer_pointers(self) -> Optional[list[DrawerPointer]]:
        if self.is_connected:
            query = """SELECT
                        d.drawer_id,
                        d.drawer_name,
                        d.drawer_type,
                        u.user_name AS owner_name
                    FROM main.drawers d
                    INNER JOIN main.users u ON d.owner_id = u.user_id;"""
            self.cur.execute(query)
            results : list[DictRow]= cast(list[DictRow], self.cur.fetchall())
            if results:
                drawer_pointer_list = []
                for d in results:
                    drawer_pointer_list.append( 
                        DrawerPointer(
                            d['drawer_id'], 
                            d['drawer_name'], 
                            d['drawer_type'], 
                            d['owner_name']
                            )
                        )
                return drawer_pointer_list
        else:
            print(f"Not Connected to db")

