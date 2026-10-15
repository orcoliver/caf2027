---
description: Revisa la semana, compara plan y realidad, ajusta y presenta la semana siguiente
---

# /resumen-semanal

1. Conéctate con el login por tokens y descarga la actividad nueva de la semana (`get_activities_by_date`, `get_activity_splits`, sueño, FC en reposo, Body Battery, `get_training_status`). Guarda los datos en `datos/`. Si un método viene vacío, indícalo y continúa.
2. Compara lo planificado en `plan.md` con lo realizado: sesiones cumplidas u omitidas, distancias, ritmos, FC, cadencia y sesiones de fuerza.
3. Revisa recuperación y carga (`get_training_four_week_load_balance`, sueño, FC en reposo). Señala riesgos de sobreentrenamiento o lesión.
4. Presenta un resumen breve con tendencia: volumen acumulado, ritmo frente al objetivo, VO2 máx y `get_race_predictions`.
5. Decide si hace falta ajustar (reprogramar, reducir o aumentar carga, cambiar ritmos, mover la tirada larga). Explica el porqué. Si el cambio es grande, pídeme confirmación.
6. Recalcula el tiempo estimado de llegada y la probabilidad de lograr 6:10 min/km (≈ 4:20:12).
7. Presenta el plan detallado de la semana que empieza, con fechas, **sin nada en sábado**, y recordatorios de las sesiones clave.
8. Actualiza `plan.md` y registra los ajustes en `bitacora.md`.
9. Si hubo ajustes y tengo sesiones ya programadas en Garmin, ofrece actualizarlas (`update_workout`, `unschedule_workout`, `schedule_workout`). Solo con mi confirmación explícita y mostrando antes los cambios.
10. Cada 4 semanas, añade un informe de progreso: volumen, ritmo, VO2 máx, forma actual y tiempo estimado.
11. Si pasó más de una semana sin datos nuevos, pregúntame qué ocurrió.
