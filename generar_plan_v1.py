#!/usr/bin/env python3
"""Genera plan.md (17 semanas). Sábado siempre libre."""
import datetime as dt
from pathlib import Path

START = dt.date(2026, 10, 5)
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
f = lambda d: f"{d.day} {MES[d.month]}"

# (fase, nota, [lun, mar, mié, jue, vie, dom], [km lun, mar, mié, jue, dom])
W = [
 ("Base", "Reinicio. Lun/Mar/Jue ya hechos (3,4 + 7,1 + 6,8 km). Solo ritmo fácil.",
  ["F 3,4 ✔", "F 7,1 ✔", "Descanso", "F 6,8 ✔", "Fuerza adaptación (A+B reducida)", "L 10 fácil"], [3.4, 7.1, 0, 6.8, 10]),
 ("Base", "Hábito y consistencia.",
  ["F 4", "F 6 + 6×20\" strides", "F 4 + Fuerza A", "F 5", "Fuerza B", "L 11 fácil"], [4, 6, 4, 5, 11]),
 ("Base", "Primer toque de ritmo.",
  ["F 5", "Fartlek 6×1' @5:30–5:40 / 1' trote (6)", "F 4 + Fuerza A", "F 6", "Fuerza B", "L 12 fácil"], [5, 6, 4, 6, 12]),
 ("Base · DESCARGA", "Semana de descarga.",
  ["F 4", "F 6 + 6 strides", "F 4 + Fuerza A", "F 5", "Fuerza B", "L 10 fácil"], [4, 6, 4, 5, 10]),
 ("Base", "Primera pista.",
  ["F 5", "Pista 6×400 m @5:10 rec 200 m trote (7)", "F 4 + Fuerza A", "Progresivo 7: 4 F + 3 @6:30", "Fuerza B", "L 13 fácil"], [5, 7, 4, 7, 13]),
 ("Desarrollo", "Inicio de fuerza máxima y umbral.",
  ["F 5", "Umbral 2×10' @5:45 rec 3' (8)", "F 4 + Fuerza A", "M 7 con 3 km @6:25", "Fuerza B", "L 14 (últimos 2 km @6:30)"], [5, 8, 4, 7, 14]),
 ("Desarrollo", "**Control 10K el domingo** (esfuerzo ~5:30–5:40/km). Recalibrar zonas.",
  ["F 5", "Pista 5×800 m @5:15 rec 400 m (9)", "F 4 + Fuerza A", "F 7 + 6 strides", "Fuerza B (ligera)", "**CARRERA 10K** (+ 4 km cal./enfr. = 14)"], [5, 9, 4, 7, 14]),
 ("Desarrollo · DESCARGA", "Semana de descarga.",
  ["F 4", "F 6 + strides", "F 4 + Fuerza A", "Umbral suave 3×6' @5:50 (5)", "Fuerza B", "L 14 fácil"], [4, 6, 4, 5, 14]),
 ("Desarrollo", "Primeros km a ritmo de maratón en tirada larga.",
  ["F 5", "Pista 6×1000 m @5:20 rec 2' (10)", "F 4 + Fuerza A", "MP 4 km @6:10 dentro de 7", "Fuerza B", "L 16: 9 F + 4 @6:10 + 3 F"], [5, 10, 4, 7, 16]),
 ("Desarrollo", "",
  ["F 5", "Umbral 3×10' @5:45 rec 2' (9)", "F 4 + Fuerza A", "MP 5 km @6:10 dentro de 8", "Fuerza B", "L 19: 6 F + 2×4 @6:10 (1 km @7:00 entre) + 4 F"], [5, 9, 4, 8, 19]),
 ("Específica", "**Control 21K el domingo** a ~6:10–6:15 (simulacro: calzado y nutrición de carrera).",
  ["F 5", "F 6 + strides (8)", "F 4 + Fuerza A (ligera)", "Umbral 2×8' @5:45 (7)", "Fuerza B (ligera)", "**CARRERA 21K** (+ 2 km cal. = 23)"], [5, 8, 4, 7, 23]),
 ("Específica · DESCARGA", "Semana de descarga (Navidad).",
  ["F 4", "F 7 + strides", "F 4 + Fuerza A", "M 6 con 3 km @6:25", "Fuerza B", "L 20 estable ~6:50"], [4, 7, 4, 6, 20]),
 ("Específica", "Gran bloque de ritmo de maratón.",
  ["F 4", "Pista 5×1200 m @5:20 rec 2' (10)", "F 4 + Fuerza A (mantenimiento)", "MP 5 km @6:10 dentro de 7", "Fuerza B (mantenimiento)", "L 26: 7 F + 2×5 @6:10 (2 km @6:50 entre) + 7 F"], [4, 10, 4, 7, 26]),
 ("Pico", "**Semana cumbre**: tirada más larga, simulacro completo.",
  ["F 4", "Umbral 3×12' @5:45 rec 2' (10)", "F 4 + Fuerza A (mantenimiento)", "F 6 + strides", "Fuerza B (mantenimiento)", "L 32: 8 F + 14 @6:10 + 10 F"], [4, 10, 4, 6, 32]),
 ("Taper 1", "Volumen −20 %, intensidad se mantiene. 1 sesión de fuerza.",
  ["F 5 + Fuerza ligera", "Pista 4×1000 m @5:15 rec 2' (9)", "F 4", "MP 3 km @6:10 dentro de 6", "Descanso/movilidad", "L 22: 6 F + 10 @6:10 + 6 F"], [5, 9, 4, 6, 22]),
 ("Taper 2", "Volumen −40 %.",
  ["F 4 + Fuerza ligera (2×8)", "Pista 3×1000 m @5:15 rec 2' (7)", "F 4", "F 5 + 4 strides", "Descanso/movilidad", "L 16: 5 F + 6 @6:10 + 5 F"], [4, 7, 4, 5, 16]),
 ("Semana de carrera", "Descanso total el sábado. Sin sorpresas: cena y desayuno ya probados.",
  ["F 5 + activación (2×10 fuerza ligera)", "6: 3×1 km @6:10 rec 2'", "F 4", "F 4 + 4 strides", "Descanso + movilidad", "**MARATÓN CAF 42,195 km**"], [5, 6, 4, 4, 42.2]),
]

