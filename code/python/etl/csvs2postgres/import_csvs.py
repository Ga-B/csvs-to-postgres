import os
import argparse

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from logger import setup_logging


def main():
    args = parse_args()
    setup_logging(log_dir=args.log_dir)
    csvs_to_postgres(csv_dir=args.csv_dir, db_url=args.db_url)

def csvs_to_postgres(csv_dir, db_url):
    """Import CSV files from a directory into PostgreSQL database."""

    # Database connection
    engine = create_engine(db_url)

    logger.info("Started CSV import to PostgreSQL.")

    # Importing each CSV as a table in the database
    for filename in os.listdir(csv_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(csv_dir, filename)
            table_name = os.path.splitext(filename)[0].lower()

            try:
                logger.info(f"* Reading file '{filename}'")
                df = pd.read_csv(filepath)

                if df.empty:
                    logger.warning(f"'{filename}' is empty.")
                    continue

                df.to_sql(
                    table_name, engine, if_exists='replace', index=False
                )
                logger.success(
                    f"'{filename}' imported as table '{table_name}'."
                )

            except pd.errors.EmptyDataError:
                logger.error(f"'{filename}' is empty or unreadable.")
            except pd.errors.ParserError as e:
                logger.error(f"Parser error in '{filename}': {str(e)}")
            except SQLAlchemyError as e:
                logger.error(f"Database error in '{filename}': {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in '{filename}': {str(e)}")

    logger.info("Import process completed.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Import CSV files into a PostgreSQL database"
    )
    parser.add_argument(
        "--csv-dir",
        default="/home/jovyan/data",
        help="Directory of CSV files to import (default: /home/jovyan/data)"
    )
    parser.add_argument(
        "--log-dir",
        default="/home/jovyan/code/logs",
        help="Directory to store logs (default: /home/jovyan/code/logs)"
    )
    parser.add_argument(
        "--db-url",
        default="postgresql://postgres:mysecretpassword@postgres:5432/imported_csvs",
        help="PostgreSQL database URL"
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()