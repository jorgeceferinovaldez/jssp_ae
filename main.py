import random
import sys
import numpy as np
from typing import Set, Dict, Any, Tuple

from globals import (
    # Constantes del sistema
    MAX_MAQ, MAX_CROM,
    
    # Tipos de datos y estructuras
    Individuo, Hijos, TipoMaqJob,
    
    # Variables de configuración del algoritmo
    popsize, pcross, pmutacion, maxgen, cantcorr,
    
    # Variables de estado y control
    gen, evals, indchild, mingl,
    
    # Variables de estadísticas y resultados
    queen, mej, child, maximo, min_val, avg,
    
    # Variables de instancia del problema
    upperb, lowerb, Cmj,
    
    # Archivos de entrada y salida
    Ins, Det, Resum
)


# --- Funciones de la UNIT Utility integradas ---
def showopt(v: np.ndarray) -> None:
    """
    Muestra la representación de un cromosoma genético en formato de cadena lineal.
    Esta función toma un vector numérico que representa un cromosoma y lo imprime
    en una sola línea, convirtiendo cada valor a entero para una representación
    limpia y sin espacios entre los dígitos.
        v (np.ndarray): Vector de numpy que representa el cromosoma genético.
            Debe tener una longitud de MAX_CROM elementos. Cada elemento se
            interpreta como un gen del cromosoma y se muestra como dígito entero.
    Returns:
        None: La función solo imprime el cromosoma, no retorna ningún valor.
    Notas:
        - Inspirado en la implementación original en Pascal que usaba write(v[i])
        - El uso de end="" evita espacios entre los dígitos impresos
        - El print(" ") final actúa como un salto de línea (equivalente a writeln)
        - MAX_CROM debe estar definido previamente como constante global
    """

    # En Pascal era `write(v[i])` sin espacio, aquí forzamos int para impresión
    for i in range(MAX_CROM):
        print(int(v[i]), end="")
    print(" ")  # writeln(' ')

def gen_cut_points(cant: int) -> Tuple[int, int]:
    """
    Genera dos puntos de corte aleatorios distintos dentro de un rango dado.
    Esta función selecciona dos enteros aleatorios distintos entre 2 y cant-1 (inclusive),
    asegurando que el primer punto sea siempre menor que el segundo punto.
    
    Args:
        cant (int): Límite superior para la selección aleatoria (exclusivo). La función
                    genera puntos en el rango [2, cant-1].
    
    Returns:
        Tuple[int, int]: Una tupla que contiene dos puntos de corte distintos (ptocorte1, ptocorte2)
                        donde ptocorte1 < ptocorte2.
    
    Raises:
        ValueError: Si cant es menor que 4, ya que se necesita al menos 4 para generar
                    dos puntos distintos en el rango [2, cant-1].
    """

    ptocorte1 = random.randint(2, cant - 1)
    
    while True:
        ptocorte2 = random.randint(2, cant - 1)
        
        # IF ptocorte2 < ptocorte1 THEN intercambiar
        if ptocorte2 < ptocorte1:
            auxi = ptocorte1
            ptocorte1 = ptocorte2
            ptocorte2 = auxi
        
        # UNTIL ptocorte2 <> ptocorte1
        if ptocorte2 != ptocorte1:
            break
    
    return ptocorte1, ptocorte2

def ordshell(v: np.ndarray) -> np.ndarray:
    """
    Ordena un cromosoma usando numpy.sort (de menor a mayor).
    Reemplaza la implementación original de Shell Sort con la función optimizada de NumPy.
    
    Args:
        v: Cromosoma a ordenar
        
    Returns:
        Cromosoma ordenado (copia)
    """
    return np.sort(v)

def validacrom(v: np.ndarray) -> bool:
    """
    Valida si un vector cromosómico contiene todos los valores requeridos en el rango esperado.
    
    Args:
        v (np.ndarray): Vector cromosómico a validar. Debe contener valores enteros.
    
    Returns:
        bool: True si el cromosoma es válido, False en caso contrario. Un cromosoma válido debe:
            - Contener solo valores entre 1 y MAX_CROM (inclusive)
            - Contener cada entero desde 1 hasta MAX_CROM exactamente una vez (permutación)
    """
    
    sn = True
    cromaux = [0] * (MAX_CROM + 1)  # cromaux: array de 0s (tamaño MAX_CROM + 1)
    
    # for i:= 1 to maxcrom do
    for i in range(MAX_CROM):
        v_i = int(v[i])
        # if v[i] <= maxcrom then cromaux[v[i]]:= 1 else sn:= false
        if 1 <= v_i <= MAX_CROM:
            cromaux[v_i] = 1
        else:
            sn = False
    
    # for i:= 1 to maxcrom do if cromaux[i] = 0 then sn:= false
    for i in range(1, MAX_CROM + 1):
        if cromaux[i] == 0:
            sn = False
    
    return sn

