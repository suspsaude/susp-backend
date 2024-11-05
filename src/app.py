import logging
import traceback
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import DB_URL, DEBUG
from src.models.endpoints import (DetailsResponse, ExpertiseItem, UnitItem,
                                  UnitRequest)
from src.utils.helpers import get_address_from_cep
from src.utils.queries import (get_all_services, get_expertise_list,
                               get_near_unit_list, get_unit)

# =============================================================================
#                                   SETUP
# =============================================================================


description = """
API para consulta de informações sobre unidades de saúde do SUS para a plataforma SUSP.

Endpoints disponíveis:

- `/especialidades`: Retorna a lista de especialidades disponíveis.
- `/unidades?cep=&esp=`: Retorna a lista de unidades de saúde próximas a um CEP com uma determinada especialidade.
- `/unidades/detalhes?cnes=`: Retorna detalhes de uma unidade de saúde a partir do numero CNES da unidade.
"""

app = FastAPI(
    title="SUSP",
    description=description,
)
engine = create_engine(DB_URL)
session = sessionmaker(bind=engine)()
logging.basicConfig(level="DEBUG" if DEBUG else "INFO")


# =============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(_, exc: Exception):
    """
    Trata exceções não tratadas e retorna uma resposta JSON com o erro.
    """
    logging.error(f"Error: {exc}")
    logging.debug(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno no servidor."},
    )


# =============================================================================
#                                   ENDPOINTS
# =============================================================================


@app.get("/")
async def root():
    return JSONResponse(
        status_code=200,
        content={"detail": "Não há nada aqui, apenas um sanity check!"},
    )


# =============================================================================


@app.get(
    "/especialidades",
    summary="Lista de especialidades disponíveis",
    response_description="Lista de especialidades",
    response_model=List[ExpertiseItem],
    description="""Retorna a lista de especialidades disponíveis para consulta.
            Consiste em uma lista de objetos do tipo `{id: [number, number], name: string}`. Onde `id` é o par de identificadores que identifica o SERVIÇO e o SERVIÇO CLASSIFICAÇÃO.
            Esses identificadores são utilizados como atributos `id` e `cls`, respectivamente, em uma requisição para a rota `/unidades`.
            """,
    responses={
        200: {
            "description": "Lista de especialidades disponíveis",
            "content": {
                "application/json": {
                    "example": [
                        {"id": [121, 12], "name": "MAMOGRAFIA"},
                        {"id": [145, 9], "name": "EXAMES MICROBIOLOGICOS"},
                    ]
                }
            },
        }
    },
)
async def expertises():
    logging.debug("Expertise list request")
    return get_expertise_list(session)


# =============================================================================


@app.get(
    "/unidades",
    summary="Obtém as unidades próximas a um CEP que atendem uma determinada especialidade",
    response_description="Lista de unidades de saúde ordenadas por distância que atendem à especialidade desejada",
    response_model=List[UnitItem],
    description="""Retorna a lista de unidades de saúde próximas a um CEP que atendem a uma determinada especialidade.
            A requisição deve conter os parâmetros `cep`, `srv` e `clf`. O parâmetro `cep` deve ser um CEP no formato 00000-000. Os parâmetros `srv` e `clf` são os identificadores do serviço e da classificação da especialidade, respectivamente.
            A resposta consiste em uma lista de objetos do tipo `{name: string, address: string, type: string, distance: float}`. Onde `name` é o nome da unidade de saúde, `address` é o endereço da unidade, `type` é o tipo da unidade e `distance` é a distância em quilômetros entre o CEP informado e a unidade de saúde.
            """,
)
async def units(params: UnitRequest = Depends()):
    logging.debug(f"Unit list request: {params}")
    (latitude, longitude) = get_address_from_cep(params.cep)
    return get_near_unit_list(session, params, latitude, longitude)


# =============================================================================


@app.get(
    "/unidades/detalhes",
    summary="Obtém detalhes de uma unidade de saúde a partir do CNES",
    response_description="Objeto com detalhes da unidade de saúde",
    response_model=DetailsResponse,
    description="""Retorna detalhes de uma unidade de saúde a partir do número CNES da unidade.
            A requisição deve conter o parâmetro `cnes`, que é o número CNES da unidade de saúde.
            A resposta consiste em um objeto com os detalhes da unidade de saúde, incluindo o nome, cidade, estado, tipo, CEP, CNPJ, endereço, número, bairro, telefone, latitude, longitude, e-mail, turno de atendimento e serviços oferecidos.
            """,
)
async def details(cnes: int):
    logging.debug(f"Details request: {cnes}")
    unit = get_unit(session, cnes)
    services_dict = get_all_services(session, cnes)

    return DetailsResponse(
        cnes=unit.cnes,
        name=unit.name,
        city=unit.city,
        state=unit.state,
        kind=unit.kind,
        cep=unit.cep,
        cnpj=unit.cnpj,
        address=unit.address,
        number=unit.number,
        district=unit.district,
        telephone=unit.telephone,
        latitude=unit.latitude,
        longitude=unit.longitude,
        email=unit.email,
        shift=unit.shift,
        services=services_dict,
    )
