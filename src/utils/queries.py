import logging
from typing import Dict, List

from fastapi import HTTPException

from config.settings import MAX_UNITIES
from src.models.endpoints import ExpertiseItem, UnitItem, UnitRequest
from src.models.helpers import Coordinate
from src.models.tables import GeneralInfo, MedicalService, ServiceRecord
from src.utils.helpers import get_distance

description = """
Funções para consulta de dados rápidos úteis para as requisicoes da API SUSP.
"""


def get_expertise_list(session) -> List[ExpertiseItem]:
    """
    Função para obter a lista de especialidades disponíveis.

    Args:
        session (Session): Sessão do banco de dados

    Returns:
        List[ExpertiseItem]: Lista de especialidades
    """

    expertises: List[MedicalService] = session.query(MedicalService).all()

    expertise_list = [
        ExpertiseItem(
            id=[expertise.id, expertise.class_id], name=expertise.classification
        )
        for expertise in expertises
    ]

    logging.info("Lista de especialidades encontrada!")
    logging.debug("Especialidades: %s", expertise_list)

    return expertise_list


def get_unit(session, cnes: int) -> GeneralInfo:
    """
    Função para obter os dados de uma unidade de saúde a partir do CNES.

    Args:
        session (Session): Sessão do banco de dados
        cnes (int): CNES da unidade de saúde

    Returns:
        GeneralInfo: Objeto com os dados da unidade de saúde
    """
    unit: GeneralInfo = (
        session.query(GeneralInfo).filter(GeneralInfo.cnes == cnes).first()
    )

    if not isinstance(unit, GeneralInfo):
        raise HTTPException(status_code=404, detail="Unidade não encontrada")

    logging.info("Unidade %s encontrada!", unit.cnes)
    logging.debug("Unidade %s encontrada: %s", unit.cnes, unit)

    return unit


def get_near_unit_list(
    session, params: UnitRequest, origin: Coordinate
) -> List[UnitItem]:
    """
    Função para obter uma lista de unidades de saúde próximas a um CEP que atendem a uma determinada especialidade.

    Args:
        session (Session): Sessão do banco de dados
        params (UnitRequest): Parâmetros da requisição
        origin (Coordinate): Coordenadas do CEP de origem

    Returns:
        List[UnitItem]: Lista de unidades de saúde ordenadas por distância
    """

    service_records = (
        session.query(ServiceRecord)
        .filter(
            ServiceRecord.service == params.srv,
            ServiceRecord.classification == params.clf,
        )
        .all()
    )

    unit_list: List[UnitItem] = []
    for record in service_records:
        unit: GeneralInfo = (
            session.query(GeneralInfo).filter(GeneralInfo.cnes == record.cnes).first()
        )

        if isinstance(unit, GeneralInfo):
            # Some units may not have coordinates :/
            if not unit.latitude or not unit.longitude:
                logging.warning(
                    "Unidade %s não possui coordenadas geográficas!", unit.cnes
                )
                continue

            destination = Coordinate(lat=unit.latitude, lng=unit.longitude)

            distance = get_distance(
                origin,
                destination,
            )

            new_unit = UnitItem(
                cnes=unit.cnes,
                name=unit.name,
                address=f"{unit.address}, {unit.number}, {unit.district}",
                type=unit.kind,
                distance=distance,
            )

            logging.debug("Unidade encontrada: %s", new_unit)

            unit_list.append(new_unit)
        else:
            print(f"Unidade {record.cnes} não encontrada!")

    unit_list = sorted(unit_list, key=lambda x: x.distance)[:MAX_UNITIES]

    logging.info("Lista de unidades encontrada!")
    logging.debug("Lista de unidades encontrada: %s", unit_list)

    return unit_list


def get_all_services(session, cnes: int) -> Dict[str, List[str]]:
    """
    Função para obter todos os serviços oferecidos por uma unidade de saúde.

    Args:
        session (Session): Sessão do banco de dados
        cnes (int): CNES da unidade de saúde

    Returns:
        Dict[str, List[str]]: Dicionário com os serviços oferecidos pela unidade
    """

    unit_services: List[ServiceRecord] = (
        session.query(ServiceRecord).filter(ServiceRecord.cnes == cnes).all()
    )

    services_dict: Dict[str, List[str]] = {}
    for unit_service in unit_services:
        services: MedicalService = (
            session.query(MedicalService)
            .filter(
                MedicalService.id == unit_service.service,
                MedicalService.class_id == unit_service.classification,
            )
            .first()
        )

        if services is None:
            logging.warning(
                "Serviço não encontrado: id: %s, classification: %s",
                unit_service.service,
                unit_service.classification,
            )
            continue

        logging.debug(
            "Serviço encontrado: class id: %s, service: %s, classification: %s, id: %s",
            services.class_id,
            services.service,
            services.classification,
            services.id,
        )

        if services.service not in services_dict:
            services_dict[str(services.service)] = []

        services_dict[services.service].append(services.classification)

    logging.info("Serviços da unidade %s encontrados!", cnes)
    logging.debug("Serviços da unidade %s: %s", cnes, services_dict)

    return services_dict