def flip(probability: float) -> bool:
    """
    Lanza una moneda sesgada con la probabilidad dada de retornar True.

    Args:
        probability: Un float entre 0.0 y 1.0 que representa la probabilidad
                     de retornar True. Si probability es 1.0, siempre retorna True.

    Returns:
        bool: True con la probabilidad dada, False en caso contrario.
    """

    # if probability = 1.0 then flip := true else flip := (random <= probability)
    if probability == 1.0:
        return True
    else:
        return random.random() <= probability

# --- Fin de funciones de la UNIT Utility integradas ---

# --- Funciones de op_mut.pas integradas/actualizadas ---
def mutacion(crom: np.ndarray) -> None:
    """
    Realiza una mutación de intercambio (exchange mutation).
    Selecciona dos posiciones aleatorias e intercambia su contenido.
    Equivalente a PROCEDURE mutacion(VAR crom:cromosoma) en Pascal.

    Args:
        crom: Cromosoma a mutar (modificado in-place).
    """
    posmut = random.randint(1, MAX_CROM)

    posmut2 = random.randint(1, MAX_CROM)
    while posmut == posmut2: # UNTIL posmut <> posmut2;
        posmut2 = random.randint(1, MAX_CROM)

    # Intercambio
    aux = crom[posmut - 1] # Ajustar a índice base 0
    crom[posmut - 1] = crom[posmut2 - 1]
    crom[posmut2 - 1] = aux

def mutshift(p1: np.ndarray) -> None:
    """
    Implementa la mutación shift de Reeves.
    Selecciona una posición y desplaza el elemento una cantidad de posiciones.
    Equivalente a PROCEDURE mutShift(VAR p1:cromosoma) en Pascal.

    Args:
        p1: Cromosoma a mutar (modificado in-place).
    """
    # Funciones internas anidadas para make_shift_right/left
    # Adaptadas para índices base 0 de NumPy
    def make_shift_right(arr: np.ndarray, desde: int, hasta: int):
        """Realiza el desplazamiento de los elementos hacia la derecha."""
        for i in range(desde - 1, hasta - 2, -1): # desde-1 hasta hasta-1 (inclusive), paso -1
            arr[i + 1] = arr[i]

    def make_shift_left(arr: np.ndarray, desde: int, hasta: int):
        """Realiza el desplazamiento de los elementos hacia la izquierda."""
        for i in range(desde - 1, hasta): # desde-1 hasta hasta-1 (inclusive), paso 1
            arr[i - 1] = arr[i]

    posmut = random.randint(1, MAX_CROM)# Posición original del elemento (base 1)
    shift = random.randint(1, MAX_CROM - 1) # Cantidad de posiciones a desplazar (base 1)

    if flip(0.5): # ir a la izquierda de posmut
        # No es circular
        if shift < posmut:
            posShift = posmut - shift
            aux = p1[posmut - 1] # Elemento a mover (base 0)
            make_shift_right(p1, posmut - 1, posShift) # posmut-1 es el "desde", posShift es el "hasta" (elementos desplazados)
            p1[posShift - 1] = aux # Colocar elemento en la nueva posición (base 0)
        # Es circular
        else:
            posShift = MAX_CROM - (shift - posmut)
            aux = p1[posmut - 1] # Elemento a mover (base 0)
            make_shift_right(p1, posmut - 1, 1) # Desplazar hasta el inicio [posmut-2 ... 0]
            p1[0] = p1[MAX_CROM - 1] # El último elemento se mueve a la posición 0
            make_shift_right(p1, MAX_CROM - 1, posShift) # Desplazar el resto desde el final [MAX_CROM-2 ... posShift-1]
            p1[posShift - 1] = aux # Colocar elemento en la nueva posición (base 0)
    else: # ir a la derecha de posmut
        # No es circular
        if shift <= MAX_CROM - posmut:
            posShift = posmut + shift
            aux = p1[posmut - 1] # Elemento a mover (base 0)
            make_shift_left(p1, posmut + 1, posShift) # posmut+1 es el "desde", posShift es el "hasta"
            p1[posShift - 1] = aux # Colocar elemento en la nueva posición (base 0)
        # Es circular
        else:
            posShift = shift - (MAX_CROM - posmut)
            aux = p1[posmut - 1] # Elemento a mover (base 0)
            make_shift_left(p1, posmut + 1, MAX_CROM) # Desplazar desde posmut hasta el final [posmut ... MAX_CROM-1]
            p1[MAX_CROM - 1] = p1[0] # El primer elemento se mueve a la última posición
            make_shift_left(p1, 2, posShift) # Desplazar el resto desde la posición 1 hasta posShift
            p1[posShift - 1] = aux # Colocar elemento en la nueva posición (base 0)

