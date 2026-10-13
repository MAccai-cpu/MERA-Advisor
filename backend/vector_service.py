"""
Módulo: backend/vector_service.py
Descripción: Lógica de conexión, inicialización y búsqueda con pgvector para MERA Advisor.
"""

from sqlalchemy import text
from backend.database import engine

def inicializar_pgvector():
    """Habilita la extensión pgvector en PostgreSQL y crea la tabla de fragmentos de conocimiento."""
    with engine.begin() as connection:
        # Habilitar extensión pgvector si la base de datos lo soporta
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        # Crear tabla para almacenar vectores de conocimiento
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS conocimiento_vectorial (
                id SERIAL PRIMARY KEY,
                capa VARCHAR(100),
                contenido TEXT,
                vector vector(1536)
            );
        """))

def insertar_documento_vectorial(capa: str, contenido: str, vector: list):
    """Inserta un documento y su representación vectorial en PostgreSQL."""
    with engine.begin() as connection:
        query = text("""
            INSERT INTO conocimiento_vectorial (capa, contenido, vector) 
            VALUES (:capa, :contenido, :vector);
        """)
        # Convertir la lista de python a un formato compatible con vector de postgresql si es necesario
        vector_str = "[" + ",".join(map(str, vector)) + "]"
        connection.execute(query, {"capa": capa, "contenido": contenido, "vector": vector_str})

def buscar_similitud_conocimiento(vector_consulta: list, limite: int = 3):
    """Realiza una búsqueda por distancia de coseno usando pgvector."""
    with engine.connect() as connection:
        vector_str = "[" + ",".join(map(str, vector_consulta)) + "]"
        query = text("""
            SELECT id, capa, contenido, (vector <=> :vector_consulta::vector) as distancia
            FROM conocimiento_vectorial
            ORDER BY distancia ASC
            LIMIT :limite;
        """)
        result = connection.execute(query, {"vector_consulta": vector_str, "limite": limite})
        
        resultados = []
        for row in result:
            resultados.append({
                "id": row[0],
                "capa": row[1],
                "contenido": row[2],
                "distancia": float(row[3])
            })
        return resultados