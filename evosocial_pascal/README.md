# Evosocial - Algoritmo evolutivo híbrido para Job Shop Scheduling

## Descripción general

Evosocial es un algoritmo evolutivo híbrido desarrollado hace más de 15 años en Pascal/Object Pascal para resolver el problema de **Job Shop Scheduling** (JSS). El proyecto implementa una estrategia evolutiva social atípica que combina elementos de algoritmos genéticos tradicionales con una aproximación basada en un individuo élite persistente denominado "Queen".

El objetivo principal es encontrar la secuencia óptima de trabajos (jobs) en múltiples máquinas para minimizar el tiempo total de finalización (makespan), un problema fundamental en la optimización de procesos industriales y manufactureros.

## Características del algoritmo

### Estrategia evolutiva híbrida

Evosocial se clasifica como híbrido debido a su combinación única de paradigmas evolutivos:

- **Estrategia social**: mantiene un único individuo élite ("Queen") en lugar de una población diversa persistente.
- **Exploración masiva**: genera individuos aleatorios frescos en cada iteración.
- **Explotación dirigida**: utiliza crossover Order (OX) entre Queen e individuos aleatorios.
- **Decisión estocástica**: alterna probabilísticamente entre crossover (65%) y mutación directa (35%).

### Componentes evolutivos

1. **Representación**: cromosomas como permutaciones de jobs (1 a N).
2. **Crossover**: order crossover (OX) que preserva el orden relativo.
3. **Mutación**: shift mutation (desplazamiento) y Exchange mutation (intercambio).
4. **Selección**: fstrategia elitista estricta con actualización condicional de Queen.
5. **Evaluación**: función objetivo basada en makespan del scheduler no-delay.

## Arquitectura del sistema

### Estructura de archivos

```
evosocial/
├── evosocial.pas          # Programa principal con lógica evolutiva.
├── evosocial.lpi          # Configuración del proyecto Lazarus.
├── varglo.pas             # Definiciones globales y tipos de datos.
├── crossvs.pas            # Implementación del operador Order Crossover.
├── op_mut.pas             # Operadores de mutación (shift y exchange).
├── utility.pas            # Funciones utilitarias y validación.
├── estadis.pas            # Recopilación de estadísticas poblacionales.
├── report.pas             # Generación de reportes de resultados.
├── evosocial.rc           # Recursos del proyecto.
├── DATOS.DAT              # Archivo de configuración de parámetros.
└── datos                  # Directorio donde se encuentran los datos de entrada y salida.
    ├── 100X5-1.TXT        # Se incluyeron aqui para no sobrecargar el raiz, sin embargo.
    ├── 100X5-2.TXT        # durante la ejecución deben encontrasre en el raiz.
    ├── ...               
    ├── 100X5-10.TXT
    ├── eas100-1.TXT
    ├── eas100-2.TXT
    ├── ...
    ├── eas100-10.TXT
    ├── resumen.pas      
    └── resumen.pas      
```

### Tipos de datos principales

```pascal
const
  maxcrom = 100;     // Máximo número de jobs
  maxmaq = 5;        // Máximo número de máquinas

type
  alelo = byte;                                    // Posición de job
  cromosoma = array[1..maxcrom] of alelo;         // Secuencia de jobs
  
  individuo = RECORD
    cromosoma : cromosoma;    // Permutación de jobs
    objective : real;         // Makespan (tiempo total)
    fitness   : real;         // Fitness = 1/objective
  END;
  
  tipoMaqJob = array[1..maxmaq, 1..maxcrom] of byte;  // Tiempos de procesamiento
```

## Algoritmo principal

### Flujo de ejecución

1. **Inicialización**:
   - Carga parámetros desde DATOS.DAT
   - Lee instancia del problema (matriz de tiempos)
   - Genera individuo Queen inicial aleatoriamente

2. **Ciclo Evolutivo por Generación**:
   ```
   Para cada individuo en popsize:
     1. Generar individuo aleatorio/inmigrante aleatorio (ri)
     2. Decisión estocástica basada en pcross:
        
        Si crossover (probabilidad 65%):
          - Aplicar Order Crossover entre Queen y ri
          - Evaluar ambos offspring (hijos)
          - Seleccionar mejor offspring
        
        Si no crossover (probabilidad 35%):
          - Aplicar mutación shift a Queen (probabilidad pmutacion)
          - Aplicar mutación shift a ri (probabilidad pmutacion)
          - Seleccionar mejor entre Queen y ri
     
     3. Actualizar estadísticas poblacionales
   ```

