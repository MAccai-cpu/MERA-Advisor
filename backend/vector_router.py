"""
Módulo: backend/vector_router.py
Descripción: Endpoints en FastAPI para la gestión de pgvector y búsqueda semántica.
Proyecto: MERA Advisor
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.vector_service import inicializar_pgvector, insertar_documento_vectorial, buscar_similitud_conocimiento

router = APIRouter(prefix="/vector", tags=["Búsqueda Vectorial pgvector"])

class VectorInsertRequest(BaseModel):
    capa: str
    contenido: str
    vector: List[float]

class VectorSearchRequest(BaseModel):
    vector_consulta: List[float]
    limite: int = 3

@router.post("/inicializar")
def api_inicializar_vector():
    """Endpoint para habilitar la extensión pgvector y crear la tabla en PostgreSQL."""
    try:
        inicializar_pgvector()
        return {"mensaje": "Extensión pgvector y tabla inicializadas correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insertar")
def api_insertar_vector(data: VectorInsertRequest):
    """Endpoint para guardar un fragmento de conocimiento y su embedding."""
    try:
        insertar_documento_vectorial(data.capa, data.contenido, data.vector)
        return {"mensaje": "Documento vectorizado insertado con éxito."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buscar")
def api_buscar_vector(data: VectorSearchRequest):
    """Endpoint para realizar una búsqueda por similitud de coseno en PostgreSQL."""
    try:
        resultados = buscar_similitud_conocimiento(data.vector_consulta, data.limite)
        return {"resultados_similitud": resultados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))