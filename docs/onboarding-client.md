# Onboarding Client

Guía operativa para incorporar un cliente nuevo a Factory Ops Brain sin improvisar el proceso humano previo y posterior a la instalación técnica.

## Objetivo

Este documento cubre el tramo que `install.sh` no resuelve por sí solo:
- entender la planta del cliente
- mapear su operación a la jerarquía del sistema
- definir metas iniciales
- asignar roles y canales
- validar que el agente quedó realmente útil después de instalarse

## Relación con otros documentos de onboarding

Este documento es para el onboarding operativo del cliente y del despliegue real en planta.

No reemplaza:
- `docs/installation-onboarding.md`, que define el onboarding conversacional mínimo de instalación/organización
- `docs/onboarding.md`, que define el onboarding individual de cada usuario final que hablará con el agente

Orden recomendado de uso:
1. `docs/onboarding-client.md`
2. `docs/installation-onboarding.md`
3. `docs/onboarding.md`

---

## 1. Checklist pre-instalación

Antes de llegar o antes de ejecutar `install.sh`, recopilar y validar lo siguiente.

### 1.1 Datos técnicos mínimos
- `DATABASE_URL` funcional hacia PostgreSQL del cliente
- confirmación de acceso de red desde la máquina donde correrá OpenClaw
- `planta_id` correcto
- zona horaria del cliente (`CLIENT_TZ`)
- nombre oficial del cliente (`CLIENT_NAME`)
- versión o rama del repo que se va a desplegar

### 1.2 Validación de base de datos
Confirmar:
- que la BD responde
- que existen las tablas mínimas del contrato de esquema
- que el `planta_id` corresponde a la planta que se quiere monitorear
- que hay datos recientes en producción, mantenimiento y calidad si esos módulos se van a usar

### 1.3 Datos operativos del cliente
Recopilar:
- nombre de la planta
- líneas o áreas principales
- máquinas críticas
- referencias/SKUs críticas
- turnos usados por la planta
- principales pérdidas conocidas
- objetivo principal del piloto

### 1.4 Contactos y canales por rol
Identificar por rol:
- gerente/directivo
- supervisor/jefe de producción
- mantenimiento
- calidad
- operador(es), si aplica

Por cada uno registrar:
- nombre
- cargo literal
- canal elegido (Telegram, WhatsApp, otro)
- identificador del canal
- horario esperado de notificaciones
- nivel de ruido tolerado

### 1.5 Configuración inicial del agente
Definir antes de instalar:
- qué roles recibirán alertas críticas
- qué roles recibirán reportes periódicos
- si el gerente quiere reporte diario o solo semanal/mensual
- si heartbeat crítico queda activo desde el día 1
- si mantenimiento y calidad quedan activos desde el piloto o en fase 2

---

## 2. Guía de configuración de metas

Las metas iniciales deben cargarse en `metas_indicadores` y adaptarse al contexto del cliente. No asumir un benchmark universal.

## 2.1 Principios
- usar metas conservadoras en la semana 1 si el cliente no tiene histórico confiable
- diferenciar meta objetivo, meta mínima y meta crítica
- definir metas por nivel cuando sea posible: planta, línea o máquina
- revisar metas por referencia si el mix de producto cambia mucho

## 2.2 Indicadores recomendados para arrancar
- `oee`
- `disponibilidad`
- `rendimiento`
- `calidad`
- si aplica: `energia`, `spc`, `materia_prima`, `mtbf`, `mttr`

## 2.3 Valores iniciales orientativos (solo referencia)

### Alimentos y bebidas
- OEE objetivo: 0.70 - 0.80
- disponibilidad objetivo: 0.80 - 0.90
- calidad objetivo: 0.97 - 0.995
- rendimiento objetivo: 0.80 - 0.90

### Farmacéutico
- OEE objetivo: 0.60 - 0.75
- disponibilidad objetivo: 0.75 - 0.88
- calidad objetivo: 0.985 - 0.999
- rendimiento objetivo: 0.75 - 0.88

### Automotriz / autopartes
- OEE objetivo: 0.75 - 0.85
- disponibilidad objetivo: 0.85 - 0.93
- calidad objetivo: 0.98 - 0.999
- rendimiento objetivo: 0.85 - 0.92

## 2.4 Recomendación práctica de carga inicial
Al crear metas en `metas_indicadores`, definir por cada indicador:
- `meta_valor`
- `meta_minima`
- `meta_critica`
- `meta_excelencia`
- `vigente_desde`
- `nivel`
- `entidad_id`

### Ejemplo de criterio inicial
Para OEE:
- `meta_valor`: meta objetivo acordada con cliente
- `meta_minima`: meta_valor - 0.05
- `meta_critica`: meta_valor - 0.10
- `meta_excelencia`: meta_valor + 0.05

> Ajustar manualmente si el baseline real del cliente está muy lejos de esos rangos.

---

## 3. Validación post-instalación

Después de instalar, hacer estas preguntas directamente al agente para validar conexión, contexto y comprensión operativa.

