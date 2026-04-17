# HEARTBEAT.md

Only detect high-signal operational issues:
- abnormal machine/line behavior
- meaningful KPI deviation
- quality deviation
- elevated failure risk
- target-miss risk
- critical deviations in supported modules

La fuente de verdad del heartbeat es:
- `analytics/anomaly_detector.py`

---

## Comando exacto

Ejecutar exactamente:

```bash
python3 analytics/anomaly_detector.py --planta-id $(cat CLIENT_CONFIG.json | jq .planta_id)
```

Si `CLIENT_CONFIG.json` está dentro de `workspace-template/`, resolver el valor equivalente desde ahí antes de ejecutar.

---

## Regla operativa

### 1. Ejecuta el detector
Ejecutar el script y parsear el JSON de salida.

### 2. Si retorna anomalías vacías
Si devuelve:
- `status = ok`
- `anomalias = []`

Responder exactamente:

`HEARTBEAT_OK`

### 3. Si retorna anomalías con severidad `critica`
Construir alerta inmediata con los datos del JSON y notificar en el mismo ciclo.

### 4. Si retorna anomalías con severidad `media`
Acumular en `memory/heartbeat-state.json` hasta el próximo heartbeat. Si la misma anomalía persiste en **2 ciclos consecutivos**, entonces notificar.

### 5. Si retorna solo anomalías `baja`
No alertar todavía. Registrar si el sistema lo soporta y responder `HEARTBEAT_OK`.

---

## Identidad de persistencia para anomalías medias

Una anomalía es la misma si coincide en:
- `entidad`
- `metrica`
- `severidad`

---

## Formato de alerta obligatorio

Toda alerta debe seguir este formato:

```text
ALERTA OPERATIVA
- Qué cambió: <metrica> anómala en <entidad>
- Severidad: <severidad>
- Causa probable: <causa_probable>
- Valor actual: <valor_actual>
- Valor esperado: <valor_esperado>
- Quién debe actuar: <quien_debe_actuar>
- Acción inmediata: <recomendacion>
```

---

## Formato por rol

### Gerente
```text
ALERTA OPERATIVA
- Qué cambió: <metrica> anómala en <entidad>
- Severidad: <severidad>
- Causa probable: <causa_probable>
- Valor actual: <valor_actual>
- Valor esperado: <valor_esperado>
- Quién debe actuar: <quien_debe_actuar>
- Acción inmediata: <recomendacion>
```

### Supervisor
```text
ALERTA DE PLANTA
- Qué cambió: <metrica> anómala en <entidad>
- Severidad: <severidad>
- Causa probable: <causa_probable>
- Actual vs esperado: <valor_actual> vs <valor_esperado>
- Quién debe actuar: <quien_debe_actuar>
- Acción inmediata: <recomendacion>
```

### Mantenimiento
```text
ALERTA DE MANTENIMIENTO
- Qué cambió: <metrica> anómala en <entidad>
- Severidad: <severidad>
- Causa probable: <causa_probable>
- Valor actual: <valor_actual>
- Valor esperado: <valor_esperado>
- Quién debe actuar: <quien_debe_actuar>
- Intervención sugerida: <recomendacion>
```

---

## Manejo de `memory/heartbeat-state.json`

### Estructura mínima sugerida
```json
{
  "lastCycle": {
    "timestamp": "2026-04-17T00:00:00Z",
    "anomalias": [
      {
        "entidad": "maquina:Envasadora 1",
        "metrica": "oee",
        "severidad": "media"
      }
    ]
  }
}
```

### Regla
- guardar las anomalías medias detectadas
- comparar contra el siguiente ciclo
- si se repiten 2 ciclos consecutivos, alertar

---

## Fallos del detector

Si el script devuelve error o JSON inválido:
- no inventar estado de planta
- no enviar alerta falsa
- responder `HEARTBEAT_OK` si no hay certeza operativa
- si el sistema lo soporta, registrar internamente el fallo

---

## Regla final

- sin anomalías → `HEARTBEAT_OK`
- anomalía crítica → alerta inmediata
- anomalía media persistente 2 ciclos → alerta
- anomalía baja → no alertar aún
- usar siempre el JSON del detector como fuente de verdad
