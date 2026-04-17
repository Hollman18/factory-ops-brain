# Min Schema Contract

Contrato mínimo del esquema requerido para Factory Ops Brain.

## Obligatorio
- `produccion_turno`
  - `planta_id`, `linea_id`, `area_id`, `maquina_id`, `turno_id`, `referencia_id`, `fecha`
  - `total_unidades`, `und_buenas`, `desperdicio`, `retrabajo`
  - `oee`, `disponibilidad`, `rendimiento`, `calidad`
  - `vel_real`, `vel_ideal`
  - `t_operativo`, `t_productivo`, `t_parada`, `t_micro`
- `metas_indicadores`
  - `nivel`, `entidad_id`, `tipo_indicador`, `meta_valor`, `meta_minima`, `meta_critica`, `meta_excelencia`
- `maquinas`
  - `id`, `nombre`, `linea_id`, `area_id`, `activo`
- `lineas_produccion`
  - `id`, `nombre`, `area_id`
- `areas`
  - `id`, `nombre`, `planta_id`
- `plantas`
  - `id`, `nombre`, `sede_id`
- `referencias_producto`
  - `id`, `nombre`, `sku`
- `capacidad_maquina_referencia`
  - `maquina_id`, `referencia_id`, `capacidad_turno_teorica`, `velocidad_ideal`

## Recomendado
- `eventos_parada`
  - `maquina_id`, `inicio`, `fin`, `duracion_min`, `tipo_parada`, `codigo_falla_id`
- `codigos_falla`
- `categorias_falla`
- `mantenimiento_log`
  - `maquina_id`, `timestamp`, `mtbf`, `mttr`, `backlog`
- `energia_eventos`
  - `maquina_id`, `timestamp`, `kwh`
- `materia_prima_consumo`
  - `planta_id`, `referencia_id`, `fecha`, `consumo_real`, `consumo_estandar`
- `lecturas_variable`
  - `punto_id`, `timestamp`, `valor`, `en_alarma`
- `puntos_medicion`
  - `id`, `nombre`, `tipo_variable_id`

## Opcional
- `tarifas_recurso`
- `tipos_recurso_energetico`
- `materias_primas`
- `turnos` con detalle ampliado
- `proceso_maquinas`
- trazabilidad detallada por lote

## Regla
Si faltan tablas obligatorias, el agente no debe responder con confianza alta y el instalador debe advertir incompatibilidad.
