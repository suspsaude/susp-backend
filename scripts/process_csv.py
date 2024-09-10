#!/usr/bin/env python
"""Script to process the CSV files from the CNES dataset (Elasticnes and API Dados Abertos SUS).

This scripts expects a `data/` folder where all CSV files are stored. The elasticnes Serviços Especializados must be located at `data/elasticnes.csv` 
and the adasus responses must be located at `data/adasus/{cnes}.csv` for each CNES.
"""
import pandas as pd
import sys
from typing import TypedDict, Union
from pprint import pprint
import os
import argparse

class GeneralInfo(TypedDict):
    """GeneralInfo for a given CNES.
    
    Args:
        cnes (int): CNES code
        name (str): Fantasy name of the establishment
        city (str): City where the establishment is located
        state (str): State where the establishment is located
        kind (str): Kind of establishment (TIPO NOVO DO ESTABELECIMENTO)
        cep (int): CEP of the establishment
        cnpj (int): CNPJ of the establishment
        address (str): Address of the establishment
        number (str): Address number of the establishment
        district (str): District of the establishment
        telephone (str): Telephone of the establishment
        latitude (float): Latitude of the establishment (latitude_estabelecimento_decimo_grau)
        longitude (float): Longitude of the establishment (longitude_estabelecimento_decimo_grau)
        email (str): e-mail address of the establishment
        shift (str): Establishment shift (descricao_turno_atendimento)
    """
    cnes: int
    name: str
    city: str
    state: str
    kind: str
    cep: int
    cnpj: int 
    address: str
    number: str
    district: str
    telephone: str
    latitude: float
    longitude: float
    email: str
    shift: str

class ServiceRecord(TypedDict):
    """ServiceRecord for a given CNES.
    
    Args:
        cnes (int): CNES code
        servico (str): Service provided by the establishment
        classificacao (str): Classification of the service
    """
    cnes: int
    service: str
    classification: str

def general_info(cnes: int, elasticnes: Union[pd.DataFrame, str], adasus: Union[pd.DataFrame, str]) -> GeneralInfo:
    """Joins the data from a elasticnes dataset row and a adasus request to `/cnes/estabelecimentos/{cnes}`. Both `Series` must have the same `CNES`/`codigo_cnes`.

    Args:
        elasticnes (DataFrame | str): the full elasticnes dataset or the name of the `.csv` file
        adasus (DataFrame): the response of `/cnes/estabelecimentos/{cnes}` or the name of the `.csv` file
    """

    if isinstance(elasticnes, str):
        elasticnes = pd.read_csv(elasticnes)
    if isinstance(adasus, str):
        adasus = pd.read_csv(adasus, delimiter=';')

    adasus: pd.Series = adasus[adasus['codigo_cnes'] == cnes].iloc[0]
    elasticnes: pd.Series = elasticnes[elasticnes['CNES'] == cnes].iloc[0]
        
    return GeneralInfo(
        cnes = elasticnes['CNES'],
        name = elasticnes['NOME FANTASIA'],
        city = elasticnes['MUNICÍPIO'],
        state = elasticnes['UF'],
        kind = elasticnes['TIPO NOVO DO ESTABELECIMENTO'],
        cep = adasus["codigo_cep_estabelecimento"],
        cnpj = adasus["numero_cnpj"],
        address = adasus["endereco_estabelecimento"],
        number = adasus["numero_estabelecimento"],
        district = adasus["bairro_estabelecimento"],
        telephone = adasus["numero_telefone_estabelecimento"],
        latitude = adasus["latitude_estabelecimento_decimo_grau"],
        longitude = adasus["longitude_estabelecimento_decimo_grau"],
        email = adasus["endereco_email_estabelecimento"],
        shift = adasus["descricao_turno_atendimento"]
    )

def service_records(elasticnes: Union[pd.DataFrame, str]) -> list[ServiceRecord]: 
    """Filters useful service information from the elasticnes dataset and build a ServiceRecord list.

    Args:
        elasticnes (str): "Serviços Especializados" `.csv` file from elasticnes 
    
    Returns:
        list[ServiceRecord]: lista of ServiceRecord
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
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='process_csv', 
                                     description="""Process the dataset from csv files.
                                     
                                     Can extract general info for a given CNES or all service records from csv files obtained 
                                     from elasticnes and API Dados Abertos SUS.

                                     Can be used as a standalone script or as a module providing the general_info and service_records functions.""")
    
    parser.add_argument('mode', type=str, help='Mode to run the script', choices=['general_info', 'service_records'])
    parser.add_argument('-c', '--cnes', type=int, help='CNES code to get the general info')
    parser.add_argument('-e', '--elasticnes', type=str, help='Path to the elasticnes csv file')
    parser.add_argument('-a', '--adasus', type=str, help='Path to the adasus csv file')
    
    args = parser.parse_args()
    
    if args.mode == 'general_info': 
        if not args.elasticnes:
            print('Please provide the path to the elasticnes csv file (via -e | --elasticnes)')
            sys.exit(1)

        records = service_records(args.elasticnes)
        pprint(records)
        
    elif args.mode == 'service_records':
        if not args.cnes or not args.elasticnes or not args.adasus:
            print('Please provide the CNES code (via -c | --cnes) and the paths to the elasticnes (via -e | --elasticnes) and adasus (via -a | --adasus) csv files')
            sys.exit(1)

        info = general_info(args.cnes, args.elasticnes, args.adasus)
        pprint(info)
    
    else:
        print(f'Invalid mode "{args.mode}"! Valid modes are "general_info" and "service_records"')
        sys.exit(1)