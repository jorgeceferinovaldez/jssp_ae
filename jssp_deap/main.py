import os
import random
import numpy as np
from deap import base, creator, tools
import copy
import time


# Lectura de parámetros desde DATOS.DAT
def leer_parametros(archivo="DATOS.DAT"):
    """
    Lee parámetros de configuración desde un archivo.
    Args:
        archivo (str, optional): Ruta del archivo de parámetros. Por defecto "DATOS.DAT".
    Returns:
        dict: Diccionario con los parámetros leídos:
            - cantcorr (int): Número de corridas
            - pmutacion (float): Probabilidad de mutación
            - pcross (float): Probabilidad de crossover
            - maxgen (int): Número máximo de generaciones
            - popsize (int): Tamaño de la población
    Raises:
        FileNotFoundError: Si el archivo especificado no existe
        ValueError: Si los datos en el archivo no tienen el formato esperado
    """

    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    parametros = {
        'cantcorr': int(lineas[0].strip()),
        'pmutacion': float(lineas[1].strip()),
        'pcross': float(lineas[2].strip()),
        'maxgen': int(lineas[3].strip()),
        'popsize': int(lineas[4].strip())
    }
    
    print("- Parámetros cargados:")
    print(f"   Corridas: {parametros['cantcorr']}")
    print(f"   P. Mutación: {parametros['pmutacion']}")
    print(f"   P. Crossover: {parametros['pcross']}")
    print(f"   Max Generaciones: {parametros['maxgen']}")
    print(f"   Tamaño Población: {parametros['popsize']}")
    
    return parametros

def leer_instancia_jsp(archivo):
    """
    Lee y procesa un archivo de instancia JSP (Job Shop Scheduling Problem).
    Args:
        archivo (str): Ruta al archivo de texto que contiene los datos de la instancia JSP.
    Returns:
        dict: Un diccionario con la información estructurada de la instancia que contiene:
            - nombre (str): Nombre de la instancia (derivado del nombre del archivo)
            - jobs (int): Número de jobs en la instancia
            - maquinas (int): Número de máquinas en la instancia
            - tiempos (list): Matriz de tiempos de procesamiento (jobs × operaciones)
            - orden_maquinas (list): Matriz de secuencia de máquinas por job
            - upper_bound (int): Cota superior del makespan
            - lower_bound (int): Cota inferior del makespan
    El formato esperado del archivo es:
        Línea 1: upper bound (entero)
        Línea 2: lower bound (entero)
        Líneas siguientes: matriz de tiempos (máquinas × jobs)
    """
    
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    upper_bound = int(lineas[0].strip())
    lower_bound = int(lineas[1].strip())
    
    # Leer matriz de tiempos (máquinas × jobs)
    tiempos_maquinas_jobs = []
    for i in range(2, len(lineas)):
        linea = lineas[i].strip()
        if linea:
            tiempos = [int(x) for x in linea.split()]
            if tiempos:
                tiempos_maquinas_jobs.append(tiempos)
    
    num_maquinas = len(tiempos_maquinas_jobs)
    num_jobs = len(tiempos_maquinas_jobs[0])
    
    # Convertir a formato jobs × operaciones
    tiempos_jobs_ops = []
    for job in range(num_jobs):
        tiempos_job = []
        for maquina in range(num_maquinas):
            tiempos_job.append(tiempos_maquinas_jobs[maquina][job])
        tiempos_jobs_ops.append(tiempos_job)
    
    # Orden de máquinas secuencial
    orden_maquinas = [list(range(num_maquinas)) for _ in range(num_jobs)]
    
    instancia = {
        'nombre': archivo.split('/')[-1].replace('.txt', ''),
        'jobs': num_jobs,
        'maquinas': num_maquinas,
        'tiempos': tiempos_jobs_ops,
        'orden_maquinas': orden_maquinas,
        'upper_bound': upper_bound,
        'lower_bound': lower_bound
    }
    
    print(f"- Instancia cargada: {instancia['nombre']}")
    print(f"   Jobs: {num_jobs}, Máquinas: {num_maquinas}")
    print(f"   Bounds: [{lower_bound}, {upper_bound}]")
    
    return instancia

