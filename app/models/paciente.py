from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, BigInteger
from app.database import Base

class Paciente(Base):
    __tablename__ = "paciente"

    idPaciente        = Column(Integer, primary_key=True, index=True)
    nome              = Column(String(150), nullable=False)
    telefone          = Column(String(20), nullable=False)
    cpf               = Column(String(14), nullable=True, unique=True)
    dataNascimento    = Column(Date, nullable=True)
    telegramChatId    = Column(BigInteger, nullable=True)
    consentimentoLGPD = Column(Boolean, nullable=False, default=False)
    dataConsentimento = Column(DateTime, nullable=True)