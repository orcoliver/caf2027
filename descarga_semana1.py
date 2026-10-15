#!/usr/bin/env python3
"""Descarga datos de la Semana 1 (2026-10-05 a 2026-10-12) para Oliver y Beatriz."""
import json
import time
from pathlib import Path
from garminconnect import Garmin

OUT_OLIVER = Path("datos")
OUT_BEATRIZ = Path("datos/esposa")
OUT_OLIVER.mkdir(exist_ok=True)
OUT_BEATRIZ.mkdir(exist_ok=True, parents=True)

START_DATE = "2026-10-05"
END_DATE = "2026-10-12"

def sync_user(token_path, out_dir, name):
    print(f"\nSincronizando {name} ({token_path})...")
    g = Garmin()
    g.login(token_path)
    
    def fetch_save(fname, fn, *args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            (out_dir / f"{fname}.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=str))
            n = len(res) if hasattr(res, '__len__') else (1 if res else 0)
            print(f"  OK {fname}: {n} registros")
            return res
        except Exception as e:
            print(f"  FALLO {fname}: {type(e).__name__} - {str(e)[:100]}")
            return None
        finally:
            time.sleep(1)

    acts = fetch_save("semana1_actividades", g.get_activities_by_date, START_DATE, END_DATE)
    fetch_save("race_predictions_s1", g.get_race_predictions)
    fetch_save("max_metrics_s1", g.get_max_metrics_range, START_DATE, END_DATE)
    fetch_save("rhr_daily_s1", g.get_rhr_daily, START_DATE, END_DATE)
    fetch_save("sleep_daily_s1", g.get_sleep_daily, START_DATE, END_DATE)
    fetch_save("body_battery_s1", g.get_body_battery, START_DATE, END_DATE)
    fetch_save("training_status_s1", g.get_training_status, END_DATE)
    fetch_save("load_balance_s1", g.get_training_four_week_load_balance, END_DATE)
    
    # Splits de actividades encontradas
    if acts:
        for a in acts:
            aid = a.get("activityId")
            atype = a.get("activityType", {}).get("typeKey", "")
            adate = a.get("startTimeLocal", "")[:10]
            print(f"    -> Actividad: {adate} | {atype} | ID: {aid} | Dist: {round(a.get('distance', 0)/1000, 2)} km | Dur: {round(a.get('duration', 0)/60, 1)} min")
            if aid and "running" in atype:
                fetch_save(f"splits_{adate}_{aid}", g.get_activity_splits, aid)

if __name__ == "__main__":
    sync_user("/home/ocarreno/.garminconnect", OUT_OLIVER, "Oliver Carreño")
    sync_user("/home/ocarreno/.garminconnect_esposa", OUT_BEATRIZ, "Beatriz Gonzalez")
