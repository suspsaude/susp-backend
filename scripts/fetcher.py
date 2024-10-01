import zipfile
import os
import subprocess

from datetime import datetime

description = """
This module contains functions to download data from the Brazilian
government's open data source and the National Registry of Health
Establishments (CNES).

Available functionalities:

- Download data from CNES or the open data base.
- Save the data locally in a chosen file.
"""

CNES_URL = "https://elasticnes.saude.gov.br/fb40c0bc-b7fa-42a1-99d0-496b1b579b26"

DEMAS_URL = "http://apidadosabertos.saude.gov.br/cnes/estabelecimentos/"

DATA_PATH = os.getenv("PYTHONPATH") + "/data/"


def __download_data(url: str) -> bytes:
    """
    Downloads data from a URL using curl and returns the data in bytes.

    Args:
    url (str): URL of the file to be downloaded

    Returns:
    bytes: Downloaded data
    """
    result = subprocess.run(['curl', '-s', url],
                            capture_output=True, check=True)
    return result.stdout

def __save_data(data: bytes, name: str) -> None:
    """
    Saves the data to a file with the desired name in the fetcher folder.

    Args:
    data (bytes): Data to be saved
    name (str): The desired file name

    Returns:
    None

    Raises:
    OSError: If there is an error creating the directory or writing the file
    """
    try:
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)

        file_path = os.path.join(DATA_PATH, name)
        with open(file_path, 'wb') as f:
            f.write(data)
    except OSError as e:
        print(f"Error saving data to {file_path}: {e}")
        raise


def __unzip_cnes_data(date: str) -> None:
    """
    Extracts the one desired .csv file in the .zip downloaded from CNES

    Args:
    date (str): Date of the data to be extracted (YYYYMM)

    Returns:
    None
    """
    zip_path = os.path.join(DATA_PATH, f"BASE_DE_DADOS_CNES_{date}.zip")

    if not os.path.exists(zip_path):
        raise ValueError(
            "There isn't any file with the specified name or date.")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(f"{ESPEC_FILE_NAME}{date}.csv", DATA_PATH)


def clean_cache() -> None:
    """
    Removes all files and directories in the cache folder.

    Args:
    None

    Returns:
    None
    """
    for item in os.listdir(DATA_PATH):
        item_path = os.path.join(DATA_PATH, item)

        if os.path.isdir(item_path):
            for root, dirs, files in os.walk(item_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(item_path)
        else:
            os.remove(item_path)

def download_cnes_data() -> None:
    data = __download_data(CNES_URL)

    if not data:
        raise ValueError("Download error: failed to download data.")

    __save_data(data, "DADOS_CNES.csv")

def download_cnes_data_old(year: int, month: int) -> None:
    """
    Downloads CNES data for a given year and month and saves it to a file named
    BASE_DE_DADOS_CNES_YYYYMM.ZIP. Extracts the "ServicosEspecializados.csv"
    file, desired for the database populator.

    Args:
    year (int): Year of the data to be downloaded (2017, 2018, etc.)
    month (int): Month of the data to be downloaded (1 to 12)

    Returns:
    None
    """
    currentYear = datetime.now().year
    if year < 2017 or year > currentYear:
        raise ValueError("Invalid year.")
    if month < 1 or month > 12:
        raise ValueError(
            "Invalid month, please provide a month between 1 and 12.")

    # Adds a leading zero to the month number if necessary
    date = f"{year}{month:02d}"
    url = f"{CNES_URL}{date}.ZIP"
    data = __download_data(url)

    if not data:
        raise ValueError("Download error: failed to download data.")

    __save_data(data, f"BASE_DE_DADOS_CNES_{date}.zip")
    __unzip_cnes_data(date)


def download_stablishment(cnes_code: int) -> None:
    """
    Downloads data from the Brazilian government's open data source and returns
    it in a JSON format.

    Returns:
    None
    """
    data = __download_data(f"{DEMAS_URL}{cnes_code}")

    if not data:
        raise ValueError("Download error: failed to download data.")

    __save_data(data, f"{cnes_code}.json")