# Configuración de deap para el problema JSP
def configurar_deap(instancia):
    """
    Configures DEAP framework for Job Shop Scheduling Problem (JSSP) optimization.
    This function sets up the DEAP evolutionary algorithm components including:
    - Custom fitness and individual classes
    - Population initialization
    - Evaluation function using correct JSP decoder
    - Genetic operators (crossover and mutation)
    Args:
        instancia (dict): JSSP instance dictionary containing:
            - 'jobs': Number of jobs
            - 'maquinas': Number of machines
    Returns:
        toolbox: DEAP toolbox object configured for JSSP optimization with:
            - individual creation method
            - population initialization
            - evaluation function
            - crossover operator (order_crossover_deap)
            - mutation operator (mutacion_shift_deap)
    Note:
        Clears any previous DEAP configuration before setting up new components.
        Individual representation: permutation of jobs repeated machines times.
        Evaluation uses decodificar_jsp_correcto function to calculate makespan.
    """
    
    # Limpiar configuración previa
    if hasattr(creator, "FitnessMin"):
        del creator.FitnessMin
    if hasattr(creator, "Individual"):
        del creator.Individual
    
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    
    def crear_individuo():
        """
        Crea un individuo para el problema JSSP.
        Genera una secuencia aleatoria de trabajos donde cada trabajo aparece
        tantas veces como máquinas tenga la instancia, y luego la mezcla aleatoriamente.
        Returns:
            creator.Individual: Un individuo con una secuencia de trabajos válida
            para el problema JSSP especificado por la instancia.
        """
        
        secuencia = []
        for job in range(instancia['jobs']):
            secuencia.extend([job] * instancia['maquinas'])
        random.shuffle(secuencia)
        return creator.Individual(secuencia)
    
    toolbox.register("individual", crear_individuo)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    def evaluar_jsp(individual):
        """
        Evalúa un individuo para el problema Job Shop Scheduling (JSP).
        Esta función toma un individuo (representando una solución al problema JSP)
        y calcula su makespan (tiempo total de finalización) utilizando el decodificador.
        Args:
            individual: Representación de la solución al problema JSP, típicamente
                       una estructura de datos que contiene la secuencia de operaciones.
        Returns:
            tuple: Una tupla que contiene el makespan calculado (valor float).
                   En caso de error durante la evaluación, retorna (infinito,).
        Raises:
            Propaga cualquier excepción que ocurra durante la decodificación,
            pero captura y maneja internamente retornando infinito en caso de error.
        """
        
        try:
            makespan = decodificar_jsp_correcto(individual, instancia)
            return makespan,
        except Exception as e:
            print(f"Error en evaluación: {e}")
            return float('inf'),
    
    toolbox.register("evaluate", evaluar_jsp)
    toolbox.register("mate", order_crossover_deap)
    toolbox.register("mutate", mutacion_shift_deap, pmut=0.05)
    
    return toolbox

def decodificar_jsp_correcto(individual, instancia):
    """
    Decodifica un individuo JSP (Job Shop Problem) en un valor de makespan.
    Esta función simula la programación de trabajos en máquinas basándose en el
    individuo dado (secuencia de trabajos) y los datos de la instancia. Calcula
    el makespan mediante el seguimiento de tiempos de finalización de trabajos
    y disponibilidad de máquinas.
    Args:
        individual (list): Secuencia de IDs de trabajos que representa el orden de procesamiento.
        instancia (dict): Diccionario con datos de la instancia JSP con claves:
            - 'jobs' (int): Número de trabajos
            - 'maquinas' (int): Número de máquinas
            - 'tiempos' (list): Lista 2D de tiempos de procesamiento [trabajo][operación]
            - 'orden_maquinas' (list): Lista 2D de asignaciones de máquinas [trabajo][operación]
    Returns:
        int: El makespan (tiempo máximo de finalización) del programa.
    Note:
        El individuo debe contener IDs de trabajos en el orden en que deben procesarse.
        Cada ID de trabajo debe aparecer exactamente tantas veces como operaciones tenga.
        Si una operación excede las máquinas disponibles, se omite.
    """
    
    jobs = instancia['jobs']
    maquinas = instancia['maquinas']
    tiempos = instancia['tiempos']
    orden_maquinas = instancia['orden_maquinas']
    
    # Inicializar contadores de operaciones por job
    job_op_count = [0] * jobs
    
    # Tiempos de finalización por job y disponibilidad de máquinas
    job_end_time = [0] * jobs
    machine_available = [0] * maquinas
    
    # Procesar cada job en la secuencia
    for job_id in individual:
        # Obtener la operación actual de este job
        op_id = job_op_count[job_id]
        
        # Verificar que no excedamos el número de operaciones
        if op_id >= maquinas:
            continue
        
        # Obtener máquina y tiempo de procesamiento
        machine_id = orden_maquinas[job_id][op_id]
        processing_time = tiempos[job_id][op_id]
        
        # Tiempo de inicio: max(fin del job, disponibilidad de máquina)
        start_time = max(job_end_time[job_id], machine_available[machine_id])
        end_time = start_time + processing_time
        
        # Actualizar tiempos
        job_end_time[job_id] = end_time
        machine_available[machine_id] = end_time
        job_op_count[job_id] += 1
    
    # Makespan = máximo tiempo de finalización
    makespan = max(job_end_time)
    return makespan


