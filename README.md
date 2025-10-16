# Maestría en Inteligencia Artificial FIUBA

# Trabajo Final - Algoritmos Evolutivos I

# Algoritmo Evolutivo Híbrido para Job Shop Scheduling (JSSP)

## Implementaciones comparativas del algoritmo Evosocial

## Integrantes

- Fabian Sarmiento
- Jorge Ceferino Valdez

---

## Inicio Rápido

### Requisitos Previos

- **Python 3.10+**
- **Conda** o **Miniconda** (recomendado)
- **Git**

### Instalación y Configuración

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/jorgeceferinovaldez/jssp_ae.git
cd jssp_ae
```

#### 2. Crear Entorno Conda

```bash
# Crear entorno virtual con Python 3.10
conda create -n jssp_env python=3.10 -y

# Activar el entorno
conda activate jssp_env
```

#### 3. Instalar Dependencias

```bash
# Instalar todas las dependencias desde requirements.txt
pip install -r requirements.txt
```

**Dependencias incluidas:**
- `numpy` - Computación científica
- `deap` - Framework de algoritmos evolutivos
- `scipy` - Análisis estadístico
- `pandas` - Manipulación de datos
- `matplotlib` - Visualización básica
- `seaborn` - Visualización avanzada

#### 4. Verificar Instalación

```bash
# Verificar que las librerías se instalaron correctamente
python -c "import numpy, deap, scipy, pandas, matplotlib, seaborn; print('✓ Todas las dependencias instaladas correctamente')"
```

### Ejecución Rápida

```bash
# Ejecutar implementación Python Puro
cd jssp_puro
python main.py

# O ejecutar implementación DEAP
cd ../jssp_deap
python main.py

