from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeneralInfo(Base):
    """GeneralInfo for a given CNES.
    
    Args:
        cnes (int): CNES code
        name (str): Fantasy name of the establishment
        city (str): City where the establishment is located - Optional (filters to SP)
        state (str): State where the establishment is located - Optional (filters to SP)
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

    cnes: Column(int, primary_key=True)
    name: Column(str)
    # city: Column(str)
    # state: Column(str)
    kind: Column(str)
    cep: Column(int)
    cnpj: Column(int) 
    address: Column(str)
    number: Column(str)
    district: Column(str)
    telephone: Column(str)
    latitude: Column(float)
    longitude: Column(float)
    email: Column(str)
    shift: Column(str)
    
class MedicalService(Base):
    """MedicalService for a type of service.

    Args:
        id (int): Medical service id
        name (str): Description of the medical expertise
    """
    __tablename__ = 'medical_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class ServiceRecord(Base):
    """ServiceRecord for a given CNES.
    
    Args:
        cnes (int): CNES code
        service (int): ID of the service provided by the establishment (foreign key to MedicalService)
        classification (str): Classification of the service
    """
    __tablename__ = 'service_records'
    
    cnes = Column(Integer, primary_key=True)
    service = Column(Integer, ForeignKey('medical_services.id'))
    classification = Column(String)
    
    medical_service = relationship("MedicalService")