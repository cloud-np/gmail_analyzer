import sqlite3

import pandas as pd

from controllers import BasicController
from models import ProposedCeremony


class ProposedCeremonyController(BasicController):

    def __init__(self):
        self.c: sqlite3.Cursor
        self.conn: sqlite3.Connection
        super().__init__()

    def create_proposed_ceremony(self, prop_dict: dict) -> ProposedCeremony | None:
        try:
            existing_proposed_ceremony: pd.DataFrame = self.get_proposed_ceremony_by_field('msg_id', prop_dict['msg_id'])
            if existing_proposed_ceremony.empty:
                if self.exec_query(f"""
                                INSERT OR IGNORE INTO 
                                proposed_ceremonies(date, people, ceremony_type, comments, user_id, msg_id) 
                                VALUES 
                                ('{prop_dict['date']}', '{prop_dict['people']}', '{prop_dict['ceremony_type']}', '{prop_dict['comments']}', '{prop_dict['user_id']}', '{prop_dict['msg_id']}')
                                """):
                    print(f"Created ProposedCeremony from user: {prop_dict['user_id']} and message: {prop_dict['msg_id']}")
                return ProposedCeremony(self.c.lastrowid, **prop_dict)
            else:
                print(f"ProposedCeremony already mentioned from message: {prop_dict['msg_id']}")
                return ProposedCeremony(*list(existing_proposed_ceremony.values[0]))
        except Exception as e:
            print(e)
        return None

    def get_proposed_ceremony_by_field(self, field_name: str, field: int | str) -> pd.DataFrame | None:
        try:
            return pd.read_sql_query(f"SELECT * FROM proposed_ceremonies WHERE {field_name} = '{field}'", self.conn)
        except Exception as e:
            print(e)
        return None

    # def insert_proposed_ceremony(self, proposed_ceremony: ProposedCeremony) -> None:
    #     try:
    #         if self.get_proposed_ceremony(proposed_ceremony._id).empty:
    #             self.exec_query(f"INSERT INTO proposed_ceremonies VALUES ({proposed_ceremony})")
    #             print(f'Added proposed ceremony with people/date: {proposed_ceremony.people}, {proposed_ceremony.date}')
    #         else:
    #             print(f'Proposed Ceremony {proposed_ceremony._id} already exists')
    #     except Exception as e:
    #         print(e)
    #     return None

    def get_proposed_ceremony(self, _id):
        try:
            return pd.read_sql_query(f"SELECT * FROM proposed_ceremonies WHERE _id = {_id}", self.conn)
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

    def get_all_proposed_ceremonies(self):
        try:
            return pd.read_sql_query("SELECT * FROM proposed_ceremonies", self.conn)
        except Exception as e:
            print(e)
            return None

    def create_proposed_ceremonies_table(self):
        self.exec_query("""
            CREATE TABLE proposed_ceremonies(
                _id integer NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                date text NOT NULL,
                people text NOT NULL,
                ceremony_type text NOT NULL,
                comments text NOT NULL,
                user_id integer NOT NULL,
                msg_id integer NOT NULL UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(_id),
                FOREIGN KEY (msg_id) REFERENCES messages(_id)
            )
            """)