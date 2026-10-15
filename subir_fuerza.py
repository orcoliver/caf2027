#!/usr/bin/env python3
"""Sube los entrenamientos estructurados de Fuerza A y Fuerza B a las cuentas Garmin de Oliver y Beatriz."""
from garminconnect import Garmin
import garminconnect.workout as gw

def build_fuerza_a():
    steps = []
    order = 1
    # 1. Goblet Squat (3 x 10, rest 60s)
    steps.append(gw.create_strength_set('SQUAT', order, sets=3, reps=10, rest_seconds=60.0, exercise_name='GOBLET_SQUAT'))
    order += 3
    # 2. Romanian Deadlift (3 x 10, rest 60s)
    steps.append(gw.create_strength_set('DEADLIFT', order, sets=3, reps=10, rest_seconds=60.0, exercise_name='ROMANIAN_DEADLIFT'))
    order += 3
    # 3. Dumbbell Lunge (3 x 8, rest 60s)
    steps.append(gw.create_strength_set('LUNGE', order, sets=3, reps=8, rest_seconds=60.0, exercise_name='ALTERNATING_DUMBBELL_LUNGE'))
    order += 3
    # 4. Glute Bridge (3 x 12, rest 60s)
    steps.append(gw.create_strength_set('BANDED_EXERCISES', order, sets=3, reps=12, rest_seconds=60.0, exercise_name='GLUTE_BRIDGE'))
    order += 3
    # 5. Calf Raise (3 x 15, rest 45s)
    steps.append(gw.create_strength_set('CALF_RAISE', order, sets=3, reps=15, rest_seconds=45.0, exercise_name='_3_WAY_WEIGHTED_CALF_RAISE'))
    
    seg = gw.WorkoutSegment(
        segmentOrder=1,
        sportType={'sportTypeId': 3, 'sportTypeKey': 'strength_training'},
        workoutSteps=steps
    )
    return gw.StrengthWorkout(
        workoutName='CAF - Fuerza A (Piernas y Glúteos)',
        description='Sentadilla Goblet, Peso Muerto Rumano, Zancadas, Glute Bridge y Gemelos.',
        estimatedDurationInSecs=1500,
        workoutSegments=[seg]
    )

def build_fuerza_b():
    steps = []
    order = 1
    # 1. Step Climb / Step up (3 x 10, rest 60s)
    steps.append(gw.create_strength_set('CRUNCH', order, sets=3, reps=10, rest_seconds=60.0, exercise_name='WEIGHTED_STEP_CLIMB'))
    order += 3
    # 2. Lateral band walk (3 x 12, rest 45s)
    steps.append(gw.create_strength_set('BANDED_EXERCISES', order, sets=3, reps=12, rest_seconds=45.0, exercise_name='LATERAL_BAND_WALKS'))
    order += 3
    # 3. Plank (3 x 1, rest 45s)
    steps.append(gw.create_strength_set('PLANK', order, sets=3, reps=1, rest_seconds=45.0, exercise_name='PLANK'))
    order += 3
    # 4. Side Plank (3 x 1, rest 45s)
    steps.append(gw.create_strength_set('PLANK', order, sets=3, reps=1, rest_seconds=45.0, exercise_name='SIDE_PLANK'))
    order += 3
    # 5. Dead bug (3 x 10, rest 45s)
    steps.append(gw.create_strength_set('HIP_STABILITY', order, sets=3, reps=10, rest_seconds=45.0, exercise_name='DEAD_BUG'))
    order += 3
    # 6. Single leg calf raise (2 x 12, rest 45s)
    steps.append(gw.create_strength_set('CALF_RAISE', order, sets=2, reps=12, rest_seconds=45.0, exercise_name='_3_WAY_SINGLE_LEG_CALF_RAISE'))
    
    seg = gw.WorkoutSegment(
        segmentOrder=1,
        sportType={'sportTypeId': 3, 'sportTypeKey': 'strength_training'},
        workoutSteps=steps
    )
    return gw.StrengthWorkout(
        workoutName='CAF - Fuerza B (Core y Estabilidad)',
        description='Step-up, Caminata lateral con banda, Plancha, Plancha lateral, Dead bug y Pantorrillas.',
        estimatedDurationInSecs=1500,
        workoutSegments=[seg]
    )

def upload_to_account(token_path, athlete_name):
    print(f"\n==========================================")
    print(f"Subiendo sesiones de Fuerza para: {athlete_name}")
    print(f"==========================================")
    g = Garmin()
    g.login(token_path)
    
    # Subir Fuerza A
    wo_a = build_fuerza_a()
    res_a = g.upload_strength_workout(wo_a)
    id_a = res_a.get("workoutId")
    print(f"-> Fuerza A subida. Workout ID: {id_a}")
    try:
        g.push_workout_to_device(id_a)
        print(f"   Enviada al dispositivo.")
    except Exception as e:
        print(f"   Aviso push: {e}")
        
    # Subir Fuerza B
    wo_b = build_fuerza_b()
    res_b = g.upload_strength_workout(wo_b)
    id_b = res_b.get("workoutId")
    print(f"-> Fuerza B subida. Workout ID: {id_b}")
    try:
        g.push_workout_to_device(id_b)
        print(f"   Enviada al dispositivo.")
    except Exception as e:
        print(f"   Aviso push: {e}")

if __name__ == "__main__":
    upload_to_account("/home/ocarreno/.garminconnect", "Oliver Carreño (Forerunner 55)")
    upload_to_account("/home/ocarreno/.garminconnect_esposa", "Beatriz Gonzalez (Forerunner 165)")
    print("\nSesiones de fuerza disponibles en ambas bibliotecas.")
