"""
Módulo: backend/engine.py
Descripción: Motor de razonamiento axiomático (ANA) basado en Clases, Arreglos dinámicos y Eventos.
Proyecto: MERA Advisor
"""

from typing import List, Dict, Any

# 1. Definición de Clases para el Modelo Axiomático Formal
class AxiomaRegla:
    def __init__(
        self, 
        id_regla: str, 
        dominio: str, 
        condicion: str, 
        consecuencia: str,
        descripcion: str,
        prioridad: int,
        fuente: str,
        version: str,
        vigencia: str,
        nivel_confianza: float
    ):
        self.id_regla = id_regla
        self.dominio = dominio
        self.condicion = condicion
        self.consecuencia = consecuencia
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fuente = fuente
        self.version = version
        self.vigencia = vigencia
        self.nivel_confianza = nivel_confianza

class EventBus:
    def __init__(self):
        self.historial_eventos: List[Dict[str, Any]] = []

    def registrar_evento(self, etapa: str, detalle: str):
        evento = {"etapa": etapa, "detalle": detalle}
        self.historial_eventos.append(evento)

# 2. Motor Principal del Sistema (MERAAdvisorEngine)
class MERAAdvisorEngine:
    def __init__(self):
        # Arreglo dinámico de axiomas oficiales con datos reales y verídicos del proyecto
        self.arreglo_axiomas: List[AxiomaRegla] = [
            AxiomaRegla(
                id_regla="AX-TR-001",
                dominio="Transporte",
                condicion="urgencia_alta",
                consecuencia="Seleccionar alternativas con menor tiempo de tránsito, descartando transporte marítimo estándar.",
                descripcion="Priorizar modalidades de transporte exprés o aéreo ante alta urgencia de entrega y plazos críticos.",
                prioridad=1,
                fuente="Política logística MERA",
                version="1.0",
                vigencia="2026-12-31",
                nivel_confianza=0.95
            ),
            AxiomaRegla(
                id_regla="AX-TR-004",
                dominio="Transporte",
                condicion="temperatura_controlada",
                consecuencia="Filtrar la flota habilitando únicamente unidades de transporte refrigeradas.",
                descripcion="Asignación obligatoria de unidades con control de temperatura para mercancía perecedera o insumos sensibles.",
                prioridad=1,
                fuente="Marco regulatorio y directrices operativas MERA",
                version="1.0",
                vigencia="2026-12-31",
                nivel_confianza=0.98
            ),
            AxiomaRegla(
                id_regla="AX-COM-001",
                dominio="Comercial",
                condicion="cliente_tier1",
                consecuencia="Ajustar las tarifas comerciales aplicando el porcentaje de bonificación autorizado.",
                descripcion="Aplicación de esquemas de descuento por volumen para clientes Tier-1 con contratos anuales vigentes.",
                prioridad=2,
                fuente="Políticas comerciales de MERA",
                version="1.0",
                vigencia="2026-12-31",
                nivel_confianza=0.90
            ),
            AxiomaRegla(
                id_regla="AX-NOR-001",
                dominio="Normatividad",
                condicion="transporte_terrestre_nacional",
                consecuencia="Bloquear la salida de la unidad si la documentación fiscal y digital no está debidamente timbrada.",
                descripcion="Cumplimiento normativo estricto del Complemento Carta Porte del SAT para el tránsito terrestre nacional.",
                prioridad=1,
                fuente="Disposiciones aduaneras y normatividad oficial",
                version="1.0",
                vigencia="2026-12-31",
                nivel_confianza=1.00
            ),
            AxiomaRegla(
                id_regla="AX-RS-002",
                dominio="Riesgos",
                condicion="alta_gama",
                consecuencia="Exigir custodia de seguridad y monitoreo GPS activo cada 15 minutos durante toda la ruta.",
                descripcion="Protocolo de resguardo y seguridad satelital para mercancías de tecnología o alto valor comercial.",
                prioridad=1,
                fuente="Matriz de riesgos y seguridad MERA",
                version="1.0",
                vigencia="2026-12-31",
                nivel_confianza=0.97
            )
        ]
        self.event_bus = EventBus()

    def procesar_evaluacion(self, datos_entrada: Dict[str, Any]) -> Dict[str, Any]:
        self.event_bus.historial_eventos.clear()
        
        # Etapa 1: Entrada
        self.event_bus.registrar_evento("Entrada", f"Datos recibidos para análisis: {datos_entrada}")
        
        acciones_tomadas = []
        
        # Etapa 2: Razonamiento (Uso de arreglos y evaluación de reglas)
        for axioma in self.arreglo_axiomas:
            if datos_entrada.get(axioma.condicion) == True:
                acciones_tomadas.append({
                    "regla": axioma.id_regla,
                    "dominio": axioma.dominio,
                    "descripcion": axioma.descripcion,
                    "consecuencia": axioma.consecuencia,
                    "fuente": axioma.fuente,
                    "nivel_confianza": axioma.nivel_confianza
                })

        # Etapa 3: Decisión
        decision = "Aprobado con restricciones operativas" if acciones_tomadas else "Aprobado estándar sin observaciones"
        self.event_bus.registrar_evento("Decisión", decision)

        # Etapa 4: Explicación
        explicacion = f"Se evaluaron {len(self.arreglo_axiomas)} axiomas en el arreglo, activando {len(acciones_tomadas)} reglas de control."
        self.event_bus.registrar_evento("Explicación", explicacion)

        # Etapa 5: Evidencia
        evidencia = {
            "estado_sistema": "Validado mediante Arquitectura ANA",
            "trazabilidad_eventos": self.event_bus.historial_eventos
        }
        self.event_bus.registrar_evento("Evidencia", "Registro de eventos completado exitosamente.")

        return {
            "entrada": datos_entrada,
            "razonamiento_aplicado": acciones_tomadas,
            "decision": decision,
            "explicacion": explicacion,
            "evidencia": evidencia
        }

# Instancia global del motor cognitivo
mera_engine = MERAAdvisorEngine()