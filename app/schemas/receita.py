from pydantic import BaseModel
from typing import Optional, List


# ── Medicamento ──────────────────────────────────────────────────────────────
class MedicamentoCreate(BaseModel):
    nomeMedicamento: str

class MedicamentoResponse(BaseModel):
    idMedicamento: int
    nomeMedicamento: str

    class Config:
        from_attributes = True


# ── MedicamentoReceita ───────────────────────────────────────────────────────
class MedicamentoReceitaCreate(BaseModel):
    idMedicamento: int
    dosagem: Optional[str] = None
    frequencia: Optional[str] = None
    duracaoDias: Optional[int] = None
    observacao: Optional[str] = None

class MedicamentoReceitaResponse(BaseModel):
    idMedicamentoReceita: int
    idReceita: int
    idMedicamento: int
    dosagem: Optional[str] = None
    frequencia: Optional[str] = None
    duracaoDias: Optional[int] = None
    observacao: Optional[str] = None

    class Config:
        from_attributes = True


# ── Receita ──────────────────────────────────────────────────────────────────
class ReceitaCreate(BaseModel):
    idConsulta: int
    hash: Optional[str] = None
    medicamentos: List[MedicamentoReceitaCreate] = []

class ReceitaResponse(BaseModel):
    idReceita: int
    idConsulta: int
    hash: Optional[str] = None
    medicamentos: List[MedicamentoReceitaResponse] = []

    class Config:
        from_attributes = True
        populate_by_name = True