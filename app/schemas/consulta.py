from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class StatusConsulta(str, Enum):
    pendente     = "pendente"
    em_andamento = "em_andamento"
    finalizada   = "finalizada"


# ── Medico ──────────────────────────────────────────────────────────────────
class MedicoCreate(BaseModel):
    nome: str

class MedicoResponse(BaseModel):
    idMedico: int
    nome: str

    class Config:
        from_attributes = True


# ── Local ───────────────────────────────────────────────────────────────────
class LocalCreate(BaseModel):
    nome: str

class LocalResponse(BaseModel):
    idLocal: int
    nome: str

    class Config:
        from_attributes = True


# ── Consulta ─────────────────────────────────────────────────────────────────
class ConsultaCreate(BaseModel):
    idPaciente: int
    idLocal: int
    idMedico: int
    data: datetime
    hashAtestado: Optional[str] = None
    status: StatusConsulta = StatusConsulta.pendente

class ConsultaUpdateStatus(BaseModel):
    status: StatusConsulta

class ConsultaResponse(BaseModel):
    idConsulta: int
    idPaciente: int
    idLocal: int
    idMedico: int
    data: datetime
    hashAtestado: Optional[str] = None
    status: StatusConsulta

    class Config:
        from_attributes = True
