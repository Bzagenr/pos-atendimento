from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class TipoDoenca(Base):
    __tablename__ = "tipodoenca"

    idTipoDoenca = Column(Integer, primary_key=True, index=True)
    nome         = Column(String(150), nullable=False)

    orientacoes_padrao = relationship("OrientacaoPadrao", back_populates="tipo_doenca")
