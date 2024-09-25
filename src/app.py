import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.tables import Base, MedicalService

description = """
API para consulta de informações sobre unidades de saúde do SUS para a plataforma SUSP.

Endpoints disponíveis:

- `/especialidades`: Retorna a lista de especialidades disponíveis.
- `/unidades?cep=&esp=`: Retorna a lista de unidades de saúde próximas a um CEP com uma determinada especialidade.
- `/unidades/detalhes?cnes=`: Retorna detalhes de uma unidade de saúde a partir do numero CNES da unidade.
"""

DB_USER = os.getenv("DBUSER")
DB_NAME = os.getenv("DBNAME")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

app = FastAPI(
    title="SUSP",
    description=description,
)

@app.get("/")
async def root():
    return {"message": "Não há nada aqui, apenas um sanity check!"}

@app.get("/especialidades", 
         summary="Lista de especialidades disponíveis", 
         response_description="Lista de especialidades",
         response_model=list[str],
         )
async def especialidades():
    engine = create_engine(DB_URL)
    session = (sessionmaker(bind=engine))()
    expertises = session.query(MedicalService.name).distinct().all()
    
    return [expertise.tuple()[0] for expertise in expertises]

@app.get("/unidades", 
         summary="Obtém as unidades próximas a um CEP que atendem uma determinada especialidade",
         response_description="Lista de unidades de saúde ordenadas por distância que atendem à especialidade desejada",
         response_model=list[dict],
         )
async def unidades(cep: str, esp: str):
    return [{"message": f"Não implementado ainda! Unidades próximas ao CEP {cep} com especialidade {esp}"}]

@app.get("/unidades/detalhes",
         summary="Obtém detalhes de uma unidade de saúde a partir do CNES",
         response_description="Objeto com detalhes da unidade de saúde",
         response_model=dict,
         )
async def detalhes(cnes: int):
    return {"message": f"Não implementado ainda! Detalhes do CNES {cnes}"}