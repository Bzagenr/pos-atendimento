from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class CanalMensagem(str, Enum):
    whatsapp = "whatsapp"
    sms      = "sms"
    email    = "email"
    link     = "link"


class StatusMensagem(str, Enum):
    agendada = "agendada"
    enviada  = "enviada"
    falha    = "falha"


# ── TipoMensagem ─────────────────────────────────────────────────────────────
class TipoMensagemCreate(BaseModel):
    nome: str
    template: str
    aceitaResposta: bool = False

class TipoMensagemResponse(BaseModel):
    idTipoMensagem: int
    nome: str
    template: str
    aceitaResposta: bool

    class Config:
        from_attributes = True


# ── OpcaoResposta ─────────────────────────────────────────────────────────────
class OpcaoRespostaCreate(BaseModel):
    idTipoMensagem: int
    descricao: str
    ordem: int = 1

class OpcaoRespostaResponse(BaseModel):
    idOpcaoResposta: int
    idTipoMensagem: int
    descricao: str
    ordem: int

    class Config:
        from_attributes = True


# ── MensagemAcompanhamento ────────────────────────────────────────────────────
class MensagemCreate(BaseModel):
    idOrientacao: int
    idTipoMensagem: int
    canal: CanalMensagem = CanalMensagem.whatsapp
    dataAgendada: datetime

class MensagemUpdateStatus(BaseModel):
    status: StatusMensagem
    dataEnvio: Optional[datetime] = None

class MensagemResponse(BaseModel):
    idMensagem: int
    idOrientacao: int
    idTipoMensagem: int
    canal: CanalMensagem
    dataAgendada: datetime
    dataEnvio: Optional[datetime] = None
    status: StatusMensagem

    class Config:
        from_attributes = True


# ── RespostaAcompanhamento ────────────────────────────────────────────────────
class RespostaCreate(BaseModel):
    idMensagem: int
    idOpcaoResposta: int
    dataResposta: datetime

class RespostaResponse(BaseModel):
    idResposta: int
    idMensagem: int
    idOpcaoResposta: int
    dataResposta: datetime

    class Config:
        from_attributes = True


# ── Webhook ManyChat ──────────────────────────────────────────────────────────
class WebhookManyChat(BaseModel):
    telefone: str
    idMensagem: int
    idOpcaoResposta: int
