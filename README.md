# Maestría en Inteligencia Artificial FIUBA

# Trabajo Práctico Desafío - Algoritmos Evolutivos I

# Evosocial Python 
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



TODO: Falta completar

## Licencia

Licencia MIT - ver archivo LICENSE para detalles.

## Contribuciones

1. Hacer fork del repositorio
2. Crear una rama de característica
3. Hacer cambios con pruebas
4. Enviar pull request

## Documentación

Para guías detalladas, consulta la documentación del código fuente.