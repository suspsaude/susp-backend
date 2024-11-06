import logging
from decimal import Decimal

import requests
from fastapi import HTTPException
from geopy.distance import geodesic

from config.settings import AWESOME_URL


def get_distance(
    origin_lat: Decimal, origin_lon: Decimal, dest_lat: Decimal, dest_lon: Decimal
) -> float:
    """
    Função para calcular a distância entre dois pontos geográficos

    Args:
        origin_lat (int): Latitude do ponto de origem
        origin_lon (int): Longitude do ponto de origem
        dest_lat (int): Latitude do ponto de destino
        dest_lon (int): Longitude do ponto de destino

    Returns:
        float: Distância entre os dois pontos em quilômetros
    """

    origin_coords = (origin_lat, origin_lon)
    destination_coords = (dest_lat, dest_lon)

    return geodesic(origin_coords, destination_coords).kilometers


def get_address_from_cep(cep: str) -> tuple[Decimal, Decimal]:
    """
    Função para obter dados de endereço a partir de um CEP usando a API AwesomeAPI

    Args:
        cep (str): CEP para consulta

    Returns:
        tuple[Decimal, Decimal]: Tupla com a latitude e longitude do CEP
    """
    api_url = f"{AWESOME_URL}{cep}"

    response = requests.get(api_url)

    if response.status_code != 200:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="CEP não encontrado ou inválido"
            )
        raise Exception("Erro ao consultar CEP")

    data = response.json()

    if not data.get("lat") or not data.get("lng"):
        raise HTTPException(status_code=404, detail="CEP não encontrado ou inválido")

    logging.debug(
        f"CEP {cep} encontrado! Lat: {data.get('lat')}, Lng: {data.get('lng')}"
    )

    return Decimal(data.get("lat")), Decimal(data.get("lng"))
