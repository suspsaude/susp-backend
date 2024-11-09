# pylint: disable=redefined-outer-name

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.models.endpoints import ExpertiseItem, UnitItem, UnitRequest
from src.models.helpers import Coordinate
from src.models.tables import GeneralInfo

client = TestClient(app, base_url="http://test")


@pytest.fixture
def mock_db_session():
    """
    Mocks the database session object.
    """
    with patch("src.app.session") as mock:
        mock.return_value = MagicMock()
        yield mock


def test_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Não há nada aqui, apenas um sanity check!"}


def test_expertises(mock_db_session):
    """
    Test the endpoint to get the list of expertises.
    """
    with patch("src.app.get_expertise_list") as mock_get_expertise_list:
        mock_get_expertise_list.return_value = [
            ExpertiseItem(id=[121, 12], name="MAMOGRAFIA"),
            ExpertiseItem(id=[145, 9], name="EXAMES MICROBIOLOGICOS"),
        ]
        response = client.get("/especialidades")
        assert response.status_code == 200
        assert response.json() == [
            {"id": [121, 12], "name": "MAMOGRAFIA"},
            {"id": [145, 9], "name": "EXAMES MICROBIOLOGICOS"},
        ]
        mock_get_expertise_list.assert_called_once_with(mock_db_session)


def test_units(mock_db_session):
    """
    Test the endpoint to get the list of units.
    """
    # pylint: disable=redefined-outer-name

    with patch("src.app.get_coord_from_cep") as mock_get_coord_from_cep:
        mock_get_coord_from_cep.return_value = Coordinate(lat="12.34", lng="56.78")
        with patch("src.app.get_near_unit_list") as mock_get_near_units:
            mock_get_near_units.return_value = [
                UnitItem(
                    cnes=123456,
                    name="Unidade de Saúde A",
                    address="Rua A, 123, Centro",
                    type="Hospital",
                    distance=5.4,
                )
            ]

            params = UnitRequest(cep="12345-678", srv=1, clf=1)
            response = client.get("/unidades", params=params.model_dump())
            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0]["name"] == "Unidade de Saúde A"

            mock_get_coord_from_cep.assert_called_once_with("12345-678")
            mock_get_near_units.assert_called_once_with(
                mock_db_session, params, Coordinate(lat="12.34", lng="56.78")
            )


def test_details(mock_db_session):
    """
    Test the endpoint to get the details of a unit.
    """
    with patch("src.app.get_unit") as mock_get_unit:
        mock_get_unit.return_value = GeneralInfo(
            cnes=123,
            name="Unidade Teste",
            city="Cidade X",
            state="Estado Y",
            kind="Tipo Z",
            cep="12345-678",
            cnpj="12.345.678/0001-12",
            address="Rua X",
            number="123",
            district="Bairro Y",
            telephone="(12) 3456-7890",
            latitude=Decimal("12.34"),
            longitude=Decimal("56.78"),
            email="contato@unidade.com",
            shift="Integral",
        )
        with patch("src.app.get_all_services") as mock_get_all_services:
            mock_get_all_services.return_value = {"Consulta": ["121", "10"]}
            response = client.get("/unidades/detalhes?cnes=123")
            assert response.status_code == 200
            assert response.json()["name"] == "Unidade Teste"
            assert response.json()["services"] == {"Consulta": ["121", "10"]}

            mock_get_unit.assert_called_once_with(mock_db_session, 123)
            mock_get_all_services.assert_called_once_with(mock_db_session, 123)
