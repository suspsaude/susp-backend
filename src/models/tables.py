from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint

Base = declarative_base()


class GeneralInfo(Base):
    """
    Informações gerais sobre um estabelecimento de saúde.

    Args:
        cnes (Integer): Código CNES
        name (String): Nome fantasia do estabelecimento
        city (String): Cidade onde o estabelecimento está localizado - Opcional (filtra para SP)
        state (String): Estado onde o estabelecimento está localizado - Opcional (filtra para SP)
        kind (String): Tipo de estabelecimento (TIPO NOVO DO ESTABELECIMENTO)
        cep (String): CEP do estabelecimento
        cnpj (String): CNPJ do estabelecimento
        address (String): Endereço do estabelecimento
        number (String): Número do endereço do estabelecimento
        district (String): Bairro do estabelecimento
        telephone (String): Telefone do estabelecimento
        latitude (Float): Latitude do estabelecimento (latitude_estabelecimento_decimo_grau)
        longitude (Float): Longitude do estabelecimento (longitude_estabelecimento_decimo_grau)
        email (String): Endereço de e-mail do estabelecimento
        shift (String): Turno de atendimento do estabelecimento (descricao_turno_atendimento)
    """

    __tablename__ = "general_infos"

    cnes = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    kind = Column(String)
    cep = Column(String)
    cnpj = Column(String)
    address = Column(String)
    number = Column(String)
    district = Column(String)
    telephone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    email = Column(String)
    shift = Column(String)


class MedicalService(Base):
    """
    Descrições de serviço médico e sua classificação.

    Args:
        id (Integer): ID 'SERVIÇO' da API do CNES
        class_id (Integer): ID 'SERVIÇO CLASSIFICAÇÃO' da API do CNES
        service (String): descrição 'SERVIÇO'
        classification (String): descrição 'SERVIÇO CLASSIFICAÇÃO'
    """

    __tablename__ = "medical_services"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, primary_key=True)
    service = Column(String)
    classification = Column(String)


class ServiceRecord(Base):
    """
    Registros de serviços oferecidos por um estabelecimento de saúde.

    Args:
        cnes (Integer): código CNES
        service (Integer): ID do serviço fornecido pelo estabelecimento (chave estrangeira para MedicalService)
        description (String): descrição do serviço
        classification (String): classificação do serviço
    """

    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnes = Column(Integer)
    service = Column(Integer)
    classification = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["service", "classification"],
            ["medical_services.id", "medical_services.class_id"],
        ),
    )
    medical_service = relationship("MedicalService")
