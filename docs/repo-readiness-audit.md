# Repo Readiness Audit

Estado de cierre técnico del repo Factory Ops Brain.

## Completo
- workspace-template limpio
- CLIENT_CONFIG template limpio
- DATA_MODEL como mapa del agente
- QUERIES como librería base
- data-connector skill
- heartbeat basado en anomaly_detector
- cron por rol documentado y ejecutable
- install.sh bastante robusto
- schema_check.py
- post_install_check.sh

## Parcial alto
- db_query.py multiárea (v1 robusta, no full-enterprise aún)
- anomaly_detector.py multiárea (más fuerte en producción/OEE)
- docs heredados aún pueden tener redundancia

## Riesgos principales
1. esquema real del cliente puede diferir del naming asumido
2. profundidad analítica desigual entre dominios
3. plantillas no tienen aún lógica de fallback avanzada

## Recomendación de uso
- usar schema_check.py antes de desplegar
- correr post_install_check.sh después de instalar
- tratar producción/OEE/capacidad como dominio más maduro
- expandir mantenimiento/energía/SPC/trazabilidad según cliente real
