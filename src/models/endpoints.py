from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExpertiseItem(BaseModel):
    id: List[int]
    name: str


class UnitRequest(BaseModel):
    cep: str = Field(
        ..., pattern=r"^\d{5}-?\d{3}$", description="CEP no formato 00000-000"
    )
    srv: int = Field(..., description="Serviço médico")
    clf: int = Field(..., description="Classificação da especialidade")


# Making stuff Optional to be more error-tolerant
class UnitItem(BaseModel):
    cnes: int
    name: Optional[str]
    address: Optional[str]
    type: Optional[str]
    distance: Optional[float]


# Making stuff Optional to be more error-tolerant
class DetailsResponse(BaseModel):
    cnes: int
    name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    kind: Optional[str]
    cep: Optional[str]
    cnpj: Optional[str]
    address: Optional[str]
    number: Optional[str]
    district: Optional[str]
    telephone: Optional[str]
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    email: Optional[str]
    shift: Optional[str]
    services: Optional[Dict[str, List[str]]]