# Operadores genéticos adaptados 
def order_crossover_deap(ind1, ind2):
    """
    Operador Order Crossover (OX) para individuos DEAP.
    Este operador de crossover preserva el orden relativo de los genes de los padres.
    Funciona seleccionando un segmento aleatorio de un padre y copiándolo al hijo,
    luego llenando las posiciones restantes con genes del otro padre en el orden
    en que aparecen, saltando los genes que ya fueron copiados del primer padre.
    Args:
        ind1: Primer individuo padre
        ind2: Segundo individuo padre
    Returns:
        tuple: Dos individuos hijos (child1, child2) resultantes del crossover
    Algoritmo:
    1. Selecciona dos puntos de crossover aleatorios
    2. Copia el segmento entre estos puntos del parent1 a child1 y del parent2 a child2
    3. Para cada hijo, llena las posiciones restantes con genes del otro padre:
       - Cuenta cuántos de cada gen se necesitan para completar el hijo
       - Toma genes del otro padre en orden, usando solo aquellos que aún se necesitan
       - Llena las posiciones vacías secuencialmente con estos genes
    Nota: Asume que ambos padres tienen la misma longitud y contienen el mismo conjunto de genes
    (posiblemente con diferentes frecuencias/órdenes).
    """
    
    size = len(ind1)
    child1 = creator.Individual([None] * size)
    child2 = creator.Individual([None] * size)
    
    # Puntos de corte
    punto1, punto2 = sorted(random.sample(range(size), 2))
    
    # Copiar segmento
    child1[punto1:punto2] = ind1[punto1:punto2]
    child2[punto1:punto2] = ind2[punto1:punto2]
    
    def llenar_hijo(child, parent_source, other_parent, p1, p2):
        """
        Completa un hijo en un algoritmo de cruce de orden preservado (POX).
        Esta función implementa el mecanismo de llenado para operadores de cruce
        que preservan el orden relativo de los elementos, como POX (Precedence
        Preservative Crossover). Copia un segmento de un padre y completa las
        posiciones restantes con elementos del otro padre manteniendo su orden
        relativo original.
        Args:
            child (list): Lista del hijo que está siendo construido, con algunos
                elementos ya copiados (posiciones p1 a p2-1) y el resto
                como None.
            parent_source (list): Padre de donde se copió el segmento inicial.
            other_parent (list): Otro padre de donde se tomarán los elementos
                    para completar el hijo.
            p1 (int): Índice de inicio del segmento copiado (inclusive).
            p2 (int): Índice de fin del segmento copiado (exclusive).
        Returns:
            None: La función modifica la lista child in-place.
        Steps:
            1. Cuenta la frecuencia de genes en el segmento copiado
            2. Determina la frecuencia total requerida basada en parent_source
            3. Calcula los genes faltantes necesarios
            4. Extrae genes del otro padre respetando el orden y las necesidades
            5. Completa las posiciones vacías del hijo
        """
        # Contar cuántos de cada gene están en el segmento copiado
        copied_count = {}
        for i in range(p1, p2):
            gene = child[i]
            copied_count[gene] = copied_count.get(gene, 0) + 1
        
        # Contar cuántos de cada gene debe tener el hijo en total
        total_count = {}
        for gene in parent_source:
            total_count[gene] = total_count.get(gene, 0) + 1
        
        # Calcular cuántos de cada gene faltan por agregar
        needed_count = {}
        for gene, total in total_count.items():
            needed = total - copied_count.get(gene, 0)
            if needed > 0:
                needed_count[gene] = needed
        
        # Tomar genes del otro padre en orden, respetando lo que falta
        available = []
        for gene in other_parent:
            if needed_count.get(gene, 0) > 0:
                available.append(gene)
                needed_count[gene] -= 1
        
        # Llenar posiciones vacías
        idx = 0
        for i in range(size):
            if child[i] is None:
                child[i] = available[idx]
                idx += 1
    
    llenar_hijo(child1, ind1, ind2, punto1, punto2)
    llenar_hijo(child2, ind2, ind1, punto1, punto2)
    
    return child1, child2

