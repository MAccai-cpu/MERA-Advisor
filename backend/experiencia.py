from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-f", tags=["Capa F - Experiencia"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ExperienciaSchema(BaseModel):
    id_caso: str
    resultado_historico: str
    vulnerabilidad_critica: Optional[bool] = False

@router.post("/registrar")
def registrar_experiencia(exp: ExperienciaSchema, db: Session = Depends(get_db)):
    # 1. Ejecución del motor cognitivo
    datos_evaluacion = {
        "vulnerabilidad_critica": exp.vulnerabilidad_critica
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Sincronización en Neo4j
    driver = get_driver()
    with driver.session() as session:
        query = """
        MERGE (e:ExperienciaCaso {id_caso: $id_caso})
        ON CREATE SET e.resultado = $resultado
        """
        session.run(query, id_caso=exp.id_caso, resultado=exp.resultado_historico)

        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (e:ExperienciaCaso {id_caso: $id_caso})
            MERGE (r:AxiomaRegla {id_regla: $id_regla})
            MERGE (e)-[:APRENDIZAJE_DE]->(r)
            """
            session.run(query_regla, id_caso=exp.id_caso, id_regla=regla["regla"])

    return {
        "mensaje": "Experiencia registrada y procesada por el motor cognitivo",
        "experiencia": {"caso": exp.id_caso, "resultado": exp.resultado_historico},
        "analisis_cognitivo": resultado_cognitivo
    }