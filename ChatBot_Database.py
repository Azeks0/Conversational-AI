import sqlite3
import json
from datetime import datetime

timeframe = 'sample'

sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))

c = connection.cursor()

def create_table():
    c.execute(" CREATE TABLE IF NOT EXISTS parent reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")


def format_data(data):
    data = data.replace("\n"," newlinechar ").replace("\r", " newlinechar ").replace('"', "'" )
    return data

def find_parent(pid):
    sql = "SELECT comment FROM parent_reply WHERE comment_id"
if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0

    with open("C:/Users/user/Desktop/reddit_comments/RC_{}".format(timeframe.split('-')[0], timeframe), buffer=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            create_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)