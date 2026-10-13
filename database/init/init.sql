-- Inicialización de esquemas y extensiones para MERA Advisor
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla de Clientes y Cuentas (Capa Comercial)
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(50) NOT NULL, -- VIP o Estandar
    limite_credito NUMERIC(12,2),
    dias_cartera_vencida INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Unidades de Transporte (Capa de Transporte)
CREATE TABLE IF NOT EXISTS unidades (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL, -- T1, T2, T3
    capacidad_peso_ton NUMERIC(5,2) NOT NULL,
    volumen_m3 NUMERIC(6,2) NOT NULL,
    rendimiento_km_l NUMERIC(4,2) NOT NULL,
    restricciones_activas TEXT[] -- Uso de arreglos para almacenar restricciones viales
);

-- Tabla de Repositorio Vectorial para Conocimiento de ANA
CREATE TABLE IF NOT EXISTS conocimiento_embeddings (
    id SERIAL PRIMARY KEY,
    capa VARCHAR(50) NOT NULL, -- comercial, transporte, operacion, riesgos, normatividad, experiencia
    contenido TEXT NOT NULL,
    vector_embedding VECTOR(1536)
);