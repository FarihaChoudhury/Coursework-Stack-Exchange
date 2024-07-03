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
        user=environ['DB_USERNAME'],
        password=environ['DB_PASSWORD'],
        host=environ['DB_IP'],
        port=environ['DB_PORT'],
        dbname=environ['DB_NAME']
    )


def get_cursor(conn: connection) -> cursor:
    """ Retrieves cursor and returns it. """
    return conn.cursor(cursor_factory=RealDictCursor)


def load_data():
    """ Load json as dictionary """
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def upload_author(author: str, conn: connection) -> int:
    """ Uploads author details to database and returns author id.
        If author exists, returns author id. """

    query = """
        WITH new_authors AS (
            INSERT INTO Author (author_username)
            VALUES (%s)
            ON CONFLICT (author_username) DO NOTHING
            RETURNING author_id
        ) 
        SELECT author_id FROM new_authors
        UNION ALL
        SELECT author_id FROM Author WHERE author_username = %s
        LIMIT 1;
    """

    cursor = get_cursor(conn)
    cursor.execute(query, (author, author))

    author_id = cursor.fetchall()[0]['author_id']

    conn.commit()
    cursor.close()

    return author_id


def upload_question(question_data: dict, author_id: int,  conn: connection) -> int:
    """ Uploads question details to database and returns question id
        If question exists, updates votes and views. """

    question_id = question_data['question_id']
    question = question_data['question']
    votes = question_data['votes']
    views = question_data['views']

    query = """
        INSERT INTO Question (question_id, author_id, question, votes, views)
            VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (question_id)
        DO UPDATE SET
            votes = EXCLUDED.votes,
            views = EXCLUDED.views;
    """

    cursor = get_cursor(conn)
    cursor.execute(query, (question_id, author_id,
                   question, votes, views))

    conn.commit()
    cursor.close()

    return question_id


def upload_tag(tag: str, conn: connection) -> int:
    """ Uploads tag to database and returns its tag id. 
        If tag exists, returns tag id"""

    query = """
        WITH new_tags AS (
            INSERT INTO Tag (tag)
            VALUES (%s)
            ON CONFLICT (tag) DO NOTHING
            RETURNING tag_id
        ) 
        SELECT tag_id FROM new_tags
        UNION ALL
        SELECT tag_id FROM Tag WHERE tag = %s
        LIMIT 1;
    """

    cursor = get_cursor(conn)
    cursor.execute(query, (tag, tag))
    tag_id = cursor.fetchall()[0]['tag_id']

    conn.commit()
    cursor.close()

    return tag_id


def upload_tags_question_assignment(question_tags_data: list[tuple], conn: connection):
    """ Uploads tag and question link to database by their ids. """

    query = """
        INSERT INTO Question_Tag_Assignment (tag_id, question_id)
        VALUES %s
        ON CONFLICT DO NOTHING;
    """

    with conn.cursor() as cur:
        execute_values(cur, query, question_tags_data)

    conn.commit()


def upload_answer(answer_data: dict, question_id: int, author_id: int, conn: connection) -> int:
    """ Uploads answer details to database and returns answer id.
        If answer exists, updates votes. """

    answer_id = answer_data['answer_id']
    answer = answer_data['answer']
    votes = answer_data['votes']

    query = """
        INSERT INTO Answer (answer_id, answer, votes, question_id, author_id)
            VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (answer_id)
        DO UPDATE SET
            votes = EXCLUDED.votes;
    """

    cursor = get_cursor(conn)
    cursor.execute(query, (answer_id, answer, votes,
                   question_id, author_id))

    conn.commit()
    cursor.close()

    return answer_id


def insert_data_to_database(questions_data: dict):
    """ Uploads question data to AWS RDS database: author of question, question, question tags, 
        author of answers, answers. """
    # questions_data = load_data()

    conn = get_connection()

    for question in questions_data:
        question_id = question['question_id']

        # insert author's username:
        author_id = upload_author(question['username'], conn)

        # insert question:
        upload_question(
            {'question_id': question_id,
             'question': question['title'],
             'votes': question['votes'],
             'views': question['views']
             },
            author_id,  conn)

        # inserts tags, and tag question assignments:
        tag_ids = [upload_tag(tag, conn) for tag in question['tags']]
        tags_questions = [(tag_id, question_id) for tag_id in tag_ids]
        upload_tags_question_assignment(tags_questions, conn)

        # insert author of answer and answer:
        for answer in question['answers']:
            answer_author_id = upload_author(answer['username'], conn)
            answer_id = upload_answer(
                {'answer_id': answer['answer_id'],
                 'answer': answer['answer'],
                 'votes': answer['vote_count']
                 },
                question_id, answer_author_id, conn)

    conn.close()


if __name__ == "__main__":
    insert_data_to_database({})
