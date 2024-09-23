from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeneralInfo(Base):
    """GeneralInfo for a given CNES.
    
    Args:
        cnes (int): CNES code
        name (str): Fantasy name of the establishment
        city (str): City where the establishment is located
        state (str): State where the establishment is located
        kind (str): Kind of establishment (TIPO NOVO DO ESTABELECIMENTO)
        cep (int): CEP of the establishment
        cnpj (int): CNPJ of the establishment
        address (str): Address of the establishment
        number (str): Address number of the establishment
        district (str): District of the establishment
        telephone (str): Telephone of the establishment
        latitude (float): Latitude of the establishment (latitude_estabelecimento_decimo_grau)
        longitude (float): Longitude of the establishment (longitude_estabelecimento_decimo_grau)
        email (str): e-mail address of the establishment
        shift (str): Establishment shift (descricao_turno_atendimento)
    """
    _tablename_ = 'general_infos'

    cnes: int
    name: str
    city: str
    state: str
    kind: str
    cep: int
    cnpj: int 
    address: str
    number: str
    district: str
    telephone: str
    latitude: float
    longitude: float
    email: str
    shift: str

class ServiceRecord(Base):
    """ServiceRecord for a given CNES.
    
    Args:
        cnes (int): CNES code
        servico (str): Service provided by the establishment
        classificacao (str): Classification of the service
    """
    _tablename_ = 'service_records'
    
    cnes: int
    service: str
    classification: str