out = []
out.append("""# Plan de entrenamiento: Maratón CAF (31 de enero de 2027)

**Versión 1.0 · generado 2026-10-08.** Meta: 6:10 min/km → ≈ 4:20:12. Inicio: lunes 5 de octubre de 2026. **Sábado siempre libre.**

> [!WARNING]
> **Fecha por confirmar.** AIMS lista el Maratón CAF 2027 el **21 de febrero de 2027**; otras fuentes citan 7 de febrero; tú indicaste 31 de enero (tentativa). Este plan está construido para el 31-ene. La organización presenta la edición el **15-oct-2026** en la Torre CAF: ahí confirmaremos y, si cambia, alargamos la fase base/desarrollo sin tocar el pico ni el taper.

## Evaluación de la meta
- Tiempo estimado hoy (Garmin): **5:43:36**, reflejo del parón (VO2 máx 41).
- Proyección si cumples el plan: **4:25–4:40**; mejor estimación central ≈ **4:32 (6:27/km)**.
- Probabilidad de 6:10/km: **≈ 20–25 %** → meta **ambiciosa**.
- Objetivos: **A** 4:20–4:25 · **B** 4:30–4:35 (realista) · **C** < 4:45 (mejorar el 4:40:46 con final fuerte).
- Se recalcula tras el control 10K (sem. 7) y el 21K (sem. 11): 21K en ≤ 2:08 (6:05/km) sostiene A; ≤ 2:13 sostiene B.

## Leyenda y zonas (provisionales; recalibrar sem. 7)
| Código | Tipo | Ritmo | FC (Z) | Propósito |
|---|---|---|---|---|
| F | Fácil | 7:00–7:30 | 125–145 (Z2) | Base aeróbica y recuperación |
| L | Tirada larga | 6:50–7:20 (bloques @6:10) | Z2–Z3 | Resistencia, economía, simulacro |
| M | Medio/estable | 6:25 | 146–155 (Z3) | Umbral aeróbico |
| MP | Ritmo de maratón | **6:10** | 150–158 | Especificidad |
| Umbral | Tempo | 5:45 (5:35–5:50) | 158–168 (Z4) | Subir umbral de lactato |
| Pista/Intervalos | Series | 5:05–5:20 | 168–175 (Z5) | VO2 máx y economía |
| Strides | 20" progresivos | ~5:15, rec 60" caminando | — | Técnica y reclutamiento |

**Calentamiento/enfriamiento** (sesiones de calidad): 2 km fácil + movilidad dinámica (5') + 4 strides; luego 1,5 km fácil + estiramientos suaves. En tirada larga: primeros 2 km muy suaves.
**Estructura semanal:** Lun F · Mar calidad · Mié F + Fuerza A · Jue calidad media/MP · Vie Fuerza B (sin correr) · **Sáb libre** · Dom larga.
**Reglas de ajuste:** si el sueño o la FC en reposo empeoran (> +5 lpm sobre ~60 varios días) o hay molestia, se cambia la calidad por fácil. En semanas pesadas de trabajo, la calidad pasa a F y se conserva la larga.

## Plan semanal (km incluyen calentamiento/enfriamiento)
""")

