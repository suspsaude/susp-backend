from fastapi import FastAPI

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
async def unidades(cep: str, esp: str):
    return [{"message": f"Não implementado ainda! Unidades próximas ao CEP {cep} com especialidade {esp}"}]

@app.get("/unidades/detalhes",
         summary="Obtém detalhes de uma unidade de saúde a partir do CNES",
         response_description="Objeto com detalhes da unidade de saúde",
         response_model=dict,
         )
async def detalhes(cnes: int):
    return {"message": f"Não implementado ainda! Detalhes do CNES {cnes}"}