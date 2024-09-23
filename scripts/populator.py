import os
import argparse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.db.tables import Base, GeneralInfo, ServiceRecord
from scripts.fetcher import DATA_PATH, ESPEC_FILE_NAME 
from scripts.fetcher import download_cnes_data, download_stablishments
from scripts.process_sus_data import general_info, service_records

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

def populate_general_info(year: int = datetime.now().year, month: int = datetime.now().month) -> None:
    """
    Populates the database with the general info data from the CNES API.
    
    Args:
    year (int): Year of the data to be downloaded (2017, 2018, etc.)
    month (int): Month of the data to be downloaded (1 to 12)
    
    Returns:
    None
    """
    download_cnes_data(year, month)

def populate_service_records() -> None:
    """
    Populates the database with the service records data from the CNES API.
    
    Args:
    None
    
    Returns:
    None
    """
    ServiceRecords = service_records(ESPEC_FILE_NAME)
    for record in ServiceRecords:
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