from fastapi import FastAPI
from sqlalchemy import text
from backend.database import engine, Base
from backend import models 

from backend.comercial import router as comercial_router
from backend.transporte import router as transporte_router
from backend.operacion import router as operacion_router
from backend.riesgos import router as riesgos_router
from backend.normatividad import router as normatividad_router
from backend.experiencia import router as experiencia_router
from backend.grafo import router as grafo_router
from backend.vector_router import router as vector_router  # Router de pgvector
from backend.engine_router import router as engine_router  # Router del Motor de Razonamiento ANA

app = FastAPI(
    title="MERA Advisor - Motor Cognitivo ANA",
    version="1.0.0"
)

# Creación automática de tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

# Registro de todas las capas cognitivas y motores del sistema
app.include_router(comercial_router)
app.include_router(transporte_router)
app.include_router(operacion_router)
app.include_router(riesgos_router)
app.include_router(normatividad_router)
app.include_router(experiencia_router)
app.include_router(grafo_router)
app.include_router(vector_router)
app.include_router(engine_router)  # <--- Incluimos los endpoints del Motor ANA

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al núcleo de MERA Advisor. Sistema operativo, motor axiomático ANA, vectores y red de grafos activos."}

@app.get("/health/db")
def test_db_connection():
    """Verifica la conexión con PostgreSQL y las tablas creadas"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
            tables = [row[0] for row in result]
        return {
            "estado": "Conexión exitosa a PostgreSQL",
            "tablas_encontradas": tables
        }
    except Exception as e:
        return {
            "estado": "Error de conexión",
            "detalles": str(e)
        }
        