# Realizar análisis comparativo
cd ../analysis
python analisis_comparativo.py
```

### Desactivar Entorno

```bash
conda deactivate
```

---

## Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido) 
   - [Requisitos Previos](#requisitos-previos)
   - [Instalación y Configuración](#instalación-y-configuración)
   - [Ejecución Rápida](#ejecución-rápida)
2. [Introducción](#introducción)
3. [Motivación](#motivación)
4. [Objetivos](#objetivos)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Algoritmo Evosocial](#algoritmo-evosocial)
7. [Implementaciones](#implementaciones)
   - [Implementación Pascal (Original)](#implementación-pascal-original)
   - [Implementación Python Puro](#implementación-python-puro)
   - [Implementación Python con DEAP](#implementación-python-con-deap)
8. [Dataset de Instancias](#dataset-de-instancias)
9. [Experimentación y Resultados](#experimentación-y-resultados)
10. [Análisis Comparativo](#análisis-comparativo)
11. [Instalación y Uso](#instalación-y-uso)
12. [Resultados Experimentales](#resultados-experimentales)
13. [Conclusiones](#conclusiones)
14. [Referencias](#referencias)
15. [Licencia](#licencia)

---

## Introducción

Este proyecto presenta una **implementación moderna en Python** del algoritmo evolutivo híbrido **Evosocial**, originalmente desarrollado hace más de 15 años en Pascal para resolver el problema de **Job Shop Scheduling** (JSSP). El trabajo incluye tres implementaciones:

1. **Implementación original en Pascal** (evosocial_pascal/)
2. **Implementación Python pura** (jssp_puro/)
3. **Implementación Python con librería DEAP** (jssp_deap/)

El proyecto incluye experimentación exhaustiva con **30 corridas** en instancias de benchmark estándar (swv06, swv07, swv08) y análisis estadístico comparativo completo.

---

## Motivación

El algoritmo **Evosocial** original demostró ser innovador al combinar un individuo élite persistente ("Queen") con individuos aleatorios frescos en cada generación, creando un balance único entre **explotación dirigida** y **exploración masiva**.

La migración a Python permite:

- **Modernización**: Aprovechar librerías optimizadas como DEAP, NumPy y SciPy
- **Extensibilidad**: Facilitar experimentación con variaciones del algoritmo
- **Análisis avanzado**: Integrar herramientas de visualización y análisis estadístico (Matplotlib, Seaborn, Pandas)
- **Reproducibilidad**: Proporcionar una implementación documentada y estructurada
- **Comparabilidad**: Evaluar el impacto de usar frameworks evolutivos modernos vs implementación directa

---

## Objetivos

### Objetivo Principal

Desarrollar implementaciones fieles del algoritmo Evosocial que preserven su estrategia evolutiva híbrida mientras se evalúa el impacto de:
- Implementación directa en Python
- Uso de frameworks evolutivos modernos (DEAP)

### Objetivos Específicos

1. **Preservar la lógica core** del algoritmo original:
   - Estrategia Queen (individuo élite persistente)
   - Decisión estocástica (65% crossover, 35% mutación)
   - Order Crossover (OX) y Shift Mutation

2. **Evaluar rendimiento comparativo**:
   - Calidad de soluciones (makespan)
   - Tiempo de ejecución
   - Convergencia del algoritmo

3. **Realizar análisis estadístico riguroso**:
   - Pruebas de Wilcoxon y Mann-Whitney U
   - Análisis de significancia estadística
   - Visualizaciones comparativas

4. **Proporcionar arquitectura extensible** para futuras investigaciones

---

## Estructura del Proyecto

```
jssp_ae/
├── README.md                          # Este archivo
├── evosocial_pascal/                  # Implementación original en Pascal
│   ├── README.md                      # Documentación detallada del algoritmo
│   ├── evosocial.pas                  # Programa principal
│   ├── varglo.pas                     # Variables globales y tipos
│   ├── crossvs.pas                    # Order Crossover
│   ├── op_mut.pas                     # Operadores de mutación
│   ├── utility.pas                    # Funciones utilitarias
│   ├── estadis.pas                    # Estadísticas
│   ├── report.pas                     # Reportes
│   ├── DATOS.DAT                      # Parámetros de configuración
│   └── datos/                         # Datos de prueba
│
├── jssp_puro/                         # Implementación Python pura
│   ├── main.py                        # Algoritmo completo
│   ├── globals.py                     # Variables globales y tipos
│   └── DATOS.DAT                      # Parámetros
│
├── jssp_deap/                         # Implementación Python con DEAP
│   ├── main.py                        # Algoritmo usando DEAP
│   └── DATOS.DAT                      # Parámetros
│
├── instancias/                        # Instancias de benchmark JSSP
│   ├── converted_swv06.txt            # 20 jobs × 15 máquinas
│   ├── converted_swv07.txt            # 20 jobs × 15 máquinas
│   ├── converted_swv08.txt            # 20 jobs × 15 máquinas
│   └── ...                            # Otras instancias
│
├── analysis/                          # Análisis estadístico y resultados
│   ├── analisis_comparativo.py        # Script de análisis completo
│   ├── puro/                          # Resultados Python puro
│   │   ├── resumen_converted_swv06.txt
│   │   ├── detalle_converted_swv06.txt
│   │   ├── tiempo_ejecucion_puro_converted_swv06.txt
│   │   └── ... (swv07, swv08)
│   ├── deap/                          # Resultados Python DEAP
│   │   ├── resumen_converted_swv06.txt
│   │   ├── detalle_converted_swv06.txt
│   │   ├── tiempo_ejecucion_deap_converted_swv06.txt
│   │   └── ... (swv07, swv08)
│   └── analisis_comparativo/          # Resultados del análisis
│       ├── pruebas_estadisticas/      # Tests estadísticos
│       ├── visualizaciones/           # Gráficos comparativos
│       └── datos_exportados/          # CSV con resultados
│
└── utils/                             # Utilidades
    └── conversion.py                  # Conversión de formatos de instancias
