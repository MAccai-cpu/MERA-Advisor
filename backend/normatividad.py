from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-e", tags=["Capa E - Normatividad"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NormatividadSchema(BaseModel):
    ley_o_norma: str
    entidad_emisora: str
    restriccion_regulatoria: Optional[bool] = True

@router.post("/validar")
def validar_normatividad(norma: NormatividadSchema, db: Session = Depends(get_db)):
    # 1. Ejecución del motor cognitivo
    datos_evaluacion = {
        "restriccion_regulatoria": norma.restriccion_regulatoria
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Sincronización en Neo4j
    driver = get_driver()
    with driver.session() as session:
        query = """
        MERGE (n:Normatividad {nombre: $nombre})
        ON CREATE SET n.entidad = $entidad
        """
        session.run(query, nombre=norma.ley_o_norma, entidad=norma.entidad_emisora)

        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (n:Normatividad {nombre: $nombre})
            MERGE (r:AxiomaRegla {id_regla: $id_regla})
            MERGE (n)-[:aplica_norma]->(r)
            """
            session.run(query_regla, nombre=norma.ley_o_norma, id_regla=regla["regla"])

    return {
        "mensaje": "Normatividad validada y mapeada en el grafo",
        "normatividad": {"norma": norma.ley_o_norma, "entidad": norma.entidad_emisora},
        "analisis_cognitivo": resultado_cognitivo
    }