from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.orientacao import Orientacao, OrientacaoPadrao
from app.schemas.orientacao import OrientacaoCreate, OrientacaoUpdate, OrientacaoResponse

router = APIRouter(tags=["Orientações"])


@router.post("/orientacoes/", response_model=OrientacaoResponse, status_code=201)
def criar_orientacao(dados: OrientacaoCreate, db: Session = Depends(get_db)):
    orientacao = Orientacao(
        idConsulta=dados.idConsulta,
        idOrientacaoPadrao=dados.idOrientacaoPadrao,
        descricao=dados.descricao,
        dataRetorno=dados.dataRetorno,
        exigeAcompanhamento=dados.exigeAcompanhamento
    )
    db.add(orientacao)
    db.commit()
    db.refresh(orientacao)
    return orientacao


@router.get("/orientacoes/consulta/{idConsulta}", response_model=OrientacaoResponse)
def buscar_orientacao_por_consulta(idConsulta: int, db: Session = Depends(get_db)):
    orientacao = db.query(Orientacao).filter(Orientacao.idConsulta == idConsulta).first()
    if not orientacao:
        raise HTTPException(status_code=404, detail="Orientação não encontrada")
    return orientacao


@router.patch("/orientacoes/{id}", response_model=OrientacaoResponse)
def atualizar_orientacao(id: int, dados: OrientacaoUpdate, db: Session = Depends(get_db)):
    orientacao = db.query(Orientacao).filter(Orientacao.idOrientacao == id).first()
    if not orientacao:
        raise HTTPException(status_code=404, detail="Orientação não encontrada")

    if dados.descricao is not None:
        orientacao.descricao = dados.descricao
    if dados.dataRetorno is not None:
        orientacao.dataRetorno = dados.dataRetorno
    if dados.exigeAcompanhamento is not None:
        orientacao.exigeAcompanhamento = dados.exigeAcompanhamento

    db.commit()
    db.refresh(orientacao)
    return orientacao


@router.get("/orientacoes-padrao/", response_model=List[dict])
def listar_orientacoes_padrao(idTipoDoenca: int = None, db: Session = Depends(get_db)):
    query = db.query(OrientacaoPadrao)
    if idTipoDoenca:
        query = query.filter(OrientacaoPadrao.idTipoDoenca == idTipoDoenca)
    return [
        {
            "idOrientacaoPadrao": o.idOrientacaoPadrao,
            "idTipoDoenca": o.idTipoDoenca,
            "descricao": o.descricao,
            "diasRetornoPadrao": o.diasRetornoPadrao,
            "exigeAcompanhamento": o.exigeAcompanhamento
        }
        for o in query.all()
    ]
