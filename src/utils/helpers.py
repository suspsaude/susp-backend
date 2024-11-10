import logging

import requests
from fastapi import HTTPException
from geopy.distance import geodesic
from pydantic import ValidationError

from config.settings import AWESOME_URL
from src.models.helpers import Coordinate


def get_distance(origin: Coordinate, destination: Coordinate) -> float:
    """
    Função para calcular a distância entre dois pontos geográficos

    Args:
        origin (Coordinate): Coordenadas do ponto de origem
        destination (Coordinate): Coordenadas do ponto de destino

    Returns:
        float: Distância entre os dois pontos em quilômetros
    """

    origin_coords = (origin.lat, origin.lng)
    destination_coords = (destination.lat, destination.lng)

    distance = geodesic(origin_coords, destination_coords).kilometers

    logging.debug("Distancia entre %s e %s: %s km", origin, destination, distance)

    return distance


def get_coord_from_cep(cep: str) -> Coordinate:
    """
    Função para obter dados de endereço a partir de um CEP usando a API AwesomeAPI

    Args:
        cep (str): CEP para consulta

    Returns:
        Coordinate: Coordenadas do endereço encontrado
    """
    api_url = f"{AWESOME_URL}{cep}"

    response = requests.get(api_url)

    if response.status_code != 200:
        if response.status_code == 404:
            logging.warning("CEP %s não encontrado", cep)
            raise HTTPException(
                status_code=404, detail="CEP não encontrado ou inválido"
            )
        logging.error(
            "Erro diferente de 404 ao consultar CEP: %s", response.status_code
        )
        raise Exception("Erro ao consultar CEP")

    try:
        data = response.json()
        coord = Coordinate(lat=data.get("lat"), lng=data.get("lng"))

    except ValidationError as e:
        logging.error("Resposta da API inválida: %s", e)
        raise Exception("Erro ao validar resposta da API") from e

    logging.debug("CEP %s encontrado! Coordenadas: %s %s", cep, coord.lat, coord.lng)

    return coord
