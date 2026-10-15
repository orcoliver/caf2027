#!/usr/bin/env python3
"""Genera plan.md (20 semanas). Sábado siempre libre."""
import datetime as dt
from pathlib import Path

START = dt.date(2026, 10, 5)
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
f = lambda d: f"{d.day} {MES[d.month]}"

# (fase, nota, [lun, mar, mié, jue, vie, dom], [km lun, mar, mié, jue, dom])
W = [
 ("Base", "Reinicio. Completada: 28,1 km (Oliver) / 28,1 km (Beatriz, reloj sin batería al km 6,4). Fuerza omitida.",
  ["F 3,4 ✔", "F 7,1 ✔", "Descanso", "F 6,8 ✔", "Fuerza adaptación (omitida)", "L 10 fácil ✔"], [3.4, 7.1, 0, 6.8, 10.75]),
 ("Base", "Hábito y consistencia. Programada en Garmin.",
  ["F 4", "F 6 + 6×20\" strides", "F 4 + Fuerza A", "F 5", "Fuerza B", "L 11 fácil"], [4, 6, 4, 5, 11]),
 ("Base", "Primer toque de ritmo.",
  ["F 5", "Fartlek 6×1' @5:30–5:40 / 1' trote (6)", "F 4 + Fuerza A", "F 6", "Fuerza B", "L 12 fácil"], [5, 6, 4, 6, 12]),
 ("Base · DESCARGA", "Semana de descarga.",
  ["F 4", "F 6 + 6 strides", "F 4 + Fuerza A", "F 5", "Fuerza B", "L 10 fácil"], [4, 6, 4, 5, 10]),
 ("Base", "Primera pista.",
  ["F 5", "Pista 6×400 m @5:10 rec 200 m trote (7)", "F 4 + Fuerza A", "Progresivo 7: 4 F + 3 @6:30", "Fuerza B", "L 13 fácil"], [5, 7, 4, 7, 13]),
 ("Desarrollo", "Inicio de fuerza máxima y umbral.",
  ["F 5", "Umbral 2×10' @5:45 rec 3' (8)", "F 4 + Fuerza A", "M 7 con 3 km @6:25", "Fuerza B", "L 14 (últimos 2 km @6:30)"], [5, 8, 4, 7, 14]),
 ("Desarrollo", "",
  ["F 5", "Pista 5×800 m @5:15 rec 400 m (9)", "F 4 + Fuerza A", "F 7 + 6 strides", "Fuerza B", "L 16 fácil"], [5, 9, 4, 7, 16]),
 ("Desarrollo · DESCARGA", "Descarga + **Control 10K el domingo** (esfuerzo ~5:30–5:40/km). Recalibrar zonas.",
  ["F 4", "F 6 + strides", "F 4 + Fuerza A", "F 5 + 4 strides", "Fuerza B (ligera)", "**CARRERA 10K** (+ 4 km cal./enfr. = 14)"], [4, 6, 4, 5, 14]),
 ("Desarrollo", "Primeros km a ritmo de maratón en tirada larga.",
  ["F 5", "Pista 6×1000 m @5:20 rec 2' (10)", "F 4 + Fuerza A", "MP 4 km @6:10 dentro de 7", "Fuerza B", "L 18: 11 F + 4 @6:10 + 3 F · cuestas en el último tercio"], [5, 10, 4, 7, 18]),
 ("Desarrollo", "",
  ["F 5", "Umbral 3×10' @5:45 rec 2' (9)", "F 4 + Fuerza A", "MP 5 km @6:10 dentro de 8", "Fuerza B", "L 20: 8 F + 2×4 @6:10 (1 km @7:00 entre) + 3 F"], [5, 9, 4, 8, 20]),
 ("Específica", "",
  ["F 5", "Pista 5×1200 m @5:20 rec 2' (10)", "F 4 + Fuerza A", "MP 5 km @6:10 dentro de 8", "Fuerza B", "L 22: 10 F + 8 @6:10 + 4 F · cuestas en el último tercio"], [5, 10, 4, 8, 22]),
 ("Específica · DESCARGA", "Semana de descarga (Navidad).",
  ["F 4", "F 7 + strides", "F 4 + Fuerza A", "M 6 con 3 km @6:25", "Fuerza B", "L 18 estable ~6:50"], [4, 7, 4, 6, 18]),
 ("Específica", "Año nuevo: tirada larga con bloques MP.",
  ["F 5", "Umbral 3×10' @5:45 rec 2' (10)", "F 4 + Fuerza A", "MP 5 km @6:10 dentro de 7", "Fuerza B", "L 26: 8 F + 2×6 @6:10 (2 km @6:50 entre) + 4 F · cuestas en el último tercio"], [5, 10, 4, 7, 26]),
 ("Específica", "**Control 21K el domingo** a ~6:05–6:15 (simulacro: calzado, nutrición y sodio de carrera).",
  ["F 5", "Pista 4×1000 m @5:15 rec 2' (8)", "F 4 + Fuerza A (ligera)", "F 6 + strides", "Fuerza B (ligera)", "**CARRERA 21K** (+ 2 km cal. = 23)"], [5, 8, 4, 6, 23]),
 ("Específica", "Tirada larga de 30 km con 14 km a ritmo de maratón.",
  ["F 5", "Umbral 3×12' @5:45 rec 2' (10)", "F 4 + Fuerza A (mantenimiento)", "MP 4 km @6:10 dentro de 6", "Fuerza B (mantenimiento)", "L 30: 10 F + 14 @6:10 + 6 F · cuestas en el último tercio"], [5, 10, 4, 6, 30]),
 ("Específica · DESCARGA", "Descarga antes del bloque cumbre.",
  ["F 4", "F 7 + strides", "F 4 + Fuerza A (mantenimiento)", "M 6 con 3 km @6:25", "Fuerza B (mantenimiento)", "L 20 estable ~6:50"], [4, 7, 4, 6, 20]),
 ("Pico", "**Semana cumbre: tirada de 35 km** (3 semanas antes de la carrera). Simulacro completo anti-calambres: ritmo, geles, sodio, calzado y horario 6 a.m.",
  ["F 5", "Umbral 2×12' @5:45 rec 2' (9)", "F 4 + Fuerza A (mantenimiento)", "F 7 + strides", "Fuerza B (mantenimiento)", "L 35: 18 F + 12 @6:10 (km 19–30) + 5 F · cuestas en el último tercio"], [5, 9, 4, 7, 35]),
 ("Taper 1", "Volumen −25 %. Sin pista 48 h después de los 35 km: el martes es recuperación y el estímulo vivo pasa al jueves. 1 sesión de fuerza ligera.",
  ["F 5 + Fuerza ligera", "F 6 + 4 strides suaves (solo si no hay fatiga en muslos)", "F 4", "Controlado 8: 3 F + 3 km @6:00–6:10 + 2 F", "Descanso/movilidad", "L 22: 12 F + 6 @6:10 + 4 F"], [5, 6, 4, 8, 22]),
 ("Taper 2", "Volumen −40 %.",
  ["F 4 + Fuerza ligera (2×8)", "Pista 3×1000 m @5:15 rec 2' (7)", "F 4", "F 5 + 4 strides", "Descanso/movilidad", "L 16: 5 F + 6 @6:10 + 5 F"], [4, 7, 4, 5, 16]),
 ("Semana de carrera", "Descanso total el sábado. Sin sorpresas: cena y desayuno ya probados.",
  ["F 5 + activación (2×10 fuerza ligera)", "6: 3×1 km @6:10 rec 2'", "F 4", "F 4 + 4 strides", "Descanso + movilidad", "**MARATÓN CAF 42,195 km**"], [5, 6, 4, 4, 42.2]),
]

