# pylint: disable=redefined-outer-name

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.models.helpers import Coordinate
from src.utils.helpers import get_coord_from_cep, get_distance


def test_get_distance():
    origin_lat = Decimal("52.2296756")
    origin_lng = Decimal("21.0122287")
    dest_lat = Decimal("41.8919300")
    dest_lng = Decimal("12.5113300")

    origin = Coordinate(lat=origin_lat, lng=origin_lng)
    destination = Coordinate(lat=dest_lat, lng=dest_lng)

    distance = get_distance(origin, destination)
    assert isinstance(distance, float)
    assert round(distance, 1) == 1316.2

    distance = get_distance(origin, origin)
    assert isinstance(distance, float)
    assert distance == 0.0

    distance = get_distance(destination, destination)
    assert isinstance(distance, float)
    assert distance == 0.0

    distance = get_distance(destination, origin)
    assert isinstance(distance, float)
    assert round(distance, 1) == 1316.2


@patch("src.utils.helpers.requests.get")
def test_get_coord_from_cep(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"lat": "12.34", "lng": "56.78"}
    mock_get.return_value = mock_response

    coord = get_coord_from_cep("12345-678")
    assert coord.lat == Decimal("12.34")
    assert coord.lng == Decimal("56.78")

    mock_response.status_code = 404
    with pytest.raises(HTTPException) as excinfo:
        get_coord_from_cep("00000-000")
    assert excinfo.value.status_code == 404
    assert "CEP não encontrado ou inválido" in str(excinfo.value.detail)

    mock_response.status_code = 500
    with pytest.raises(Exception) as excinfo:
        get_coord_from_cep("00000-000")
    assert "Erro ao consultar CEP" in str(excinfo.value)

    mock_response.status_code = 200
    mock_response.json.return_value = {}
    with pytest.raises(Exception) as excinfo:
        get_coord_from_cep("00000-000")
    assert "Erro ao validar resposta da API" in str(excinfo.value)
