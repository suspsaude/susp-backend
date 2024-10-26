from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base()

class GeneralInfo(Base):
    """GeneralInfo for a given CNES.
    
    Args:
        cnes (Integer): CNES code
        name (String): Fantasy name of the establishment
        city (String): City where the establishment is located - Optional (filters to SP)
        state (String): State where the establishment is located - Optional (filters to SP)
        kind (String): Kind of establishment (TIPO NOVO DO ESTABELECIMENTO)
        cep (String): CEP of the establishment
        cnpj (String): CNPJ of the establishment
        address (String): Address of the establishment
        number (String): Address number of the establishment
        district (String): District of the establishment
        telephone (String): Telephone of the establishment
        latitude (Float): Latitude of the establishment (latitude_estabelecimento_decimo_grau)
        longitude (Float): Longitude of the establishment (longitude_estabelecimento_decimo_grau)
        email (String): e-mail address of the establishment
        shift (String): Establishment shift (descricao_turno_atendimento)
    """
    __tablename__='general_infos'

    cnes=Column(Integer, primary_key=True)
    name=Column(String)
    city=Column(String)
    state=Column(String)
    kind=Column(String)
    cep=Column(String)
    cnpj=Column(String) 
    address=Column(String)
    number=Column(String)
    district=Column(String)
    telephone=Column(String)
    latitude=Column(Float)
    longitude=Column(Float)
    email=Column(String)
    shift=Column(String)
    
class MedicalService(Base):
    """MedicalService for a type of service.

    Args:
        id (Integer): Medical service id
        name (String): Description of the medical expertise
    """
    __tablename__='medical_services'

    id=Column(Integer, primary_key=True)
    name=Column(String)

class ServiceRecord(Base):
    """ServiceRecord for a given CNES.
    
    Args:
        cnes (Integer): CNES code
        service (Integer): ID of the service provided by the establishment (foreign key to MedicalService)
        description (String): Service description
        classification (String): Classification of the service
    """
    __tablename__='service_records'
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    cnes=Column(Integer)
    service=Column(Integer, ForeignKey('medical_services.id'))
    #description=Column(String)
    classification=Column(String)
    
    medical_service=relationship("MedicalService")