tot_prev = None
resumen = []
for i, (fase, nota, ses, km) in enumerate(W):
    mon = START + dt.timedelta(days=7 * i)
    total = round(sum(km), 1)
    resumen.append((i + 1, mon, total, fase))
    out.append(f"\n### Semana {i+1} · {fase} · {f(mon)} – {f(mon + dt.timedelta(days=6))} · **{total:g} km**\n")
    if nota:
        out.append(f"_{nota}_\n")
    out.append("| Día | Fecha | Sesión |\n|---|---|---|")
    order = [0, 1, 2, 3, 4, None, 5]
    for d, idx in enumerate(order):
        date = mon + dt.timedelta(days=d)
        s = "**Libre (no se entrena)**" if idx is None else ses[idx]
        out.append(f"| {DIAS[d]} | {f(date)} | {s} |")
    out.append("")

out.append("\n## Progresión de carga\n| Sem | Inicio | Km | Fase | Δ vs semana previa |\n|---|---|---|---|---|")
prev = None
for n, mon, t, fase in resumen:
    d = "—" if prev is None else f"{(t / prev - 1) * 100:+.0f} %"
    out.append(f"| {n} | {f(mon)} | {t:g} | {fase} | {d} |")
    prev = t
out.append("""
Descargas: semanas 4, 8 y 12. Tras cada descarga el aumento es ≤ 10 % frente a la última semana de carga plena (el % de la tabla es contra la semana inmediata). El taper es de 3 semanas (15–17).

## Fuerza (2 sesiones/semana; 1 en el taper)
Equipo: mancuernas y bandas. **Mié = Fuerza A** (≥24 h después de la calidad del martes); **Vie = Fuerza B** (ligera, sin correr). Si la calidad del jueves queda comprometida, baja a 2 series en A.

| Fase | Semanas | Series × reps | Carga | Descanso |
|---|---|---|---|---|
| Adaptación anatómica | 1–5 | 2–3 × 12–15 | RPE 6 | 60 s |
| Fuerza | 6–12 | 3–4 × 6–10 | RPE 7–8 (sin llegar al fallo) | 90–120 s |
| Mantenimiento | 13–14 | 2 × 6–8 | RPE 7 | 90 s |
| Taper | 15–17 | 1 sesión ligera, 2 × 8 | RPE 5–6 | 60 s |

### Fuerza A (piernas y glúteos)
| Ejercicio | Series × reps | Nota técnica | Alternativa |
|---|---|---|---|
| Sentadilla goblet (mancuerna) | 3 × 10 | Espalda neutra, rodillas alineadas con los pies | Sentadilla a una silla con banda |
| Peso muerto rumano con mancuernas | 3 × 8–10 | Cadera atrás, rodillas semiflexionadas; sentir isquios | A una pierna sin carga |
| Zancada inversa → sentadilla búlgara (desde sem. 6) | 3 × 8 c/pierna | Torso erguido, paso largo | Zancada estática |
| Puente de glúteos con mancuerna | 3 × 12 | Pausa 1 s arriba, sin hiperextender lumbar | Con banda sobre rodillas |
| Elevación de talones de pie (mancuerna) | 3 × 12–15 | Subida explosiva, bajada 3 s | A una pierna |
| Elevación de talones sentado/rodilla flexionada (sóleo) | 3 × 15 | Sóleo es clave en maratón | — |

### Fuerza B (estabilidad, core y pantorrillas; ligera)
| Ejercicio | Series × reps | Nota técnica | Alternativa |
|---|---|---|---|
| Step-up con mancuernas | 3 × 10 c/pierna | Banco o escalón bajo; sube con el talón | Sin carga |
| Caminata lateral con banda | 3 × 12 pasos c/lado | Banda sobre rodillas, pies paralelos | Clamshell con banda |
| Plancha frontal | 3 × 30–45 s | Pelvis neutra | Rodillas apoyadas |
| Plancha lateral | 3 × 20–30 s c/lado | Cuerpo en línea | Con rodilla inferior apoyada |
| Bird-dog | 3 × 8 c/lado | Sin rotar la cadera | Dead bug |
| Elevación de talones a una pierna | 2 × 10 | Control y rango completo | Dos pies |
| Pliometría ligera (desde sem. 8): pogos / skipping | 3 × 20 s | Contactos cortos, sin dolor | Omitir |

> [!NOTE]
> **Enlaces:** referencia https://musclewiki.com/es-es — busca por el nombre del ejercicio (p. ej. "peso muerto rumano", "plancha lateral") y filtra por mancuernas, bandas o peso corporal. No incluyo URLs directas por ejercicio porque el sitio bloquea mi verificación automática (HTTP 403) y no quiero darte enlaces sin comprobar. Si prefieres, puedo añadirlos cuando me pases los que ya conozcas.

## Movilidad y prevención (10 min, antes de correr o tras la fuerza)
1. Círculos de cadera y balanceo de piernas (adelante/lateral): 10 c/lado.
2. Zancada con rotación de torso: 6 c/lado.
3. Puente de glúteos isométrico: 2 × 20 s.
4. Estiramiento suave de flexores de cadera, gemelos y sóleo (pared): 30 s c/lado.
5. Rodillo o pelota en glúteo/cuádriceps (opcional): 1 min/zona.
6. Caminata lateral con banda: 1 × 10 c/lado.
Señales de alarma (dolor que cambia el paso, hinchazón, dolor nocturno): detener la calidad y consultar a un profesional.

## Estrategia de carrera (Maratón CAF)
Datos: ruta urbana certificada World Athletics/AIMS; ≈ **258 m** de ascenso y 242 m de descenso en 42K (soymaratonista.com); salidas matutinas ~5:50–6:05 a.m. (caf.com); horario 2027 por confirmar.

| Tramo | Ritmo | Notas |
|---|---|---|
| Km 1–5 | 6:15–6:20 | Salir contenido (en febrero salí a ~6:16 y lo pagué) |
| Km 6–30 | 6:10 | Estable; FC 150–158; subir un poco menos de esfuerzo en repechos |
| Km 31–37 | 6:10–6:15 | Mantener forma, no apretar |
| Km 38–42,2 | Lo que quede | Solo si la FC y las piernas responden |

Plan B (tiempo 4:30–4:35): 6:25–6:30 estable. Decide en el km 25 con FC y sensaciones.
- **Hidratación:** 400–600 ml/h con sodio; beber en cada punto, a sorbos. En clima fresco, ajustar a sed.
- **Carbohidratos:** 60 g/h (gel cada 25–30 min + bebida deportiva) empezando en el km 5; probar hasta 75–90 g/h en las tiradas largas si el estómago lo tolera.
- **Calzado:** zapatillas ya usadas en ≥ 2 tiradas largas (> 20 km) y la ropa de carrera; no estrenar nada.
- **Simulacros:** semana 9–10 (primeros bloques MP), **semana 11 (21K)**, **semana 13 (26 km)** y **semana 14 (32 km: 14 @6:10)** con la nutrición, el calzado y el horario de la carrera (salida ~6 a.m.).
- **Pre-carrera:** carga de carbohidratos 8–10 g/kg/día durante 36–48 h el viernes y sábado; desayuno 2–3 h antes; sin fibra excesiva.
Los números de nutrición son pautas generales de la literatura deportiva (ACSM/IOC); pruébalas en entrenamiento y ajusta a tu tolerancia. No es consejo médico.

## Carreras de control
- **Dom 22-nov (sem. 7): 10K.** Objetivo ≤ 55:00 (5:30/km) para sostener la meta B/A.
- **Dom 20-dic (sem. 11): 21K.** Objetivo ≤ 2:08 (A) / ≤ 2:13 (B).
Elegiremos carreras reales cuando haya calendario; si no existen, hacerlas como pruebas contrarreloj en pista o asfalto.
""")

Path("/home/ocarreno/dev/maratonCAF/plan.md").write_text("\n".join(out), encoding="utf-8")
for n, mon, t, fase in resumen:
    print(n, mon, t, fase)
