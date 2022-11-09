import contextlib
import re
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


class Datavisuzalion:
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.df['date'] = self.df['date'].apply(Cleaner.clean_date)
        self.df['people'] = self.df['people'].apply(Cleaner.clean_people)

        # df['date'] = df['date'].apply(clean_date)

        # df['month'] = df['date'].apply(lambda x: x is not None and x.split('-')[0])
        # df = df.loc[:, ~df.columns.isin(['comments', '_id'])]

        # .to_csv('ceremonies.txt', sep='\t', index=False)
        # df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y'))
        # df['bin'] = pd.cut(df['people'], [0, 50, 100, 150, 200, 300, 500])
        # df['bin'].value_counts().plot(kind='bar')
        # df = df[df['date'].apply(lambda x: x is not None and x.isnumeric())]
        # df = df[df.duplicated(subset=["date"], keep=False)]
        self.df.groupby(['date']).size().plot(kind='bar', figsize=(30, 8), fontsize=7)
        plt.show()

class Cleaner:

    @staticmethod
    def clean_people(people) -> str:
        people = "".join(people.split())

        people.replace('+', '')
        if len(people.split('-')) >= 2:
            people = people.split('-')
            people = people[0]
        else:
            try:
                people = int(re.search(r'\d+', people).group())
            except Exception as e:
                return 0

        return 0 if type(people) == str else people

    @staticmethod
    def clean_date(date) -> str:
        # format date and seprate it into tokens
        date_arr  = date.replace('.', '-').replace('/', '-').split('-')
        year = ''

        with contextlib.suppress(Exception):
            # y-m-d
            if int(date_arr[0]) >= 2017:
                year = date_arr[0] 
                m = date_arr[1] 
                d = date_arr[2] 
                date = f'{m}-{d}-{year}'
            # d-m-y
            elif int(date_arr[2]) >= 2017 or int(date_arr[2]) in {17, 18, 19, 20, 21, 22, 23, 24}:
                year = date_arr[2] 
                m = date_arr[1]
                d = date_arr[0] 
                date = f'{m}-{d}-{year}'
            return date
        if year == '':
            return None
        raise ValueError(f'Error: {date}')
    
    
if __name__ == "__main__":
    conn = sqlite3.connect('gmails_test.db')
    query = "SELECT * FROM proposed_ceremonies"
    df = pd.read_sql_query(query, conn)

    Datavisuzalion(df)