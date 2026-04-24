from fastapi import FastAPI
from app.database import Base, engine
from app.routers import paciente, consulta, orientacao, receita, acompanhamento, consulta_completa

import app.models.paciente
import app.models.tipodoenca
import app.models.consulta
import app.models.orientacao
import app.models.receita
import app.models.acompanhamento

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Pos-Atendimento em Saude",
    description="API para acompanhamento do paciente apos consulta medica",
    version="0.1.0"
)

app.include_router(paciente.router)
app.include_router(consulta.router)
app.include_router(orientacao.router)
app.include_router(receita.router)
app.include_router(acompanhamento.router)
app.include_router(consulta_completa.router)


@app.get("/")
def root():
    return {"status": "online", "docs": "/docs"}
