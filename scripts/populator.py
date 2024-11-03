import os
import argparse
import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.db.tables import Base, GeneralInfo, ServiceRecord, MedicalService
from scripts.fetcher import DATA_PATH
from scripts.fetcher import download_cnes_data, download_stablishment, clean_cache
from scripts.process_sus_data import process_general_info, process_service_records, process_medical_services
from scripts.utils import progress_bar

from datetime import datetime

description = """
This module contains functions to populate the database with data from the Brazilian
government's open data source and the National Registry of Health Establishments (CNES).

Available functionalities:

- Populate the database with general info data from the CNES API.
- Populate the database with service records data from the CNES API.
- Populate the database with data from a specific year and month.
"""

DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DB_URL)

# DB session creation
SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()

# If tabelas doesn't exist, creates it
Base.metadata.create_all(bind=engine)

def db_is_populated() -> bool:
    exists = session.query(GeneralInfo).first() is not None
    if exists:
        return True
    return False

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

def populate_general_info(elasticnes: pd.DataFrame) -> None:
    """
    Populates the database with the general info data from the CNES API.

    Args:
    elasticnes (DataFrame): the elasticnes.csv dataframe

    Returns:
    None
    """
    codes = set(elasticnes['CNES'])
    total = len(codes)
    current = 0
    startedAt = datetime.now()

    for cnes_code in codes:
        current += 1
        progress_bar(current, total, startedAt, suffix=f"Downloading {cnes_code}")
        while True:
            try:
                download_stablishment(cnes_code)
            except Exception as e:
                print(f"\nError downloading {cnes_code}, trying again: {e}")
                continue
            break
        general_info = process_general_info(elasticnes, f"{DATA_PATH}/{cnes_code}.json")
        populate_db_from_object(general_info)
        progress_bar(current, total, startedAt, suffix=cnes_code)

def filter_dataframe(elasticnes: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the dataframe to remove unnecessary rows.

    Args:
    elasticnes (DataFrame): the elasticnes.csv dataframe

    Returns:
    elasticnes (DataFrame): the elasticnes.csv filtered dataframe
    """
    filtered_data = elasticnes[elasticnes['MUNICÍPIO'] == 'SAO PAULO']

    return filtered_data

def populate_medical_services(elasticnes: pd.DataFrame) -> None:
    """
    Populates the database with the medical services data from the CNES API.

    Args:
    elasticnes (DataFrame): the elasticnes.csv dataframe

    Returns:
    None
    """
    medical_services = process_medical_services(elasticnes)
    total = len(medical_services)
    current = 0
    startedAt = datetime.now()

    for service in medical_services:
        populate_db_from_object(service)
        current += 1
        progress_bar(current, total, startedAt, suffix=service.id)


def populate_service_records(elasticnes: pd.DataFrame) -> None:
    """
    Populates the database with the service records data from the CNES API and
    returns a set of medical services.

    Args:
    elasticnes (DataFrame): the elasticnes.csv dataframe

    Returns:
    None
    """
    records = process_service_records(elasticnes)
    total = len(records)
    current = 0
    startedAt = datetime.now()

    for record in records:
        populate_db_from_object(record)
        current += 1
        progress_bar(current, total, startedAt, suffix=f"{record.cnes} {record.service}")

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
    parser.add_argument("--skip-to", type=int, default=0, help="Pula para a etapa desejada")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if db_is_populated():
        print("Database already populated. Skipping population.")
        exit(0)

    if args.skip_to <= 0:
        print("[0] Downloading data")
        download_cnes_data(args.year, args.month)

    # Reads .csv from ELASTICNES to a dataframe
    if args.skip_to <= 1:
        print("[1] Reading data from file")
        elasticnes = pd.read_csv(f"{DATA_PATH}DADOS_CNES.csv")

    if args.skip_to <= 2:
        print("[2] Populating medical services")
        populate_medical_services(elasticnes)

    if args.skip_to <= 3:
        print("[3] Populating service records")
        populate_service_records(elasticnes)

    if args.skip_to <= 4:
        print("[4] Populating general info")
        populate_general_info(elasticnes)

    if args.skip_to <= 5:
        print("[5] Cleaning cache")
        clean_cache()
