from csv import DictReader
import json

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor, execute_values
from os import environ
from dotenv import load_dotenv


def get_connection() -> connection:
    """ Retrieves connection and returns it. """
    load_dotenv()
    return connect(
        user=environ["DATABASE_USERNAME"],
        password=environ["DATABASE_PASSWORD"],
        host=environ["DATABASE_IP"],
        port=environ["DATABASE_PORT"],
        dbname=environ["DATABASE_NAME"]
    )


def get_cursor(conn: connection) -> cursor:
    """ Retrieves cursor and returns it. """
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return cur


def load_data():
    """ Load json as dictionary """
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


# def insert_tag_data():
#     query = f'''INSERT INTO Tag (tag, question_id) VALUES (%s)'''
#     ...


if __name__ == "__main__":
    data = load_data()
    for a in data:
        # insert author / username, get its id:
        print(a['username'])

        # insert question, with author id, get questions's id
        print(a['title'], a['votes'], a['views'])

        # insert tags (list), with question's id
        print(a['tags'])

        # insert answer - use question id, author id
        for answer in a['answers']:
            print(answer['answer'], answer['username'], answer['vote_count'])


# use execute values and pass multiple inputs

# if tags, insert into the tags table then get id -