def mutacion_shift_deap(individual, pmut=0.05):
    """
    Realiza una mutación de desplazamiento en un individuo con una probabilidad dada.
    Este operador de mutación selecciona un segmento contiguo aleatorio del individuo,
    lo remueve, y lo inserta en una posición aleatoria diferente. La operación se
    realiza con probabilidad pmut, y solo si el individuo tiene longitud > 3.
    Args:
        individual (list): El cromosoma individual a mutar
        pmut (float): Probabilidad de mutación (por defecto: 0.05)
    Returns:
        tuple: Una tupla que contiene el individuo mutado
    """
    
    if random.random() < pmut and len(individual) > 3:
        size = len(individual)
        
        # Seleccionar segmento aleatorio
        seg_len = random.randint(1, min(5, size // 2))
        start = random.randint(0, size - seg_len)
        end = start + seg_len
        
        # Extraer segmento
        segment = individual[start:end]
        remaining = individual[:start] + individual[end:]
        
        # Insertar en nueva posición
        insert_pos = random.randint(0, len(remaining))
        individual[:] = remaining[:insert_pos] + segment + remaining[insert_pos:]
    
    return individual,

# Algoritmo Evosocial 
def calcular_error_relativo(makespan, lower_bound):
    """
    Calcula el error relativo porcentual entre el makespan y un límite inferior.
    Args:
        makespan (float): El tiempo total de finalización de la programación.
        lower_bound (float): El límite inferior teórico o valor de referencia.
    Returns:
        float: El error relativo porcentual calculado como:
               ((makespan - lower_bound) / lower_bound) * 100.0
               Retorna 0.0 si lower_bound es 0 para evitar división por cero.
    """
    
    if lower_bound == 0:
        return 0.0
    return ((makespan - lower_bound) / lower_bound) * 100.0

def algoritmo_evosocial_deap(instancia, parametros, toolbox):
    """
    Ejecuta un algoritmo genético híbrido inspirado en estrategias evolutivas usando DEAP.
    Este algoritmo implementa una estrategia evolutiva que mantiene una solución elite (reina)
    y genera nuevos individuos que interactúan con esta solución mediante operadores genéticos.
    Args:
        instancia (dict): Diccionario con información de la instancia del problema,
            debe contener 'lower_bound' con el límite inferior teórico.
        parametros (dict): Parámetros del algoritmo:
            - popsize (int): Tamaño de la población de individuos por generación
            - maxgen (int): Número máximo de generaciones
            - pcross (float): Probabilidad de aplicar crossover (vs mutación)
            - pmutacion (float): Probabilidad de mutación
        toolbox (deap.base.Toolbox): Toolbox de DEAP con operadores evolutivos:
            - individual(): Función para crear individuos
            - evaluate(): Función de evaluación de fitness
            - mate(): Operador de crossover
            - mutate(): Operador de mutación
    Returns:
        dict: Resultados del algoritmo con las siguientes claves:
            - mejor_global (float): Mejor valor de fitness encontrado
            - gen_mejor (int): Generación donde se encontró el mejor
            - error_mejor (float): Error relativo del mejor respecto al límite inferior
            - error_promedio (float): Error relativo promedio de la última generación
            - historial_convergencia (list): Historial de convergencia por generación
    """
    
    popsize = parametros['popsize']
    maxgen = parametros['maxgen']
    pcross = parametros['pcross']
    pmutacion = parametros['pmutacion']
    lower_bound = instancia['lower_bound']
    
    # Inicializar Queen
    queen = toolbox.individual()
    queen.fitness.values = toolbox.evaluate(queen)
    mejor_global = queen.fitness.values[0]
    gen_mejor = 0
    
    # Historial
    historial_convergencia = []
    evaluaciones_totales = 1  # Queen inicial
    
    # Variables para tracking de población
    suma_fitness_gen = 0
    count_fitness_gen = 0
    
    # Evolución generacional
    for gen in range(1, maxgen + 1):
        suma_fitness_gen = queen.fitness.values[0]  # Incluir Queen
        count_fitness_gen = 1
        
        # Procesar popsize individuos (inmigrantes aleatorios)
        for i in range(popsize):
            # 1. Generar inmigrante aleatorio
            inmigrante = toolbox.individual()
            inmigrante.fitness.values = toolbox.evaluate(inmigrante)
            evaluaciones_totales += 1
            
            # 2. Decisión estocástica: crossover o mutación
            if random.random() < pcross:
                # CROSSOVER: Queen × inmigrante
                hijo1, hijo2 = toolbox.mate(copy.deepcopy(queen), copy.deepcopy(inmigrante))
                hijo1.fitness.values = toolbox.evaluate(hijo1)
                hijo2.fitness.values = toolbox.evaluate(hijo2)
                evaluaciones_totales += 2
                
                # Seleccionar mejor offspring
                mejor_hijo = hijo1 if hijo1.fitness.values[0] < hijo2.fitness.values[0] else hijo2
                candidato = mejor_hijo
            else:
                # MUTACIÓN: aplicar a ambos y seleccionar mejor
                queen_mut = copy.deepcopy(queen)
                queen_mut, = toolbox.mutate(queen_mut)
                queen_mut.fitness.values = toolbox.evaluate(queen_mut)
                
                inm_mut = copy.deepcopy(inmigrante)
                inm_mut, = toolbox.mutate(inm_mut)
                inm_mut.fitness.values = toolbox.evaluate(inm_mut)
                
                evaluaciones_totales += 2
                
                # Seleccionar mejor entre ambos mutados
                candidato = queen_mut if queen_mut.fitness.values[0] < inm_mut.fitness.values[0] else inm_mut
            
            # 3. Actualizar estadísticas poblacionales
            suma_fitness_gen += candidato.fitness.values[0]
            count_fitness_gen += 1
            
            # 4. Actualizar Queen si hay mejora
            if candidato.fitness.values[0] < queen.fitness.values[0]:
                queen = copy.deepcopy(candidato)
                mejor_global = queen.fitness.values[0]
                gen_mejor = gen
        
        # Guardar punto de convergencia
        historial_convergencia.append({
            'gen': gen,
            'mingl': mejor_global,
            'evals': evaluaciones_totales
        })
    
    # Calcular error del mejor
    error_mejor = calcular_error_relativo(mejor_global, lower_bound)
    
    # Error promedio de la última generación
    makespan_promedio = suma_fitness_gen / count_fitness_gen
    error_promedio = calcular_error_relativo(makespan_promedio, lower_bound)
    
    return {
        'mejor_global': mejor_global,
        'gen_mejor': gen_mejor,
        'error_mejor': error_mejor,
        'error_promedio': error_promedio,
        'historial_convergencia': historial_convergencia
    }


# Generación de archivos de resumen y detalle
def ejecutar_experimento_completo(instancia, parametros, archivo_resumen="resumen.txt", archivo_detalle="detalle.txt"):
    """
    Ejecuta un experimento completo del algoritmo evolutivo social utilizando DEAP.
    Esta función coordina múltiples corridas del algoritmo evolutivo, almacena los resultados
    en archivos de texto y genera estadísticas resumen del experimento.
    Args:
        instancia (dict): Diccionario con información de la instancia del problema JSSP.
            Debe contener al menos la clave 'nombre' con el nombre de la instancia.
        parametros (dict): Diccionario con los parámetros de configuración del algoritmo.
            Debe contener la clave 'cantcorr' con el número de corridas a ejecutar.
        archivo_resumen (str, optional): Nombre del archivo para guardar el resumen de resultados.
            Por defecto "resumen.txt".
        archivo_detalle (str, optional): Nombre del archivo para guardar el detalle completo
            del historial de convergencia. Por defecto "detalle.txt".
    Returns:
        list: Lista de diccionarios con los resultados de cada corrida. Cada diccionario contiene:
            - indcorr (int): Índice de la corrida
            - ebest (float): Error del mejor individuo
            - epop (float): Error promedio de la población
            - mingl (float): Mejor makespan global encontrado
            - genmax (int): Generación donde se encontró el mejor resultado
    Side effects:
        - Crea dos archivos de texto con los resultados
        - Imprime información de progreso y estadísticas en consola
        - Utiliza numpy para cálculos estadísticos (debe estar importado como np)
    """
    
    cantcorr = parametros['cantcorr']
    
    print(f"\n  Ejecutando experimento Evosocial con DEAP")
    print(f"{'='*60}")
    print(f"Instancia: {instancia['nombre']}")
    print(f"Corridas: {cantcorr}")
    print(f"{'='*60}\n")
    
    toolbox = configurar_deap(instancia)
    resultados_corridas = []
    
    # Archivo detalle
    with open(archivo_detalle, 'w') as f_detalle:
        for corrida in range(cantcorr):
            print(f"Corrida {corrida + 1}/{cantcorr}...", end='\r')
            
            resultado = algoritmo_evosocial_deap(instancia, parametros, toolbox)
            
            resultados_corridas.append({
                'indcorr': corrida,
                'ebest': resultado['error_mejor'],
                'epop': resultado['error_promedio'],
                'mingl': resultado['mejor_global'],
                'genmax': resultado['gen_mejor']
            })
            
            # Escribir detalle de TODAS las corridas
            for punto in resultado['historial_convergencia']:
                f_detalle.write(f"{punto['gen']:4d} {punto['mingl']:8.2f} {punto['evals']}\n")
    
    print(f"\n  {cantcorr} corridas completadas")
    
    # Escribir resumen
    with open(archivo_resumen, 'w') as f:
        for resultado in resultados_corridas:
            f.write(f"{resultado['indcorr']:2d} {resultado['ebest']:5.2f} {resultado['epop']:5.2f} "
                   f"{resultado['mingl']:7.2f} {resultado['genmax']:4d}\n")
    
    # Estadísticas
    mingls = [r['mingl'] for r in resultados_corridas]
    ebests = [r['ebest'] for r in resultados_corridas]
    
    print(f"\n  Estadísticas globales:")
    print(f"{'='*40}")
    print(f"Mejor makespan: {min(mingls):.2f}")
    print(f"Makespan promedio: {np.mean(mingls):.2f} ± {np.std(mingls):.2f}")
    print(f"Makespan mediana: {np.median(mingls):.2f}")
    print(f"Error mejor: {min(ebests):.2f}%")
    print(f"Error promedio: {np.mean(ebests):.2f}%")
    print(f"\n  Archivos generados:")
    print(f"  - {archivo_resumen}")
    print(f"  - {archivo_detalle}")
    print(f"{'='*40}\n")
    
    return resultados_corridas


# Función main que orquesta la ejecución del experimento
def main():
    
    start_time = time.time()
    print("[] Algoritmo Evosocial - Implementación mediante librería DEAP")
    print("="*60)
    
    # Leer parámetros
    parametros = leer_parametros("DATOS.DAT")
    
    # Leer instancia
    dir_instancias = 'instancias'
    #file_instancia = 'converted_swv06.txt'
    #file_instancia = 'converted_swv07.txt'
    file_instancia = 'converted_swv08.txt'
    archivo_instancia = f'../{dir_instancias}/{file_instancia}'
    
    try:
        instancia = leer_instancia_jsp(archivo_instancia)
    except FileNotFoundError:
        print(f"x Error: No se encontró el archivo {archivo_instancia}")
        return
    
    # Ejecutar experimento
    nombre_instancia = instancia['nombre']
    archivo_resumen = f"resumen_{nombre_instancia}.txt"
    archivo_detalle = f"detalle_{nombre_instancia}.txt"
    
    resultados = ejecutar_experimento_completo(
        instancia, 
        parametros,
        archivo_resumen=archivo_resumen,
        archivo_detalle=archivo_detalle
    )
    
    print("+ Experimento completado exitosamente")
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Guardo el tiempo en un archivo especificando instancia y tiempo
    #archivo_tiempo = "tiempo_deap_"+ nombre_instancia + ".txt"
    archivo_tiempo = "tiempo_ejecucion_deap_"+ nombre_instancia + ".txt"
    print(archivo_tiempo)
    with open(archivo_tiempo, "w", encoding="utf-8") as f:
        f.write(f"Instancia: {nombre_instancia}\n")
        f.write(f"Tiempo de ejecución: {elapsed_time:.2f} segundos\n")

if __name__ == "__main__":
    main()
    
