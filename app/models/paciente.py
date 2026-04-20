from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class Paciente(Base):
    __tablename__ = "paciente"

    idPaciente        = Column(Integer, primary_key=True, index=True)
    nome              = Column(String(150), nullable=False)
    telefone          = Column(String(20), nullable=False)
    consentimentoLGPD = Column(Boolean, nullable=False, default=False)
    dataConsentimento = Column(DateTime, nullable=True)