# --- Ajuste de crossox para usar la nueva función mutacion ---
def crossox(p1: np.ndarray, p2: np.ndarray) -> None:
    """
    Crossover OX2 (Order Crossover 2) entre dos cromosomas.
    Implementa el algoritmo crossox de Pascal.

    Args:
        p1: Primer cromosoma padre (np.ndarray de uint8)
        p2: Segundo cromosoma padre (np.ndarray de uint8)
    """
    global child, indchild, pmutacion # Acceder a las variables globales

    def gen_hijo(max_crom_len: int, ptocorte1: int, ptocorte2: int, v: np.ndarray, w: np.ndarray):
        """
        Función interna para generar un cromosoma hijo.
        Equivalente a GenHijo en Pascal.
        """
        # CORRECCIÓN: indchild es una variable GLOBAL, no nonlocal.
        # Por lo tanto, se debe declarar como 'global' si se va a modificar.
        global indchild 

        h = np.zeros(max_crom_len, dtype=np.uint8) # h: cromosoma
        conj: Set[int] = set() # conj: tipoconj

        # Copiar segmento central de v a h y añadir al conjunto
        for i in range(ptocorte1 - 1, ptocorte2): # Convertir rangos Pascal (1..N) a Python (0..N-1)
            h[i] = v[i]
            conj.add(int(h[i])) # Asegurar que se añaden enteros al set

        aux = np.zeros(max_crom_len, dtype=np.uint8) # aux: cromosoma
        j_aux = 0 # índice para el array auxiliar

        # Armar auxiliar con genes del extremo del segundo corte del padre w
        # FOR i := ptocorte2+1 TO maxcrom DO
        for i_pascal in range(ptocorte2 + 1, max_crom_len + 1):
            i_python = i_pascal - 1 # Convertir a índice Python
            if int(w[i_python]) not in conj:
                aux[j_aux] = w[i_python]
                j_aux += 1

        # Completar auxiliar con el segundo padre desde el inicio hasta el primer corte
        # FOR i:= 1 to ptocorte2 DO
        for i_pascal in range(1, ptocorte2 + 1):
            i_python = i_pascal - 1 # Convertir a índice Python
            if int(w[i_python]) not in conj:
                aux[j_aux] = w[i_python]
                j_aux += 1
        
        # Armar el hijo h final con los genes del auxiliar
        j_aux_read = 0
        
        # Segmento después del segundo punto de corte
        # FOR i := ptocorte2+1 TO maxcrom DO
        for i_pascal in range(ptocorte2 + 1, max_crom_len + 1):
            i_python = i_pascal - 1 # Convertir a índice Python
            h[i_python] = aux[j_aux_read]
            j_aux_read += 1
        
        # Segmento antes del primer punto de corte
        # FOR i:= 1 TO ptocorte-1 DO
        for i_pascal in range(1, ptocorte1): # ptocorte-1 Pascal -> ptocorte-1 Python (exclusivo)
            i_python = i_pascal - 1 # Convertir a índice Python
            h[i_python] = aux[j_aux_read]
            j_aux_read += 1

        # Aplicar mutación al hijo generado si flip(pmutacion) es True
        if flip(pmutacion):
            mutacion(h) # Usa la nueva función `mutacion` de intercambio

        indchild += 1
        child[indchild] = Individuo() # Crear una nueva instancia de Individuo para el hijo
        child[indchild].cromosoma = h

    # Comienzo de crossox
    ptocorte1, ptocorte2 = gen_cut_points(MAX_CROM)

    # Obtiene el primer hijo (v=p1, w=p2)
    gen_hijo(MAX_CROM, ptocorte1, ptocorte2, p1, p2)

    # Obtiene el segundo hijo (v=p2, w=p1)
    gen_hijo(MAX_CROM, ptocorte1, ptocorte2, p2, p1)


