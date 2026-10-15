#!/usr/bin/env python3
"""Crea, agenda en el calendario y envía al reloj las 6 actividades de la Semana 2 (12 al 18 oct 2026)
para Oliver Carreño (Forerunner 55) y Beatriz Gonzalez (Forerunner 165). Sábado libre garantizado."""
import time
from garminconnect import Garmin
import garminconnect.workout as gw

def create_easy_run(name, dist_km, desc):
    slow = gw.pace_to_mps(7, 30, 'km')
    fast = gw.pace_to_mps(7, 0, 'km')
    target = gw.PaceTarget(lower_limit=slow, upper_limit=fast)
    step = gw.create_targeted_distance_interval_step(float(dist_km * 1000), 1, target)
    seg = gw.WorkoutSegment(
        segmentOrder=1,
        sportType={'sportTypeId': 1, 'sportTypeKey': 'running'},
        workoutSteps=[step]
    )
    est_sec = int(dist_km * 440)
    return gw.RunningWorkout(
        workoutName=name,
        description=desc,
        estimatedDurationInSecs=est_sec,
        workoutSegments=[seg]
    )

def create_run_with_strides(name, dist_km, num_strides, desc):
    slow = gw.pace_to_mps(7, 30, 'km')
    fast = gw.pace_to_mps(7, 0, 'km')
    target = gw.PaceTarget(lower_limit=slow, upper_limit=fast)
    step1 = gw.create_targeted_distance_interval_step(float(dist_km * 1000), 1, target)
    
    stride_fast = gw.pace_to_mps(5, 10, 'km')
    stride_slow = gw.pace_to_mps(5, 30, 'km')
    stride_target = gw.PaceTarget(lower_limit=stride_slow, upper_limit=stride_fast)
    
    stride_step = gw.create_targeted_interval_step(20.0, 3, stride_target)
    recovery_step = gw.create_recovery_step(60.0, 4)
    repeat = gw.create_repeat_group(num_strides, [stride_step, recovery_step], 2)
    
    seg = gw.WorkoutSegment(
        segmentOrder=1,
        sportType={'sportTypeId': 1, 'sportTypeKey': 'running'},
        workoutSteps=[step1, repeat]
    )
    est_sec = int(dist_km * 440 + num_strides * 80)
    return gw.RunningWorkout(
        workoutName=name,
        description=desc,
        estimatedDurationInSecs=est_sec,
        workoutSegments=[seg]
    )

def schedule_week2_for_user(token_path, user_name, fuerza_a_id, fuerza_b_id):
    print(f"\n=======================================================")
    print(f"Programando Semana 2 para: {user_name} ({token_path})")
    print(f"=======================================================")
    g = Garmin()
    g.login(token_path)
    
    # Definición del calendario de la Semana 2
    # Formato: (fecha, dia, tipo, builder/id, nombre)
    calendar_plan = [
        ("2026-10-12", "Lun", "run", 
         lambda: create_easy_run("S2D1 - F 4K Fácil", 4.0, "Rodaje suave regenerativo post-tirada (7:00-7:30 min/km).")),
        
        ("2026-10-13", "Mar", "run", 
         lambda: create_run_with_strides("S2D2 - F 6K + 6 Strides", 6.0, 6, "6 km fácil (7:00-7:30) + 6 rectas progresivas de 20s (85-90%) con 60s caminando.")),
        
        ("2026-10-14", "Mié", "run", 
         lambda: create_easy_run("S2D3 - F 4K Fácil", 4.0, "4 km regenerativo (7:00-7:30 min/km) previo o posterior a sesión de Fuerza A.")),
        
        ("2026-10-14", "Mié", "strength", fuerza_a_id),
        
        ("2026-10-15", "Jue", "run", 
         lambda: create_easy_run("S2D4 - F 5K Fácil", 5.0, "Rodaje aeróbico continuo y cómodo (7:00-7:30 min/km).")),
        
        ("2026-10-16", "Vie", "strength", fuerza_b_id),
        
        # SÁBADO 2026-10-17: DESCANSO ABSOLUTO (0 PROGRAMACIÓN)
        
        ("2026-10-18", "Dom", "run", 
         lambda: create_easy_run("S2D7 - Tirada Larga 11K Fácil", 11.0, "Tirada larga semanal 11 km a ritmo fácil (7:00-7:30 min/km). Llevar hidratación."))
    ]
    
    for item in calendar_plan:
        cdate = item[0]
        dia = item[1]
        kind = item[2]
        
        if kind == "run":
            wo_obj = item[3]()
            print(f"[{cdate} {dia}] Subiendo carrera: '{wo_obj.workoutName}'...")
            res_up = g.upload_running_workout(wo_obj)
            wo_id = res_up.get("workoutId")
            print(f"  -> Creado Workout ID: {wo_id}")
            time.sleep(1)
        elif kind == "strength":
            wo_id = item[3]
            print(f"[{cdate} {dia}] Agendando Fuerza existente ID: {wo_id}...")
        
        # Agendar en calendario
        res_sched = g.schedule_workout(wo_id, cdate)
        sched_id = res_sched.get("workoutScheduleId")
        print(f"  -> Agendado en calendario para {cdate} (Schedule ID: {sched_id})")
        
        # Enviar al dispositivo
        try:
            res_push = g.push_workout_to_device(wo_id)
            print(f"  -> Enviado al reloj ✔")
        except Exception as e:
            print(f"  -> Aviso push: {e}")
            
        time.sleep(1)

if __name__ == "__main__":
    # IDs de fuerza guardados previamente:
    # Oliver: Fuerza A (1723548953), Fuerza B (1723548962)
    # Beatriz: Fuerza A (1723548970), Fuerza B (1723548974)
    
    schedule_week2_for_user("/home/ocarreno/.garminconnect", "Oliver Carreño (Forerunner 55)", 1723548953, 1723548962)
    schedule_week2_for_user("/home/ocarreno/.garminconnect_esposa", "Beatriz Gonzalez (Forerunner 165)", 1723548970, 1723548974)
    print("\n¡Semana 2 completamente programada y sincronizada para ambos!")
