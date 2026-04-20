from sqlalchemy import Column, Integer, Date, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
 
 
class OrientacaoPadrao(Base):
    __tablename__ = "orientacaopadrao"
 
    idOrientacaoPadrao  = Column(Integer, primary_key=True, index=True)
    idTipoDoenca        = Column(Integer, ForeignKey("tipodoenca.idTipoDoenca"), nullable=True)
    descricao           = Column(Text, nullable=False)
    diasRetornoPadrao   = Column(Integer, nullable=True)
    exigeAcompanhamento = Column(Boolean, nullable=False, default=False)
 
    tipo_doenca = relationship("TipoDoenca", back_populates="orientacoes_padrao")
    orientacoes = relationship("Orientacao", back_populates="orientacao_padrao")
 
 
class Orientacao(Base):
    __tablename__ = "orientacao"
 
    idOrientacao        = Column(Integer, primary_key=True, index=True)
    idConsulta          = Column(Integer, ForeignKey("consulta.idConsulta"), nullable=False)
    idOrientacaoPadrao  = Column(Integer, ForeignKey("orientacaopadrao.idOrientacaoPadrao"), nullable=True)
    descricao           = Column(Text, nullable=False)
    dataRetorno         = Column(Date, nullable=True)
    exigeAcompanhamento = Column(Boolean, nullable=False, default=False)
 
    consulta          = relationship("Consulta", back_populates="orientacao")
    orientacao_padrao = relationship("OrientacaoPadrao", back_populates="orientacoes")
 