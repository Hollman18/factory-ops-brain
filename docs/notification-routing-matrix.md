# Notification routing matrix

## Purpose
Make alert delivery more precise by mapping event types to likely recipients.

## Matrix

### Operational performance deterioration
- Primary role: Supervisor / Jefe de planta / Líder de turno
- Escalate to management if: target risk or business impact becomes material

### Elevated failure risk / technical instability
- Primary role: Mantenimiento / Confiabilidad
- Secondary role: Supervisor if operations are affected
- Escalate to management if: continuity risk is material

### Quality deviation / rejection spike
- Primary role: Calidad
- Secondary role: Supervisor
- Escalate to management if: output/customer/business impact is material

### Monthly target risk
- Primary role: Gerente / Directivo
- Secondary roles: Supervisor, Maintenance, or Quality depending on driver

### Entity-specific anomaly (plant / area / line / machine / shift / reference)
- Primary role: the role closest to action for that entity
- Escalate according to severity and expected impact

## Personalization rule
Routing defaults may be refined by user preferences, but operational logic should remain primary.
