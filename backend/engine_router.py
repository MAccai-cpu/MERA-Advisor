"""
Módulo: backend/engine_router.py
Descripción: Endpoint REST para ejecutar el motor de razonamiento axiomático (ANA).
Proyecto: MERA Advisor
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.engine import mera_engine

router = APIRouter(prefix="/engine", tags=["Motor de Razonamiento ANA"])

class EvaluacionRequest(BaseModel):
    datos_entrada: Dict[str, Any]

@router.post("/evaluar")
def evaluar_caso_logistico(request: EvaluacionRequest):
    """
    Ejecuta el motor analítico ANA evaluando las reglas y axiomas vigentes 
    en función de los datos de la operación logística ingresados.
    """
    try:
        resultado = mera_engine.procesar_evaluacion(request.datos_entrada)
        return {
            "mensaje": "Evaluación ejecutada exitosamente por el Motor ANA",
            "resultado": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el motor de razonamiento: {str(e)}")