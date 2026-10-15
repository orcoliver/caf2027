import json, collections, datetime as dt
from pathlib import Path
D = Path("/home/ocarreno/dev/maratonCAF/datos")
L = lambda n: json.load(open(D / f"{n}.json"))
acts = L("actividades_2025-10_a_2026-10")
runs = [a for a in acts if "running" in (a.get("activityType", {}).get("typeKey", ""))]
print("tipos:", collections.Counter(a["activityType"]["typeKey"] for a in acts).most_common())
pace = lambda d, t: (lambda s: f"{int(s//60)}:{int(s%60):02d}")(t / (d / 1000)) if d else "-"
wk = collections.defaultdict(float); mo = collections.defaultdict(float)
for a in runs:
    d = dt.date.fromisoformat(a["startTimeLocal"][:10])
    wk[d - dt.timedelta(days=d.weekday())] += a["distance"] / 1000
    mo[a["startTimeLocal"][:7]] += a["distance"] / 1000
print("\nKM POR MES"); [print(k, round(v, 1)) for k, v in sorted(mo.items())]
print("\nKM POR SEMANA (últimas 30)")
for k, v in sorted(wk.items())[-30:]: print(k, round(v, 1))
print("\nCARRERAS >=15km")
for a in sorted(runs, key=lambda a: a["startTimeLocal"]):
    if a["distance"] >= 15000:
        print(a["startTimeLocal"][:10], round(a["distance"]/1000, 1), pace(a["distance"], a["duration"]), a.get("averageHR"), a.get("maxHR"), a.get("name"))
print("\nÚLTIMAS 25 CARRERAS")
for a in sorted(runs, key=lambda a: a["startTimeLocal"])[-25:]:
    print(a["startTimeLocal"][:10], round(a["distance"]/1000, 1), pace(a["distance"], a["duration"]), a.get("averageHR"), a["activityType"]["typeKey"], a.get("name"))
print("\nRACE PRED"); print(json.dumps(L("race_predictions"), indent=0)[:1500])
print("\nTRAINING STATUS"); print(json.dumps(L("training_status"), default=str)[:2500])
print("\nLOAD BALANCE"); print(json.dumps(L("load_balance"), default=str)[:1500])
print("\nLACTATE"); print(json.dumps(L("lactate_threshold"), default=str)[:1200])
print("\nHR ZONES"); print(json.dumps(L("hr_zones"), default=str)[:1500])
mm = L("max_metrics_range")
print("\nVO2 muestras", len(mm))
for x in mm[::25] + mm[-1:]: print(json.dumps(x.get("generic", x), default=str)[:200])
print("\nRHR"); r = L("rhr_daily"); print(json.dumps(r[:2], default=str)[:500], json.dumps(r[-3:], default=str)[:600])
print("\nBODY BATTERY"); print(json.dumps(L("body_battery"), default=str)[:1200])
print("\nWEIGH"); print(json.dumps(L("weigh_ins"), default=str)[:1000])
print("\nPERFIL"); print(json.dumps(L("user_profile"), default=str)[:1200])
print("\nMARATON"); m = L("maraton_resumen"); print(json.dumps({k: m.get(k) for k in m if k in ("activityName","summaryDTO")}, default=str)[:2500])
print("\nSPLITS"); print(json.dumps(L("maraton_splits"), default=str)[:800])
print("\nHRZ"); print(json.dumps(L("maraton_hr_zonas"), default=str)[:800])
