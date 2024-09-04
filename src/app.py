from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Não há nada aqui, apenas um sanity check!"}

@app.get("/especialidades")
async def especialidades():
    return {"message": "Não implementado ainda!"}

@app.get("/unidades")
async def unidades(cep: str, esp: str):
    return {"message": f"Não implementado ainda! Unidades próximas ao CEP {cep} com especialidade {esp}"}

@app.get("/detalhes")
async def detalhes(cnes: int):
    return {"message": f"Não implementado ainda! Detalhes do CNES {cnes}"}