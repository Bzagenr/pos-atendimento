from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models.acompanhamento import (
    TipoMensagem, OpcaoResposta,
    MensagemAcompanhamento, RespostaAcompanhamento
)
from app.models.paciente import Paciente
from app.schemas.acompanhamento import (
    TipoMensagemCreate, TipoMensagemResponse,
    OpcaoRespostaCreate, OpcaoRespostaResponse,
    MensagemCreate, MensagemUpdateStatus, MensagemResponse,
    RespostaCreate, RespostaResponse,
    WebhookManyChat
)

router = APIRouter(tags=["Acompanhamento"])


# ── TipoMensagem ─────────────────────────────────────────────────────────────
@router.post("/tipos-mensagem/", response_model=TipoMensagemResponse, status_code=201)
def criar_tipo_mensagem(dados: TipoMensagemCreate, db: Session = Depends(get_db)):
    tipo = TipoMensagem(
        nome=dados.nome,
        template=dados.template,
        aceitaResposta=dados.aceitaResposta
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.get("/tipos-mensagem/", response_model=List[TipoMensagemResponse])
def listar_tipos_mensagem(db: Session = Depends(get_db)):
    return db.query(TipoMensagem).all()


# ── OpcaoResposta ─────────────────────────────────────────────────────────────
@router.post("/opcoes-resposta/", response_model=OpcaoRespostaResponse, status_code=201)
def criar_opcao_resposta(dados: OpcaoRespostaCreate, db: Session = Depends(get_db)):
    opcao = OpcaoResposta(
        idTipoMensagem=dados.idTipoMensagem,
        descricao=dados.descricao,
        ordem=dados.ordem
    )
    db.add(opcao)
    db.commit()
    db.refresh(opcao)
    return opcao


@router.get("/opcoes-resposta/tipo/{idTipoMensagem}", response_model=List[OpcaoRespostaResponse])
def listar_opcoes_por_tipo(idTipoMensagem: int, db: Session = Depends(get_db)):
    return db.query(OpcaoResposta).filter(
        OpcaoResposta.idTipoMensagem == idTipoMensagem
    ).order_by(OpcaoResposta.ordem).all()


# ── MensagemAcompanhamento ────────────────────────────────────────────────────
@router.post("/mensagens/", response_model=MensagemResponse, status_code=201)
def criar_mensagem(dados: MensagemCreate, db: Session = Depends(get_db)):
    mensagem = MensagemAcompanhamento(
        idOrientacao=dados.idOrientacao,
        idTipoMensagem=dados.idTipoMensagem,
        canal=dados.canal,
        dataAgendada=dados.dataAgendada,
        status="agendada"
    )
    db.add(mensagem)
    db.commit()
    db.refresh(mensagem)
    return mensagem


@router.get("/mensagens/orientacao/{idOrientacao}", response_model=List[MensagemResponse])
def listar_mensagens_por_orientacao(idOrientacao: int, db: Session = Depends(get_db)):
    return db.query(MensagemAcompanhamento).filter(
        MensagemAcompanhamento.idOrientacao == idOrientacao
    ).all()


@router.patch("/mensagens/{id}/status", response_model=MensagemResponse)
def atualizar_status_mensagem(id: int, dados: MensagemUpdateStatus, db: Session = Depends(get_db)):
    mensagem = db.query(MensagemAcompanhamento).filter(
        MensagemAcompanhamento.idMensagem == id
    ).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    mensagem.status = dados.status
    if dados.dataEnvio:
        mensagem.dataEnvio = dados.dataEnvio
    db.commit()
    db.refresh(mensagem)
    return mensagem


# ── RespostaAcompanhamento ────────────────────────────────────────────────────
@router.post("/respostas/", response_model=RespostaResponse, status_code=201)
def criar_resposta(dados: RespostaCreate, db: Session = Depends(get_db)):
    resposta = RespostaAcompanhamento(
        idMensagem=dados.idMensagem,
        idOpcaoResposta=dados.idOpcaoResposta,
        dataResposta=dados.dataResposta
    )
    db.add(resposta)
    db.commit()
    db.refresh(resposta)
    return resposta


# ── Webhook ManyChat ──────────────────────────────────────────────────────────
@router.post("/webhook/manychat", status_code=200)
def webhook_manychat(dados: WebhookManyChat, db: Session = Depends(get_db)):
    """
    Recebe a resposta do paciente via ManyChat.
    O ManyChat envia o telefone, o idMensagem e a opcao escolhida.
    """
    # Verifica se o paciente existe pelo telefone
    paciente = db.query(Paciente).filter(
        Paciente.telefone == dados.telefone
    ).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Verifica se a mensagem existe
    mensagem = db.query(MensagemAcompanhamento).filter(
        MensagemAcompanhamento.idMensagem == dados.idMensagem
    ).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    # Registra a resposta
    resposta = RespostaAcompanhamento(
        idMensagem=dados.idMensagem,
        idOpcaoResposta=dados.idOpcaoResposta,
        dataResposta=datetime.now()
    )
    db.add(resposta)

    # Atualiza status da mensagem para enviada
    mensagem.status = "enviada"
    mensagem.dataEnvio = datetime.now()

    db.commit()
    db.refresh(resposta)

    return {"status": "ok", "idResposta": resposta.idResposta}
