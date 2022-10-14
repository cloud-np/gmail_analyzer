import sqlite3
import numpy as np
import pandas as pd
import json
import os
from dotenv import load_dotenv

EXAMPLE_DB = "gmails_test.db"
DB_NAME = "gmails.db"

class BasicController:
    def __init__(self):
        self.c: sqlite3.Cursor
        self.conn: sqlite3.Connection
        load_dotenv()
        self.db_name: str = EXAMPLE_DB if bool(os.getenv('DEBUG')) else DB_NAME
        self.c, self.conn = self.connect_db()

    def connect_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            return c, conn
        except Exception as e:
            raise Exception(f'Could not connect to database: {str(e)}')

    def exec_query(self, query):
        try:
            self.c.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Could not execute {query}: {str(e)}')
            return False

    def close_db(self):
        try:
            self.conn.close()
        except Exception as e:
            raise Exception(f'Could not close database: {str(e)}')

# def get_match(self, match_id):
#     try:
#         return pd.read_sql_query(f"SELECT * FROM matches WHERE match_id = {match_id}", self.conn)
#     except Exception as e:
#         print(e)
#         return None

# def insert_match(self, match: Match):
#     try:
#         if self.get_match(match.match_id).empty:
#             self.exec_query(f"INSERT INTO matches VALUES ({match})")
#             print(f'Added match {match.match_id}')
#         else:
#             print(f'Match {match.match_id} already exists')
#     except Exception as e:
#         print(e)
#         return False

# def clear_bad_values(self):
#     self.exec_query(query="DELETE FROM matches WHERE prc_one <= 0 OR prc_x <= 0 OR prc_two <= 0 OR prc_one >= 100 OR prc_x >= 100 OR prc_two >= 100 OR one <= 0.99 OR x <= 0.99 OR two <= 0.99")

# def get_matches_main_info(self):
#     # return pd.read_sql_query("SELECT prc_one, prc_x, prc_two, final_score, one, x, two, cup FROM matches", self.conn)
#     try:
#         return pd.read_sql_query("SELECT prc_one, prc_x, prc_two, final_score, one, x, two, cup FROM matches", self.conn)
#     except Exception as e:
#         print(e)
#         return None

# def get_matches(self):
#     try:
#         return pd.read_sql_query("SELECT * FROM matches", self.conn)
#     except Exception as e:
#         print(e)
#         return None