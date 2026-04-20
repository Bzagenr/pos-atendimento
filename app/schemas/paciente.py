from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PacienteCreate(BaseModel):
    nome: str
    telefone: str
    consentimentoLGPD: bool = False

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    consentimentoLGPD: Optional[bool] = None

class PacienteResponse(BaseModel):
    idPaciente: int
    nome: str
    telefone: str
    consentimentoLGPD: bool
    dataConsentimento: Optional[datetime] = None

    class Config:
        from_attributes = True
