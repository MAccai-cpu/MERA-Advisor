from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-c", tags=["Capa C - Operación"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OperacionSchema(BaseModel):
    codigo_operacion: str
    centro_logistico: str
    urgencia_alta: Optional[bool] = False
    saturacion_ruta: Optional[bool] = False

@router.post("/ejecutar")
def registrar_operacion(operacion: OperacionSchema, db: Session = Depends(get_db)):
    # 1. Ejecución del motor cognitivo
    datos_evaluacion = {
        "urgencia_alta": operacion.urgencia_alta,
        "saturacion_ruta": operacion.saturacion_ruta
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Sincronización en Neo4j
    driver = get_driver()
    with driver.session() as session:
        query = """
        MERGE (op:OperacionLogistica {codigo: $codigo})
        ON CREATE SET op.centro = $centro
        """
        session.run(query, codigo=operacion.codigo_operacion, centro=operacion.centro_logistico)

        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (op:OperacionLogistica {codigo: $codigo})
            MERGE (r:AxiomaRegla {id_regla: $id_regla})
            MERGE (op)-[:DISPARA_REGLA]->(r)
            """
            session.run(query_regla, codigo=operacion.codigo_operacion, id_regla=regla["regla"])

    return {
        "mensaje": "Operación registrada y evaluada por el motor cognitivo",
        "operacion": {"codigo": operacion.codigo_operacion, "centro": operacion.centro_logistico},
        "analisis_cognitivo": resultado_cognitivo
    }