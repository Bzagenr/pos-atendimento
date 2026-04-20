from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Medico(Base):
    __tablename__ = "medico"

    idMedico = Column(Integer, primary_key=True, index=True)
    nome     = Column(String(150), nullable=False)

    consultas = relationship("Consulta", back_populates="medico")


class Local(Base):
    __tablename__ = "local"

    idLocal = Column(Integer, primary_key=True, index=True)
    nome    = Column(String(150), nullable=False)

    consultas = relationship("Consulta", back_populates="local")


class Consulta(Base):
    __tablename__ = "consulta"

    idConsulta   = Column(Integer, primary_key=True, index=True)
    idPaciente   = Column(Integer, ForeignKey("paciente.idPaciente"), nullable=False)
    idLocal      = Column(Integer, ForeignKey("local.idLocal"), nullable=False)
    idMedico     = Column(Integer, ForeignKey("medico.idMedico"), nullable=False)
    data         = Column(DateTime, nullable=False)
    hashAtestado = Column(String(255), nullable=True)
    status       = Column(
        Enum("pendente", "em_andamento", "finalizada", name="status_consulta"),
        nullable=False,
        default="pendente"
    )

    medico     = relationship("Medico", back_populates="consultas")
    local      = relationship("Local", back_populates="consultas")
    paciente   = relationship("Paciente", foreign_keys=[idPaciente])
    orientacao = relationship("Orientacao", back_populates="consulta", uselist=False)
