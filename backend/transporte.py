from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import SessionLocal, get_driver  # Importamos el driver de Neo4j
from backend.models import UnidadTransporteModel
from backend.engine import mera_engine

router = APIRouter(prefix="/capa-b", tags=["Capa B - Transporte"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UnidadSchema(BaseModel):
    codigo_unidad: str
    tipo_vehiculo: str
    capacidad_carga: float
    estado: str = "Disponible"
    urgencia_alta: Optional[bool] = False
    temperatura_controlada: Optional[bool] = False
    saturacion_ruta: Optional[bool] = False

@router.get("/flota")
def obtener_flota(db: Session = Depends(get_db)):
    unidades = db.query(UnidadTransporteModel).all()
    return {
        "capa": "B - Transporte",
        "total": len(unidades),
        "unidades": [{"id": u.id, "codigo": u.codigo_unidad, "tipo": u.tipo_vehiculo, "capacidad": u.capacidad_carga, "estado": u.estado} for u in unidades]
    }

@router.post("/flota")
def crear_unidad(unidad: UnidadSchema, db: Session = Depends(get_db)):
    # 1. Ejecutamos el motor cognitivo (Clases, arreglos y eventos)
    datos_evaluacion = {
        "urgencia_alta": unidad.urgencia_alta,
        "temperatura_controlada": unidad.temperatura_controlada,
        "saturacion_ruta": unidad.saturacion_ruta
    }
    resultado_cognitivo = mera_engine.procesar_evaluacion(datos_evaluacion)

    # 2. Guardamos en PostgreSQL
    nueva = UnidadTransporteModel(
        codigo_unidad=unidad.codigo_unidad,
        tipo_vehiculo=unidad.tipo_vehiculo,
        capacidad_carga=unidad.capacidad_carga,
        estado=unidad.estado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # 3. Guardamos/Sincronizamos en el Grafo (Neo4j Local)
    driver = get_driver()
    with driver.session() as session:
        # Creamos el nodo de la Unidad y si hay reglas activas, creamos relaciones dinámicas
        query = """
        MERGE (u:UnidadTransporte {codigo: $codigo})
        ON CREATE SET u.tipo = $tipo, u.capacidad = $capacidad, u.estado = $estado
        """
        session.run(query, codigo=unidad.codigo_unidad, tipo=unidad.tipo_vehiculo, capacidad=unidad.capacidad_carga, estado=unidad.estado)

        # Si el motor cognitivo activó reglas, las vinculamos al grafo como trazabilidad
        for regla in resultado_cognitivo.get("razonamiento_aplicado", []):
            query_regla = """
            MATCH (u:UnidadTransporte {codigo: $codigo})
            MERGE (r:AxiomaRegla {id_regla: $id_regla})
            ON CREATE SET r.dominio = $dominio, r.consecuencia = $consecuencia
            MERGE (u)-[:DISPARA_REGLA]->(r)
            """
            session.run(query_regla, 
                        codigo=unidad.codigo_unidad, 
                        id_regla=regla["regla"], 
                        dominio=regla["dominio"], 
                        consecuencia=regla["consecuencia"])

    # 4. Respuesta unificada
    return {
        "mensaje": "Unidad registrada con éxito, evaluada cognitivamente y sincronizada en Neo4j",
        "unidad": {
            "id": nueva.id, 
            "codigo": nueva.codigo_unidad,
            "tipo": nueva.tipo_vehiculo
        },
        "analisis_cognitivo": resultado_cognitivo
    }