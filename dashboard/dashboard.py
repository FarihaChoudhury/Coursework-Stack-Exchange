import pandas as pd
import streamlit as st
# import charts
import connect


def get_data_from_rds_database() -> pd.DataFrame:
    """ Returns data from redshift database. """
    conn = connect.get_connection()
    transaction_data = connect.load_all_data(conn)
    conn.close()
    print(transaction_data)
    return transaction_data


if __name__ == "__main__":
    get_data_from_rds_database()
