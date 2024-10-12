import os

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field

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

MAX_DISTANCE = 10

app = FastAPI(
    title="SUSP",
    description=description,
)

class UnidadeRequest(BaseModel):
    cep: str = Field(..., regex=r'^\d{5}-?\d{3}$', description="CEP no formato 00000000")
    esp: int = Field(..., min_length=1, description="Especialidade médica")

@app.get("/")
async def root():
    return {"message": "Não há nada aqui, apenas um sanity check!"}

@app.get("/especialidades", 
         summary="Lista de especialidades disponíveis", 
         response_description="Lista de especialidades",
         response_model=list[str],
         )
async def especialidades():
    return ["Não implementado ainda!"]

@app.get("/unidades", 
         summary="Obtém as unidades próximas a um CEP que atendem uma determinada especialidade",
         response_description="Lista de unidades de saúde ordenadas por distância que atendem à especialidade desejada",
         response_model=list[dict],
         )
async def unidades(params: UnidadeRequest = Depends()):
    engine = create_engine(DB_URL)
    session = sessionmaker(bind=engine)()
    
    address_data = get_address_from_cep(params.cep)
    latitude = address_data["latitude"]
    longitude = address_data["longitude"]

    service_records = session.query(ServiceRecord).filter(ServiceRecord.service == params.esp).all()

    result = []
    for record in service_records:
        unit = session.query(GeneralInfo).filter(GeneralInfo.cnes == record.cnes).first()

        if unit:
            distance = get_distance(
                {"latitude": latitude, "longitude": longitude},
                {"latitude": unit.latitude, "longitude": unit.longitude}
            )

            if distance <= MAX_DISTANCE:
                result.append({
                    "name": unit.name,
                    "address": f"{unit.address}, {unit.number}, {unit.district}",
                    "type": unit.kind,
                    "rating": record.classification,
                    "distance": distance
                })
        else:
            print(f"Unidade {record.cnes} não encontrada!")

    return sorted(result, key=lambda x: x["distance"])

@app.get("/unidades/detalhes",
         summary="Obtém detalhes de uma unidade de saúde a partir do CNES",
         response_description="Objeto com detalhes da unidade de saúde",
         response_model=dict,
         )
async def detalhes(cnes: int):
    return {"message": f"Não implementado ainda! Detalhes do CNES {cnes}"}