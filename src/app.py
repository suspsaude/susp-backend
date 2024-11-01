import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field

from typing import Optional, List, Dict
from db.tables import Base, MedicalService, ServiceRecord, GeneralInfo
from src.utils import get_address_from_cep, get_distance

description = """
API para consulta de informações sobre unidades de saúde do SUS para a plataforma SUSP.

Endpoints disponíveis:

- `/especialidades`: Retorna a lista de especialidades disponíveis.
- `/unidades?cep=&esp=`: Retorna a lista de unidades de saúde próximas a um CEP com uma determinada especialidade.
- `/unidades/detalhes?cnes=`: Retorna detalhes de uma unidade de saúde a partir do numero CNES da unidade.
"""

DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_NAME}"

MAX_UNITIES = 20

app = FastAPI(
    title="SUSP",
    description=description,
)

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"], 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

class UnidadeRequest(BaseModel):
    cep: str = Field(..., pattern=r'^\d{5}-?\d{3}$', description="CEP no formato 00000-000")
    srv: int = Field(..., description="Serviço médico")
    clf: int = Field(..., description="Classificação da especialidade")

@app.get("/")
async def root():
    return {"message": "Não há nada aqui, apenas um sanity check!"}

@app.get("/especialidades", 
         summary="Lista de especialidades disponíveis", 
         response_description="Lista de especialidades",
         response_model=list[dict],
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
                }
            }
        })
async def especialidades():
    engine = create_engine(DB_URL)
    session = (sessionmaker(bind=engine))()
    expertises = session.query(MedicalService).all()
    
    return [{"id": [expertise.id, expertise.class_id], "name": expertise.classification} for expertise in expertises]

@app.get("/unidades", 
         summary="Obtém as unidades próximas a um CEP que atendem uma determinada especialidade",
         response_description="Lista de unidades de saúde ordenadas por distância que atendem à especialidade desejada",
         response_model=list[dict],
         description="""Retorna a lista de unidades de saúde próximas a um CEP que atendem a uma determinada especialidade.
            A requisição deve conter os parâmetros `cep`, `srv` e `clf`. O parâmetro `cep` deve ser um CEP no formato 00000-000. Os parâmetros `srv` e `clf` são os identificadores do serviço e da classificação da especialidade, respectivamente.
            A resposta consiste em uma lista de objetos do tipo `{name: string, address: string, type: string, distance: float}`. Onde `name` é o nome da unidade de saúde, `address` é o endereço da unidade, `type` é o tipo da unidade e `distance` é a distância em quilômetros entre o CEP informado e a unidade de saúde.
            """,
         )
async def unidades(params: UnidadeRequest = Depends()):
    engine = create_engine(DB_URL)
    session = sessionmaker(bind=engine)()
    
    address_data = get_address_from_cep(params.cep)
    latitude = address_data["latitude"]
    longitude = address_data["longitude"]

    service_records = session.query(ServiceRecord).filter(
        ServiceRecord.service == params.srv,
        ServiceRecord.classification == params.clf
    ).all()

    result = []
    for record in service_records:
        unit = session.query(GeneralInfo).filter(GeneralInfo.cnes == record.cnes).first()

        if unit:
            distance = get_distance(
                {"latitude": latitude, "longitude": longitude},
                {"latitude": unit.latitude, "longitude": unit.longitude}
            )

            result.append({
                "cnes": unit.cnes,
                "name": unit.name,
                "address": f"{unit.address}, {unit.number}, {unit.district}",
                "type": unit.kind,
                "distance": distance
            })
        else:
            print(f"Unidade {record.cnes} não encontrada!")

    return sorted(result, key=lambda x: x["distance"])[:MAX_UNITIES]

@app.get("/unidades/detalhes",
         summary="Obtém detalhes de uma unidade de saúde a partir do CNES",
         response_description="Objeto com detalhes da unidade de saúde",
         response_model=dict,
         description="""Retorna detalhes de uma unidade de saúde a partir do número CNES da unidade.
            A requisição deve conter o parâmetro `cnes`, que é o número CNES da unidade de saúde.
            A resposta consiste em um objeto com os detalhes da unidade de saúde, incluindo o nome, cidade, estado, tipo, CEP, CNPJ, endereço, número, bairro, telefone, latitude, longitude, e-mail, turno de atendimento e serviços oferecidos.
            """,
         )
async def detalhes(cnes: int):
    engine = create_engine(DB_URL)
    session = sessionmaker(bind=engine)()

    unit = session.query(GeneralInfo).filter(GeneralInfo.cnes == cnes).first()
    unit_services = session.query(ServiceRecord).filter(ServiceRecord.cnes == cnes).all()

    services_dict: Dict[str, List[str]] = {}

    for unit_service in unit_services:
        service = session.query(MedicalService).filter(
            MedicalService.id == unit_service.service,
            MedicalService.class_id == unit_service.classification
        ).first()

        if service.service not in services_dict:
            services_dict[service.service] = []
        services_dict[service.service].append(service.classification)

    unit_dict = {
        "cnes": unit.cnes,
        "name": unit.name,
        "city": unit.city,
        "state": unit.state,
        "kind": unit.kind,
        "cep": unit.cep,
        "cnpj": unit.cnpj,
        "address": unit.address,
        "number": unit.number,
        "district": unit.district,
        "telephone": unit.telephone,
        "latitude": unit.latitude,
        "longitude": unit.longitude,
        "email": unit.email,
        "shift": unit.shift,
        "services": services_dict
    }

    return unit_dict