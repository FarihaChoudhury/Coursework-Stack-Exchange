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


def load_all_data(conn: connection) -> DataFrame:
    """Returns a dataframe containing all the transaction data."""

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Question;")
        data = cur.fetchall()

    return DataFrame(data)
