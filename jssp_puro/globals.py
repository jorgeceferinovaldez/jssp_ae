"""
Definiciones globales, usadas por el main y módulos
Conversión de Pascal a Python con NumPy
"""

import numpy as np
from typing import Set, List, TextIO
from dataclasses import dataclass

# Constantes
MAX_CROM = 20 #100
MAX_MAQ = 15 #5

# Tipos de datos
# alelo = byte (posición de bit)
Alelo = np.uint8  # Tipo para valores 0-255

# cromosoma = array[1..maxcrom] of alelo
def crear_cromosoma() -> np.ndarray:
    """Crea un cromosoma como array de numpy de tipo uint8"""
    return np.zeros(MAX_CROM, dtype=np.uint8)

@dataclass 
class Individuo:
    """Estructura equivalente al RECORD individuo de Pascal"""
    cromosoma: np.ndarray  # array de MAX_CROM elementos tipo uint8
    objective: float
    fitness: float
    
    def __init__(self):
        self.cromosoma = crear_cromosoma()
        self.objective = 0.0
        self.fitness = 0.0

# tipoconj = set of 1..maxcrom
TipoConj = Set[int]  # Set de enteros (rango 1 a MAX_CROM)

# hijos = array [1..2] of individuo
class Hijos:
    """Array de 2 individuos"""
    def __init__(self):
        self.data: List[Individuo] = [Individuo(), Individuo()]
    
    def __getitem__(self, index: int) -> Individuo:
        if index < 1 or index > 2:
            raise IndexError("Índice debe ser 1 o 2")
        return self.data[index - 1]  # Convertir a índice base 0
    
    def __setitem__(self, index: int, value: Individuo):
        if index < 1 or index > 2:
            raise IndexError("Índice debe ser 1 o 2")
        self.data[index - 1] = value

# tipoMaqJob = array [1..maxmaq, 1.. maxcrom] of byte
class TipoMaqJob:
    """Array bidimensional [1..maxmaq, 1..maxcrom] de bytes"""
    def __init__(self):
        self._data = np.zeros((MAX_MAQ, MAX_CROM), dtype=np.uint8)
    
    def __getitem__(self, indices) -> int:
        maq, crom = indices
        if not (1 <= maq <= MAX_MAQ and 1 <= crom <= MAX_CROM):
            raise IndexError(f"Índices fuera de rango: maq={maq}, crom={crom}")
        return self._data[maq-1, crom-1]
    
    def __setitem__(self, indices, valor: int):
        maq, crom = indices
        if not (1 <= maq <= MAX_MAQ and 1 <= crom <= MAX_CROM):
            raise IndexError(f"Índices fuera de rango: maq={maq}, crom={crom}")
        if not (0 <= valor <= 255):
            raise ValueError(f"Valor debe estar entre 0 y 255, recibido: {valor}")
        self._data[maq-1, crom-1] = valor
    
    @property
    def array(self) -> np.ndarray:
        """Acceso directo al array numpy subyacente"""
        return self._data

# Variables globales
queen: Individuo = Individuo()
mej: Individuo = Individuo()

# Archivos de texto (en Python usamos TextIO o simplemente file handles)
Datos: TextIO = None
Det: TextIO = None  
Resum: TextIO = None
Ins: TextIO = None

# Variables enteras y byte
indcorr: int = 0  # byte en Pascal, int en Python
cantcorr: int = 0
maxgen: int = 0
popsize: int = 0
gen: int = 0
genmax: int = 0
indchild: int = 0

# Variables reales (float)
pmutacion: float = 0.0
pcross: float = 0.0
mingl: float = 0.0
ebest: float = 0.0
epop: float = 0.0
min_val: float = 0.0  # 'min' es palabra reservada en Python
maximo: float = 0.0
avg: float = 0.0

# Variables long integer
upperb: int = 0  # longint en Pascal = int en Python
lowerb: int = 0
evals: int = 0

# Instancias de tipos complejos
child: Hijos = Hijos()
Cmj: TipoMaqJob = TipoMaqJob()

# Funciones auxiliares para trabajar con los tipos
def crear_conjunto_cromosomas() -> Set[int]:
    """Crea un conjunto vacío para cromosomas (rango 1 a MAX_CROM)"""
    return set()

def validar_rango_cromosoma(valor: int) -> bool:
    """Valida que un valor esté en el rango válido para cromosomas"""
    return 1 <= valor <= MAX_CROM

def crear_individuo_aleatorio() -> Individuo:
    """Crea un individuo con cromosoma aleatorio"""
    individuo = Individuo()
    individuo.cromosoma = np.random.randint(0, 256, MAX_CROM, dtype=np.uint8)
    return individuo

# Ejemplo de uso y validaciones
if __name__ == "__main__":
    # Ejemplo de uso de los tipos definidos
    print("Ejemplo de uso de las estructuras de datos:")
    
    # Crear individuo
    ind = crear_individuo_aleatorio()
    print(f"Cromosoma shape: {ind.cromosoma.shape}")
    print(f"Cromosoma dtype: {ind.cromosoma.dtype}")
    
    # Usar conjunto
    conjunto = crear_conjunto_cromosomas()
    conjunto.add(50)
    conjunto.add(25)
    print(f"Conjunto: {conjunto}")
    
    # Usar hijos
    child[1] = ind
    print(f"Primer hijo fitness: {child[1].fitness}")
    
    # Usar matriz de trabajos
    Cmj[1, 1] = 20 #100
    Cmj[5, 100] = 255
    print(f"Cmj[1,1] = {Cmj[1, 1]}")
    print(f"Cmj[5,100] = {Cmj[5, 100]}")
    print(f"Matriz shape: {Cmj.array.shape}")