## 10 preguntas de validación
1. ¿Qué planta tienes configurada actualmente y qué `planta_id` estás usando?
2. ¿Cuáles son las principales áreas, líneas o máquinas que identificas en la base?
3. Muéstrame el OEE agregado de hoy de la planta.
4. ¿Qué máquina o línea tuvo peor desempeño en el último turno y por qué?
5. ¿Qué metas de OEE, disponibilidad, rendimiento y calidad tienes registradas para esta planta?
6. ¿Detectas alguna anomalía operativa relevante en las últimas 24 horas?
7. ¿Qué principales causas de pérdida observas en el periodo reciente?
8. ¿Tienes datos recientes de mantenimiento, calidad/SPC, energía y materia prima o falta alguno?
9. Si fueras a alertar al gerente hoy, ¿qué le dirías en dos líneas?
10. Si fueras a alertar al supervisor ahora mismo, ¿qué acción priorizarías?

## Criterios de éxito
- responde con datos reales y no genéricos
- entiende la jerarquía del cliente
- identifica correctamente la planta
- no confunde líneas, máquinas o roles
- adapta la respuesta según el rol pedido

---

## 4. Script de primer mensaje

Usar este prompt inicial tras terminar la instalación y validar conectividad básica.

```text
A partir de ahora operarás para el cliente {{CLIENT_NAME}} en la planta {{PLANTA_ID}} con zona horaria {{CLIENT_TZ}}.
Tu objetivo es actuar como analista operativo industrial orientado a producción, OEE, mantenimiento, calidad, energía y materia prima.
Debes usar la base de datos conectada como fuente principal de verdad.
Prioriza anomalías, deterioros sostenidos, riesgos de incumplimiento de meta y causas de pérdida accionables.
Adapta tus respuestas por rol: gerente/directivo, supervisor, mantenimiento, calidad y operador.
Evita ruido innecesario para gerencia.
Antes de responder con confianza sobre desempeño, valida si hay datos recientes suficientes.
Si faltan datos o la cobertura es parcial, dilo claramente.
```

### Variante sugerida para arranque de piloto
```text
Estamos en fase piloto. Sé conservador con las alertas, prioriza hallazgos de alto valor y evita falsas alarmas mientras aprendemos el comportamiento normal de la planta.
```

---

## 5. FAQ de problemas comunes

## 5.1 La BD no tiene datos del día
### Posibles causas
- ETL retrasado
- turno no cerrado
- problema de sincronización entre fuentes
- `planta_id` incorrecto

### Qué hacer
- validar si hay datos de ayer o del último turno
- comprobar hora local del cliente vs timestamps cargados
- confirmar cierre de turno
- correr `schema_check.py` y una consulta simple de recencia
- si no hay datos del día, el agente debe decirlo explícitamente y evitar conclusiones fuertes

## 5.2 Los sensores no están enviando
### Señales
- huecos en lecturas IoT
- consumo/velocidad en cero cuando la línea sí produjo
- últimas marcas muy antiguas

### Qué hacer
- revisar timestamp de última lectura por sensor o máquina
- validar conectividad del origen IoT
- revisar si la tabla tiene fallback manual
- pedir al agente que diferencie dato faltante vs paro real

## 5.3 El operador no cerró el turno
### Señales
- producción parcial del turno
- KPI incompletos
- ausencia de consolidado final

### Qué hacer
- consultar último turno cerrado y penúltimo turno
- marcar explícitamente el turno actual como preliminar
- evitar enviar resumen ejecutivo definitivo hasta cierre

## 5.4 El agente responde genérico y no con datos reales
### Posibles causas
- no está leyendo la skill correcta
- `CLIENT_CONFIG.json` incompleto
- problema de conexión a BD
- schema mismatch

### Qué hacer
- validar `CLIENT_CONFIG.json`
- probar consulta directa a la BD
- revisar `skills/data-connector/SKILL.md`
- correr `analytics/schema_check.py`

## 5.5 El gerente recibe demasiado ruido
### Qué hacer
- desactivar reporte diario si no es imprescindible
- dejar al gerente solo con semanal, mensual y alertas críticas
- mover alertas tácticas a supervisor o mantenimiento

## 5.6 Falta cobertura de un dominio (SPC, energía, MP)
### Qué hacer
- identificar si el cliente sí tiene esas tablas/datos
- mapear brecha contra `docs/min-schema-contract.md`
- dejar documentado si ese dominio queda fuera del piloto inicial

---

## 6. Recomendación operativa para el primer cliente

No activar todo el framework de una vez.

### Fase 1 recomendada
- producción/OEE
- capacidad
- alertas críticas
- supervisor
- gerente con mínimo ruido

### Fase 2
- mantenimiento
- calidad/SPC
- energía

### Fase 3
- materia prima
- trazabilidad avanzada
- predicción más específica por cliente

---

## 7. Entregables mínimos del onboarding

Al cerrar onboarding debe existir:
- `CLIENT_CONFIG.json` correcto
- acceso validado a BD
- `planta_id` confirmado
- metas iniciales cargadas o definidas
- roles mapeados
- canales definidos
- heartbeat validado
- al menos un reporte probado
- preguntas post-instalación respondidas satisfactoriamente

---

## 8. Siguiente paso sugerido

Después del onboarding, ejecutar:
1. `python3 analytics/schema_check.py`
2. `bash scripts/post_install_check.sh`
3. prueba de `analytics/db_query.py`
4. prueba de `analytics/anomaly_detector.py`
5. prueba de un cron y de un reporte por rol