3. **Actualización de Queen**:
   - Si el mejor individuo de la generación mejora a Queen actual
   - Queen := mejor individuo
   - Actualizar estadísticas globales

### Evaluación - Job Shop Scheduler

El algoritmo implementa un scheduler **no-delay** que:

1. **Asigna jobs a máquinas** siguiendo la secuencia del cromosoma.
2. **Respeta restricciones de precedencia** entre operaciones.
3. **Calcula makespan** como tiempo de finalización del último job.
4. **Usa matriz de posiciones** para tracking temporal: `Pos[máquina, posición]`.

La función objetivo es **minimizar el makespan**, con fitness calculado como `1/objective`.

## Operadores genéticos

### Order crossover (OX) - crossvs.pas

Implementación clásica del Order Crossover para permutaciones:

1. Generar dos puntos de corte aleatorios.
2. Copiar segmento del primer padre al hijo.
3. Completar posiciones restantes con genes del segundo padre en orden original.
4. Aplicar mutación probabilística a offspring.
5. Generar dos hijos intercambiando roles de padres.

### Operadores de mutación - op_mut.pas

**Shift mutation (mutshift)**:
- Selecciona posición aleatoria y desplazamiento.
- Mueve elemento a nueva posición (manejo circular).
- Desplaza elementos intermedios para mantener permutación válida.

**Exchange mutation (mutacion)**:
- Selecciona dos posiciones aleatorias diferentes.
- Intercambia contenido de ambas posiciones.

## Configuración y parámetros

### Archivo DATOS.DAT

```
30 0.05 0.65 500 250
```

**Parámetros**:

- `cantcorr = 30`: número de ejecuciones independientes.
- `pmutacion = 0.05`: probabilidad de mutación (5%).
- `pcross = 0.65`: probabilidad de crossover (65%).
- `maxgen = 500`: Mmximo número de generaciones.
- `popsize = 250`: tamaño de población por generación.

### Formato de instancias del problema

El programa espera un archivo de instancia (ej: `100X5-10.txt`) con formato:

```
upperb                    // Límite superior conocido del problema
lowerb                    // Límite inferior conocido del problema
t[1,1] t[1,2] ... t[1,N]  // Tiempos máquina 1 para jobs 1..N
t[2,1] t[2,2] ... t[2,N]  // Tiempos máquina 2 para jobs 1..N
...
t[M,1] t[M,2] ... t[M,N]  // Tiempos máquina M para jobs 1..N
```

**Compatibilidad**: el formato es compatible con instancias estándar del repositorio de benchmarks de Job Shop Scheduling disponible en el repositorio de referencia.

## Compilación y ejecución

### Requisitos del sistema

- **Compilador**: Free Pascal Compiler (FPC) 2.0 o superior.
- **IDE**: Lazarus (recomendado) o línea de comandos.
- **Sistema operativo**: Windows, Linux, macOS (multiplataforma).

### Instrucciones de compilación

**Usando Lazarus**:

1. Abrir archivo `evosocial.lpi` en Lazarus
2. Compilar: Run → Compile (Ctrl+F9)
3. Ejecutar: Run → Run (F9)

**Usando línea de comandos**:

```bash
fpc evosocial.pas
./evosocial        # En Linux/macOS
evosocial.exe      # En Windows
```

### Archivos de entrada requeridos

- `DATOS.DAT`: parámetros de configuración del algoritmo.
- `100X5-10.txt`: instancia del problema (nombre configurable en código).

### Archivos de salida generados

- `detalle.txt`: progreso por generación (generación, mejor_fitness, evaluaciones).
- `resumen.txt`: resultados finales por corrida (corrida, error_best, error_población, mejor_objetivo, generación_mejor).

## Métricas de evaluación

### Función objetivo
- **Makespan**: Tiempo total de finalización del scheduling.
- **Objetivo**: Minimización del makespan.
- **Fitness**: Transformación inversa (1/makespan).

### Métricas de calidad
- **Error Relativo Best**: `ebest = |upperb - mejor_global| / upperb × 100`
- **Error Relativo Población**: `epop = |upperb - promedio_población| / upperb × 100`

