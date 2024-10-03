import zipfile
import os
import subprocess
import requests
import json
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

DEMAS_URL = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/"

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


def download_cnes_data(year: int, month: int) -> None:
    currentDate = datetime.now()
    currentYear = currentDate.year

    formattedDate = currentDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    print(formattedDate)

    if year < 2017 or year > currentYear:
        raise ValueError("Invalid year.")
    if month < 1 or month > 12:
        raise ValueError(
            "Invalid month, please provide a month between 1 and 12.")

    url = "https://elasticnes.saude.gov.br/kibana/api/reporting/v1/generate/immediate/csv_searchsource"

    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }

    payload = {
        "browserTimezone": "Etc/GMT-3",
        "version": "8.8.2",
        "searchSource": {
            "query": {
                "query": "",
                "language": "kuery"
            },
            "fields": [
                {"field": "COMPETÊNCIA", "include_unmapped": "true"},
                {"field": "UF", "include_unmapped": "true"},
                {"field": "CÓDIGO DO MUNICÍPIO", "include_unmapped": "true"},
                {"field": "MUNICÍPIO", "include_unmapped": "true"},
                {"field": "CNES", "include_unmapped": "true"},
                {"field": "NOME FANTASIA", "include_unmapped": "true"},
                {"field": "TIPO NOVO DO ESTABELECIMENTO",
                    "include_unmapped": "true"},
                {"field": "TIPO DO ESTABELECIMENTO", "include_unmapped": "true"},
                {"field": "SUBTIPO DO ESTABELECIMENTO", "include_unmapped": "true"},
                {"field": "GESTÃO", "include_unmapped": "true"},
                {"field": "CONVÊNIO SUS", "include_unmapped": "true"},
                {"field": "CATEGORIA NATUREZA JURÍDICA", "include_unmapped": "true"},
                {"field": "SERVIÇO", "include_unmapped": "true"},
                {"field": "SERVIÇO CLASSIFICAÇÃO", "include_unmapped": "true"},
                {"field": "SERVIÇO - AMBULATORIAL SUS", "include_unmapped": "true"},
                {"field": "SERVIÇO - AMBULATORIAL NÃO SUS",
                    "include_unmapped": "true"},
                {"field": "SERVIÇO - HOSPITALAR SUS", "include_unmapped": "true"},
                {"field": "SERVIÇO - HOSPITALAR NÃO SUS",
                    "include_unmapped": "true"},
                {"field": "SERVIÇO TERCEIRO", "include_unmapped": "true"},
                {"field": "STATUS DO ESTABELECIMENTO", "include_unmapped": "true"}
            ],
            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
            "sort": [{"COMPETÊNCIA": "desc"}],
            "filter": [
                {
                    "meta": {
                        "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                        "params": {},
                        "field": "COMPETÊNCIA"
                    },
                    "query": {
                        "range": {
                            "COMPETÊNCIA": {
                                "format": "strict_date_optional_time",
                                "gte": "2007-06-30T21:00:00.000Z",
                                "lte": formattedDate
                            }
                        }
                    }
                }
            ],
            "parent": {
                "query": {
                    "query": "",
                    "language": "kuery"
                },
                "highlightAll": True,
                "filter": [
                    {
                        "meta": {
                            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                            "key": "index_comp.keyword"
                        },
                        "query": {
                            "match_phrase": {
                                "index_comp.keyword": f"{year}{month:02}"
                            }
                        }
                    },
                    {
                        "meta": {
                            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                            "key": "MUNICÍPIO.keyword"
                        },
                        "query": {
                            "match_phrase": {
                                "MUNICÍPIO.keyword": "SAO PAULO"
                            }
                        }
                    },
                    {
                        "meta": {
                            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                            "key": "STATUS DO ESTABELECIMENTO.keyword"
                        },
                        "query": {
                            "match_phrase": {
                                "STATUS DO ESTABELECIMENTO.keyword": "ATIVO"
                            }
                        }
                    },
                    {
                        "meta": {
                            "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                            "type": "phrases",
                            "key": "CATEGORIA NATUREZA JURÍDICA.keyword",
                            "params": ["PÚBLICO", "SEM FINS LUCRATIVOS"]
                        },
                        "query": {
                            "bool": {
                                "should": [
                                    {"match_phrase": {
                                        "CATEGORIA NATUREZA JURÍDICA.keyword": "PÚBLICO"}},
                                    {"match_phrase": {
                                        "CATEGORIA NATUREZA JURÍDICA.keyword": "SEM FINS LUCRATIVOS"}}
                                ],
                                "minimum_should_match": 1
                            }
                        }
                    }
                ],
                "parent": {
                    "filter": [
                        {
                            "meta": {
                                "index": "f5130dd0-f661-11ec-b6ec-efe6c06beef6",
                                "params": {},
                                "field": "COMPETÊNCIA"
                            },
                            "query": {
                                "range": {
                                    "COMPETÊNCIA": {
                                        "format": "strict_date_optional_time",
                                        "gte": "2007-06-30T21:00:00.000Z",
                                        "lte": formattedDate
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        },
        "columns": [
            "COMPETÊNCIA",
            "UF",
            "CÓDIGO DO MUNICÍPIO",
            "MUNICÍPIO",
            "CNES",
            "NOME FANTASIA",
            "TIPO NOVO DO ESTABELECIMENTO",
            "TIPO DO ESTABELECIMENTO",
            "SUBTIPO DO ESTABELECIMENTO",
            "GESTÃO",
            "CONVÊNIO SUS",
            "CATEGORIA NATUREZA JURÍDICA",
            "SERVIÇO",
            "SERVIÇO CLASSIFICAÇÃO",
            "SERVIÇO - AMBULATORIAL SUS",
            "SERVIÇO - AMBULATORIAL NÃO SUS",
            "SERVIÇO - HOSPITALAR SUS",
            "SERVIÇO - HOSPITALAR NÃO SUS",
            "SERVIÇO TERCEIRO",
            "STATUS DO ESTABELECIMENTO"
        ],
        "title": "EXTRATO DOS ESTABELECIMENTOS COM SERVIÇOS ESPECIALIZADOS"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Tratar a resposta como bytes, pois é um CSV
    data = response.content

    __save_data(data, "DADOS_CNES.csv")


def download_stablishment(cnes_code: int) -> None:
    """
    Downloads data from the Brazilian government's open data source and returns
    it in a JSON format.

    Returns:
    None
    """
    url = f"{DEMAS_URL}{cnes_code}"
    data = subprocess.run(['curl', '-X', 'GET', url, '-H', 'accept: application/json'],
                          capture_output=True, check=True).stdout

    if not data:
        raise ValueError("Download error: failed to download data.")

    __save_data(data, f"{cnes_code}.json")
