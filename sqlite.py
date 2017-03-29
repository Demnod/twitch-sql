import requests
import json
import sqlite3 as lite
import os
from pathlib import Path


# #### TWITCH VARIABLES ##############


# Url provided by User as starting point
user_url = 'https://api.twitch.tv/kraken/streams'

# Json Style Dictionary for Output
API_MAP_DICT = {}


# ######## DATABASE VARIABLES ####################

DB = 'sqlite_data/newtest.db'

DB_FOLDER = Path('sqlite_data')

CREATE_STREAMS_DB = """ CREATE TABLE IF NOT EXISTS streams (
                                        ID INTEGER PRIMARY KEY autoincrement,
                                        action_id int NULL,
                                        self_link text NULL,
                                        create_date text NULL,
                                        display_name text NULL,
                                        followers int NULL,
                                        game text NULL,
                                        language text NULL,
                                        mature text NULL,
                                        name text NULL,
                                        partner text NULL,
                                        status text NULL,
                                        time text NULL,
                                        url text NULL,
                                        views int NULL
                                    ); """

SHOW_TWITCH_TABLE = "SELECT * FROM streams"


def main():
    check_db()


def check_db():
    if DB_FOLDER.exists():
        conn = create_connection(DB)

        if conn is not None:
            create_table(conn, CREATE_STREAMS_DB)

            print('Printing Current Table Results now: \n')
            check_twitch_table(conn, SHOW_TWITCH_TABLE)

            print('Starting new retrieval now... \n\n')
            check_url()

    else:
        try:
            os.makedirs('sqlite_data')
            print('''There was an error connecting to the DB, attempting to create
                  the folder and retry retrieval now...\n\n''')
            check_db()
        except OSError as ose:
            print(ose)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = lite.connect(db_file)
        return conn
    except lite.Error as e:
        print(e)
    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit
    except lite.Error as e:
        print(e)


def check_twitch_table(conn, SHOW_TWITCH_TABLE):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM streams")
        results = c.fetchall()
        print(results)
    except lite.Error as e:
        print(e)


def creds_to_headers():
    # Function to retrieve Auth VARIABLES
    with open('../.credbox/.twitch-creds2') as cred_file:
        cred_string = cred_file.read().rstrip()
        url_headers = {'client_id': cred_string,
                       'Accept': 'application/vnd.twitchtv.v5+json'}
        return url_headers


def check_url():
    headers = creds_to_headers()
    check_query = requests.get(user_url + '/?limit=100', params=headers)
    base_json = check_query.json()
    if check_query.status_code == 200:
        insert_stream_log(base_json)
        conn = create_connection(DB)
        check_twitch_table(conn, SHOW_TWITCH_TABLE)
    else:
        print('There was an error on the response from the API')
        print(check_query.status_code)
        exit()


def insert_stream_log(base_json):
    upload_list = []
    for stream in base_json['streams']:
        upload_list.append('(' + stream['_links']['self'] + ')')
    conn = create_connection(DB)

    if conn is not None:
        c = conn.cursor()
        for item in upload_list:
            print(item)
            c.executemany(''' INSERT INTO streams(url) VALUES (?)''', item)
        conn.commit


if __name__ == '__main__':
    main()
