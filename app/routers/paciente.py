from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteResponse

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteResponse, status_code=201)
def criar_paciente(dados: PacienteCreate, db: Session = Depends(get_db)):
    paciente = Paciente(
        nome=dados.nome,
        telefone=dados.telefone,
        consentimentoLGPD=dados.consentimentoLGPD,
        dataConsentimento=datetime.now() if dados.consentimentoLGPD else None
    )
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()


@router.get("/{id}", response_model=PacienteResponse)
def buscar_paciente(id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.idPaciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.get("/telefone/{telefone}", response_model=PacienteResponse)
def buscar_por_telefone(telefone: str, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.telefone == telefone).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.patch("/{id}", response_model=PacienteResponse)
def atualizar_paciente(id: int, dados: PacienteUpdate, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.idPaciente == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    if dados.nome is not None:
        paciente.nome = dados.nome
    if dados.cpf is not None: 
        paciente.cpf = dados.cpf
    if dados.telefone is not None:
        paciente.telefone = dados.telefone
    if dados.consentimentoLGPD is not None:
        paciente.consentimentoLGPD = dados.consentimentoLGPD
        if dados.consentimentoLGPD and not paciente.dataConsentimento:
            paciente.dataConsentimento = datetime.now()

    db.commit()
    db.refresh(paciente)
    return paciente
