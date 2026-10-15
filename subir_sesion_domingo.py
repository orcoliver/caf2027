#!/usr/bin/env python3
"""Sube y programa el entrenamiento del domingo 11-oct-2026 en los relojes de Oliver y Beatriz."""
import sys
from garminconnect import Garmin
from garminconnect.workout import (
    RunningWorkout,
    WorkoutSegment,
    create_targeted_distance_interval_step,
    PaceTarget,
    pace_to_mps
)

FECHA_SESION = "2026-10-11"
TITULO = "S1D7 - Tirada Larga 10K Fácil"
DESC = "Tirada larga base aeróbica 10 km a ritmo fácil (7:00 - 7:30 min/km). Respiración cómoda."

def build_workout():
    slow = pace_to_mps(7, 30, 'km')
    fast = pace_to_mps(7, 0, 'km')
    target = PaceTarget(lower_limit=slow, upper_limit=fast)
    step = create_targeted_distance_interval_step(10000.0, 1, target)
    segment = WorkoutSegment(
        segmentOrder=1,
        sportType={'sportTypeId': 1, 'sportTypeKey': 'running'},
        workoutSteps=[step]
    )
    return RunningWorkout(
        workoutName=TITULO,
        description=DESC,
        estimatedDurationInSecs=4350,
        workoutSegments=[segment]
    )

def upload_and_schedule(token_path, nombre_atleta):
    print(f"\n==========================================")
    print(f"Procesando para {nombre_atleta} ({token_path})")
    print(f"==========================================")
    g = Garmin()
    g.login(token_path)
    
    workout = build_workout()
    print(f"1. Subiendo entrenamiento: '{workout.workoutName}'...")
    res_upload = g.upload_running_workout(workout)
    workout_id = res_upload.get("workoutId")
    print(f"   -> Subido con éxito. Workout ID: {workout_id}")
    
    print(f"2. Programando en el calendario para {FECHA_SESION}...")
    res_schedule = g.schedule_workout(workout_id, FECHA_SESION)
    print(f"   -> Programado en calendario: {res_schedule}")
    
    print(f"3. Enviando al dispositivo...")
    try:
        res_push = g.push_workout_to_device(workout_id)
        print(f"   -> Enviado al reloj: {res_push}")
    except Exception as e:
        print(f"   -> Aviso al enviar al dispositivo (se sincronizará automáticamente por la app): {e}")

if __name__ == "__main__":
    # 1. Oliver Carreño (FR 55)
    upload_and_schedule("/home/ocarreno/.garminconnect", "Oliver Carreño (Forerunner 55)")
    
    # 2. Beatriz Gonzalez (FR 165)
    upload_and_schedule("/home/ocarreno/.garminconnect_esposa", "Beatriz Gonzalez (Forerunner 165)")
    print("\nProceso finalizado para ambos dispositivos.")
