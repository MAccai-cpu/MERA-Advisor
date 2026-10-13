from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from backend.database import Base

class PoliticaComercialModel(Base):
    """Capa A - Comercial"""
    __tablename__ = "politicas_comerciales"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class UnidadTransporteModel(Base):
    """Capa B - Transporte"""
    __tablename__ = "unidades_transporte"

    id = Column(Integer, primary_key=True, index=True)
    codigo_unidad = Column(String(100), unique=True, nullable=False)
    tipo_vehiculo = Column(String(100), nullable=False)
    capacidad_carga = Column(Float, nullable=True)
    estado = Column(String(50), default="Disponible")

class RegistroOperacionModel(Base):
    """Capa C - Operación"""
    __tablename__ = "registros_operacion"

    id = Column(Integer, primary_key=True, index=True)
    unidad = Column(String(100), nullable=False)
    estado_operativo = Column(String(100), nullable=False)
    detalles = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

class EvaluacionRiesgoModel(Base):
    """Capa D - Riesgos"""
    __tablename__ = "evaluaciones_riesgos"

    id = Column(Integer, primary_key=True, index=True)
    nivel_riesgo = Column(String(50), nullable=False) # Bajo, Medio, Alto
    factor_riesgo = Column(String(255), nullable=False)
    recomendacion = Column(Text, nullable=True)

class NormativaModel(Base):
    """Capa E - Normatividad"""
    __tablename__ = "normativas"

    id = Column(Integer, primary_key=True, index=True)
    codigo_norma = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    entidad_emisora = Column(String(150), nullable=True)

class RegistroExperienciaModel(Base):
    """Capa F - Experiencia / Experiencia MERA"""
    __tablename__ = "registros_experiencia"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False)
    retroalimentacion = Column(Text, nullable=False)
    puntuacion = Column(Integer, nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)