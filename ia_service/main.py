# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from auth import require_token
import models_sim as sim

app = FastAPI(title="IA-as-a-Service (simulado)", version="1.0")

# --- Request / Response models ---
class PredicaoVendaRequest(BaseModel):
    mes: int = Field(..., ge=1, le=12, example=9)
    ano: int = Field(..., ge=1900, le=3000, example=2025)

class ClassificacaoClienteRequest(BaseModel):
    cpf: str = Field(..., example="123.456.789-09")

class PredicaoDemandaRequest(BaseModel):
    product_id: str = Field(..., example="SKU-9876")
    period: str = Field(..., example="2025-09" ) # or "2025-06:2025-09"

class ClassificacaoSentimentoRequest(BaseModel):
    text: str = Field(..., example="O produto foi ótimo, adorei!")

# --- Endpoints (protegidos) ---
@app.post("/predicaoVenda")
def predicao_venda(req: PredicaoVendaRequest, token: str = Depends(require_token)):
    try:
        result = sim.predicao_venda(req.mes, req.ano)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classificacaoCliente")
def classificacao_cliente(req: ClassificacaoClienteRequest, token: str = Depends(require_token)):
    try:
        result = sim.classificacao_cliente(req.cpf)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predicaoDemanda")
def predicao_demanda(req: PredicaoDemandaRequest, token: str = Depends(require_token)):
    try:
        result = sim.predicao_demanda(req.product_id, req.period)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classificacaoSentimento")
def classificacao_sentimento(req: ClassificacaoSentimentoRequest, token: str = Depends(require_token)):
    try:
        result = sim.classificacao_sentimento(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# rota simples para checar status (também protegida)
@app.get("/health")
def health(token: str = Depends(require_token)):
    return {"status": "ok", "time": __import__("datetime").datetime.utcnow().isoformat() + "Z"}