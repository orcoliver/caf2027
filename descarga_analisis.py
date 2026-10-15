#!/usr/bin/env python3
"""Descarga de solo lectura para /analisis-inicial. Guarda JSON en datos/."""
import json
import time
from pathlib import Path

from garminconnect import Garmin

OUT = Path(__file__).parent / "datos"
OUT.mkdir(exist_ok=True)
g = Garmin()
g.login("/home/ocarreno/.garminconnect")


def save(name, fn, *a, **k):
    try:
        data = fn(*a, **k)
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str))
        n = len(data) if hasattr(data, "__len__") else "-"
        print(f"OK   {name} ({n})")
        return data
    except Exception as e:
        print(f"FALLO {name}: {type(e).__name__}: {str(e)[:120]}")
    finally:
        time.sleep(1)


acts = save("actividades_2025-10_a_2026-10", g.get_activities_by_date, "2025-10-01", "2026-10-08") or []
save("race_predictions", g.get_race_predictions)
save("max_metrics_range", g.get_max_metrics_range, "2025-10-01", "2026-10-08")
save("training_status", g.get_training_status, "2026-10-08")
save("load_balance", g.get_training_four_week_load_balance, "2026-10-08")
save("lactate_threshold", g.get_lactate_threshold)
save("hr_zones", g.get_heart_rate_zones)
save("rhr_daily", g.get_rhr_daily, "2026-08-01", "2026-10-08")
save("sleep_daily", g.get_sleep_daily, "2026-09-08", "2026-10-08")
save("body_battery", g.get_body_battery, "2026-09-24", "2026-10-08")
save("weigh_ins", g.get_weigh_ins, "2026-01-01", "2026-10-08")
save("personal_records", g.get_personal_record)
save("user_profile", g.get_userprofile_settings)

# Maratón del 8-feb-2026
mar = [a for a in acts if str(a.get("startTimeLocal", "")).startswith("2026-02-08")
       and (a.get("distance") or 0) > 30000]
if mar:
    aid = mar[0]["activityId"]
    print("Maratón activityId:", aid)
    save("maraton_resumen", g.get_activity, aid)
    save("maraton_splits", g.get_activity_splits, aid)
    save("maraton_hr_zonas", g.get_activity_hr_in_timezones, aid)
else:
    print("No se encontró actividad >30 km el 2026-02-08")