```

---

## Algoritmo Evosocial

### Características Principales

**Evosocial** es un algoritmo evolutivo **híbrido** que combina:

1. **Estrategia Social Atípica**:
   - Mantiene un único individuo élite llamado **"Queen"**
   - No mantiene población diversa persistente
   - Genera individuos **aleatorios frescos** en cada generación (inmigrantes)

2. **Decisión Estocástica**:
   - **65% probabilidad**: Crossover entre Queen e inmigrante
   - **35% probabilidad**: Mutación de ambos individuos

3. **Operadores Genéticos**:
   - **Crossover**: Order Crossover (OX) - preserva orden relativo
   - **Mutación**: Shift Mutation (desplazamiento circular)
   - **Selección**: Elitista estricta - actualiza Queen solo si hay mejora

### Pseudocódigo del Algoritmo

```
Algoritmo Evosocial(instancia, parámetros):

    # Inicialización
    Queen ← Generar_Individuo_Aleatorio()
    Evaluar(Queen)
    mejor_global ← Queen.makespan
    gen_mejor ← 0

    # Evolución
    Para gen = 1 hasta MAX_GEN:

        Para i = 1 hasta POPSIZE:
            # Generar inmigrante aleatorio
            inmigrante ← Generar_Individuo_Aleatorio()
            Evaluar(inmigrante)

            # Decisión estocástica
            Si random() < P_CROSS:
                # Aplicar crossover
                hijo1, hijo2 ← OrderCrossover(Queen, inmigrante)
                Evaluar(hijo1)
                Evaluar(hijo2)
                candidato ← Mejor(hijo1, hijo2)
            Sino:
                # Aplicar mutación
                Si random() < P_MUT:
                    ShiftMutation(Queen)
                    Evaluar(Queen)
                Si random() < P_MUT:
                    ShiftMutation(inmigrante)
                    Evaluar(inmigrante)
                candidato ← Mejor(Queen, inmigrante)

            # Actualizar estadísticas poblacionales
            Actualizar_Stats(candidato)

        # Actualizar Queen si hay mejora global
        Si mejor_de_generacion.makespan < mejor_global:
            Queen ← mejor_de_generacion
            mejor_global ← Queen.makespan
            gen_mejor ← gen

    Retornar Queen, mejor_global, gen_mejor
```

### Componentes Clave

#### 1. Representación
- **Cromosoma**: Permutación de jobs (1 a N)
- **Ejemplo** (N=5): [3, 1, 5, 2, 4]
- Cada gen representa un job en el orden de scheduling

#### 2. Order Crossover (OX)

```
Padre1: [1 2 3 | 4 5 | 6 7 8]
Padre2: [5 4 6 | 7 8 | 1 2 3]
              ↓
