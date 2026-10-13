# Capa A: Repositorio Comercial - MERA Advisor

## 1. Objetivo de la Capa
Proveer al sistema cognitivo ANA la base normativo-comercial para evaluar la viabilidad de contratos, acuerdos de nivel de servicio (SLA) y márgenes de rentabilidad antes de aceptar o proponer rutas logísticas.

## 2. Tipología de Clientes y Clasificación de Cuentas
* **Categoría VIP (Enterprise)**:
  * *Prioridad de atención*: Alta (Atención de incidencias en < 2 horas).
  * *SLA de entrega*: Cumplimiento mínimo exigido del 98.5%.
  * *Penalizaciones por retraso*: 5% sobre el valor del flete por cada hora excedida tras la ventana horaria pactada.
* **Categoría Estándar (PyME)**:
  * *Prioridad de atención*: Media (Atención de incidencias en < 4 horas).
  * *SLA de entrega*: Cumplimiento mínimo exigido del 95.0%.
  * *Penalizaciones por retraso*: 2% sobre el valor del flete por cada hora excedida.

## 3. Reglas de Negocio y Restricciones Comerciales
* **Margen de Utilidad Mínimo**: Ninguna operación logística puede ser aprobada por ANA si el margen de retorno financiero proyectado es inferior al 14% sobre los costos operativos base (combustible + peajes + viáticos).
* **Restricción de Crédito**: Cuentas con cartera vencida mayor a 45 días naturales pasan automáticamente a estado de bloqueo comercial preventivo, requiriendo validación gerencial para despachar nuevas unidades.
* **Políticas de Carga Mixta**: Se permite la consolidación de carga de distintos clientes en una misma unidad siempre y cuando la naturaleza de los productos sea compatible (ej. prohibido mezclar alimentos perecederos con químicos o materiales peligrosos).