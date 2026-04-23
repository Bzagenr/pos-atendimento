from fastapi import FastAPI
from app.database import Base, engine
from app.routers import paciente, consulta, orientacao, receita

import app.models.paciente
import app.models.consulta
import app.models.orientacao
import app.models.tipodoenca
import app.models.receita

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Pós-Atendimento em Saúde",
    description="API para acompanhamento do paciente após consulta médica",
    version="0.1.0"
)

app.include_router(paciente.router)
app.include_router(consulta.router)
app.include_router(orientacao.router)
app.include_router(receita.router)


@app.get("/")
def root():
    return {"status": "online", "docs": "/docs"}