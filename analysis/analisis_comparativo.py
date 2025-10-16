import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import os
from datetime import datetime
import seaborn as sns
import re


# Funciones de lectura de archivos.
def read_resumen(filepath):
    """
    Lee un archivo de resumen y extrae los resultados de optimización.
    Analiza un archivo de texto que contiene resultados de optimización donde cada línea no vacía
    debe contener al menos 5 valores separados por espacios. La función extrae estos valores
    y los retorna como una lista de diccionarios con datos estructurados.
    
    Args:
        filepath (str): Ruta al archivo que contiene los resultados de optimización.
    
    Returns:
        list[dict]: Una lista de diccionarios donde cada diccionario contiene:
            - indcorr (int): Valor de corrección individual
            - ebest (float): Mejor valor de error
            - epop (float): Valor de error de la población
            - mingl (float): Valor mínimo global
            - genmax (int): Valor máximo de generación
    
    Note:
        Omite líneas vacías y líneas con menos de 5 valores. Solo procesa
        líneas que coinciden con el formato esperado con exactamente 5 o más valores.
    """
    
    results = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 5:
                    results.append({
                        'indcorr': int(parts[0]),
                        'ebest': float(parts[1]),
                        'epop': float(parts[2]),
                        'mingl': float(parts[3]),
                        'genmax': int(parts[4])
                    })
    return results

def read_detalle(filepath):
    """
    Lee un archivo de detalle de convergencia y lo parsea en una lista de diccionarios.
    Se espera que el archivo contenga líneas con tres valores separados por espacios:
    número de generación, valor mínimo de makespan y número de evaluaciones.
    
    Args:
        filepath (str): Ruta al archivo que contiene los datos de convergencia.
    
    Returns:
        list: Una lista de diccionarios donde cada diccionario contiene:
            - 'gen' (int): Número de generación
            - 'mingl' (float): Valor mínimo de makespan para esa generación
            - 'evals' (int): Número de evaluaciones realizadas
    """
    
    convergence = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 3:
                    convergence.append({
                        'gen': int(parts[0]),
                        'mingl': float(parts[1]),
                        'evals': int(parts[2])
                    })
    return convergence

def read_tiempo_ejecucion(filepath):
    """
    Lee el tiempo de ejecución y nombre de instancia de un archivo de resultados JSSP.
    Esta función parsea un archivo de texto que contiene resultados de JSSP (Job Shop Scheduling Problem)
    para extraer el nombre de la instancia y el tiempo de ejecución. Busca patrones específicos
    en el archivo para identificar estos valores.
    
    Args:
        filepath (str): Ruta al archivo de texto que contiene los resultados JSSP.
    
    Returns:
        dict: Un diccionario con dos claves:
            - 'instancia' (str): El nombre de la instancia extraído del archivo.
            - 'tiempo_segundos' (float): El tiempo de ejecución en segundos.
    
    Note:
        La función espera que el archivo contenga líneas con patrones específicos:
        - El nombre de la instancia debe estar en una línea que comience con 'Instancia:'
        - El tiempo de ejecución debe estar en una línea que contenga 'Tiempo de ejecución:' 
          o 'Tiempo de ejecucion:' seguido de un número y 'segundos'
        Si no se encuentran los patrones, los valores correspondientes serán None.
    """

    tiempo = None
    instancia = None
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Instancia:'):
                instancia = line.split('Instancia:')[1].strip()
            elif 'Tiempo de ejecución:' in line or 'Tiempo de ejecucion:' in line:
                # Extraer número del tiempo
                match = re.search(r'(\d+\.?\d*)\s*segundos?', line)
                if match:
                    tiempo = float(match.group(1))
    
    return {'instancia': instancia, 'tiempo_segundos': tiempo}

