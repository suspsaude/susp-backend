"""Script to process the CSV files from the CNES dataset (Elasticnes and API
Dados Abertos SUS).

This scripts expects a `data/` folder where all CSV files are stored. The
elasticnes Serviços Especializados must be located at `data/elasticnes.csv` and
the adasus responses must be located at `data/adasus/{cnes}.csv` for each CNES.
"""
import pandas as pd
import sys
import json
from typing import TypedDict, Union
from pprint import pprint
import argparse

from src.models.tables import GeneralInfo, ServiceRecord, MedicalService

def process_general_info(elasticnes: Union[pd.DataFrame, str], adasus: Union[dict, str]) -> GeneralInfo:
    """Joins the data from a elasticnes dataset row and a adasus request to
    `/cnes/estabelecimentos/{cnes}`. Both `Series` must have the same
    `CNES`/`codigo_cnes`.

    Args:
        elasticnes (DataFrame | str): the full elasticnes dataset or the name of the `.csv` file
        adasus (DataFrame): the response of `/cnes/estabelecimentos/{cnes}` or the name of the `.json` file
    """

    if isinstance(elasticnes, str):
        elasticnes = pd.read_csv(elasticnes)
    if isinstance(adasus, str):
        try:
            adasus = json.load(open(adasus))
        except Exception as e:
            print(f"Error loading JSON file {adasus}: {e}")
            return


    elasticnes: pd.Series = elasticnes[elasticnes['CNES']
                                       == adasus['codigo_cnes']].iloc[0]

    return GeneralInfo(
        cnes=elasticnes['CNES'].item(),
        name=elasticnes['NOME FANTASIA'],
        city=elasticnes['MUNICÍPIO'],
        state=elasticnes['UF'],
        kind=elasticnes['TIPO NOVO DO ESTABELECIMENTO'],
        cep=adasus["codigo_cep_estabelecimento"],
        cnpj=adasus["numero_cnpj"],
        address=adasus["endereco_estabelecimento"],
        number=adasus["numero_estabelecimento"],
        district=adasus["bairro_estabelecimento"],
        telephone=adasus["numero_telefone_estabelecimento"],
        latitude=adasus["latitude_estabelecimento_decimo_grau"],
        longitude=adasus["longitude_estabelecimento_decimo_grau"],
        email=adasus["endereco_email_estabelecimento"],
        shift=adasus["descricao_turno_atendimento"]
    )
def process_medical_services(elasticnes: Union[pd.DataFrame, str]) -> list[MedicalService]:
    """Takes the elasticnes dataset and filters the medical services from it.
    A medical service is a tuple of (SERVIÇO, SERVIÇO CLASSIFICAÇÃO).

    Args:
        elasticnes (DataFrame | str): the full elasticnes dataset or the name of the `.csv` file
    Returns:
        list[MedicalService]: list of unique MedicalService
    """
    if isinstance(elasticnes, str):
        data = pd.read_csv(elasticnes)
    else:
        data = elasticnes

    medical_services = set([(service['SERVIÇO'], service['SERVIÇO CLASSIFICAÇÃO']) for service in data[['SERVIÇO', 'SERVIÇO CLASSIFICAÇÃO']].to_dict(orient='records')])

    processed: list[MedicalService] = []

    for service in medical_services:
        [id, serv] = service[0].split(maxsplit=1)
        [class_id, cls] = service[1].split(maxsplit=1)

        processed.append(MedicalService(
            id = int(int(id)),
            class_id = int(int(class_id)),
            service = serv,
            classification = cls
        ))

    return processed


def process_service_records(elasticnes: Union[pd.DataFrame, str]) -> list[ServiceRecord]:
    """Filters useful service information from the elasticnes dataset and build
    a ServiceRecord list.

    Args:
        elasticnes (str): "Serviços Especializados" `.csv` file from elasticnes

    Returns:
        list[ServiceRecord]: list of ServiceRecord
    """
    if isinstance(elasticnes, str):
        data = pd.read_csv(elasticnes)
    else:
        data = elasticnes

    services_table = data[['CNES', 'SERVIÇO', 'SERVIÇO CLASSIFICAÇÃO']]
    services_table.columns = ['cnes', 'service', 'classification']
    services_list = services_table.to_dict(orient='records')
    services_records = [ServiceRecord(
        cnes = service["cnes"],
        service = int(service["service"].split(maxsplit=1)[0]),
        classification = int(service["classification"].split(maxsplit=1)[0])
        ) for service in services_list]

    return services_records
