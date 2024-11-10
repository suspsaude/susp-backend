from decimal import Decimal

from pydantic import BaseModel


class Coordinate(BaseModel):
    lat: Decimal
    lng: Decimal

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.lat == other.lat and self.lng == other.lng
        return False
