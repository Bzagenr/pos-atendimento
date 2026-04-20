from pydantic import BaseModel
from datetime import date
from typing import Optional


class OrientacaoCreate(BaseModel):
    idConsulta: int
    idOrientacaoPadrao: Optional[int] = None
    descricao: str
    dataRetorno: Optional[date] = None
    exigeAcompanhamento: bool = False

class OrientacaoUpdate(BaseModel):
    descricao: Optional[str] = None
    dataRetorno: Optional[date] = None
    exigeAcompanhamento: Optional[bool] = None

class OrientacaoResponse(BaseModel):
    idOrientacao: int
    idConsulta: int
    idOrientacaoPadrao: Optional[int] = None
    descricao: str
    dataRetorno: Optional[date] = None
    exigeAcompanhamento: bool

    class Config:
        from_attributes = True
