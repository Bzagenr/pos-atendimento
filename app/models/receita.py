from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Medicamento(Base):
    __tablename__ = "medicamento"

    idMedicamento   = Column(Integer, primary_key=True, index=True)
    nomeMedicamento = Column(String(200), nullable=False)

    medicamento_receitas = relationship("MedicamentoReceita", back_populates="medicamento")


class Receita(Base):
    __tablename__ = "receita"

    idReceita  = Column(Integer, primary_key=True, index=True)
    idConsulta = Column(Integer, ForeignKey("consulta.idConsulta"), nullable=False)
    hash       = Column(String(255), nullable=True)

    consulta             = relationship("Consulta", foreign_keys=[idConsulta])
    medicamentos = relationship("MedicamentoReceita", back_populates="receita")


class MedicamentoReceita(Base):
    __tablename__ = "medicamentoreceita"

    idMedicamentoReceita = Column(Integer, primary_key=True, index=True)
    idReceita            = Column(Integer, ForeignKey("receita.idReceita"), nullable=False)
    idMedicamento        = Column(Integer, ForeignKey("medicamento.idMedicamento"), nullable=False)
    dosagem              = Column(String(100), nullable=True)
    frequencia           = Column(String(100), nullable=True)
    duracaoDias          = Column(Integer, nullable=True)
    observacao           = Column(Text, nullable=True)

    receita = relationship("Receita", back_populates="medicamentos")
    medicamento  = relationship("Medicamento", back_populates="medicamento_receitas")
