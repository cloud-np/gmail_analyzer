import sqlite3
from controllers import BasicController
from models import Message
import pandas as pd


class MessageController(BasicController):

    def __init__(self):
        self.c: sqlite3.Cursor
        self.conn: sqlite3.Connection
        super().__init__()

    def insert_message(self, message: Message):
        try:
            if self.get_message(message.msg_id).empty:
                self.exec_query(f"INSERT INTO messages VALUES ({message})")
                print(f'Added match {message.message}')
            else:
                print(f'Match {message.msg_id} already exists')
        except Exception as e:
            print(e)
            return False

    def get_message(self, msg_id: str):
        try:
            return pd.read_sql_query(f"SELECT * FROM messages WHERE msg_id = '{msg_id}'", self.conn)
        except Exception as e:
            print(e)
            raise Exception('Failed to run sql query.') 

    # def clear_bad_values(self):
    #     self.exec_query(query="DELETE FROM matches WHERE prc_one <= 0 OR prc_x <= 0 OR prc_two <= 0 OR prc_one >= 100 OR prc_x >= 100 OR prc_two >= 100 OR one <= 0.99 OR x <= 0.99 OR two <= 0.99")

    # def get_matches_main_info(self):
    #     try:
    #         return pd.read_sql_query("SELECT prc_one, prc_x, prc_two, final_score, one, x, two, cup FROM matches", self.conn)
    #     except Exception as e:
    #         print(e)
    #         return None

    def get_all_messages(self):
        try:
            return pd.read_sql_query("SELECT * FROM messages", self.conn)
        except Exception as e:
            print(e)
            return None

    def create_message_table(self):
        self.exec_query("""
            CREATE TABLE messages(
                msg_id text NOT NULL PRIMARY KEY,
                frm text NOT NULL,
                _to text NOT NULL,
                subject text NOT NULL,
                _datetime text NOT NULL,
                content text NOT NULL
            )
            """)