# Capa C: Repositorio Operativo - MERA Advisor

## 1. Objetivo de la Capa
Establecer los procesos, tiempos de tránsito estándar y flujos de control logístico que permiten a ANA auditar el rendimiento operativo de las rutas y coordinar los centros de distribución (CEDIS).

## 2. Parámetros de Ventanas de Tiempo y Tránsito
* **Tiempos de Carga en Origen**: 
  * *Carga consolidada (Pallets)*: Máximo 90 minutos asignados desde el arribo de la unidad al muelle.
  * *Carga a granel o frágil*: Máximo 180 minutos de tolerancia para validación y estiba.
* **Tolerancia en Ventana de Entrega (OTD - On-Time Delivery)**:
  * El margen de aceptación para considerar una entrega puntual es de $\pm 30$ minutos respecto a la hora pactada con el cliente final. Cualquier variación superior a este rango activa una alerta de desviación operacional.

## 3. Protocolos de Gestión en CEDIS
* **Validación de Inventarios**: Todo despacho de salida debe cruzar validación automática de stock contra la base de datos relacional para evitar quiebres de inventario o envíos con faltantes.
* **Trazabilidad en Tiempo Real**: Las unidades activas deben reportar telemetría de posición y estado operativo cada 15 minutos durante trayectos en carretera federal.