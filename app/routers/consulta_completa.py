from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.paciente import Paciente
from app.models.consulta import Consulta
from app.models.orientacao import Orientacao
from app.models.receita import Receita, MedicamentoReceita, Medicamento
from app.models.consulta import Medico, Local

router = APIRouter(tags=["Consulta Completa"])


@router.get("/paciente/{cpf}/ultima-consulta")
def ultima_consulta_por_cpf(cpf: str, dataNascimento: str = None, db: Session = Depends(get_db)):
    # Busca o paciente pelo CPF
    paciente = db.query(Paciente).filter(Paciente.cpf == cpf).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Valida data de nascimento se informada
    if dataNascimento and paciente.dataNascimento:
        from datetime import date
        data_informada = date.fromisoformat(dataNascimento)
        if data_informada != paciente.dataNascimento:
            raise HTTPException(status_code=404, detail="CPF ou data de nascimento não conferem")
    # Busca a consulta mais recente finalizada
    consultas = (
        db.query(Consulta)
        .filter(
            Consulta.idPaciente == paciente.idPaciente,
            Consulta.status == "finalizada"
        )
        .order_by(Consulta.data.desc())
        .all()
    )

    if not consultas:
        raise HTTPException(status_code=404, detail="Nenhuma consulta finalizada encontrada")

    # Se houver mais de uma consulta, retorna lista para o paciente escolher
    if len(consultas) > 1:
        return {
            "multiplas_consultas": True,
            "mensagem": "Encontrei mais de uma consulta recente. Qual deseja acompanhar?",
            "consultas": [
                {
                    "idConsulta": c.idConsulta,
                    "data": c.data.strftime("%d/%m/%Y"),
                    "medico": db.query(Medico).filter(Medico.idMedico == c.idMedico).first().nome,
                    "local": db.query(Local).filter(Local.idLocal == c.idLocal).first().nome,
                }
                for c in consultas
            ]
        }

    consulta = consultas[0]

    # Busca médico e local
    medico = db.query(Medico).filter(Medico.idMedico == consulta.idMedico).first()
    local  = db.query(Local).filter(Local.idLocal == consulta.idLocal).first()

    # Busca orientação
    orientacao = db.query(Orientacao).filter(
        Orientacao.idConsulta == consulta.idConsulta
    ).first()

    # Busca receita e medicamentos
    receita = db.query(Receita).filter(
        Receita.idConsulta == consulta.idConsulta
    ).first()

    medicamentos = []
    if receita:
        itens = db.query(MedicamentoReceita).filter(
            MedicamentoReceita.idReceita == receita.idReceita
        ).all()
        for item in itens:
            med = db.query(Medicamento).filter(
                Medicamento.idMedicamento == item.idMedicamento
            ).first()
            medicamentos.append({
                "nome": med.nomeMedicamento if med else "Desconhecido",
                "dosagem": item.dosagem,
                "frequencia": item.frequencia,
                "duracaoDias": item.duracaoDias,
                "observacao": item.observacao
            })

    return {
        "multiplas_consultas": False,
        "paciente": {
            "nome": paciente.nome,
            "telefone": paciente.telefone
        },
        "consulta": {
            "idConsulta": consulta.idConsulta,
            "data": consulta.data.strftime("%d/%m/%Y"),
            "medico": medico.nome if medico else None,
            "local": local.nome if local else None,
        },
        "orientacao": {
            "descricao": orientacao.descricao if orientacao else None,
            "dataRetorno": orientacao.dataRetorno.strftime("%d/%m/%Y") if orientacao and orientacao.dataRetorno else None,
            "exigeAcompanhamento": orientacao.exigeAcompanhamento if orientacao else False
        },
        "receita": {
            "possui_receita": receita is not None,
            "medicamentos": medicamentos
        }
    }


@router.get("/paciente/{cpf}/consulta/{idConsulta}")
def consulta_por_id(cpf: str, idConsulta: int, db: Session = Depends(get_db)):
    # Busca o paciente pelo CPF
    paciente = db.query(Paciente).filter(Paciente.cpf == cpf).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Busca a consulta específica
    consulta = db.query(Consulta).filter(
        Consulta.idConsulta == idConsulta,
        Consulta.idPaciente == paciente.idPaciente
    ).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    medico = db.query(Medico).filter(Medico.idMedico == consulta.idMedico).first()
    local  = db.query(Local).filter(Local.idLocal == consulta.idLocal).first()

    orientacao = db.query(Orientacao).filter(
        Orientacao.idConsulta == consulta.idConsulta
    ).first()

    receita = db.query(Receita).filter(
        Receita.idConsulta == consulta.idConsulta
    ).first()

    medicamentos = []
    if receita:
        itens = db.query(MedicamentoReceita).filter(
            MedicamentoReceita.idReceita == receita.idReceita
        ).all()
        for item in itens:
            med = db.query(Medicamento).filter(
                Medicamento.idMedicamento == item.idMedicamento
            ).first()
            medicamentos.append({
                "nome": med.nomeMedicamento if med else "Desconhecido",
                "dosagem": item.dosagem,
                "frequencia": item.frequencia,
                "duracaoDias": item.duracaoDias,
                "observacao": item.observacao
            })

    return {
        "paciente": {
            "nome": paciente.nome,
            "telefone": paciente.telefone
        },
        "consulta": {
            "idConsulta": consulta.idConsulta,
            "data": consulta.data.strftime("%d/%m/%Y"),
            "medico": medico.nome if medico else None,
            "local": local.nome if local else None,
        },
        "orientacao": {
            "descricao": orientacao.descricao if orientacao else None,
            "dataRetorno": orientacao.dataRetorno.strftime("%d/%m/%Y") if orientacao and orientacao.dataRetorno else None,
            "exigeAcompanhamento": orientacao.exigeAcompanhamento if orientacao else False
        },
        "receita": {
            "possui_receita": receita is not None,
            "medicamentos": medicamentos
        }
    }
