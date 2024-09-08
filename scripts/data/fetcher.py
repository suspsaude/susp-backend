import requests
import zipfile
import os

description = """
This module contains functions to download data from the Brazilian government's open data source 
and the National Registry of Health Establishments (CNES).

Available functionalities:

- Download data from CNES or the open data base.
- Save the data locally in a chosen file.
"""

CNES_URL = "https://cnes.datasus.gov.br/EstatisticasServlet?path=BASE_DE_DADOS_CNES_"
DEMAS_URL = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/"

def download_data(url: str) -> bytes:
    """
    Downloads data from a URL and returns the data in bytes.

    Args:
    url (str): URL of the file to be downloaded

    Returns:
    bytes: Downloaded data
    """
    response = requests.get(url)
    response.raise_for_status()

    return response.content
    
def save_data(data: bytes, path: str) -> None:
    """
    Saves the data to a file at the specified path.

    Args:
    data (bytes): Data to be saved
    path (str): Path of the file where the data will be saved

    Returns:
    None
    """
    with open(path, "wb") as f:
        f.write(data)

def extract_data(path: str) -> None:
    """
    Extracts a ZIP file at the specified path into a folder with the same name as the file.

    Args:
    path (str): Path of the ZIP file to be extracted

    Returns:
    None
    """
    if not path.endswith('.zip'):
        raise ValueError("The path must be a ZIP file.")
    
    folder_name = os.path.splitext(path)[0]
    
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(folder_name)

def clean_directory(path: str = '.') -> None:
    """
    Removes all files and directories in the current folder that do not end with .py.

    Args:
    path (str): Path of the folder where files and directories will be removed

    Returns:
    None
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        if os.path.isdir(item_path):
            # Remove directory and all its contents
            for root, dirs, files in os.walk(item_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(item_path)
        elif not item.endswith('.py'):
            os.remove(item_path)
    
def download_cnes_data(year: int, month: int) -> None:
    """
    Downloads CNES data for a given year and month and saves it to a file named BASE_DE_DADOS_CNES_YYYYMM.ZIP.

    Args:
    year (int): Year of the data to be downloaded (2017, 2018, etc.)
    month (int): Month of the data to be downloaded (1 to 12)

    Returns:
    None
    """
    if year < 2017 or year > 2024:
        raise ValueError("Invalid year.")
    if month < 1 or month > 12:
        raise ValueError("Invalid month, please provide a month between 1 and 12.")

    date = f"{year}{month:02d}"  # Adds a leading zero to the month number if necessary
    url = f"{CNES_URL}{date}.ZIP"
    data = download_data(url)

    if not data:
        raise ValueError("Download error: failed to download data.")

    save_data(data, f"BASE_DE_DADOS_CNES_{date}.zip")
    extract_data(f"BASE_DE_DADOS_CNES_{date}.zip")

def download_stablishments(cnes_codes: list) -> None:
    """
    Downloads data from the Brazilian government's open data source and saves it to a file with the stablishment name.

    Returns:
    None
    """
    for code in cnes_codes:
        data = download_data(f"{DEMAS_URL}{code}")

        if not data:
            raise ValueError("Download error: failed to download data.")

        save_data(data, "{code}.csv")