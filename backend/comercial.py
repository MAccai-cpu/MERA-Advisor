from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver
from backend.models import PoliticaComercialModel  # Asegúrate de tener tu modelo en models.py o ajústalo según corresponda
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-a", tags=["Capa A - Comercial"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ComercialSchema(BaseModel):
    titulo: str
    vigencia: str
    descripcion: str
    modifica_riesgo: Optional[bool] = False
    urgencia_alta: Optional[bool] = False

@router.post("/politicas")
def crear_politica(politica: ComercialSchema, db: Session = Depends(get_db)):
    # 1. Ejecutar motor cognitivo
    datos_evaluacion = {
        "modifica_riesgo": politica.modifica_riesgo,
        "urgencia_alta": politica.urgencia_alta
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Sincronización en Neo4j
    driver = get_driver()
    with driver.session() as session:
        query = """
        MERGE (p:PoliticaComercial {titulo: $titulo})
        ON CREATE SET p.vigencia = $vigencia, p.descripcion = $descripcion
        """
        session.run(query, titulo=politica.titulo, vigencia=politica.vigencia, descripcion=politica.descripcion)

        # Vincular con reglas disparadas
        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (p:PoliticaComercial {titulo: $titulo})
            MERGE (r:AxiomaRegla {id_regla: $id_regla})
            MERGE (p)-[:DISPARA_REGLA]->(r)
            """
            session.run(query_regla, titulo=politica.titulo, id_regla=regla["regla"])

    return {
        "mensaje": "Política comercial registrada y evaluada cognitivamente",
        "politica": {"titulo": politica.titulo, "vigencia": politica.vigencia},
        "analisis_cognitivo": resultado_cognitivo
    }