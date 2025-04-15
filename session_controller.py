import time
import psycopg2
from psycopg2 import extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_controller import db_cabinet

class db_session:
    conn : extensions.connection
    cur : extensions.cursor
    is_connected : bool = False
    def __init__(self):
        pass

    def init_conn(self, cabinet : db_cabinet):
        while not self.is_connected:
            try:
                cabinet.create_session_db() #check if exists!!!

                self.conn = psycopg2.connect(
                    dbname = "cabinet_session",
                    user = "admin",
                    password = "admin",
                    host = "localhost",
                    port = 5432
                )
                self.cur = self.conn.cursor()
                self.is_connected=True
            except Exception as e:
                self.is_connected=False
                print("Failed to Connect to Session DB")
                print(e)
                time.sleep(5)
                continue
       

    #def init_db(self):
        #self.cur.execute("CREATE SCHEMA main")
        #self.conn.commit()