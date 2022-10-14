import sqlite3
from controllers import BasicController
from models import User 
import pandas as pd

class UserController(BasicController):

    def __init__(self):
        self.c: sqlite3.Cursor
        self.conn: sqlite3.Connection
        super().__init__()
    
    def create_user(self, user_info: dict) -> User | None:
        try:
            existing_user: pd.DataFrame = self.get_user_by_field('email', user_info['email'])
            if existing_user.empty:
                if self.exec_query(f"INSERT OR IGNORE INTO users(email, name, phone) VALUES ('{user_info['email']}', '{user_info['name']}', '{user_info['phone']}')"):
                    print(f"Created User with e-mail: {user_info['email']}")
                return User(self.c.lastrowid, **user_info)
            else:
                print(f"User's e-mail: {user_info['email']} already exists.")
                return User(*list(existing_user.values[0]))
        except Exception as e:
            print(e)
        return None
    
    def get_user_by_field(self, field_name: str, field: int | str):
        try:
            return pd.read_sql_query(f"SELECT * FROM users WHERE {field_name} = '{field}'", self.conn)
        except Exception as e:
            print(e)
            return None

    def get_user(self, user_id):
        try:
            return pd.read_sql_query(f"SELECT * FROM users WHERE _id = {user_id}", self.conn)
        except Exception as e:
            print(e)
            return None

    def get_all_users(self):
        try:
            return pd.read_sql_query("SELECT * FROM users", self.conn)
        except Exception as e:
            print(e)
            return None

    def create_users_table(self):
        self.exec_query("""
            CREATE TABLE users(
                _id integer NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                email text NOT NULL UNIQUE,
                name text NOT NULL,
                phone text NOT NULL
            )
            """)