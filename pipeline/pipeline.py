""" Runs ETL pipeline """

import logging
import scrape
import insert


def run_pipeline():
    """ Runs ETL pipeline for scraping StackExchange history page and uploading to database. """

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("SCRAPING: ")
    data = scrape.extract_stack_exchange_history_data()

    logging.info("INSERTING: ")
    insert.insert_data_to_database(data)

    logging.info("ETL COMPLETE. ")


if __name__ == "__main__":
    run_pipeline()
