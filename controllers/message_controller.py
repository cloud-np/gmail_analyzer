import sqlite3

import pandas as pd

from controllers import BasicController
from models import Message


class MessageController(BasicController):

    def __init__(self):
        self.c: sqlite3.Cursor
        self.conn: sqlite3.Connection
        super().__init__()

    def insert_message(self, message: Message) -> None:
        try:
            existing_message: pd.DataFrame = self.get_message(message._id)
            if existing_message.empty:
                if self.exec_query(f"""
                                INSERT INTO messages(_id, frm, _to, subject, _datetime, content, user_id) 
                                VALUES ('{message._id}', '{message.frm}', '{message._to}', '{message.subject}', '{message._datetime}', '{message.content}', '{message.user_id}')
                                """):
                    print(f'Added message {message._id}')
            else:
                print(f'Message {message._id} already exists')
        except Exception as e:
            print(e)
        return None

    def get_message(self, msg_id: str) -> Message | None:
        try:
            return pd.read_sql_query(f"SELECT * FROM messages WHERE _id = '{msg_id}'", self.conn)
        except Exception as e:
            print(e)
            return None

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

    def create_messages_table(self):
        self.exec_query("""
            CREATE TABLE messages(
                _id text NOT NULL UNIQUE, 
                frm text NOT NULL,
                _to text NOT NULL,
                subject text NOT NULL,
                _datetime text NOT NULL,
                content text NOT NULL,
                user_id integer NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(_id) 
            )
            """)