from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.receita import Receita, Medicamento, MedicamentoReceita
from app.schemas.receita import (
    ReceitaCreate, ReceitaResponse,
    MedicamentoCreate, MedicamentoResponse
)

router = APIRouter(tags=["Receitas"])


# ── Medicamento ──────────────────────────────────────────────────────────────
@router.post("/medicamentos/", response_model=MedicamentoResponse, status_code=201)
def criar_medicamento(dados: MedicamentoCreate, db: Session = Depends(get_db)):
    medicamento = Medicamento(nomeMedicamento=dados.nomeMedicamento)
    db.add(medicamento)
    db.commit()
    db.refresh(medicamento)
    return medicamento


@router.get("/medicamentos/", response_model=List[MedicamentoResponse])
def listar_medicamentos(db: Session = Depends(get_db)):
    return db.query(Medicamento).all()


# ── Receita ──────────────────────────────────────────────────────────────────
@router.post("/receitas/", response_model=ReceitaResponse, status_code=201)
def criar_receita(dados: ReceitaCreate, db: Session = Depends(get_db)):
    receita = Receita(
        idConsulta=dados.idConsulta,
        hash=dados.hash
    )
    db.add(receita)
    db.flush()  # gera o idReceita sem commitar ainda

    for item in dados.medicamentos:
        med_receita = MedicamentoReceita(
            idReceita=receita.idReceita,
            idMedicamento=item.idMedicamento,
            dosagem=item.dosagem,
            frequencia=item.frequencia,
            duracaoDias=item.duracaoDias,
            observacao=item.observacao
        )
        db.add(med_receita)

    db.commit()
    db.refresh(receita)
    return receita


@router.get("/receitas/{id}", response_model=ReceitaResponse)
def buscar_receita(id: int, db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.idReceita == id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita


@router.get("/receitas/consulta/{idConsulta}", response_model=ReceitaResponse)
def buscar_receita_por_consulta(idConsulta: int, db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.idConsulta == idConsulta).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada para esta consulta")
    return receita