Hijo1:  [2 3 7 | 4 5 | 8 1 6]
Hijo2:  [3 4 1 | 7 8 | 2 5 6]
```

- Preserva orden relativo de genes
- Mantiene validez de permutación

#### 3. Shift Mutation

```
Original: [1 2 3 4 5 6 7 8]
Seleccionar posición 3, shift 2 → izquierda
Resultado: [3 1 2 4 5 6 7 8]
```

- Desplazamiento circular de elementos
- Mantiene diversidad genética

#### 4. Evaluación (Scheduler No-Delay)

El fitness se calcula mediante un scheduler que:
1. Asigna jobs a máquinas siguiendo el orden del cromosoma
2. Respeta precedencia de operaciones
3. Calcula **makespan** = tiempo de finalización del último job
4. **Fitness** = 1/makespan (minimización)

---

## Implementaciones

### Implementación Pascal (Original)

**Ubicación**: `evosocial_pascal/`

- **Lenguaje**: Object Pascal (Free Pascal/Lazarus)
- **Características**:
  - Implementación histórica (15+ años)
  - Código modular estructurado en units
  - Límites fijos: 100 jobs × 5 máquinas
  - Sin dependencias externas

**Compilación**:
```bash
cd evosocial_pascal
fpc evosocial.pas
./evosocial
```

**Documentación completa**: Ver `evosocial_pascal/README.md`

---

### Implementación Python Puro

**Ubicación**: `jssp_puro/`

- **Características**:
  - Traducción directa del algoritmo Pascal
  - Sin frameworks evolutivos
  - Usa NumPy para operaciones vectoriales
  - Implementación completa de todos los operadores

**Ventajas**:
- Control total sobre el algoritmo
- Fácil debugging y modificación
- Mínimas dependencias

**Ejecutar**:
```bash
cd jssp_puro
python main.py
```

**Parámetros configurables** (`DATOS.DAT`):
```
30          # cantcorr: número de corridas
0.05        # pmutacion: probabilidad de mutación
0.65        # pcross: probabilidad de crossover
500         # maxgen: máximo de generaciones
250         # popsize: tamaño de población
```

**Salidas generadas**:
- `resumen_*.txt`: Resultados por corrida
- `detalle_*.txt`: Convergencia generación a generación
- `tiempo_ejecucion_puro_*.txt`: Tiempos de ejecución

---

### Implementación Python con DEAP

**Ubicación**: `jssp_deap/`

- **Características**:
  - Usa framework DEAP (Distributed Evolutionary Algorithms in Python)
  - Aprovecha operadores optimizados
  - Representación adaptada para JSSP
  - Misma lógica evolutiva que versión pura

**Ventajas**:
- Operadores evolutivos optimizados
- Infraestructura probada
- Facilita experimentación

**Diferencias clave con versión pura**:
1. **Representación**: Lista de jobs repetidos (cada job aparece M veces)
2. **Decodificación**: Scheduler adapta secuencia a operaciones
3. **Operadores**: Implementados como wrappers de DEAP

**Ejecutar**:
```bash
cd jssp_deap
python main.py
```

**Dependencias**:
```bash
pip install deap numpy
```

---

## Dataset de Instancias

### Fuente

Dataset extraído del repositorio **JSPLIB** - "Benchmark instances for the job-shop scheduling problem (minimizing makespan)"

**Repositorio**: [https://github.com/tamy0612/JSPLIB](https://github.com/tamy0612/JSPLIB)

### Instancias Convertidas

Directorio: `instancias/`

| Instancia | Jobs | Máquinas | Lower Bound | Upper Bound | Dificultad |
|-----------|------|----------|-------------|-------------|------------|
| swv06     | 20   | 15       | 1591        | 1678        | Media      |
| swv07     | 20   | 15       | 1446        | 1594        | Media-Alta |
| swv08     | 20   | 15       | 1640        | 1752        | Media      |
| swv09     | 20   | 15       | 1604        | 1655        | Media      |
| swv10     | 20   | 15       | 1631        | 1743        | Media      |
| swv11     | 50   | 10       | 2983        | 3664        | Alta       |
| swv12     | 50   | 10       | 2972        | 3618        | Alta       |
| swv15     | 50   | 10       | 2885        | 3645        | Alta       |

### Formato de Instancias

```
upperb                    # Cota superior conocida
lowerb                    # Cota inferior conocida
t[1,1] t[1,2] ... t[1,N]  # Tiempos máquina 1
t[2,1] t[2,2] ... t[2,N]  # Tiempos máquina 2
...
t[M,1] t[M,2] ... t[M,N]  # Tiempos máquina M
```

### Conversión de Formato

Script: `utils/conversion.py`

```bash
python utils/conversion.py
```

Convierte instancias del formato JSPLIB al formato requerido por el algoritmo.

---

## Experimentación y Resultados

### Configuración Experimental

**Parámetros del algoritmo**:
- **Corridas independientes**: 30
- **Generaciones**: 500
- **Tamaño de población**: 250
- **Probabilidad de crossover**: 0.65 (65%)
- **Probabilidad de mutación**: 0.05 (5%)

**Instancias evaluadas**: swv06, swv07, swv08

**Hardware utilizado**:
- Procesador: AMD Ryzen 9 5900x
- RAM: 32 GB @3200 Mhz
- Sistema Operativo: Pop!_OS 22.04 LTS x86_64 | Linux 6.16.3

**Total de experimentos**: 180 corridas (30 × 3 instancias × 2 implementaciones)

---

## Análisis Comparativo

### Script de Análisis

**Ubicación**: `analysis/analisis_comparativo.py`

**Funcionalidades**:

1. **Carga de resultados**: Lee archivos de resumen, detalle y tiempos
2. **Análisis estadístico**:
   - Pruebas de Wilcoxon signed-rank
   - Pruebas de Mann-Whitney U
   - Cálculo de medias, desviaciones, medianas
3. **Visualizaciones**:
   - Box plots y violin plots de makespan
   - Gráficos de convergencia
   - Comparación de tiempos de ejecución
   - Trade-off tiempo vs calidad
4. **Exportación**: CSV con resultados completos

**Ejecutar análisis**:
```bash
cd analysis
python analisis_comparativo.py
```

### Clase AnalizadorEvosocial

```python
analizador = AnalizadorEvosocial(directorio_salida="analisis_comparativo")

# Cargar resultados
analizador.cargar_resultados("puro", "puro/", instancias=["swv06", "swv07", "swv08"])
analizador.cargar_resultados("deap", "deap/", instancias=["swv06", "swv07", "swv08"])

# Comparar
analizador.comparar_algoritmos("puro", "deap")

# Visualizar
analizador.crear_visualizaciones("puro", "deap")
analizador.crear_graficos_convergencia("puro", "deap")

