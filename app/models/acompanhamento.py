from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class TipoMensagem(Base):
    __tablename__ = "tipomensagem"

    idTipoMensagem = Column(Integer, primary_key=True, index=True)
    nome           = Column(String(100), nullable=False)
    template       = Column(Text, nullable=False)
    aceitaResposta = Column(Boolean, nullable=False, default=False)

    opcoes    = relationship("OpcaoResposta", back_populates="tipo_mensagem")
    mensagens = relationship("MensagemAcompanhamento", back_populates="tipo_mensagem")


class OpcaoResposta(Base):
    __tablename__ = "opcaoresposta"

    idOpcaoResposta = Column(Integer, primary_key=True, index=True)
    idTipoMensagem  = Column(Integer, ForeignKey("tipomensagem.idTipoMensagem"), nullable=False)
    descricao       = Column(String(150), nullable=False)
    ordem           = Column(Integer, nullable=False, default=1)

    tipo_mensagem = relationship("TipoMensagem", back_populates="opcoes")
    respostas     = relationship("RespostaAcompanhamento", back_populates="opcao_resposta")


class MensagemAcompanhamento(Base):
    __tablename__ = "mensagemacompanhamento"

    idMensagem     = Column(Integer, primary_key=True, index=True)
    idOrientacao   = Column(Integer, ForeignKey("orientacao.idOrientacao"), nullable=False)
    idTipoMensagem = Column(Integer, ForeignKey("tipomensagem.idTipoMensagem"), nullable=False)
    canal          = Column(
        Enum("whatsapp", "sms", "email", "link", name="canal_mensagem"),
        nullable=False,
        default="whatsapp"
    )
    dataAgendada = Column(DateTime, nullable=False)
    dataEnvio    = Column(DateTime, nullable=True)
    status       = Column(
        Enum("agendada", "enviada", "falha", name="status_mensagem"),
        nullable=False,
        default="agendada"
    )

    orientacao    = relationship("Orientacao", foreign_keys=[idOrientacao])
    tipo_mensagem = relationship("TipoMensagem", back_populates="mensagens")
    respostas     = relationship("RespostaAcompanhamento", back_populates="mensagem")


class RespostaAcompanhamento(Base):
    __tablename__ = "respostaacompanhamento"

    idResposta      = Column(Integer, primary_key=True, index=True)
    idMensagem      = Column(Integer, ForeignKey("mensagemacompanhamento.idMensagem"), nullable=False)
    idOpcaoResposta = Column(Integer, ForeignKey("opcaoresposta.idOpcaoResposta"), nullable=False)
    dataResposta    = Column(DateTime, nullable=False)

    mensagem       = relationship("MensagemAcompanhamento", back_populates="respostas")
    opcao_resposta = relationship("OpcaoResposta", back_populates="respostas")
