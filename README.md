![header](doc/imgs/LogoHeader.png)
# Maestría en Inteligencia Artificial FIUBA

# Trabajo Práctico Desafío - Algoritmos Evolutivos I

# AG Python 
## Implementación moderna del algoritmo evolutivo híbrido

## Integrantes:

- Fabian Sarmiento.
- Jorge Ceferino Valdez.

## Introducción

Este proyecto presenta una implementación moderna en Python del algoritmo evolutivo híbrido Evosocial, originalmente desarrollado hace más de 15 años en Pascal para resolver el problema de Job Shop Scheduling (JSS). La implementación actual utiliza librerías especializadas en algoritmos evolutivos de Python para proporcionar una versión actualizada y de alto rendimiento del algoritmo original.

## Motivación

El algoritmo EvoSocial original demostró ser innovador al combinar un individuo élite persistente ("Queen") con individuos aleatorios frescos en cada generación, creando un balance único entre explotación dirigida y exploración masiva. La migración a Python permite:

- **Modernización**: aprovechar librerías optimizadas como DEAP, GEATPY o PyGAD.
- **Extensibilidad**: facilitar experimentación con variaciones del algoritmo.
- **Análisis avanzado**: integrar herramientas de visualización y análisis estadístico.
- **Reproducibilidad**: proporcionar una implementación documentada y estructurada.

## Objetivos

**Objetivo principal**: desarrollar una implementación fiel del algoritmo Evosocial que preserve su estrategia evolutiva híbrida mientras aprovecha las ventajas de las librerías modernas de Python.

**Objetivos específicos**:
- Mantener la lógica core del algoritmo original (estrategia Queen, decisión estocástica, Order Crossover).
- Utilizar implementaciones optimizadas de operadores evolutivos.
- Permitir configuración dinámica de parámetros.
- Facilitar comparación directa con resultados originales en Pascal.
- Proporcionar arquitectura extensible para variaciones experimentales.

## Dataset de instancias:

El dataset de instancias empleado fue extraido del repositorio JSPLIB "Benchmark instances for the job-shop scheduling problem (minimizing makespan)."

[Repositorio](https://github.com/tamy0612/JSPLIB#)

En el directorio utils se puede encontrar un script Python que realiza la lectura de las instancias disponibles en el repositorio. En nuestro caso convertimos las instancias:
 - swv06 
 - swv07 
 - swv08 
 - swv09 
 - swv10
 - swv11
 - swv12
 - swv15

Las mismas se encuentran convertidas al formato que empleamos en el directorio instancias.
Para la conversión del formato de JSPLIB a nuestro formato empleamos la siguiente instrucción desde el repositorio JSPLIB clonado:

$ python conversion.py

## Alcance

La implementación se enfoca en Job Shop Scheduling, manteniendo compatibilidad con las instancias de benchmark estándar (100 jobs × 5 máquinas) y extendiendo soporte para instancias de mayor escala. Está dirigido a investigación académica, educación en computación evolutiva y aplicaciones industriales de scheduling.


---


## Trabajando con DEAP

Este proyecto implementa un Algoritmo Genético (GA) utilizando DEAP
```
tpfinal/
├── ga_deap.py
├── instancias/
│   ├── 100X5-10.txt
│   ├── ... (otros archivos de instancias)
├── evolution_<instancia>.png  # Gráficos generados
├── jssp_results.csv           # Resumen de resultados
```

Instalar dependencias:
```
pip install deap numpy pandas matplotlib seaborn
```
### Formato de Archivo de Instancia

* Línea 1: Mejor valor obtenido (entero, ignorado por el GA)

* Línea 2: Segundo valor (entero, ignorado por el GA)

* Línea 3 en adelante: Cada línea representa un trabajo (job), con pares de [máquina] [tiempo_de_proceso] (enteros).

Ejemplo:

```
5328
5272
88 11 99 20 63 67 79 91 13 77 ...
43 9 81 83 90 44 60 70 85 11 ...
```

### Cómo Ejecutar

1. Coloca tus archivos de instancia .txt en la carpeta instancias/.

2. Ejecuta el script desde el directorio del proyecto:

```
python ga_deap.py
```

3. El script realizará las siguientes acciones:

* Procesará cada archivo de instancia

* Ejecutará el algoritmo genético

* Guardará los gráficos de evolución (evolution_<instancia>.png)

* Guardará los resultados en jssp_results.csv

* Mostrará un resumen en la consola

### Resultados

* Gráficos: Evolución del makespan por generación para cada instancia.

* CSV: Resumen del mejor makespan y la secuencia óptima encontrada para cada instancia.

### Solución de Problemas

* Si aparece un error como “list assignment index out of range”, revisa el formato del archivo de instancia.

* Asegúrate de que todos los trabajos tengan el mismo número de pares máquina/tiempo.

* Si aparece “Instance must have at least one job”, revisa que el archivo no tenga líneas vacías o datos faltantes.

## Licencia

Licencia MIT - ver archivo LICENSE para detalles.

## Contribuciones

1. Hacer fork del repositorio
2. Crear una rama de característica
3. Hacer cambios con pruebas
4. Enviar pull request

## Documentación

Para guías detalladas, consulta la documentación del código fuente.
![header](doc/imgs/LogoFooter.png)