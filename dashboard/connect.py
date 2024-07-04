""" Redshift database connection functions for T3 dashboard."""

from os import environ
from dotenv import load_dotenv
import logging

from pandas import DataFrame


from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor, execute_values


def get_connection() -> connection:
    """ Retrieves connection and returns it. """
    load_dotenv()
    try:
        conn = connect(
            user=environ['DB_USERNAME'],
            password=environ['DB_PASSWORD'],
            host=environ['DB_IP'],
            port=environ['DB_PORT'],
            dbname=environ['DB_NAME']
        )
        logging.info("Successful connection to Redshift database.")
        return conn
    except ConnectionError as e:
        logging.error("Unsuccessful connection to database: %s", e)
        return None


# my queries:


def load_most_popular_tags(conn: connection) -> DataFrame:
    """ Returns DataFrame of tags that appeared the most. """

    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.tag, COUNT(qt.tag_id) AS tag_count
            FROM Question_Tag_Assignment qt
            JOIN Tag t ON qt.tag_id = t.tag_id
            GROUP BY t.tag
            ORDER BY tag_count DESC
            LIMIT 10;
                    """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_most_popular_tags_this_week(conn: connection) -> DataFrame:
    """ Returns DataFrame of tags that appeared the most. """

    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.tag, COUNT(qt.tag_id) AS tag_count
            FROM Question_Tag_Assignment qt
            JOIN Tag t ON qt.tag_id = t.tag_id
            JOIN Question q ON qt.question_id = q.question_id
            WHERE q.upload_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
            GROUP BY t.tag
            ORDER BY tag_count DESC
            LIMIT 10;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_num_questions_asked_before_12pm(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
                COUNT(*) AS question_count
            FROM Question q
            WHERE DATE_PART('HOUR', q.upload_timestamp) < 12
            GROUP BY upload_hour
            ORDER BY upload_hour;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return DataFrame(data, columns=column_names)


def load_num_questions_asked_between_12_5pm(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
                COUNT(*) AS question_count
            FROM Question q
            WHERE DATE_PART('HOUR', q.upload_timestamp) >= 12
                AND DATE_PART('HOUR', q.upload_timestamp) < 17
            GROUP BY upload_hour
            ORDER BY upload_hour;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_num_questions_asked_after_5pm(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT DATE_PART('hour', q.upload_timestamp) AS upload_hour,
                COUNT(*) AS question_count
            FROM Question q
            WHERE DATE_PART('HOUR', q.upload_timestamp) >= 17
            GROUP BY upload_hour
            ORDER BY upload_hour;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_tags_for_questions_with_most_votes(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.tag, SUM(q.votes) AS total_votes
            FROM Tag t 
            JOIN Question_Tag_Assignment qt ON t.tag_id = qt.tag_id
            JOIN Question q ON q.question_id = qt.question_id
            GROUP BY t.tag
            ORDER BY total_votes DESC
            LIMIT 10;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_tags_for_questions_with_most_answers(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.tag, COUNT(a.answer_id) AS total_answers
            FROM Tag t 
            JOIN Question_Tag_Assignment qt ON t.tag_id = qt.tag_id
            JOIN Question q ON q.question_id = qt.question_id
            JOIN Answer a on a.question_id = q.question_id
            GROUP BY t.tag
            ORDER BY total_answers DESC
            LIMIT 10;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_author_asks_most_questions(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.author_username, a.author_id, COUNT(q.question_id) AS num_questions_asked
            FROM Author a 
            JOIN Question q on q.author_id = a.author_id
            GROUP BY a.author_id, a.author_username
            ORDER BY num_questions_asked DESC
            LIMIT 10;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)


def load_author_writes_most_answers(conn: connection) -> DataFrame:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.author_username, a.author_id, COUNT(aw.answer_id) AS num_answers_written
            FROM Author a 
            JOIN Answer aw on aw.author_id = a.author_id
            GROUP BY a.author_id, a.author_username
            ORDER BY num_answers_written DESC
            LIMIT 10;
            """
                    )
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]

    return DataFrame(data, columns=column_names)
