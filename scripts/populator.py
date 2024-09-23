import os
import argparse
import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.db.tables import Base, GeneralInfo, ServiceRecord
from scripts.fetcher import DATA_PATH, ESPEC_FILE_NAME 
from scripts.fetcher import download_cnes_data, download_stablishment, clean_cache
from scripts.process_sus_data import process_general_info, process_service_records

from datetime import datetime

description = """
This module contains functions to populate the database with data from the Brazilian
government's open data source and the National Registry of Health Establishments (CNES).

Available functionalities:

- Populate the database with general info data from the CNES API.
- Populate the database with service records data from the CNES API.
- Populate the database with data from a specific year and month.
"""

DB_USER = os.getenv("DBUSER")
DB_NAME = os.getenv("DBNAME")
DB_PASSWORD = os.getenv("DBPASSWORD")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

engine = create_engine(DB_URL)

# DB session creation
SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()

# If tabelas doesn't exist, creates it
Base.metadata.create_all(bind=engine)

def populate_db_from_object(obj: object) -> None:
    """
    Populates the database with the object passed as argument.

    Args:
    obj (object): Object to be added to the database

    Returns:
    None
    """
    session.add(obj)
    session.commit()

def populate_general_info() -> None:
    """
    Populates the database with the general info data from the CNES API.
    
    Args:
    None
    
    Returns:
    None
    """
    elasticnes = pd.read_csv(f"{DATA_PATH}{ESPEC_FILE_NAME}")

    for cnes_code in elasticnes['CNES']:
        download_stablishment(cnes_code)
        general_info = process_general_info(elasticnes, f"{DATA_PATH}/{cnes_code}.json")
        populate_db_from_object(general_info)


def populate_service_records() -> None:
    """
    Populates the database with the service records data from the CNES API.
    
    Args:
    None
    
    Returns:
    None
    """
    records = process_service_records(f"{DATA_PATH}{ESPEC_FILE_NAME}")
    for record in records:
        populate_db_from_object(record)

def parse_args() -> argparse.Namespace:
    """
    Parses the command line arguments.
    
    Args:
    None
    
    Returns:
    args (Namespace): Arguments parsed from the command line
    """
    parser = argparse.ArgumentParser(description="Popula banco de dados para ano e mês específico.")

    parser.add_argument("--year", type=int, required=True, help="Ano (formato: YYYY)")
    parser.add_argument("--month", type=int, required=True, help="Mês (formato: MM, 1 a 12)")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    download_cnes_data(args.year, args.month)

    populate_service_records()
    populate_general_info(args.year, args.month)

    clean_cache()