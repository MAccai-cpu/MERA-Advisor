from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_driver

router = APIRouter(prefix="/grafo", tags=["Motor Cognitivo - Neo4j"])

class RelacionNormaSchema(BaseModel):
    codigo_unidad: str
    codigo_norma: str

@router.post("/relacionar-unidad-norma")
def crear_relacion_unidad_norma(data: RelacionNormaSchema):
    """Crea una relación de cumplimiento entre una unidad de transporte y una normativa en Neo4j"""
    driver = get_driver()
    try:
        with driver.session() as session:
            query = """
            MERGE (u:UnidadTransporte {codigo: $codigo_unidad})
            MERGE (n:Normativa {codigo: $codigo_norma})
            MERGE (u)-[:CUMPLE_CON]->(n)
            RETURN u.codigo AS unidad, n.codigo AS norma
            """
            result = session.run(query, codigo_unidad=data.codigo_unidad, codigo_norma=data.codigo_norma)
            record = result.single()
            
            if not record:
                raise HTTPException(status_code=400, detail="No se pudo establecer la relación en el grafo.")
                
            return {
                "mensaje": "Relación cognitiva creada con éxito en Neo4j",
                "relacion": {
                    "unidad": record["unidad"],
                    "normativa": record["norma"],
                    "tipo": "CUMPLE_CON"
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Neo4j: {str(e)}")