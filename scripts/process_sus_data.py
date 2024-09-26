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

from src.db.tables import GeneralInfo, ServiceRecord, MedicalService

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
        adasus = json.load(open(adasus))

    elasticnes: pd.Series = elasticnes[elasticnes['CNES']
                                       == adasus['codigo_cnes']].iloc[0]

    return GeneralInfo(
        cnes=elasticnes['CNES'],
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

def process_medical_services(elasticnes: Union[pd.DataFrame, str]) -> set[MedicalService]:
    """
    """
    if isinstance(elastcines, str):
        data = pd.read_csv(elasticnes)
    else:
        data = elasticnes

    medical_services = set()

    for service in data['service']:
        medical_services.add(service)

    return medical_services
    

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
    services_records = [ServiceRecord(**service) for service in services_list]

    return services_records
