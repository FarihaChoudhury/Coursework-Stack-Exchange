import scrape
import insert


def run_pipeline():
    """ Runs ETL pipeline for scraping StackExchange history page and uploading to database. """

    data = scrape.extract_stack_exchange_history_data()

    insert.insert_data_to_database(data)


def lambda_handler(event=None, context=None):
    """ Lambda handler to get web scrape and upload to database. """
    run_pipeline()


if __name__ == "__main__":
    run_pipeline()
