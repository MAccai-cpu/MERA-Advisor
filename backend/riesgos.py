from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-d", tags=["Capa D - Riesgos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RiesgoSchema(BaseModel):
    factor: str
    impacto: str
    vulnerabilidad_critica: Optional[bool] = False
    saturacion_ruta: Optional[bool] = False

@router.post("/evaluar")
def registrar_riesgo(riesgo: RiesgoSchema, db: Session = Depends(get_db)):
    # 1. Ejecutar motor cognitivo
    datos_evaluacion = {
        "vulnerabilidad_critica": riesgo.vulnerabilidad_critica,
        "saturacion_ruta": riesgo.saturacion_ruta
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Sincronización en Neo4j
    driver = get_driver()
    with driver.session() as session:
        query = """
        MERGE (r:Riesgo {factor: $factor})
        ON CREATE SET r.impacto = $impacto
        """
        session.run(query, factor=riesgo.factor, impacto=riesgo.impacto)

        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (r:Riesgo {factor: $factor})
            MERGE (ax:AxiomaRegla {id_regla: $id_regla})
            MERGE (r)-[:ACTIVA_RIESGO]->(ax)
            """
            session.run(query_regla, factor=riesgo.factor, id_regla=regla["regla"])

    return {
        "mensaje": "Riesgo evaluado y sincronizado en el motor cognitivo",
        "riesgo": {"factor": riesgo.factor, "impacto": riesgo.impacto},
        "analisis_cognitivo": resultado_cognitivo
    }