# Exportar
analizador.exportar_csv("puro", "deap")
```

---

## Resultados Experimentales

### Resumen Global

**Análisis estadístico completo**: `analysis/analisis_comparativo/pruebas_estadisticas/`

| Métrica | Python Puro | Python DEAP | Mejora DEAP |
|---------|-------------|-------------|-------------|
| **Tiempo Promedio** | 29.68 min | 27.84 min | **+6.20%** ⚡ |
| **Victorias (calidad)** | 3/3 | 0/3 | - |
| **Diferencias significativas** | - | - | 3/3 ✓ |

### Resultados por Instancia

#### swv06 (20×15)

| Implementación | Mejor | Media ± Std | Mediana | GenMax | Tiempo |
|----------------|-------|-------------|---------|--------|--------|
| **Python Puro** | **2053** | **2075.17 ± 11.87** | **2077** | 242.8 | 1777.81s |
| Python DEAP | 2376 | 2641.70 ± 95.15 | 2658.5 | 453.1 | 1685.69s |
| **Ventaja Puro** | **-15.73%** | **-27.30%** | - | - | +5.18% |

- **p-value (Wilcoxon)**: 0.0000 ✓ (significativo)
- **p-value (Mann-Whitney)**: 0.0000 ✓ (significativo)
- **Upper Bound**: 1678

#### swv07 (20×15)

| Implementación | Mejor | Media ± Std | Mediana | GenMax | Tiempo |
|----------------|-------|-------------|---------|--------|--------|
| **Python Puro** | **1934** | **1973.93 ± 16.31** | **1973.5** | 260.8 | 1772.59s |
| Python DEAP | 2367 | 2515.60 ± 88.95 | 2512 | 445.0 | 1661.19s |
| **Ventaja Puro** | **-22.39%** | **-27.44%** | - | - | +6.28% |

- **p-value (Wilcoxon)**: 0.0000 ✓ (significativo)
- **p-value (Mann-Whitney)**: 0.0000 ✓ (significativo)
- **Upper Bound**: 1594

#### swv08 (20×15)

| Implementación | Mejor | Media ± Std | Mediana | GenMax | Tiempo |
|----------------|-------|-------------|---------|--------|--------|
| **Python Puro** | **2153** | **2174.97 ± 9.89** | **2176.5** | 234.7 | 1792.51s |
| Python DEAP | 2466 | 2691.17 ± 96.62 | 2718.5 | 455.9 | 1664.56s |
| **Ventaja Puro** | **-14.54%** | **-23.73%** | - | - | +7.14% |

- **p-value (Wilcoxon)**: 0.0000 ✓ (significativo)
- **p-value (Mann-Whitney)**: 0.0000 ✓ (significativo)
- **Upper Bound**: 1752

### Visualizaciones

Todas las visualizaciones están disponibles en: `analysis/analisis_comparativo/visualizaciones/`

1. **Box plots comparativos**: Distribución de makespan
2. **Violin plots**: Distribución detallada de resultados
3. **Gráficos de convergencia**: Evolución del mejor makespan
4. **Comparación de tiempos**: Barras lado a lado
5. **Trade-off tiempo vs calidad**: Scatter plot

---

## Conclusiones

### Hallazgos Principales

1. **Calidad de Soluciones**:
   - **Python Puro supera consistentemente a DEAP** en calidad de soluciones
   - Mejora promedio: **15-27%** en makespan
   - Diferencias **estadísticamente significativas** (p < 0.0001)
   - Menor desviación estándar (más consistente)

2. **Tiempo de Ejecución**:
   - **DEAP es ~6% más rápido** en promedio
   - Diferencia: ~2 minutos por instancia (30 corridas)
   - Trade-off: Velocidad vs Calidad

3. **Convergencia**:
   - **Puro encuentra mejores soluciones más rápido**
   - GenMax promedio: 246 (puro) vs 451 (deap)
   - Convergencia ~48% más temprana

### Análisis de Diferencias

**¿Por qué Python Puro supera a DEAP?**

1. **Representación del Problema**:
   - **Puro**: Permutación directa de jobs (más natural para JSSP)
   - **DEAP**: Jobs repetidos M veces (overhead en decodificación)

2. **Scheduler**:
   - **Puro**: Scheduler optimizado específicamente para el formato
   - **DEAP**: Necesita procesamiento adicional por representación indirecta

3. **Operadores**:
   - Ambos usan Order Crossover y Shift Mutation
   - Implementación pura tiene control fino sobre aplicación

4. **Overhead del Framework**:
   - DEAP añade abstracciones generales
   - Puro elimina overhead innecesario

### Recomendaciones

**Para Investigación**:
- Usar **Python Puro** cuando la calidad de solución es crítica
- Considerar DEAP solo si se requiere experimentación rápida
- Explorar representaciones alternativas en DEAP

**Para Producción**:
- **Python Puro** es preferible para JSSP
- Balance entre desarrollo rápido (DEAP) vs rendimiento (puro)

**Trabajo Futuro**:
1. Optimizar representación en DEAP para JSSP
2. Evaluar instancias más grandes (50×10, 100×5)
3. Hibridación con búsqueda local
4. Paralelización de corridas

---

## Instalación y Uso

### Requisitos

**Python**:
- Python 3.10+
- pip

**Pascal** (opcional):
- Free Pascal Compiler (FPC) 2.0+
- Lazarus IDE (recomendado)

### Instalación

```bash
# Clonar repositorio
git clone <repository-url>
cd jssp_ae

