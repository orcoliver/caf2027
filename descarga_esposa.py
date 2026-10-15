#!/usr/bin/env python3
"""Descarga de solo lectura del historial de Beatriz. Guarda en datos/esposa/."""
import json, time, collections, datetime as dt
from pathlib import Path
from garminconnect import Garmin

OUT = Path(__file__).parent / "datos" / "esposa"
OUT.mkdir(parents=True, exist_ok=True)
g = Garmin()
g.login("/home/ocarreno/.garminconnect_esposa")


def save(name, fn, *a, **k):
    try:
        data = fn(*a, **k)
        (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str))
        print(f"OK   {name} ({len(data) if hasattr(data, '__len__') else '-'})")
        return data
    except Exception as e:
        print(f"FALLO {name}: {type(e).__name__}: {str(e)[:100]}")
    finally:
        time.sleep(1)


acts = save("actividades", g.get_activities_by_date, "2025-10-01", "2026-10-08") or []
save("race_predictions", g.get_race_predictions)
mm = save("max_metrics_range", g.get_max_metrics_range, "2025-10-01", "2026-10-08")
save("hr_zones", g.get_heart_rate_zones)
save("rhr_daily", g.get_rhr_daily, "2026-08-01", "2026-10-08")
save("sleep_daily", g.get_sleep_daily, "2026-09-08", "2026-10-08")
save("training_status", g.get_training_status, "2026-10-08")
save("weigh_ins", g.get_weigh_ins, "2026-01-01", "2026-10-08")

pace = lambda d, t: "%d:%02d" % divmod(int(t / (d / 1000)), 60) if d else "-"
runs = [a for a in acts if "running" in a.get("activityType", {}).get("typeKey", "")]
print("\nTipos:", collections.Counter(a["activityType"]["typeKey"] for a in acts).most_common())
mo = collections.defaultdict(float); wk = collections.defaultdict(float)
for a in runs:
    d = dt.date.fromisoformat(a["startTimeLocal"][:10])
    wk[d - dt.timedelta(days=d.weekday())] += a["distance"] / 1000
    mo[a["startTimeLocal"][:7]] += a["distance"] / 1000
print("\nKM/MES:", {k: round(v) for k, v in sorted(mo.items())})
print("KM/SEM (últimas 20):", {str(k): round(v) for k, v in sorted(wk.items())[-20:]})
print("\nCARRERAS >=15 km:")
for a in sorted(runs, key=lambda a: a["startTimeLocal"]):
    if a["distance"] >= 15000:
        print(a["startTimeLocal"][:10], round(a["distance"]/1000, 1), pace(a["distance"], a["duration"]), a.get("averageHR"), a.get("activityName"))
print("\nÚLTIMAS 15 CARRERAS:")
for a in sorted(runs, key=lambda a: a["startTimeLocal"])[-15:]:
    print(a["startTimeLocal"][:10], round(a["distance"]/1000, 1), pace(a["distance"], a["duration"]), a.get("averageHR"))
big = [a for a in runs if a["distance"] > 40000]
print("\nMARATONES >40 km:", [(a["startTimeLocal"][:10], round(a["distance"]/1000, 1), pace(a["distance"], a["duration"]), a.get("averageHR")) for a in big])
print("\nRACE PRED:", json.dumps(json.load(open(OUT / "race_predictions.json")))[:400] if (OUT / "race_predictions.json").exists() else "-")
if mm:
    s = mm[::30] + mm[-1:]
    print("VO2:", [(x.get("calendarDate"), x.get("vo2MaxPreciseValue")) for x in s])
for n in ("hr_zones", "rhr_daily", "sleep_daily", "training_status"):
    p = OUT / f"{n}.json"
    if p.exists():
        print(n.upper(), json.dumps(json.load(open(p)), default=str)[:350])
