from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class PacienteCreate(BaseModel):
    nome: str
    telefone: str
    cpf: Optional[str] = None
    dataNascimento: Optional[date] = None
    consentimentoLGPD: bool = False
    telegramChatId: Optional[int] = None

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    dataNascimento: Optional[date] = None
    consentimentoLGPD: Optional[bool] = None
    telegramChatId: Optional[int] = None

class PacienteResponse(BaseModel):
    idPaciente: int
    nome: str
    telefone: str
    cpf: Optional[str] = None
    dataNascimento: Optional[date] = None
    consentimentoLGPD: bool
    dataConsentimento: Optional[datetime] = None
    telegramChatId: Optional[int] = None

    class Config:
        from_attributes = True