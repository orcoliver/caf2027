---
description: Analiza mis datos de Garmin, el maratón del 8 feb 2026 y evalúa la meta de 6:10 min/km
---

# /analisis-inicial

Sigue estos pasos en orden:

1. Lee `CAPACIDADES_GARMINCONNECT.md`. Conéctate con el login por tokens (`garmin_login.py`) y descarga los datos necesarios con la librería. Guarda los resultados en `datos/`. Si un método falla o viene vacío (Forerunner 55), indícalo y continúa.
2. Resume mis estadísticas del año (`get_activities_by_date`): volumen semanal y mensual (km), número de carreras, ritmo promedio por tipo de sesión, tirada más larga, consistencia, tendencia de FC y de VO2 máx (`get_max_metrics_range`).
3. Analiza el maratón del **8 de febrero de 2026** (`get_activity_splits`, `get_activity_hr_in_timezones`): ritmo, parciales, deriva de FC, desgaste en la segunda mitad, y volumen y tiradas largas de las semanas previas. Extrae lecciones concretas.
4. Evalúa mi estado actual desde el **5 de octubre de 2026** (`get_training_status`, `get_training_four_week_load_balance`, sueño, FC en reposo, Body Battery): base disponible, riesgo de lesión, carga frente a capacidad.
5. Calcula mis zonas de ritmo y FC (fácil, maratón, umbral, intervalos) con mis datos (`get_heart_rate_zones`, `get_race_predictions`) y la meta de 6:10 min/km.
6. Evalúa con honestidad si 6:10 min/km (≈ 4:20:12) es alcanzable, con probabilidad aproximada y condiciones necesarias.
7. Completa `perfil.md` con los datos obtenidos. Haz como máximo 3 preguntas sobre lo que falte (lesiones, equipo de fuerza, terreno y clima).
8. Muéstrame el perfil y el análisis para validarlos, y registra el resultado en `bitacora.md`.

Este flujo es solo de lectura: no uses métodos de escritura de Garmin.
Formato: tablas claras, conclusiones al inicio, sin relleno.
