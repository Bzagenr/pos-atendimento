from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.consulta import Consulta, Medico, Local
from app.schemas.consulta import (
    ConsultaCreate, ConsultaUpdateStatus, ConsultaResponse,
    MedicoCreate, MedicoResponse,
    LocalCreate, LocalResponse
)

router = APIRouter(tags=["Consultas"])


# ── Medico ──────────────────────────────────────────────────────────────────
@router.post("/medicos/", response_model=MedicoResponse, status_code=201)
def criar_medico(dados: MedicoCreate, db: Session = Depends(get_db)):
    medico = Medico(nome=dados.nome)
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico


@router.get("/medicos/", response_model=List[MedicoResponse])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(Medico).all()


# ── Local ───────────────────────────────────────────────────────────────────
@router.post("/locais/", response_model=LocalResponse, status_code=201)
def criar_local(dados: LocalCreate, db: Session = Depends(get_db)):
    local = Local(nome=dados.nome)
    db.add(local)
    db.commit()
    db.refresh(local)
    return local


@router.get("/locais/", response_model=List[LocalResponse])
def listar_locais(db: Session = Depends(get_db)):
    return db.query(Local).all()


# ── Consulta ─────────────────────────────────────────────────────────────────
@router.post("/consultas/", response_model=ConsultaResponse, status_code=201)
def criar_consulta(dados: ConsultaCreate, db: Session = Depends(get_db)):
    consulta = Consulta(
        idPaciente=dados.idPaciente,
        idLocal=dados.idLocal,
        idMedico=dados.idMedico,
        data=dados.data,
        hashAtestado=dados.hashAtestado,
        status=dados.status
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


@router.get("/consultas/", response_model=List[ConsultaResponse])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(Consulta).all()


@router.get("/consultas/{id}", response_model=ConsultaResponse)
def buscar_consulta(id: int, db: Session = Depends(get_db)):
    consulta = db.query(Consulta).filter(Consulta.idConsulta == id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta


@router.get("/consultas/paciente/{idPaciente}", response_model=List[ConsultaResponse])
def consultas_por_paciente(idPaciente: int, db: Session = Depends(get_db)):
    return db.query(Consulta).filter(Consulta.idPaciente == idPaciente).all()


@router.patch("/consultas/{id}/status", response_model=ConsultaResponse)
def atualizar_status(id: int, dados: ConsultaUpdateStatus, db: Session = Depends(get_db)):
    consulta = db.query(Consulta).filter(Consulta.idConsulta == id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    consulta.status = dados.status
    db.commit()
    db.refresh(consulta)
    return consulta