# Clase analizador de tiempos
class AnalizadorEvosocial:
    """
    Analizador completo para comparar resultados de rendimiento de algoritmos evolutivos.
    
    Esta clase proporciona funcionalidad para cargar, analizar, comparar y visualizar
    resultados de diferentes algoritmos evolutivos, incluyendo métricas de tiempo de ejecución.
    
    Atributos:
        directorio_salida (str): Directorio de salida para los resultados del análisis
        datos_algoritmos (dict): Diccionario que almacena los datos de algoritmos cargados
        resultados_comparacion (dict): Diccionario que almacena los resultados de comparación
    
    Métodos:
        crear_directorios(): Crea estructura de directorios para archivos de salida
        cargar_resultados(): Carga resultados de algoritmos incluyendo tiempos de ejecución
        comparar_algoritmos(): Compara dos algoritmos estadísticamente
        crear_visualizaciones(): Crea visualizaciones de comparación
        crear_graficos_convergencia(): Crea gráficos de convergencia
        exportar_csv(): Exporta resultados a formato CSV
    
    La clase maneja detección automática de instancias, pruebas estadísticas (Wilcoxon y
    Mann-Whitney U), cálculo de métricas de rendimiento y visualización completa
    incluyendo box plots, violin plots, comparaciones de tiempo de ejecución
    y análisis de convergencia.
    """
    
    def __init__(self, directorio_salida="analisis_resultados"):
        self.directorio_salida = directorio_salida
        self.crear_directorios()
        self.datos_algoritmos = {}
        self.resultados_comparacion = {}
    
    def crear_directorios(self):
        """
        Crea los subdirectorios necesarios para el almacenamiento de resultados.
        Genera las siguientes carpetas dentro del directorio de salida:
        - visualizaciones: Para gráficos y representaciones visuales
        - pruebas_estadisticas: Para resultados de análisis estadísticos
        - datos_exportados: Para datos exportados en diferentes formatos
        Utiliza os.makedirs con exist_ok=True para evitar errores si los
        directorios ya existen.
        """
        
        #subdirs = ['resumenes', 'visualizaciones', 'pruebas_estadisticas', 'datos_exportados']
        subdirs = ['visualizaciones', 'pruebas_estadisticas', 'datos_exportados']
        for subdir in subdirs:
            path = os.path.join(self.directorio_salida, subdir)
            os.makedirs(path, exist_ok=True)
    
    def cargar_resultados(self, nombre_algoritmo, directorio_base, instancias=None, prefijo="", sufijo=""):
        """
        Carga los resultados de un algoritmo desde archivos de texto en un directorio.
        Este método carga datos de resumen, convergencia y tiempo de ejecución para
        múltiples instancias de un algoritmo, calculando estadísticas descriptivas
        de los resultados obtenidos.
        Args:
            nombre_algoritmo (str): Nombre identificador del algoritmo
            directorio_base (str): Ruta del directorio donde se encuentran los archivos
            instancias (list, optional): Lista de nombres de instancias. Si es None,
            se detectan automáticamente de los archivos en el directorio
            prefijo (str, optional): Prefijo común en los nombres de archivo
            sufijo (str, optional): Sufijo común en los nombres de archivo
        Returns:
            None: Los resultados se almacenan en self.datos_algoritmos[nombre_algoritmo]
        El método crea una estructura con:
        - Datos de resumen de cada corrida (makespan mínimo global)
        - Datos de convergencia (si están disponibles)
        - Tiempos de ejecución (si están disponibles)
        - Estadísticas descriptivas (mínimo, máximo, media, desviación estándar, mediana)
        Los archivos esperados tienen el formato:
        - resumen_[PREFIJO][INSTANCIA][SUFIJO].txt
        - detalle_[PREFIJO][INSTANCIA][SUFIJO].txt
        - tiempo_ejecucion_[ALGORITMO]_[PREFIJO][INSTANCIA][SUFIJO].txt
        """
        
        print(f"- Cargando resultados de '{nombre_algoritmo}' desde: {directorio_base}")
        
        datos_algoritmo = {'instancias': {}}
        
        # Autodetección de instancias si no se especifican
        if instancias is None:
            archivos = os.listdir(directorio_base)
            resumen_files = [f for f in archivos if f.startswith('resumen_') and f.endswith('.txt')]
            
            instancias = []
            for archivo in resumen_files:
                # Extraer nombre: resumen_PREFIJO_NOMBRE_SUFIJO.txt
                nombre = archivo.replace('resumen_', '').replace('.txt', '')
                if prefijo:
                    nombre = nombre.replace(prefijo, '')
                if sufijo:
                    nombre = nombre.replace(sufijo, '')
                instancias.append(nombre)
        
        # Cargar datos de cada instancia
        for nombre_instancia in instancias:
            print(f"  - Cargando instancia: {nombre_instancia}")
            
            # Construir nombres de archivos
            nombre_completo = f"{prefijo}{nombre_instancia}{sufijo}"
            archivo_resumen = os.path.join(directorio_base, f"resumen_{nombre_completo}.txt")
            archivo_detalle = os.path.join(directorio_base, f"detalle_{nombre_completo}.txt")
            archivo_tiempo = os.path.join(directorio_base, f"tiempo_ejecucion_{nombre_algoritmo}_{nombre_completo}.txt")
            
            datos_instancia = {
                'resumen': [],
                'convergencia': [],
                'tiempo_ejecucion': None,
                'estadisticas': {}
            }
            
            # Cargar resumen
            if os.path.exists(archivo_resumen):
                datos_instancia['resumen'] = read_resumen(archivo_resumen)
                print(f"    + {len(datos_instancia['resumen'])} corridas cargadas")
            else:
                print(f"    X No encontrado: {archivo_resumen}")
                continue
            
            # Cargar convergencia
            if os.path.exists(archivo_detalle):
                datos_instancia['convergencia'] = read_detalle(archivo_detalle)
                print(f"    + {len(datos_instancia['convergencia'])} puntos de convergencia")
            else:
                print(f"    !  Detalle no encontrado: {archivo_detalle}")
            
            # Cargar tiempo de ejecución
            if os.path.exists(archivo_tiempo):
                datos_instancia['tiempo_ejecucion'] = read_tiempo_ejecucion(archivo_tiempo)
                tiempo = datos_instancia['tiempo_ejecucion']['tiempo_segundos']
                print(f"    + Tiempo de ejecución: {tiempo:.2f} segundos ({tiempo/60:.2f} minutos)")
            else:
                print(f"    !  Tiempo no encontrado: {archivo_tiempo}")
            
            # Calcular estadísticas
            if datos_instancia['resumen']:
                mingls = [r['mingl'] for r in datos_instancia['resumen']]
                genmaxs = [r['genmax'] for r in datos_instancia['resumen']]
                ebests = [r['ebest'] for r in datos_instancia['resumen']]
                
                datos_instancia['estadisticas'] = {
                    'mingl_mejor': min(mingls),
                    'mingl_peor': max(mingls),
                    'mingl_media': np.mean(mingls),
                    'mingl_std': np.std(mingls),
                    'mingl_mediana': np.median(mingls),
                    'genmax_media': np.mean(genmaxs),
                    'genmax_std': np.std(genmaxs),
                    'ebest_media': np.mean(ebests),
                    'total_corridas': len(mingls)
                }
            
            datos_algoritmo['instancias'][nombre_instancia] = datos_instancia
        
        self.datos_algoritmos[nombre_algoritmo] = datos_algoritmo
        print(f"+ Carga completada: {len(datos_algoritmo['instancias'])} instancias\n")
    
    def comparar_algoritmos(self, algoritmo1, algoritmo2, instancias=None):
        """
        Compara dos algoritmos incluyendo tiempos de ejecución y análisis estadístico.
        Este método realiza una comparación exhaustiva entre dos algoritmos a través de
        múltiples instancias de problemas, calculando métricas estadísticas, tiempos de
        ejecución y realizando pruebas de hipótesis para determinar diferencias significativas.
        
        Args:
            algoritmo1 (str): Nombre del primer algoritmo a comparar
            algoritmo2 (str): Nombre del segundo algoritmo a comparar
            instancias (list, opcional): Lista de nombres de instancias a comparar.
            Si es None, utiliza la intersección de instancias disponibles para ambos algoritmos.
        
        Returns:
            dict: Diccionario que contiene resultados de comparación para cada instancia, con claves:
            - algoritmo1: Nombre del primer algoritmo
            - algoritmo2: Nombre del segundo algoritmo
            - stats1: Métricas estadísticas para algoritmo1 (media, std, mediana, mejor, peor, genmax_media, tiempo_segundos)
            - stats2: Métricas estadísticas para algoritmo2
            - mejora_media: Mejora porcentual en makespan medio
            - mejora_mejor: Mejora porcentual en mejor makespan
            - mejora_genmax: Mejora porcentual en conteo medio de generaciones
            - mejora_tiempo: Mejora porcentual en tiempo de ejecución (si está disponible)
            - p_wilcoxon: Valor p de prueba de Wilcoxon signed-rank
            - p_mannwhitney: Valor p de prueba de Mann-Whitney U
            - significativo: Booleano que indica si los resultados son estadísticamente significativos
            - mejor_algoritmo: Nombre del algoritmo con mejor rendimiento basado en makespan medio
            - mingls1: Valores brutos de makespan para algoritmo1
            - mingls2: Valores brutos de makespan para algoritmo2
            - genmaxs1: Valores brutos de conteo de generaciones para algoritmo1
            - genmaxs2: Valores brutos de conteo de generaciones para algoritmo2
        
        El método también almacena resultados en self.resultados_comparacion y llama
        a _guardar_resumen_estadistico para almacenamiento persistente.
        
        Raises:
            Imprime mensaje de error si los algoritmos no están cargados en self.datos_algoritmos
        """
        
        print(f"- Comparación Estadística: {algoritmo1} vs {algoritmo2}")
        print("=" * 70)
        
        if algoritmo1 not in self.datos_algoritmos or algoritmo2 not in self.datos_algoritmos:
            print(f"X Error: Algoritmos no cargados")
            return
        
        if instancias is None:
            instancias = list(
                set(self.datos_algoritmos[algoritmo1]['instancias'].keys()) & 
                set(self.datos_algoritmos[algoritmo2]['instancias'].keys())
            )
        
        resultados_comparacion = {}
        
        for nombre_instancia in instancias:
            print(f"\n- Instancia: {nombre_instancia}")
            print("-" * 50)
            
            # Obtener datos
            datos1 = self.datos_algoritmos[algoritmo1]['instancias'][nombre_instancia]['resumen']
            datos2 = self.datos_algoritmos[algoritmo2]['instancias'][nombre_instancia]['resumen']
            
            tiempo1 = self.datos_algoritmos[algoritmo1]['instancias'][nombre_instancia]['tiempo_ejecucion']
            tiempo2 = self.datos_algoritmos[algoritmo2]['instancias'][nombre_instancia]['tiempo_ejecucion']
            
            mingls1 = [r['mingl'] for r in datos1]
            mingls2 = [r['mingl'] for r in datos2]
            genmaxs1 = [r['genmax'] for r in datos1]
            genmaxs2 = [r['genmax'] for r in datos2]
            
            # Estadísticas
            stats1 = {
                'media': np.mean(mingls1),
                'std': np.std(mingls1),
                'mediana': np.median(mingls1),
                'mejor': np.min(mingls1),
                'peor': np.max(mingls1),
                'genmax_media': np.mean(genmaxs1),
                'tiempo_segundos': tiempo1['tiempo_segundos'] if tiempo1 else None
            }
            
            stats2 = {
                'media': np.mean(mingls2),
                'std': np.std(mingls2),
                'mediana': np.median(mingls2),
                'mejor': np.min(mingls2),
                'peor': np.max(mingls2),
                'genmax_media': np.mean(genmaxs2),
                'tiempo_segundos': tiempo2['tiempo_segundos'] if tiempo2 else None
            }
            
            # Tests estadísticos
            try:
                if len(mingls1) == len(mingls2):
                    stat_wilcoxon, p_wilcoxon = stats.wilcoxon(mingls1, mingls2, alternative='two-sided')
                else:
                    stat_wilcoxon, p_wilcoxon = 0, 1.0
            except:
                stat_wilcoxon, p_wilcoxon = 0, 1.0
            
            try:
                stat_mannwhitney, p_mannwhitney = stats.mannwhitneyu(mingls1, mingls2, alternative='two-sided')
            except:
                stat_mannwhitney, p_mannwhitney = 0, 1.0
            
            # Calcular mejoras
            mejora_media = ((stats1['media'] - stats2['media']) / stats1['media']) * 100
            mejora_mejor = ((stats1['mejor'] - stats2['mejor']) / stats1['mejor']) * 100
            mejora_genmax = ((stats1['genmax_media'] - stats2['genmax_media']) / stats1['genmax_media']) * 100
            
            # Mejora en tiempo
            mejora_tiempo = None
            if stats1['tiempo_segundos'] and stats2['tiempo_segundos']:
                mejora_tiempo = ((stats1['tiempo_segundos'] - stats2['tiempo_segundos']) / stats1['tiempo_segundos']) * 100
            
            # Mostrar resultados
            print(f"{algoritmo1:15} → Mejor: {stats1['mejor']:7.2f}  Media: {stats1['media']:7.2f} ± {stats1['std']:5.2f}")
            if stats1['tiempo_segundos']:
                print(f"{'':15}   Tiempo: {stats1['tiempo_segundos']:.2f}s ({stats1['tiempo_segundos']/60:.2f} min)")
            
            print(f"{algoritmo2:15} → Mejor: {stats2['mejor']:7.2f}  Media: {stats2['media']:7.2f} ± {stats2['std']:5.2f}")
            if stats2['tiempo_segundos']:
                print(f"{'':15}   Tiempo: {stats2['tiempo_segundos']:.2f}s ({stats2['tiempo_segundos']/60:.2f} min)")
            
            print(f"\nMejoras de {algoritmo2}:")
            print(f"  Makespan Media:  {mejora_media:+6.2f}%")
            print(f"  Makespan Mejor:  {mejora_mejor:+6.2f}%")
            print(f"  GenMax:          {mejora_genmax:+6.2f}% (menos es mejor)")
            if mejora_tiempo is not None:
                print(f"  Tiempo:          {mejora_tiempo:+6.2f}% (menos es mejor)")
            
            print(f"\nTests estadísticos:")
            print(f"  Wilcoxon p-value:     {p_wilcoxon:.4f}")
            print(f"  Mann-Whitney p-value: {p_mannwhitney:.4f}")
            
            significativo = min(p_wilcoxon, p_mannwhitney) < 0.05
            mejor_algoritmo = algoritmo2 if mejora_media > 0 else algoritmo1
            
            print(f"\n{'+' if significativo else 'x'} Resultado: {'Significativo' if significativo else 'No significativo'}")
            print(f"  Mejor algoritmo (calidad): {mejor_algoritmo}")
            
            if mejora_tiempo is not None:
                mejor_tiempo = algoritmo2 if mejora_tiempo > 0 else algoritmo1
                print(f"  Mejor algoritmo (tiempo):  {mejor_tiempo}")
            
            # Guardar resultados
            resultados_comparacion[nombre_instancia] = {
                'algoritmo1': algoritmo1,
                'algoritmo2': algoritmo2,
                'stats1': stats1,
                'stats2': stats2,
                'mejora_media': mejora_media,
                'mejora_mejor': mejora_mejor,
                'mejora_genmax': mejora_genmax,
                'mejora_tiempo': mejora_tiempo,
                'p_wilcoxon': p_wilcoxon,
                'p_mannwhitney': p_mannwhitney,
                'significativo': significativo,
                'mejor_algoritmo': mejor_algoritmo,
                'mingls1': mingls1,
                'mingls2': mingls2,
                'genmaxs1': genmaxs1,
                'genmaxs2': genmaxs2
            }
        
        self.resultados_comparacion[f"{algoritmo1}_vs_{algoritmo2}"] = resultados_comparacion
        self._guardar_resumen_estadistico(algoritmo1, algoritmo2, resultados_comparacion)
        
        return resultados_comparacion
    
    def _guardar_resumen_estadistico(self, algoritmo1, algoritmo2, resultados):
        """
        Guarda un resumen estadístico comparativo entre dos algoritmos en un archivo de texto.
        Args:
            algoritmo1 (str): Nombre del primer algoritmo a comparar
            algoritmo2 (str): Nombre del segundo algoritmo a comparar
            resultados (dict): Diccionario con los resultados estadísticos de la comparación.
                               Debe contener para cada instancia:
                               - stats1: estadísticas del algoritmo1 (mejor, media, std, mediana, genmax_media, tiempo_segundos)
                               - stats2: estadísticas del algoritmo2
                               - mejor_algoritmo: cuál algoritmo tuvo mejor rendimiento
                               - significativo: si la diferencia fue estadísticamente significativa
                               - p_wilcoxon: valor p de prueba de Wilcoxon
                               - p_mannwhitney: valor p de prueba de Mann-Whitney
                               - mejora_media: porcentaje de mejora en media
                               - mejora_mejor: porcentaje de mejora en mejor resultado
                               - mejora_genmax: porcentaje de mejora en generación máxima
                               - mejora_tiempo: porcentaje de mejora en tiempo (opcional)
        El archivo generado incluye:
        - Resumen global con estadísticas agregadas
        - Tiempos promedio de ejecución y mejora porcentual
        - Detalle completo por cada instancia con todas las métricas comparativas
        El archivo se guarda en el directorio de salida con timestamp en el nombre.
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(self.directorio_salida, 'pruebas_estadisticas',
                           f'comparacion_{algoritmo1}_vs_{algoritmo2}_{timestamp}.txt')
        
        with open(ruta, 'w') as f:
            f.write(f"Comparación Estadística: {algoritmo1} vs {algoritmo2}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Resumen global
            instancias_sig = sum(1 for r in resultados.values() if r['significativo'])
            total = len(resultados)
            victorias_alg2 = sum(1 for r in resultados.values() if r['mejor_algoritmo'] == algoritmo2)
            
            f.write(f"Resumen Global:\n")
            f.write(f"  Instancias analizadas: {total}\n")
            f.write(f"  Diferencias significativas: {instancias_sig}/{total}\n")
            f.write(f"  Victorias {algoritmo2} (calidad): {victorias_alg2}/{total}\n")
            
            # Tiempos promedio
            tiempos1 = [r['stats1']['tiempo_segundos'] for r in resultados.values() if r['stats1']['tiempo_segundos']]
            tiempos2 = [r['stats2']['tiempo_segundos'] for r in resultados.values() if r['stats2']['tiempo_segundos']]
            
            if tiempos1 and tiempos2:
                f.write(f"\nTiempos Promedio:\n")
                f.write(f"  {algoritmo1}: {np.mean(tiempos1):.2f}s ({np.mean(tiempos1)/60:.2f} min)\n")
                f.write(f"  {algoritmo2}: {np.mean(tiempos2):.2f}s ({np.mean(tiempos2)/60:.2f} min)\n")
                mejora_tiempo_prom = ((np.mean(tiempos1) - np.mean(tiempos2)) / np.mean(tiempos1)) * 100
                f.write(f"  Mejora promedio: {mejora_tiempo_prom:+.2f}%\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            # Detalle por instancia
            for nombre, resultado in resultados.items():
                f.write(f"Instancia: {nombre}\n")
                f.write("-" * 50 + "\n")
                f.write(f"{algoritmo1}:\n")
                f.write(f"  Mejor:    {resultado['stats1']['mejor']:.2f}\n")
                f.write(f"  Media:    {resultado['stats1']['media']:.2f} ± {resultado['stats1']['std']:.2f}\n")
                f.write(f"  Mediana:  {resultado['stats1']['mediana']:.2f}\n")
                f.write(f"  GenMax:   {resultado['stats1']['genmax_media']:.1f}\n")
                if resultado['stats1']['tiempo_segundos']:
                    f.write(f"  Tiempo:   {resultado['stats1']['tiempo_segundos']:.2f}s\n")
                f.write(f"\n{algoritmo2}:\n")
                f.write(f"  Mejor:    {resultado['stats2']['mejor']:.2f}\n")
                f.write(f"  Media:    {resultado['stats2']['media']:.2f} ± {resultado['stats2']['std']:.2f}\n")
                f.write(f"  Mediana:  {resultado['stats2']['mediana']:.2f}\n")
                f.write(f"  GenMax:   {resultado['stats2']['genmax_media']:.1f}\n")
                if resultado['stats2']['tiempo_segundos']:
                    f.write(f"  Tiempo:   {resultado['stats2']['tiempo_segundos']:.2f}s\n")
                
                f.write(f"\Comparación:\n")
                f.write(f"  Mejora Media:   {resultado['mejora_media']:+.2f}%\n")
                f.write(f"  Mejora Mejor:   {resultado['mejora_mejor']:+.2f}%\n")
                f.write(f"  Mejora GenMax:  {resultado['mejora_genmax']:+.2f}%\n")
                if resultado['mejora_tiempo']:
                    f.write(f"  Mejora Tiempo:  {resultado['mejora_tiempo']:+.2f}%\n")
                f.write(f"  P-value (Wilcoxon):     {resultado['p_wilcoxon']:.4f}\n")
                f.write(f"  P-value (Mann-Whitney): {resultado['p_mannwhitney']:.4f}\n")
                f.write(f"  Significativo: {'SÍ' if resultado['significativo'] else 'NO'}\n")
                f.write(f"  Mejor: {resultado['mejor_algoritmo']}\n")
                f.write("=" * 50 + "\n\n")
        
        print(f"\n- Resumen guardado: {ruta}")
    
    def crear_visualizaciones(self, algoritmo1, algoritmo2):
        """
        Genera visualizaciones comparativas entre dos algoritmos de optimización.
        Crea un dashboard con múltiples gráficos que comparan el rendimiento de dos
        algoritmos en términos de makespan y tiempo de ejecución. Incluye boxplots,
        violin plots, gráficos de barras comparativas y análisis de trade-off entre
        tiempo y calidad.
        Args:
            algoritmo1 (str): Nombre del primer algoritmo a comparar
            algoritmo2 (str): Nombre del segundo algoritmo a comparar
        Returns:
            None: La función guarda las visualizaciones en archivo PNG y las muestra
        Raises:
            Implicitamente muestra advertencias si no hay datos de comparación o
            si faltan datos de tiempo de ejecución
        Notes:
            - Requiere que los resultados de comparación estén previamente cargados
            - Genera archivos en el directorio de salida con timestamp
            - Incluye 6 subplots cuando hay datos de tiempo, 3 cuando no
        """
        
        clave = f"{algoritmo1}_vs_{algoritmo2}"
        
        if clave not in self.resultados_comparacion:
            print(f"X No hay resultados de comparación")
            return
        
        datos_comparacion = self.resultados_comparacion[clave]
        
        # Preparar datos
        datos_plot = []
        datos_tiempo = []
        
        for nombre_instancia, resultado in datos_comparacion.items():
            # Makespan
            for valor in resultado['mingls1']:
                datos_plot.append({
                    'instancia': nombre_instancia,
                    'algoritmo': algoritmo1,
                    'makespan': valor,
                })
            
            for valor in resultado['mingls2']:
                datos_plot.append({
                    'instancia': nombre_instancia,
                    'algoritmo': algoritmo2,
                    'makespan': valor,
                })
            
            # Tiempos
            if resultado['stats1']['tiempo_segundos']:
                datos_tiempo.append({
                    'instancia': nombre_instancia,
                    'algoritmo': algoritmo1,
                    'tiempo_segundos': resultado['stats1']['tiempo_segundos'],
                    'tiempo_minutos': resultado['stats1']['tiempo_segundos'] / 60
                })
            
            if resultado['stats2']['tiempo_segundos']:
                datos_tiempo.append({
                    'instancia': nombre_instancia,
                    'algoritmo': algoritmo2,
                    'tiempo_segundos': resultado['stats2']['tiempo_segundos'],
                    'tiempo_minutos': resultado['stats2']['tiempo_segundos'] / 60
                })
        
        df_makespan = pd.DataFrame(datos_plot)
        df_tiempo = pd.DataFrame(datos_tiempo) if datos_tiempo else None
        
        # Verificar si hay datos de tiempo
        if df_tiempo is None or len(df_tiempo) == 0:
            print("!  ADVERTENCIA: No se encontraron datos de tiempo de ejecución.")
            print("    Verifica que los archivos tiempo_ejecucion_XXX.txt existan y tengan el formato correcto.")
            print("    Solo se generarán gráficos de makespan.\n")
        else:
            print(f"+ Datos de tiempo cargados: {len(df_tiempo)} registros")
            print(f"   Algoritmos con tiempo: {df_tiempo['algoritmo'].unique().tolist()}\n")
        
        # Crear figura con subplots
        if df_tiempo is not None and len(df_tiempo) > 0:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        else:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        axes = axes.flatten()
        
        # 1. Boxplot de Makespan
        sns.boxplot(data=df_makespan, x='instancia', y='makespan', hue='algoritmo', ax=axes[0])
        axes[0].set_title(f'Distribución de Makespan', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Instancia')
        axes[0].set_ylabel('Makespan')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].legend(title='Algoritmo')
        
        # 2. Violin plot
        sns.violinplot(data=df_makespan, x='instancia', y='makespan', hue='algoritmo', ax=axes[1])
        axes[1].set_title('Distribución Detallada', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Instancia')
        axes[1].set_ylabel('Makespan')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].legend(title='Algoritmo')
        
        # 3. Barplot de mejoras en makespan (valores negativos = puro es mejor)
        instancias = []
        mejoras_makespan = []
        for nombre, resultado in datos_comparacion.items():
            instancias.append(nombre)
            # Invertir el signo para que sea más intuitivo
            # Positivo = algoritmo1 (puro) es mejor
            mejora_invertida = -resultado['mejora_media']
            mejoras_makespan.append(mejora_invertida)
        
        # Verde si puro (algoritmo1) es mejor, rojo si deap (algoritmo2) es mejor
        colores = ['green' if x > 0 else 'red' for x in mejoras_makespan]
        bars = axes[2].bar(instancias, mejoras_makespan, color=colores, alpha=0.7)
        axes[2].set_title(f'Ventaja en Makespan: {algoritmo1} es Mejor', fontsize=14, fontweight='bold')
        axes[2].set_xlabel('Instancia')
        axes[2].set_ylabel(f'Ventaja de {algoritmo1} (%)')
        axes[2].axhline(y=0, color='black', linestyle='-', linewidth=1)
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].grid(True, alpha=0.3, axis='y')
        
        for bar, mejora in zip(bars, mejoras_makespan):
            altura = bar.get_height()
            if mejora > 0:
                texto = f'{algoritmo1}\n+{mejora:.1f}%'
            else:
                texto = f'{algoritmo2}\n+{abs(mejora):.1f}%'
            axes[2].text(bar.get_x() + bar.get_width()/2., altura,
                        texto,
                        ha='center', va='bottom' if altura > 0 else 'top', fontsize=8)
        
        # 4. Comparación de tiempos con barras apareadas LADO A LADO
        if df_tiempo is not None and len(df_tiempo) > 0:
            # Crear posiciones para barras grupadas
            x = np.arange(len(instancias))
            width = 0.35  # Ancho de cada barra
            
            # Extraer tiempos para cada algoritmo
            tiempos_alg1 = []
            tiempos_alg2 = []
            
            for nombre in instancias:
                resultado = datos_comparacion[nombre]
                
                t1 = resultado['stats1']['tiempo_segundos']
                t2 = resultado['stats2']['tiempo_segundos']
                
                # Convertir a minutos, manejar None
                tiempo1_min = (t1 / 60) if t1 is not None else 0
                tiempo2_min = (t2 / 60) if t2 is not None else 0
                
                tiempos_alg1.append(tiempo1_min)
                tiempos_alg2.append(tiempo2_min)
            
            # Crear barras lado a lado
            bars1 = axes[3].bar(x - width/2, tiempos_alg1, width, 
                              label=algoritmo1, color='steelblue', alpha=0.8, edgecolor='black', linewidth=1)
            bars2 = axes[3].bar(x + width/2, tiempos_alg2, width, 
                              label=algoritmo2, color='coral', alpha=0.8, edgecolor='black', linewidth=1)
            
            # Añadir etiquetas de valor arriba de cada barra
            for bar in bars1:
                height = bar.get_height()
                if height > 0:  # Solo mostrar si hay valor
                    axes[3].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                               f'{height:.1f}m',
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            for bar in bars2:
                height = bar.get_height()
                if height > 0:  # Solo mostrar si hay valor
                    axes[3].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                               f'{height:.1f}m',
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # Configurar ejes
            axes[3].set_title('Tiempo de Ejecución por Instancia', fontsize=14, fontweight='bold')
            axes[3].set_xlabel('Instancia', fontsize=11)
            axes[3].set_ylabel('Tiempo (minutos)', fontsize=11)
            axes[3].set_xticks(x)
            axes[3].set_xticklabels(instancias, rotation=45, ha='right')
            #axes[3].legend(loc='upper right', framealpha=0.9)
            axes[3].legend(loc='lower right', framealpha=0.9)
            axes[3].grid(True, alpha=0.3, axis='y', linestyle='--')
            axes[3].set_ylim(bottom=0)  # Empezar desde 0
            
            # Advertencia si hay valores en 0
            if sum(tiempos_alg1) == 0 or sum(tiempos_alg2) == 0:
                axes[3].text(0.5, 0.95, '! Algunos tiempos no se cargaron correctamente', 
                           transform=axes[3].transAxes, ha='center', va='top',
                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                           fontsize=9)
            
            # 5. Diferencia de tiempo absoluta (más intuitivo)
            diferencias_tiempo = []
            algoritmo_mas_rapido = []
            
            for nombre in instancias:
                resultado = datos_comparacion[nombre]
                t1 = resultado['stats1']['tiempo_segundos']  # puro
                t2 = resultado['stats2']['tiempo_segundos']  # deap
                
                if t1 and t2:
                    # Calcular diferencia absoluta
                    diferencia_segundos = abs(t1 - t2)
                    diferencias_tiempo.append(diferencia_segundos)
                    
                    # Determinar quién es más rápido
                    if t1 < t2:
                        algoritmo_mas_rapido.append(algoritmo1)  # puro más rápido
                    else:
                        algoritmo_mas_rapido.append(algoritmo2)  # deap más rápido
                else:
                    diferencias_tiempo.append(0)
                    algoritmo_mas_rapido.append("N/A")
            
            # Colores: verde si puro es más rápido, rojo si deap es más rápido
            colores_tiempo = ['green' if alg == algoritmo1 else 'red' for alg in algoritmo_mas_rapido]
            
            bars_tiempo = axes[4].bar(instancias, diferencias_tiempo, color=colores_tiempo, 
                                     alpha=0.7, edgecolor='black', linewidth=1)
            
            axes[4].set_title('Diferencia de Tiempo entre Algoritmos', fontsize=14, fontweight='bold')
            axes[4].set_xlabel('Instancia', fontsize=11)
            axes[4].set_ylabel('Diferencia de Tiempo (segundos)', fontsize=11)
            axes[4].set_xticks(range(len(instancias)))
            axes[4].set_xticklabels(instancias, rotation=45, ha='right')
            axes[4].grid(True, alpha=0.3, axis='y', linestyle='--')
            axes[4].set_ylim(bottom=0)
            
            # Añadir etiquetas informativas arriba de cada barra
            for i, (bar, diferencia, alg_rapido) in enumerate(zip(bars_tiempo, diferencias_tiempo, algoritmo_mas_rapido)):
                if diferencia > 0 and alg_rapido != "N/A":
                    altura = bar.get_height()
                    
                    # Calcular porcentaje de ventaja
                    resultado = datos_comparacion[instancias[i]]
                    t1 = resultado['stats1']['tiempo_segundos']
                    t2 = resultado['stats2']['tiempo_segundos']
                    
                    if alg_rapido == algoritmo1:
                        porcentaje = ((t2 - t1) / t2) * 100
                    else:
                        porcentaje = ((t1 - t2) / t1) * 100
                    
                    # Etiqueta más informativa
                    etiqueta = f'{alg_rapido} más rápido\n+{diferencia:.0f}s ({porcentaje:.1f}%)'
                    
                    axes[4].text(bar.get_x() + bar.get_width()/2., altura + max(diferencias_tiempo)*0.001,
                               etiqueta,
                               ha='center', va='bottom', fontsize=8, fontweight='bold')
            
            # Leyenda personalizada
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='green', edgecolor='black', label=f'{algoritmo1}'),
                Patch(facecolor='red', edgecolor='black', label=f'{algoritmo2}')
            ]
            #axes[4].legend(handles=legend_elements, loc='upper right', framealpha=0.9)
            axes[4].legend(handles=legend_elements, loc='lower right', framealpha=0.9)
            
            # 6. Scatter mejorado: Tiempo vs Calidad
            colores_algoritmos = {'puro': 'blue', 'deap': 'orange'}
            markers_algoritmos = {'puro': 'o', 'deap': 's'}
            
            for alg in [algoritmo1, algoritmo2]:
                tiempos = []
                medias = []
                nombres_puntos = []
                
                for nombre in instancias:
                    resultado = datos_comparacion[nombre]
                    if alg == algoritmo1:
                        if resultado['stats1']['tiempo_segundos']:
                            tiempos.append(resultado['stats1']['tiempo_segundos'])
                            medias.append(resultado['stats1']['media'])
                            nombres_puntos.append(nombre)
                    else:
                        if resultado['stats2']['tiempo_segundos']:
                            tiempos.append(resultado['stats2']['tiempo_segundos'])
                            medias.append(resultado['stats2']['media'])
                            nombres_puntos.append(nombre)
                
                if tiempos and medias:
                    color = colores_algoritmos.get(alg, 'gray')
                    marker = markers_algoritmos.get(alg, 'o')
                    axes[5].scatter(tiempos, medias, label=alg, s=150, alpha=0.7, 
                                  color=color, marker=marker, edgecolors='black', linewidth=1)
                    
                    # Añadir etiquetas de instancia
                    for t, m, n in zip(tiempos, medias, nombres_puntos):
                        axes[5].annotate(n, (t, m), textcoords="offset points", 
                                       xytext=(0,5), ha='center', fontsize=8)
            
            axes[5].set_title('Trade-off: Tiempo vs Calidad (Menor es Mejor)', fontsize=14, fontweight='bold')
            axes[5].set_xlabel('Tiempo de Ejecución (segundos)')
            axes[5].set_ylabel('Makespan Promedio')
            axes[5].legend(loc='best')
            axes[5].grid(True, alpha=0.3)
            
            # Añadir región ideal (esquina inferior izquierda)
            axes[5].annotate('Ideal\n(rápido y bueno)', 
                           xy=(0.05, 0.05), xycoords='axes fraction',
                           fontsize=10, color='green', alpha=0.5,
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        else:
            # Si no hay datos de tiempo, ocultar ejes extra
            for i in range(3, 6):
                axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(self.directorio_salida, 'visualizaciones',
                           f'{algoritmo1}_vs_{algoritmo2}_{timestamp}.png')
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"- Visualizaciones guardadas: {ruta}")
    
    def crear_graficos_convergencia(self, algoritmo1, algoritmo2, instancias=None):
        """
        Genera y guarda gráficos comparativos de convergencia entre dos algoritmos.
        Crea una visualización comparativa de las curvas de convergencia de dos algoritmos
        evolutivos para las instancias especificadas, mostrando la evolución del mejor
        makespan global a lo largo de las generaciones.
        Parameters:
        -----------
        algoritmo1 : str
            Nombre del primer algoritmo a comparar (debe existir en datos_algoritmos)
        algoritmo2 : str
            Nombre del segundo algoritmo a comparar (debe existir en datos_algoritmos)
        instancias : list, optional
            Lista de nombres de instancias a visualizar. Si es None, usa todas las
            instancias disponibles del primer algoritmo.
        Returns:
        --------
        None
        Outputs:
        --------
        - Genera una figura con subplots para cada instancia
        - Guarda la figura como archivo PNG en el directorio de visualizaciones
        - Muestra la figura en pantalla
        - Imprime la ruta del archivo guardado
        Notes:
        ------
        - La figura se organiza en una grilla de hasta 3 columnas
        - Los subplots vacíos se ocultan automáticamente
        - El nombre del archivo incluye timestamp para evitar sobrescritura
        - Usa datos de convergencia almacenados en self.datos_algoritmos
        """
        
        if instancias is None:
            instancias = list(self.datos_algoritmos[algoritmo1]['instancias'].keys())
        
        n_instancias = len(instancias)
        cols = min(3, n_instancias)
        rows = (n_instancias + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
        
        if n_instancias == 1:
            axes = np.array([axes])
        axes = axes.flatten() if n_instancias > 1 else axes
        
        for i, nombre_instancia in enumerate(instancias):
            if i >= len(axes):
                break
            
            ax = axes[i] if n_instancias > 1 else axes[0]
            
            # Algoritmo 1
            if nombre_instancia in self.datos_algoritmos[algoritmo1]['instancias']:
                conv1 = self.datos_algoritmos[algoritmo1]['instancias'][nombre_instancia]['convergencia']
                if conv1:
                    gens1 = [c['gen'] for c in conv1]
                    mingls1 = [c['mingl'] for c in conv1]
                    ax.plot(gens1, mingls1, label=algoritmo1, linewidth=2, alpha=0.8)
            
            # Algoritmo 2
            if nombre_instancia in self.datos_algoritmos[algoritmo2]['instancias']:
                conv2 = self.datos_algoritmos[algoritmo2]['instancias'][nombre_instancia]['convergencia']
                if conv2:
                    gens2 = [c['gen'] for c in conv2]
                    mingls2 = [c['mingl'] for c in conv2]
                    ax.plot(gens2, mingls2, label=algoritmo2, linewidth=2, alpha=0.8)
            
            ax.set_title(f'Convergencia - {nombre_instancia}', fontweight='bold')
            ax.set_xlabel('Generación')
            ax.set_ylabel('Mejor Makespan Global')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Ocultar subplots vacíos
        for i in range(n_instancias, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(self.directorio_salida, 'visualizaciones',
                           f'convergencia_{algoritmo1}_vs_{algoritmo2}_{timestamp}.png')
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"- Convergencia guardada: {ruta}")
    
    def exportar_csv(self, algoritmo1, algoritmo2):
        """
        Exporta los resultados de comparación entre dos algoritmos a un archivo CSV.
        Genera un archivo CSV con estadísticas comparativas detalladas entre dos algoritmos,
        incluyendo métricas de rendimiento, pruebas estadísticas y mejoras porcentuales.
        Args:
            algoritmo1 (str): Nombre del primer algoritmo a comparar
            algoritmo2 (str): Nombre del segundo algoritmo a comparar
        Returns:
            str or None: Ruta del archivo CSV generado, o None si no hay datos para comparar
        El archivo CSV incluye las siguientes columnas:
            - instancia: Nombre de la instancia del problema
            - algoritmo1/algoritmo2: Nombres de los algoritmos comparados
            - Métricas por algoritmo (mejor, media, std, mediana, genmax, tiempo_s)
            - Mejoras porcentuales (makespan, mejor, genmax, tiempo)
            - Valores p de pruebas estadísticas (Wilcoxon, Mann-Whitney)
            - Indicadores de significancia y mejor algoritmo
        El archivo se guarda en el directorio de salida con timestamp para evitar sobreescrituras.
        """
        
        clave = f"{algoritmo1}_vs_{algoritmo2}"
        
        if clave not in self.resultados_comparacion:
            print(f"X No hay resultados")
            return
        
        datos_comparacion = self.resultados_comparacion[clave]
        
        datos_csv = []
        for nombre, resultado in datos_comparacion.items():
            datos_csv.append({
                'instancia': nombre,
                'algoritmo1': algoritmo1,
                'algoritmo2': algoritmo2,
                f'{algoritmo1}_mejor': resultado['stats1']['mejor'],
                f'{algoritmo1}_media': resultado['stats1']['media'],
                f'{algoritmo1}_std': resultado['stats1']['std'],
                f'{algoritmo1}_mediana': resultado['stats1']['mediana'],
                f'{algoritmo1}_genmax': resultado['stats1']['genmax_media'],
                f'{algoritmo1}_tiempo_s': resultado['stats1']['tiempo_segundos'],
                f'{algoritmo2}_mejor': resultado['stats2']['mejor'],
                f'{algoritmo2}_media': resultado['stats2']['media'],
                f'{algoritmo2}_std': resultado['stats2']['std'],
                f'{algoritmo2}_mediana': resultado['stats2']['mediana'],
                f'{algoritmo2}_genmax': resultado['stats2']['genmax_media'],
                f'{algoritmo2}_tiempo_s': resultado['stats2']['tiempo_segundos'],
                'mejora_makespan_pct': resultado['mejora_media'],
                'mejora_mejor_pct': resultado['mejora_mejor'],
                'mejora_genmax_pct': resultado['mejora_genmax'],
                'mejora_tiempo_pct': resultado['mejora_tiempo'],
                'p_wilcoxon': resultado['p_wilcoxon'],
                'p_mannwhitney': resultado['p_mannwhitney'],
                'significativo': resultado['significativo'],
                'mejor_algoritmo': resultado['mejor_algoritmo']
            })
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(self.directorio_salida, 'datos_exportados',
                           f'comparacion_{algoritmo1}_vs_{algoritmo2}_{timestamp}.csv')
        
        df = pd.DataFrame(datos_csv)
        df.to_csv(ruta, index=False)
        
        print(f"- CSV exportado: {ruta}")
        return ruta


# Funcion para ejecutar el análisis 
def analizar_corridas():
    """
    Analiza y compara los resultados de ejecuciones de algoritmos evolutivos.
    Esta función realiza un análisis comparativo entre los resultados obtenidos
    por implementaciones Python puro y DEAP de algoritmos evolutivos para
    problemas de scheduling (instancias swv06, swv07, swv08).
    Realiza las siguientes operaciones:
    1. Carga los resultados de ambas implementaciones
    2. Compara el rendimiento de los algoritmos
    3. Genera visualizaciones comparativas
    4. Crea gráficos de convergencia
    5. Exporta los datos a formato CSV
    Los resultados se guardan en el directorio 'analisis_comparativo'
    """
    
    print("- Análisis de resultados con tiempos")
    print("=" * 60 + "\n")
    
    # Crear analizador
    analizador = AnalizadorEvosocial(directorio_salida="analisis_comparativo")
    
    # Cargar resultados Python puro
    print("- Cargando Python Puro...")
    analizador.cargar_resultados(
        nombre_algoritmo="puro",
        directorio_base="puro",
        instancias=["swv06", "swv07", "swv08"],
        prefijo="converted_"
    )
    
    # Cargar resultados DEAP
    print("- Cargando DEAP...")
    analizador.cargar_resultados(
        nombre_algoritmo="deap",
        directorio_base="deap",
        instancias=["swv06", "swv07", "swv08"],
        prefijo="converted_"
    )
    
    # Comparar
    print("- Comparando algoritmos...")
    analizador.comparar_algoritmos("puro", "deap")
    
    # Visualizar
    print("\n- Generando visualizaciones...")
    analizador.crear_visualizaciones("puro", "deap")
    analizador.crear_graficos_convergencia("puro", "deap")
    
    # Exportar
    print("\n- Exportando datos...")
    analizador.exportar_csv("puro", "deap")
    
    print("\n+ Análisis completado")
    print(f"- Resultados en: {analizador.directorio_salida}/")

if __name__ == "__main__":
    analizar_corridas()
    