def cargar_configuracion(archivo_datos: str = 'DATOS.DAT') -> Dict[str, Any]:
    """
    Carga la configuración desde archivo de datos.
    
    Args:
        archivo_datos: Ruta al archivo de configuración
        
    Returns:
        Diccionario con los parámetros de configuración
    """
    try:
        with open(archivo_datos, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
            
        if len(lineas) < 5:
            raise ValueError(f"El archivo {archivo_datos} debe contener al menos 5 valores")
            
        config = {
            'cantcorr': int(lineas[0]),
            'pmutacion': float(lineas[1]),
            'pcross': float(lineas[2]),
            'maxgen': int(lineas[3]),
            'popsize': int(lineas[4])
        }
        
        return config
        
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo {archivo_datos}") from FileNotFoundError
    except (ValueError, IndexError) as e:
        raise ValueError(f"Error al parsear {archivo_datos}: {e}") from e

def setup(archivo_datos: str = 'DATOS.DAT'):
    """
    Inicializa las variables globales con los parámetros de configuración.
    
    Args:
        archivo_datos: Ruta al archivo de configuración
    """
    global cantcorr, pmutacion, pcross, maxgen, popsize
    
    config = cargar_configuracion(archivo_datos)
    
    cantcorr = config['cantcorr']
    pmutacion = config['pmutacion']
    pcross = config['pcross']
    maxgen = config['maxgen']
    popsize = config['popsize']
    
    print("Configuración cargada!!!:")
    print(f"  Corridas: {cantcorr}")
    print(f"  P. Mutación: {pmutacion}")
    print(f"  P. Cruzamiento: {pcross}")
    print(f"  Max. Generaciones: {maxgen}")
    print(f"  Tamaño Población: {popsize}")

def inicializar_archivos(
    archivo_detalle: str = 'detalle.txt',
    archivo_resumen: str = 'resumen.txt',
    archivo_instancia: str = '100X5-10.txt'
):
    """
    Inicializa los archivos de salida.
    
    Args:
        archivo_detalle: Archivo para escribir detalles
        archivo_resumen: Archivo para escribir resumen
        archivo_instancia: Archivo con datos de instancia
    """
    global Det, Resum, Ins

    Det = open(archivo_detalle, 'w', encoding='utf-8')
    Resum = open(archivo_resumen, 'w', encoding='utf-8')
    Ins = open(archivo_instancia, 'r', encoding='utf-8')

    print("Archivos inicializados:")
    print(f"  Detalle: {archivo_detalle}")
    print(f"  Resumen: {archivo_resumen}")
    print(f"  Instancia: {archivo_instancia}")

def inicializar_sistema(archivo_datos: str = 'DATOS.DAT'):
    """
    Inicializa todo el sistema: configuración y archivos.
    
    Args:
        archivo_datos: Archivo con parámetros de configuración
    """
    setup(archivo_datos)
    inicializar_archivos()

def cerrar_archivos():
    """Cierra todos los archivos abiertos de manera segura."""
    global Det, Resum, Ins
    
    archivos = [
        ('Det', Det),
        ('Resum', Resum), 
        ('Ins', Ins)
    ]
    
    for nombre, archivo in archivos:
        try:
            if archivo and hasattr(archivo, 'close') and not archivo.closed:
                archivo.close()
                print(f"Archivo {nombre} cerrado")
        except Exception as e:
            print(f"Error al cerrar {nombre}: {e}")

def leer_instancia():
    """
    Lee el archivo de instancia y llena la matriz Cmj con los datos.
    
    Formato esperado:
    - Línea 1: upperb
    - Línea 2: lowerb  
    - Líneas 3-7: 100 valores cada una (5 máquinas x 100 trabajos)
    """
    global upperb, lowerb, Ins, Cmj
    
    try:
        # Leer upperb (primera línea)
        upperb = int(Ins.readline().strip())
        print(f"upperb leído: {upperb}")
        
        # Leer lowerb (segunda línea)  
        lowerb = int(Ins.readline().strip())
        print(f"lowerb leído: {lowerb}")
        
        # Leer matriz de máquinas-trabajos
        for i in range(1, MAX_MAQ + 1):  # máquinas 1 a 5
            linea = Ins.readline().strip()
            if not linea:
                raise ValueError(f"Archivo termina inesperadamente en máquina {i}")
                
            valores = [int(x) for x in linea.split()]
            
            if len(valores) != MAX_CROM:
                raise ValueError(f"Máquina {i}: se esperaban {MAX_CROM} valores, se encontraron {len(valores)}")
                
            # Llenar la fila i de la matriz
            for j in range(1, MAX_CROM + 1):  # trabajos 1 a 100
                Cmj[i, j] = valores[j-1]  # valores está en base 0
                
        print(f"Matriz {MAX_MAQ}x{MAX_CROM} cargada correctamente")
        #print(Cmj.array)

    except ValueError as e:
        # ValueError específico para problemas de parsing
        raise ValueError(f"Error en el formato del archivo de instancia: {e}") from e
    except IOError as e:
        # IOError para problemas de E/S del archivo
        raise IOError(f"Error de E/S al leer el archivo de instancia: {e}") from e
    except Exception as e:
        # Captura cualquier otro error inesperado y lo relanza con contexto
        raise RuntimeError(f"Error inesperado al procesar la instancia: {e}") from e


def gen_scheduler(vdec: np.ndarray, cmj: TipoMaqJob) -> tuple[float, float]:
    """
    Genera el schedule para un cromosoma y calcula objective y fitness.
    
    Args:
        vdec: Cromosoma (permutación de trabajos)
        cmj: Matriz de tiempos máquina-trabajo
        
    Returns:
        Tupla (objective, fitness) donde objective es el makespan
    """
    # Tipo equivalente a tipoPos = array [1..maxMaq, 1..maxcrom] of integer
    pos = np.zeros((MAX_MAQ + 1, MAX_CROM + 1), dtype=int)  # +1 para índices base 1
    
    # Inicializa la matriz de última posición del job en el scheduler
    # (ya inicializada en 0 por numpy)
    
    # Asigna a la primera máquina el scheduler del job
    for i in range(1, MAX_CROM + 1):
        indice = int(vdec[i-1])  # vdec está en base 0, convertir a base 1. Asegurar que es int.
        if i == 1:
            pos[1, i] = cmj[1, indice]
        else:
            pos[1, i] = pos[1, i-1] + cmj[1, indice]
    
    # Asigna a las siguientes máquinas el scheduler del job
    for j in range(2, MAX_MAQ + 1):
        for i in range(1, MAX_CROM + 1):
            ult = pos[j-1, i]
            indice = int(vdec[i-1])  # vdec está en base 0. Asegurar que es int.
            
            if (i-1 != 0) and (pos[j, i-1] >= ult):
                ult = pos[j, i-1] + cmj[j, indice]
            else:
                ult = ult + cmj[j, indice]
            
            pos[j, i] = ult
    
    objective = float(ult)
    fitness = 1.0 / objective if objective > 0 else float('inf')
    
    return objective, fitness

def evalua(child: Hijos, ch: int) -> None:
    """
    Evalúa los primeros ch individuos del array de hijos.
    
    Args:
        child: Array de individuos hijos
        ch: Número de hijos a evaluar (máximo 2)
    """
    for i in range(1, min(ch + 1, 3)):  # Máximo 2 hijos
        objective, fitness = gen_scheduler(child[i].cromosoma, Cmj)
        child[i].objective = objective
        child[i].fitness = fitness

def ind_aleatorio() -> Individuo:
    """
    Genera un individuo aleatorio con cromosoma de permutación.
    
    Returns:
        Individuo con cromosoma aleatorio, objective y fitness calculados
    """
    ri = Individuo()
    
    # Generar individuo permutación
    C: Set[int] = set()  # Conjunto vacío equivalente a C := [ ]
    
    for j in range(1, MAX_CROM + 1):  # j := 1 TO maxcrom
        # Generar job aleatorio que no esté en C
        while True:
            job = random.randint(1, MAX_CROM)  # Usa la función random.randint
            if job not in C:  # UNTIL NOT(job in C)
                break
        
        C.add(job)  # C := C + [job]
        ri.cromosoma[j-1] = job  # cromosoma[j] := job (convertir a índice base 0)
    
    # Validar cromosoma con la función validacrom integrada
    if not validacrom(ri.cromosoma):
        print("Cromosoma inválido en ind_aleatorio")
        print("Cromosoma:", end=" ")
        for j in range(MAX_CROM):
            print(ri.cromosoma[j], end=" ")
        print()
        sys.exit(1)  # halt
    
    # Evaluar cromosoma
    ri.objective, ri.fitness = gen_scheduler(ri.cromosoma, Cmj)
    
    return ri

def mostrar_individuo(individuo: Individuo, num_genes: int = 10) -> None:
    """
    Muestra información de un individuo.
    
    Args:
        individuo: Individuo a mostrar
        num_genes: Número de genes del cromosoma a mostrar
    """
    print(f"Objective (makespan): {individuo.objective:.2f}")
    print(f"Fitness: {individuo.fitness:.6f}")
    print(f"Cromosoma (primeros {num_genes}): ", end="")
    for i in range(min(num_genes, MAX_CROM)):
        print(f"{individuo.cromosoma[i]:3d}", end=" ")
    if num_genes < MAX_CROM:
        print("...")
    else:
        print()

def mostrar_estadisticas_poblacion(poblacion: list[Individuo]) -> None:
    """
    Muestra estadísticas de una población.
    
    Args:
        poblacion: Lista de individuos
    """
    if not poblacion:
        print("Población vacía")
        return
    
    objectives = [ind.objective for ind in poblacion]
    fitnesses = [ind.fitness for ind in poblacion]
    
    print(f"\n=== Estadísticas de población (n={len(poblacion)}) ===")
    print(f"Makespan - Min: {min(objectives):.2f}, Max: {max(objectives):.2f}, Avg: {sum(objectives)/len(objectives):.2f}")
    print(f"Fitness  - Min: {min(fitnesses):.6f}, Max: {max(fitnesses):.6f}, Avg: {sum(fitnesses)/len(fitnesses):.6f}")
    
    # Encontrar mejor y peor individuo
    mejor_idx = fitnesses.index(max(fitnesses))
    peor_idx = fitnesses.index(min(fitnesses))
    
    print(f"\nMejor individuo (makespan: {objectives[mejor_idx]:.2f}):")
    mostrar_individuo(poblacion[mejor_idx], 15)
    
    print(f"\nPeor individuo (makespan: {objectives[peor_idx]:.2f}):")
    mostrar_individuo(poblacion[peor_idx], 15)

def stats(indi: Individuo) -> None:
    """
    Actualiza estadísticas globales (min_val, maximo) basándose en el individuo proporcionado.
    También actualiza el mejor individuo global 'mej' si el actual es mejor.
    Equivalente a PROCEDURE stats(indi:individuo) en Pascal.

    Args:
        indi: Individuo a evaluar para actualizar las estadísticas.
    """
    global min_val, maximo, mej # Declarar variables globales que se van a modificar

    # La lógica `with indi do begin...end;` en Pascal se traduce a acceder
    # directamente a los atributos de `indi` en Python.
    
    # IF objective < min THEN
    if indi.objective < min_val:
        min_val = indi.objective # min := objective;
        mej = indi               # mej := indi; (Asigna el objeto Individuo completo)

    # if objective > maximo then
    if indi.objective > maximo:
        maximo = indi.objective # maximo := objective;

def next_generacion() -> None:
    """
    Genera una nueva generación usando crossover, mutación y selección.
    
    Algoritmo:
    1. Para cada individuo de la nueva población:
       - Genera un inmigrante aleatorio (ri)
       - Decide si hacer crossover o mutación
       - Si crossover: OX2 entre queen y ri, selecciona mejor hijo
       - Si mutación: aplica mutshift a queen y ri, selecciona mejor
       - Actualiza estadísticas con el mejor
    2. Calcula fitness promedio de la población
    """
    global maximo, min_val, avg, indchild, mej, queen
    
    # Inicialización
    maximo = 0.0
    min_val = float(upperb * 10.5) # Asegurarse que es float
    sumobjective = 0.0
    j = 0  # Primer individuo de la población actual
    
    print(f"Generando nueva generación (población: {popsize})...")
    
    # Loop principal - generar popsize individuos
    while j < popsize:
        indchild = 0
        
        # Generar inmigrante aleatorio
        ri = ind_aleatorio()
        
        # Realizar crossover OX2 con probabilidad pcross
        if flip(pcross): # Usa la función flip integrada
            # Hacer crossover
            crossox(queen.cromosoma, ri.cromosoma)
            evalua(child, 2)
            
            # Elegir el mejor hijo
            if child[1].objective < child[2].objective:
                mejor = 1
            else:
                mejor = 2
            
            mej = child[mejor]
            
        else:
            # No hacer crossover, aplicar mutación
            
            # Mutar queen con probabilidad pmutacion
            if flip(pmutacion): # Usa la función flip integrada
                mutshift(queen.cromosoma)
                queen.objective, queen.fitness = gen_scheduler(queen.cromosoma, Cmj)
            
            # Mutar ri con probabilidad pmutacion
            if flip(pmutacion): # Usa la función flip integrada
                mutshift(ri.cromosoma)
                ri.objective, ri.fitness = gen_scheduler(ri.cromosoma, Cmj)
            
            # Elegir el mejor entre ri y queen
            if ri.objective < queen.objective:
                mej = ri
            else:
                mej = queen
        
        # Actualizar estadísticas
        stats(mej)
        sumobjective += mej.objective
        j += 1
        
        # Mostrar progreso cada 10% de la población
        if popsize >= 10 and j % (popsize // 10) == 0:
            porcentaje = (j * 100) // popsize
            print(f"  Progreso: {porcentaje}% ({j}/{popsize}) - Mejor actual: {min_val:.2f}")
    
    # Calcular fitness promedio poblacional
    avg = sumobjective / popsize
    
    print("Generación completada:")
    print(f"  Fitness promedio: {avg:.2f}")
    print(f"  Mejor objective: {min_val:.2f}")
    print(f"  Peor objective: {maximo:.2f}")

# Suponiendo que estas funciones imprimir_detalle y imprimir_resumen existen o serán creadas.
# Si no las tienes, estas son versiones placeholder:
def imprimir_detalle() -> None:
    """
    Imprime una línea de detalle en el archivo de detalle (Det) para la generación actual.
    Equivalente a PROCEDURE imprimir_detalle en Pascal.
    """
    global Det, gen, mingl, evals # Asegurarse de acceder a las variables globales

    if Det and not Det.closed:
        # Aquí 'mingl' representa el mejor objetivo global hasta el momento,
        # 'gen' es la generación actual, y 'evals' son las evaluaciones acumuladas.
        Det.write(f"{gen:4d}  {mingl:6.2f} {evals:d}\n") # Imprime gen, mingl, evals donde gen es la generación actual, mingl es el mejor objetivo global, y evals son las evaluaciones acumuladas.
    else:
        print("ADVERTENCIA: Archivo Det no está abierto o es nulo. No se pudo escribir el detalle de la generación.")

def imprimir_resumen() -> None:
    """
    Imprime una línea de resumen en el archivo de resumen (Resum) al final de una corrida.
    Equivalente a PROCEDURE imprimir_resumen en Pascal.
    """
    global Resum, indcorr, ebest, epop, mingl, genmax # Asegurarse de acceder a las variables globales

    if Resum and not Resum.closed:
        # Imprime indcorr es la cantidad de corrida, ebest es el error del mejor individuo, 
        # epop es el error promedio de la población, mingl es el mejor objetivo global, genmax es la generación en que se encontró el mejor global.
        Resum.write(f"{indcorr:2d} {ebest:5.2f} {epop:5.2f} {mingl:6.2f} {genmax:4d}\n") # Imprime indcorr, ebest, epop, mingl, genmax
    else:
        print("ADVERTENCIA: Archivo Resum no está abierto o es nulo. No se pudo escribir el resumen final.")

def evoso():
    """
    Implementa el algoritmo genético principal (EVOSO) como se especifica en Pascal.
    Gestiona las generaciones, la evolución de la población y la recopilación de estadísticas.
    """
    global queen, evals, gen, min_val, maximo, mej, avg
    # Necesitamos variables globales para mingl, genmax, ebest, epop.
    # Si no están en globals.py, las declaramos aquí y las inicializamos.
    global mingl, genmax, ebest, epop 

    # randomize; (En Python, random se inicializa automáticamente al importarse,
    #             o puedes usar random.seed() para un control explícito)
    # random.seed() # Opcional: para inicializar de forma predecible con el tiempo actual

    evals = 0
    gen = 0 # Reiniciar el contador de generación

    # indAleatorio(Queen); (En Pascal, Queen se pasaría como VAR y se modificaría.
    #                     Aquí, como Queen es global, simplemente la asignamos.)
    queen = ind_aleatorio() # Llama a la función para generar un individuo aleatorio

    mingl = queen.objective # mingl := queen.objective; (Mejor objetivo global)

    # Inicializar las estadísticas globales para la corrida
    # maximo   := 0; {fitness } -> maximo se usa para el makespan, no fitness.
    # min      := upperb * 10.5; -> min_val se usa para el makespan.
    maximo = 0.0 # Reiniciar el máximo makespan de la generación
    min_val = float(upperb * 10.5) # Reiniciar el mínimo makespan de la generación

    genmax = 0 # Inicializa la generación en la que se encontró el mejor global.

    print("\n=== Iniciando Proceso de Evolución (EVOSO) ===")
    print(f"Mejor objetivo inicial (Queen): {queen.objective:.2f}")
    print(f"Rango de makespan esperado: [{lowerb}, {upperb}]")

    # Evoluciona
    # gen := gen + 1; (El loop while incrementa gen al principio en Pascal,
    #                 pero lo haremos de forma más idiomática en Python)
    gen = 1 # Empezamos con la generación 1

    while gen <= maxgen:
        print(f"\n--- Ejecutando Generación {gen}/{maxgen} ---")
        next_generacion() # Esta función actualiza min_val, maximo, avg, y mej de la generación

        # IF min < mingl THEN (min_val es el min de la generación actual)
        if min_val < mingl:
            mingl = min_val   # mingl := min;
            queen = mej       # Queen := mej; (Actualiza la 'reina' con el mejor individuo global)
            genmax = gen      # genmax := gen;
            print(f"  Nuevo mejor global encontrado: {mingl:.2f} en generación {genmax}")

        evals += popsize # evals := evals + popsize; (Cada individuo evaluado en next_generacion)

        imprimir_detalle() # Llama a la función para imprimir detalles (si está implementada)
        print(f"Generación {gen:4d} - Mejor Global: {mingl:6.2f} - Mejor de Gen: {min_val:6.2f} - Avg de Gen: {avg:6.2f}")
        
        gen += 1 # gen := gen + 1;

    print("\n=== Proceso EVOSO Finalizado ===")
    print(f"Mejor Makespan global encontrado: {mingl:.2f} (en generación {genmax})")
    print(f"Mejor individuo global: Objective={queen.objective:.2f}, Fitness={queen.fitness:.6f}")
    
    # Calcular ebest y epop (errores relativos respecto al upperb, si es una métrica de referencia)
    # abs(upperb - mingl) / upperb * 100
    ebest = (abs(upperb - mingl) / upperb) * 100 if upperb != 0 else float('inf')
    # abs(upperb - avg) / upperb * 100
    epop = (abs(upperb - avg) / upperb) * 100 if upperb != 0 else float('inf')

    print(f"Error del mejor individuo (ebest): {ebest:.2f}%")
    print(f"Error promedio de la población (epop): {epop:.2f}%")

    imprimir_resumen() # Llama a la función para imprimir el resumen final

if __name__ == "__main__":
    
    try:
        print("Iniciando sistema...")
        inicializar_sistema()
        print(f"Sistema listo. Población: {popsize}, Generaciones: {maxgen}")
        
        #Ins = open('./instancias/100X5-10.txt', 'r', encoding='utf-8')
        Ins = open('./instancias/converted_swv06.txt', 'r', encoding='utf-8')
        print("Leyendo archivo de instancia...")
        leer_instancia()

        print("\n=== Test: Ejecutar Algorimo Genético ===")
        for indcorr in range(0, cantcorr):
            print(f"\n--- Corrida {indcorr}/{cantcorr} ---")
            evoso()
        
    except TypeError as e: 
        print(f"Ocurrió un error de tipo: {e}")
    finally:
        if Ins and not Ins.closed:
            Ins.close()
        cerrar_archivos()

    print("Ejecución finalizada.")