out = []
out.append("""# Plan de entrenamiento: Maratón CAF (21 de febrero de 2027)

**Versión 2.1 · 2026-10-15 (fecha oficial 21-feb-2027; 20 semanas; tirada máx. 35 km).** Meta: 6:10 min/km → ≈ 4:20:12. Inicio: lunes 5 de octubre de 2026. **Sábado siempre libre.**

> [!NOTE]
> **Fecha oficial: domingo 21 de febrero de 2027.** 20 semanas (5-oct-2026 → 21-feb-2027).
> **v2.1 (15-oct-2026):** ajuste biomecánico y anti-calambres del muslo derecho a partir de la telemetría completa del maratón de 2026: fuerza excéntrica de cuádriceps y aductores, técnica de bajada en tiradas largas, cuestas en fatiga, semana 18 más segura y estrategia con techo de FC y micro-pausas.

## Evaluación de la meta
- Tiempo estimado hoy (Garmin): **5:43:36**, reflejo del parón (VO2 máx 41).
- Proyección si cumples el plan: **4:25–4:40**; mejor estimación central ≈ **4:32 (6:27/km)**.
- Probabilidad de 6:10/km: **≈ 20–25 %** → meta **ambiciosa**.
- Objetivos: **A** 4:20–4:25 · **B** 4:30–4:35 (realista) · **C** < 4:40 (mejorar el 4:40:36 chip con un final sin calambres).
- Se recalcula tras el control 10K (sem. 8) y el 21K (sem. 14): 21K en ≤ 2:08 (6:05/km) sostiene A; ≤ 2:13 sostiene B.

## Leyenda y zonas (provisionales; recalibrar sem. 8)
| Código | Tipo | Ritmo | FC (Z) | Propósito |
|---|---|---|---|---|
| F | Fácil | 7:00–7:30 | 125–145 (Z2) | Base aeróbica y recuperación |
| L | Tirada larga | 6:50–7:20 (bloques @6:10) | Z2–Z3 | Resistencia, economía, simulacro |
| M | Medio/estable | 6:25 | 146–155 (Z3) | Umbral aeróbico |
| MP | Ritmo de maratón | **6:10** | 150–158 | Especificidad |
| Umbral | Tempo | 5:45 (5:35–5:50) | 158–168 (Z4) | Subir umbral de lactato |
| Pista/Intervalos | Series | 5:05–5:20 | 168–175 (Z5) | VO2 máx y economía |
| Strides | 20" progresivos | ~5:15, rec 60" caminando | — | Técnica y reclutamiento |

**Directrices obligatorias en tiradas largas (L) desde la semana 6:**
- **Bajadas:** prohibido alargar la zancada por encima de **0,98 m** o acelerar por debajo de **6:05/km**. Cadencia **162–165 ppm**, aterrizaje suave bajo el centro de masa para ahorrar cuádriceps. (En 2026 las bajadas de los km 10–15 se corrieron a 6:00–6:06 con zancada de 1,03 m.)
- **Cuestas en fatiga (sem. 9, 11, 13, 15 y 17):** incluir repechos deliberados en el último tercio de la tirada para replicar el tramo km 30–40 de Caracas (+208 m medidos por el reloj en 2026).

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
Descargas: semanas 4, 8, 12 y 16. Tras cada descarga el aumento es ≤ 10 % frente a la última semana de carga plena (el % de la tabla es contra la semana inmediata). Taper: semanas 18–20; la tirada de 35 km cae 3 semanas antes de la carrera.

## Fuerza (2 sesiones/semana; 1 en el taper)
Equipo: mancuernas, bandas y un escalón o banco. **Mié = Fuerza A** (≥24 h después de la calidad del martes); **Vie = Fuerza B** (sin correr). Si la calidad del jueves queda comprometida, baja a 2 series en A.
**Enfoque v2.1:** el calambre de 2026 fue en el **muslo derecho** (vasto medial y aductores), no en la pantorrilla. Por eso entran el control excéntrico del cuádriceps (bajadas) y la fuerza de aductores. El trabajo unilateral empieza siempre por la pierna más débil.

| Fase | Semanas | Series × reps | Carga | Descanso |
|---|---|---|---|---|
| Adaptación anatómica | 1–5 | 2–3 × 12–15 | RPE 6 | 60 s |
| Fuerza | 6–14 | 3–4 × 6–10 | RPE 7–8 (sin llegar al fallo) | 90–120 s |
| Mantenimiento | 15–17 | 2 × 6–8 | RPE 7 | 90 s |
| Taper | 18–20 | 1 sesión ligera, 2 × 8 | RPE 5–6 | 60 s |

### Fuerza A (Miércoles · piernas, cuádriceps excéntrico y glúteos)
| # | Ejercicio | Series × reps | Nota técnica | Enlace |
|---|---|---|---|---|
| 1 | Sentadilla goblet con mancuerna | 3 × 10 | Bajada en 3 s; rodillas alineadas con los pies | [MuscleWiki](https://musclewiki.com/es-es/exercise/dumbbell-goblet-pulse-squat?model=f) |
| 2 | Peso muerto rumano con mancuernas | 3 × 8–10 | Cadera atrás, rodillas semiflexionadas; foco en isquios | [MuscleWiki](https://musclewiki.com/es-es/exercise/dumbbell-romanian-deadlift?model=f) |
| 3 | Zancada inversa → sentadilla búlgara unilateral | 3 × 8 por pierna | Empezar siempre por la pierna más débil; rodilla estable sobre el 2.º dedo | [MuscleWiki](https://musclewiki.com/es-es/exercise/dumbbell-split-squat?model=f) |
| 4 | **NUEVO · Step-down excéntrico lento (bajada de escalón a una pierna)** | 3 × 8–10 por pierna | Bajar en 3–4 s tocando el suelo con el talón libre sin apoyar peso; la rodilla no colapsa hacia dentro. Blindaje del vasto medial para los −642 m de descenso | Pendiente: enlace directo no verificado ([MuscleWiki](https://musclewiki.com/es-es), buscar "step down") |
| 5 | Elevación de talones de pie con mancuerna | 3 × 12–15 | Subida explosiva, bajada en 3 s (todo el trabajo de pantorrilla del miércoles) | [MuscleWiki](https://musclewiki.com/es-es/exercise/standing-calf-raise?model=f) |

### Fuerza B (Viernes · aductores, estabilidad de cadera y core)
| # | Ejercicio | Series × reps | Nota técnica | Enlace |
|---|---|---|---|---|
| 1 | **NUEVO · Puente de Copenhague** (alternativa: puente de glúteos con compresión isométrica de aductores) | 3 × 20–30 s por lado (o 3 × 12 apretando un cojín/pelota entre las rodillas) | Empezar con la rodilla de arriba apoyada en el banco (palanca corta); progresar al pie. Blindaje directo del aductor derecho | Pendiente: enlace directo no verificado ([MuscleWiki](https://musclewiki.com/es-es), buscar "copenhagen") |
| 2 | Caminata lateral con banda elástica | 3 × 12 pasos por lado | Banda sobre rodillas; glúteo medio | [MuscleWiki](https://musclewiki.com/es-es/exercise/side-walks-resisted?model=f) |
| 3 | Plancha frontal de antebrazos | 3 × 35–45 s | Pelvis neutra, glúteos apretados | [MuscleWiki](https://musclewiki.com/es-es/exercise/forearm-plank?model=f) |
| 4 | Dead bug / bicho muerto | 3 × 10 por lado | Lumbar pegada al suelo | [MuscleWiki](https://musclewiki.com/es-es/exercise/dead-bug?model=f) |
| 5 | Elevación de talones sentado / rodilla flexionada (sóleo) | 3 × 15 | Mancuerna sobre la rodilla; rango completo y bajada lenta | Pendiente: enlace directo no verificado ([MuscleWiki](https://musclewiki.com/es-es), buscar "seated calf raise") |

> [!NOTE]
> Los enlaces directos que pasaste están en uso. Para el step-down, el puente de Copenhague y la elevación de talones sentado no encontré una URL de MuscleWiki que pueda verificar (el sitio bloquea la comprobación automática), así que dejé la portada como referencia. Si me pasas esos tres enlaces, los añado.
> Las rutinas "CAF - Fuerza A/B" que ya están en los relojes tienen la **versión anterior** de los ejercicios. Se actualizarán solo cuando lo confirmes.

## Movilidad y prevención (10 min, antes de correr o tras la fuerza)
1. Círculos de cadera y balanceo de piernas (adelante/lateral): 10 c/lado.
2. Zancada con rotación de torso: 6 c/lado.
3. Puente de glúteos isométrico: 2 × 20 s.
4. Estiramiento suave de flexores de cadera, gemelos y sóleo (pared): 30 s c/lado.
5. Rodillo o pelota en glúteo/cuádriceps (opcional): 1 min/zona.
6. Caminata lateral con banda: 1 × 10 c/lado.
Señales de alarma (dolor que cambia el paso, hinchazón, dolor nocturno): detener la calidad y consultar a un profesional.

## Estrategia de carrera (Maratón CAF)
Datos: ruta urbana certificada World Athletics/AIMS; ≈ **258 m** de ascenso y 242 m de descenso en 42K según soymaratonista.com. Tu reloj midió +640/−642 m en 2026; el Forerunner 55 no tiene altímetro barométrico, así que esa cifra probablemente está inflada, pero dónde están las bajadas y las subidas sí es fiable. Salidas matutinas ~5:50–6:05 a.m. (caf.com); horario 2027 por confirmar.

**Regla de oro km 10–25:** techo estricto de **FC < 156 lpm hasta el km 21** y **prohibido dejarse ir a 6:00/km en las bajadas** de la primera mitad. Beatriz (Forerunner 165, 133–144 lpm a este ritmo) actúa como ancla a **6:10–6:12/km**.

| Tramo | Ritmo | FC Oliver | Notas |
|---|---|---|---|
| Km 1–5 | 6:15–6:25 | < 150 | En 2026 saliste bien (32:50, 6:34/km de media); repítelo |
| Km 6–10 | 6:10–6:12 | < 154 | Asentarse detrás del ancla |
| Km 10–25 | 6:10–6:12 (bajadas ≥ 6:05) | **< 156 hasta el km 21** | Aquí se perdió la carrera en 2026: −188 m de bajada a 6:00–6:13 y FC de 152 a 163 (pico 174). Zancada ≤ 0,98 m, cadencia 162–165 |
| Km 25–30 | 6:10–6:15 | ≤ 160 | Mantener, no recuperar tiempo |
| Km 30–40 | 6:15–6:25 en subida | Por sensación | Tramo de subidas (+116 m entre los km 30 y 35). Acortar zancada y subir por esfuerzo, no por ritmo |
| Km 40–42,2 | Lo que quede | — | Solo apretar si el muslo está libre |

**Micro-pausas activas:** en 2026 corriste sin detenerte (4,3 s parado en 3 horas) hasta el km 30,2 y luego perdiste 7:29 parado por el calambre. En 2027: **15–20 s de caminata rápida controlada en cada puesto de hidratación cada 5 km desde el km 15** (km 15, 20, 25, 30, 35, 40) para tomar agua, gel o sales sin atragantarse. Son ~2 min en total, frente a los 7:29 de 2026, y descargan el cuádriceps antes de las subidas.

Plan B (4:30–4:35): 6:25–6:30 estable. Decide en el km 25 con FC y sensaciones del muslo derecho.
- **Hidratación:** 400–600 ml/h con sodio; beber en cada puesto durante la micro-pausa. En clima fresco, ajustar a sed.
- **Carbohidratos:** 60 g/h (gel cada 25–30 min + bebida deportiva) desde el km 5; probar hasta 75–90 g/h en las tiradas largas si el estómago lo tolera.
- **Calzado:** zapatillas ya usadas en ≥ 2 tiradas largas (> 20 km) y la ropa de carrera; no estrenar nada.
- **Simulacros:** semanas 9–11 (bloques MP), **semana 13 (26 km)**, **semana 14 (21K)**, **semana 15 (30 km: 14 @6:10)** y **semana 17 (35 km: 12 @6:10 entre los km 19 y 30)**, con micro-pausas, nutrición, calzado y salida a las 6 a.m.
- **Pre-carrera:** carga de carbohidratos 8–10 g/kg/día durante 36–48 h (viernes y sábado); desayuno 2–3 h antes; sin fibra excesiva.
Los números de nutrición son pautas generales de la literatura deportiva (ACSM/IOC); pruébalos en entrenamiento y ajusta a tu tolerancia. No es consejo médico.

## Prevención de calambres (diagnóstico del maratón 2026)
**Qué pasó:** calambre severo desde el **km 30,2** solo en el **muslo derecho** (ambas caras, más intenso en la interna: vasto medial y aductores). Las pantorrillas no se afectaron. El muslo se soltó en pocos días sin dolor residual, lo que encaja con un **calambre asociado al ejercicio por fatiga neuromuscular (EAMC)** y no con una rotura ni con un fallo sistémico de electrolitos.
**Por qué:** ritmo bien controlado hasta el km 30,22 (3:10:06, ~6:17/km, cadencia 160–162). La fatiga se generó antes:
1. **Daño excéntrico en bajadas (km 10–25):** −417 m acumulados antes del km 30, con las bajadas de los km 10–15 (−110 m) corridas a 6:00–6:06 con zancada de 1,03 m y las de los km 20–25 (−78 m) a 6:11–6:13. La FC subió de 152 a 163 (pico de 174 cerca del km 25).
2. **Gatillo en las subidas (km 30–35):** +116 m (vueltas de +42 y +40 m) con el cuádriceps fatigado sobrecargaron el vasto medial y los aductores derechos.
3. **Coste real:** 7:29 detenido después del km 30,2, aunque en movimiento sostuviste 6:42/km los últimos 12,4 km y cerraste los últimos 200 m a 6:02 y 166 ppm.

**Plan de acción:**
1. **Fuerza excéntrica de cuádriceps** (step-down lento, goblet con bajada en 3 s) y **fuerza de aductores** (puente de Copenhague) cada semana.
2. **Técnica de bajada** en todas las tiradas largas desde la semana 6 (zancada ≤ 0,98 m, ≥ 6:05/km, 162–165 ppm).
3. **Cuestas en fatiga** en el último tercio de las tiradas de las semanas 9, 11, 13, 15 y 17.
4. **Techo de FC < 156 hasta el km 21** y micro-pausas activas desde el km 15.
5. **Tiradas largas progresivas hasta 35 km** (sem. 17) con bloques MP en la segunda mitad.
6. Carbohidratos (60–90 g/h) y sodio (300–600 mg/h) practicados en tiradas ≥ 26 km. Ayudan, aunque no fueron la causa principal.
7. Si aparece un calambre: bajar ritmo, caminar 1–2 min, estirar suave y retomar.
Si los calambres se repiten fuera de la carrera o hay otros síntomas, consulta a un profesional de la salud.

## Carreras de control
- **Dom 29-nov (sem. 8): 10K.** Objetivo ≤ 55:00 (5:30/km) para sostener la meta B/A.
- **Dom 10-ene (sem. 14): 21K.** Objetivo ≤ 2:08 (A) / ≤ 2:13 (B).
Elegiremos carreras reales cuando haya calendario; si no existen, hacerlas como pruebas contrarreloj en pista o asfalto.
""")

Path("/home/ocarreno/dev/maratonCAF/plan.md").write_text("\n".join(out), encoding="utf-8")
for n, mon, t, fase in resumen:
    print(n, mon, t, fase)
