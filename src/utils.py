import requests

description = """
Funções para consulta de dados rápidos úteis para as requisicoes da API SUSP.
"""

AWESOME_URL = "https://cep.awesomeapi.com.br/json/"

def get_address_from_cep(cep: str) -> dict:
    """
    Função para obter dados de endereço a partir de um CEP usando a API AwesomeAPI.

    Args:
        cep (str): CEP para consulta
    
    Returns:
        dict: Dicionário com os dados úteis do endereço
    """
    api_url = f"{AWESOME_URL}{cep}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return {
            #"address_type": data["address_type"],
            #"address_name": data["address_name"],
            #"address": data["address"],
            #"neighborhood": data["neighborhood"],
            #"city": data["city"],
            #"state": data["state"],
            "latitude": data["lat"],
            "longitude": data["lng"],
        }
    else:
        raise Exception("Erro ao buscar dados do endereço")
    
def get_distance(origin: dict, destination: dict) -> float:
    """
    Função para calcular a distância entre dois pontos geográficos.

    Args:
        origin (dict): Dicionário com as coordenadas do ponto de origem
        destination (dict): Dicionário com as coordenadas do ponto de destino
    
    Returns:
        float: Distância entre os dois pontos em quilômetros
    """
    from geopy.distance import geodesic

    origin_coords = (origin["latitude"], origin["longitude"])
    destination_coords = (destination["latitude"], destination["longitude"])

    return geodesic(origin_coords, destination_coords).kilometers