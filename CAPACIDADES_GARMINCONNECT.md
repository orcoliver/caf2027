# Capacidades de `python-garminconnect` (v0.3.17)

Generado inspeccionando la clase `Garmin` instalada (~160 métodos públicos).
Cuenta conectada: Oliver Carreño · Dispositivo: Forerunner 55.

> Las fechas usan formato `'YYYY-MM-DD'`. Algunos métodos dependen del modelo
> de reloj o de la suscripción; si el Forerunner 55 no registra un dato
> (p. ej. potencia, golf, solar), el método devolverá vacío o error.

## Conexión
```python
from garminconnect import Garmin
g = Garmin()
g.login("/home/ocarreno/.garminconnect")   # usa tokens, sin contraseña
```
Ver [garmin_login.py](garmin_login.py) para el login inicial.

---

## 1. LECTURA (seguro, no modifica nada)

### Actividades y carreras
`get_activities`, `get_activities_by_date`, `get_activities_fordate`, `get_last_activity`,
`count_activities`, `get_activity`, `get_activity_details`, `get_activity_splits`,
`get_activity_split_summaries`, `get_activity_typed_splits`, `get_activity_hr_in_timezones`,
`get_activity_power_in_timezones`, `get_activity_weather`, `get_activity_gear`,
`get_activity_exercise_sets`, `get_activity_types`, `download_activity` (FIT/TCX/GPX/CSV),
`get_progress_summary_between_dates`, `get_personal_record`.

### Rendimiento y entrenamiento (clave para maratón)
`get_race_predictions` (5K/10K/21K/42K), `get_training_status`, `get_daily_training_status`,
`get_training_readiness`, `get_morning_training_readiness`, `get_training_load_activities`,
`get_training_four_week_load_balance`, `get_max_metrics` / `get_max_metrics_range` (VO2 máx),
`get_endurance_score`, `get_hill_score`, `get_lactate_threshold`, `get_running_tolerance`,
`get_fitnessage_data`, `get_primary_training_device`, `get_weekly_intensity_minutes`,
`get_intensity_minutes_data`.

### Salud y bienestar
- **Frecuencia cardíaca:** `get_heart_rates`, `get_rhr_day`, `get_rhr_daily`, `get_heart_rate_zones`
- **Sueño:** `get_sleep_data`, `get_sleep_daily`
- **HRV:** `get_hrv_data`, `get_hrv_data_range`
- **Estrés:** `get_stress_data`, `get_all_day_stress`, `get_weekly_stress`
- **Body Battery:** `get_body_battery`, `get_body_battery_events`
- **Respiración / SpO2:** `get_respiration_data`, `get_spo2_data`
- **Actividad diaria:** `get_stats`, `get_user_summary`, `get_stats_and_body`, `get_steps_data`,
  `get_daily_steps`, `get_weekly_steps`, `get_floors`, `get_calories_daily`, `get_all_day_events`
- **Composición corporal / peso:** `get_body_composition`, `get_weigh_ins`, `get_daily_weigh_ins`
- **Otros:** `get_hydration_data`, `get_blood_pressure`, `get_lifestyle_logging_data`,
  `download_health_snapshot`, `get_nutrition_daily_food_log/meals/settings`,
  datos de ciclo menstrual (`get_menstrual_*`), `get_pregnancy_summary`

### Entrenamientos y planes
`get_workouts`, `get_workout_by_id`, `download_workout`, `get_scheduled_workouts(año, mes)`,
`get_scheduled_workout_by_id`, `get_next_scheduled_workout`, `get_training_plans`,
`get_training_plan_by_id`, `get_adaptive_training_plan_by_id`.

### Dispositivo, perfil y extras
`get_devices`, `get_device_last_used`, `get_device_settings`, `get_device_alarms`,
`get_device_solar_data`, `get_full_name`, `get_user_profile`, `get_userprofile_settings`,
`get_unit_system`, `get_goals`, `get_gear`, `get_gear_stats`, `get_gear_activities`,
`get_gear_defaults`, badges (`get_earned_badges`, `get_available_badges`, `get_in_progress_badges`,
`get_badge_challenges`, ...), retos (`get_adhoc_challenges`, `get_inprogress_virtual_challenges`),
FTP/potencia (`get_cycling_ftp`, `get_functional_threshold_power_range`, `get_power_zones`),
golf (`get_golf_*`).

---

## 2. ESCRITURA (modifica tu cuenta Garmin Connect)

### Entrenamientos (muy útil para un plan de maratón)
- Crear: `upload_workout`, `upload_running_workout` (modelos tipados; también ciclismo, natación,
  caminata, senderismo, fuerza)
- Editar / borrar: `update_workout`, `delete_workout`
- Calendario: `schedule_workout(id, fecha)`, `unschedule_workout`
- Enviar al reloj: `push_workout_to_device`

### Actividades
`upload_activity` / `import_activity` (archivos FIT), `create_manual_activity`,
`set_activity_name`, `set_activity_description`, `set_activity_type`,
`set_activity_exercise_sets`, `add_gear_to_activity`, `remove_gear_from_activity`,
`delete_activity` ⚠️ (irreversible).

### Salud / registros
`add_weigh_in`, `add_weigh_in_with_timestamps`, `add_body_composition`, `add_hydration_data`,
`set_blood_pressure`, `delete_weigh_in(s)`, `delete_blood_pressure` ⚠️, y actualización de datos
de ciclo menstrual (`update_menstrual_*`, `confirm_menstrual_period_start`).

### Equipamiento
`create_gear` (p. ej. zapatillas), `set_gear_default`.

---

## 3. Avanzado
`connectapi`, `connectwebproxy`, `download` (llamadas directas a endpoints no cubiertos),
`query_garmin_graphql`, `request_reload(fecha)` (forzar recarga de datos de un día),
`logout`.

## Límites
- Es la API **no oficial** de Garmin Connect: puede romperse si Garmin cambia algo y puede
  aplicar límites de peticiones (evitar bucles masivos).
- Trabaja con datos **ya sincronizados** a Garmin Connect, no con el reloj por USB/Bluetooth.
- Las acciones de escritura/borrado afectan tu cuenta real: confirmar antes de ejecutarlas.
- Los tokens (`~/.garminconnect`) dan acceso a tu cuenta: no los compartas ni los subas a git.

## Ideas para `maratonCAF`
1. Bajar todas las carreras y calcular ritmos, volumen semanal y progresión.
2. Seguir `get_race_predictions`, VO2 máx y `get_training_status` en el tiempo.
3. Cruzar sueño, HRV y Body Battery con la calidad de tus entrenamientos.
4. Generar el plan de maratón y enviarlo al Forerunner 55 con `upload_running_workout` +
   `schedule_workout` + `push_workout_to_device`.
