from django.core.management import execute_from_command_line

import os
import sys
import threading
import requests
import time
import random
from datetime import datetime

def generador_ocupaciones():    
    # Configura los parámetros para el generador de ocupaciones
    hora_inicial_dia = datetime.strptime('08:00:00', '%H:%M:%S').time()
    hora_final_dia = datetime.strptime('22:00:00', '%H:%M:%S').time()

    # Lanza el generador de ocupaciones como un subproceso
    while True:
        # Obtiene todos los IDs de estacionamiento de la base de datos
        id_estacionamiento = random.randint(0, 13)
        
        # Supongamos que la capacidad máxima es de 100 espacios de estacionamiento
        ocupacion_maxima = random.randint(0, 1000)
        
        ocupacion_actual = random.randint(0, ocupacion_maxima)
        
        # Crea los datos de ocupación para enviar al servidor Django
        data = {
            'parking_id': id_estacionamiento,
            'occupancy_current': ocupacion_actual,
            'occupancy_max': ocupacion_maxima
        }
        
        # Envía la solicitud POST al servidor Django para registrar la ocupación
        response = requests.post('http://127.0.0.1:8000/register_occupancy/', json=data)
        
        # Verifica si la solicitud fue exitosa
        if response.status_code == 201:
            print(f'Ocupación registrada para el estacionamiento {id_estacionamiento}')
        else:
            print(f'Error al registrar ocupación para el estacionamiento {id_estacionamiento}')
            
        # Calcula el tiempo de espera aleatorio
        now = datetime.now().time()
        if hora_inicial_dia <= now <= hora_final_dia:
            tiempo_espera = random.uniform(0, 60)  # Aleatorio entre 0 y 1 minuto
        else:
            tiempo_espera = random.uniform(0, 300)  # Aleatorio entre 0 y 5 minutos
        
        # Espera el tiempo aleatorio antes de generar nuevas ocupaciones
        time.sleep(tiempo_espera)

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AIbarra_TFG.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Inicia el subproceso para el generador de ocupaciones
    thread_generador = threading.Thread(target=generador_ocupaciones)
    thread_generador.start()

    execute_from_command_line(sys.argv)

    # Termina el subproceso del generador de ocupaciones al finalizar la ejecución
    thread_generador.join()

if __name__ == "__main__":
    main()