# Instalar dependencias Python
pip install numpy scipy matplotlib seaborn pandas deap

# O usar requirements (si existe)
pip install -r requirements.txt
```

### Uso Básico

#### 1. Ejecutar Python Puro

```bash
cd jssp_puro
# Editar main.py para seleccionar instancia
python main.py
```

#### 2. Ejecutar Python DEAP

```bash
cd jssp_deap
# Editar main.py para seleccionar instancia
python main.py
```

#### 3. Análisis Comparativo

```bash
cd analysis
python analisis_comparativo.py
```

### Configuración de Parámetros

Editar archivo `DATOS.DAT` en cada directorio:

```
30          # Número de corridas
0.05        # Probabilidad de mutación
0.65        # Probabilidad de crossover
500         # Máximo de generaciones
250         # Tamaño de población
```

### Seleccionar Instancia

En `main.py`:

```python
# Cambiar esta línea
archivo_instancia = 'converted_swv06.txt'  # o swv07, swv08, etc.
```

---

## Referencias

### Bibliografía del Algoritmo

1. **JSPLIB**: Benchmark instances for Job Shop Scheduling
   - Repository: https://github.com/tamy0612/JSPLIB

2. **Order Crossover (OX)**:
   - Davis, L. (1985). "Applying Adaptive Algorithms to Epistatic Domains"

3. **Job Shop Scheduling**:
   - Graham, R.L., et al. (1979). "Optimization and Approximation in Deterministic Sequencing and Scheduling"

### Herramientas y Frameworks

- **DEAP**: [https://github.com/DEAP/deap](https://github.com/DEAP/deap)
- **NumPy**: [https://numpy.org/](https://numpy.org/)
- **SciPy**: [https://scipy.org/](https://scipy.org/)
- **Matplotlib**: [https://matplotlib.org/](https://matplotlib.org/)
- **Free Pascal**: [https://www.freepascal.org/](https://www.freepascal.org/)

---

## Alcance

La implementación se enfoca en **Job Shop Scheduling**, manteniendo compatibilidad con las instancias de benchmark estándar y extendiendo soporte para instancias de mayor escala. Está dirigido a:

- **Investigación académica** en algoritmos evolutivos
- **Educación** en computación evolutiva
- **Aplicaciones industriales** de scheduling

---

## Licencia

Licencia MIT - ver archivo LICENSE para detalles.

---

## Contribuciones

1. Hacer fork del repositorio
2. Crear una rama de característica (`git checkout -b feature/nueva-caracteristica`)
3. Hacer cambios con pruebas
4. Commit de cambios (`git commit -m 'Agregar nueva característica'`)
5. Push a la rama (`git push origin feature/nueva-caracteristica`)
6. Enviar pull request

---

## Documentación Adicional

Para guías detalladas, consulta:

- **Algoritmo Pascal**: `evosocial_pascal/README.md`
- **Documentación de código**: Docstrings en archivos Python
- **Análisis estadístico**: `analysis/analisis_comparativo/pruebas_estadisticas/`

---

## Contacto

Para preguntas o sugerencias sobre este proyecto:

- Fabian Sarmiento: fsarmiento1805@gmail.com
- Jorge Ceferino Valdez: jorgecvaldez@gmail.com

---

**Estado del proyecto**: Completo y funcional
