import enum

from pydantic import BaseModel


class State(enum.Enum):
    UT = "UT"
    NV = "NV"
    TX = "TX"
    AL = "AL"
    CA = "CA"


class InCalculateQuery(BaseModel):
    count: int
    price: float
    state: State


class OutCalculateQuery(BaseModel):
    calculated_price: float
