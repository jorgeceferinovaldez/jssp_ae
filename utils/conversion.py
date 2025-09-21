import os
import sys

def convert_jsplib_to_custom_format(jsplib_file, output_file):
    """
    Convierte formato JSPLIB estándar al formato personalizado
    Formato de salida:
    - Primera línea: upper bound (opcional)
    - Segunda línea: lower bound (opcional)  
    - Líneas siguientes: tiempos por máquina
    """
    
    with open(jsplib_file, 'r') as f:
        lines = f.readlines()
    
    # Obtener dimensiones
    dimensions = lines[4].strip().split()
    num_jobs = int(dimensions[0])
    num_machines = int(dimensions[1])
    
    # Leer datos de jobs
    jobs_data = []
    for i in range(5, 5 + num_jobs):
        line_data = list(map(int, lines[i].strip().split()))
        jobs_data.append(line_data)
    
    # Reorganizar: de [job][máquina, tiempo] a [máquina][job][tiempo]
    machine_times = [[] for _ in range(num_machines)]
    
    for job_idx, job in enumerate(jobs_data):
        for op_idx in range(0, len(job), 2):
            machine = job[op_idx]
            time = job[op_idx + 1]
            machine_times[machine].append(time)
    
    # Escribir en formato personalizado
    with open(output_file, 'w') as f:
        # Escribir bounds (puedes ajustar estos valores)
        f.write("1000\n")  # Upper bound placeholder
        f.write("800\n")   # Lower bound placeholder
        
        # Escribir tiempos por máquina
        for machine_idx in range(num_machines):
            line = " ".join(f"{time:3}" for time in machine_times[machine_idx])
            f.write(line + "\n")

def convert_multiple_instances():
    """Convierte todas las instancias SWV"""
    instances = [
        "swv06", "swv07", "swv08", "swv09", "swv10",
        "swv11", "swv12", "swv13", "swv14", "swv15"
    ]
    
    for instance in instances:
        input_file = f"instances/{instance}"
        output_file = f"converted_{instance}.txt"
        
        if os.path.exists(input_file):
            convert_jsplib_to_custom_format(input_file, output_file)
            print(f"Converted {instance} -> {output_file}")
        else:
            print(f"File not found: {input_file}")

# Conversión individual
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = f"converted_{os.path.basename(input_file)}.txt"
        convert_jsplib_to_custom_format(input_file, output_file)
        print(f"Conversion complete: {output_file}")
    else:
        # Convertir todas las instancias SWV
        convert_multiple_instances()