## Aplicaciones y casos de uso

### Problema principal: Job Shop Scheduling

**Descripción**: optimización de la secuencia de N jobs que deben procesarse en M máquinas.

**Restricciones**:
- Cada job tiene una secuencia fija de operaciones.
- Cada máquina procesa un job a la vez.
- No hay interrupción de operaciones (no-preemptive).
- Tiempos de procesamiento determinísticos.

**Objetivo**: Minimizar el tiempo total de finalización (makespan).

### Aplicaciones industriales

- **Planificación de producción** en entornos manufactureros.
- **Scheduling de procesos batch** en industrias químicas.
- **Asignación de recursos** en sistemas de producción flexible.
- **Optimización de líneas de ensamblaje** automotrices.
- **Gestión de operaciones** en talleres mecánicos.

## Limitaciones técnicas

### Restricciones de diseño
- **Escalabilidad fija**: limitado a 100 jobs y 5 máquinas máximo.
- **Memoria estática**: arrays de tamaño fijo compilados.
- **Representación simple**: solo permutaciones directas de jobs.
- **Evaluación básica**: scheduler no-delay sin optimizaciones.

### Limitaciones evolutivas
- **Diversidad limitada**: solo un individuo élite persiste entre generaciones.
- **Presión selectiva alta**: riesgo de convergencia prematura local.
- **Exploración dependiente**: calidad limitada por generación aleatoria.
- **Sin memoria adaptativa**: parámetros fijos durante ejecución.

## Ventajas del Diseño

### Fortalezas algorítmicas
- **Convergencia rápida**: Queen mantiene siempre la mejor solución encontrada.
- **Balance exploración/explotación**: decisión estocástica entre paradigmas evolutivos.
- **Robustez**: validación de cromosomas y múltiples corridas independientes.
- **Simplicidad**: implementación directa y comprensible del algoritmo.

### Características distintivas
- **Estrategia social única**: no sigue patrones tradicionales de algoritmos genéticos.
- **Hibridación efectiva**: combina elementos de AGs y estrategias evolutivas.
- **Especialización JSS**: optimizado específicamente para problemas de scheduling.
- **Portabilidad**: código Pascal estándar multiplataforma.

## Datos de benchmark

### Compatibilidad con Instancias Estándar

El proyecto está diseñado para trabajar con instancias de benchmark estándar del problema Job Shop Scheduling, específicamente aquellas disponibles en repositorios académicos de investigación. El formato de entrada es compatible con las instancias clásicas utilizadas en la literatura especializada.

### Instancias de prueba recomendadas

El código está configurado para instancias del tipo:
- **100×5**: 100 jobs, 5 máquinas
- **Formato estándar**: Matriz de tiempos de procesamiento
- **Límites conocidos**: Upperb y lowerb para evaluación de calidad

## Consideraciones de rendimiento

### Complejidad computacional
- **Evaluación**: O(M × N) por scheduler de individuo.
- **Generación**: O(PopSize × MaxGen) evaluaciones totales.
- **Crossover**: O(N) para Order Crossover.
- **Mutación**: O(N) para shift y exchange.

### Optimizaciones implementadas
- **Validación eficiente**: verificación rápida de permutaciones válidas.
- **Generación controlada**: evita cromosomas inválidos desde construcción.
- **Estadísticas incrementales**: actualización eficiente de métricas poblacionales.

## Historial y contexto

Este proyecto representa una implementación histórica de técnicas de computación evolutiva aplicadas a problemas de optimización combinatorial. Desarrollado hace más de 15 años, el código refleja las mejores prácticas y enfoques algorítmicos de la época en el campo de los algoritmos evolutivos para scheduling.

La implementación en Pascal demuestra la portabilidad y efectividad de los conceptos evolutivos independientemente del lenguaje de programación, proporcionando una base sólida para comprender los fundamentos de estas técnicas antes de su evolución hacia implementaciones más modernas.

## Licencia y Uso

Este código se proporciona con fines educativos y de investigación, representando una implementación histórica de algoritmos evolutivos para Job Shop Scheduling. Se recomienda su uso para:

- Estudio de algoritmos evolutivos clásicos.
- Comparación con implementaciones modernas.
- Base para nuevas investigaciones en scheduling evolutivo.
- Educación en computación evolutiva y optimización combinatorial.