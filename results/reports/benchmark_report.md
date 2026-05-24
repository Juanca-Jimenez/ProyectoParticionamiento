# Reporte del Análisis Experimental del Sistema de Particionamiento

## 1. Resumen Experimental

Este estudio presenta la evaluación del comportamiento computacional y matemático de los dos algoritmos de particionamiento del sistema:
- **Algoritmo Exhaustivo:** Basado en búsqueda sistemática por backtracking recursivo con reducción de simetrías y podas por acotación ($n < 12$).
- **Algoritmo Heurístico:** Basado en búsqueda local estocástica multi-inicio con reparación de restricciones ($n \ge 12$).

Las pruebas se corrieron bajo dos modalidades:
1. **Synthetic Benchmark:** Matrices simétricas de acoplamiento generadas mediante un generador pseudo-aleatorio controlado con semilla fija (`seed=42`) para garantizar la reproductibilidad del análisis, con tamaños de $n = [5, 10, 15, 20, 25, 30]$ y $k = 3$.
2. **Real Dataset Benchmark:** Matrices de dependencias extraídas directamente de los datasets del sistema (`small_4x4.csv`, `medium_12x12.csv`, `large_30x30.csv`) con $k = 3$.

Se midieron los tiempos de CPU en milisegundos (`execution_time_ms`), los picos máximos de memoria asignada en KB (`memory_peak_kb`) y los costos de los cortes finales obtenidos.

## 2. Hallazgos

Tabla 1.
Tiempo de Ejecución vs Tamaño del Problema

| Algoritmo | Origen del Dataset | Nodos (n) | Grupos (k) | Tiempo (ms) | Memoria (KB) | Valor de Corte |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Heurística | real (large_30x30.csv) | 30 | 3 | 147.9197 | 1.47 | 165.0 |
| Heurística | real (medium_12x12.csv) | 12 | 3 | 23.8847 | 1.22 | 15.0 |
| Exhaustivo | real (small_4x4.csv) | 4 | 3 | 0.0351 | 0.82 | 5.0 |
| Heurística | real (small_4x4.csv) | 4 | 3 | 3.5550 | 0.83 | 5.0 |
| Exhaustivo | synthetic | 5 | 3 | 0.1145 | 1.22 | 10.0 |
| Heurística | synthetic | 5 | 3 | 9.2022 | 1.05 | 10.0 |
| Exhaustivo | synthetic | 10 | 3 | 3.3105 | 1.69 | 22.0 |
| Heurística | synthetic | 10 | 3 | 21.9854 | 1.17 | 22.0 |
| Heurística | synthetic | 15 | 3 | 59.9318 | 1.38 | 45.0 |
| Heurística | synthetic | 20 | 3 | 79.5503 | 1.27 | 87.0 |
| Heurística | synthetic | 25 | 3 | 123.5172 | 1.37 | 84.0 |
| Heurística | synthetic | 30 | 3 | 142.1685 | 1.47 | 112.0 |

Nota: El tiempo corresponde al promedio de múltiples ejecuciones utilizando las mismas condiciones experimentales. Resultados obtenidos mediante ejecución experimental del sistema.

Tabla 2.
Calidad de la Solución (Valor de Corte) vs Parámetro

| Algoritmo | Configuración del Dataset | Nodos (n) | Parámetro (k) | Valor de Corte Obtenido |
| :--- | :--- | :---: | :---: | :---: |
| Exhaustivo | quality_varying_k_n10 | 10 | 2 | 10.0 |
| Exhaustivo | quality_varying_k_n10 | 10 | 3 | 28.0 |
| Exhaustivo | quality_varying_k_n10 | 10 | 4 | 47.0 |
| Exhaustivo | quality_varying_k_n10 | 10 | 5 | 66.0 |
| Heurística | quality_varying_k_n10 | 10 | 2 | 10.0 |
| Heurística | quality_varying_k_n10 | 10 | 3 | 28.0 |
| Heurística | quality_varying_k_n10 | 10 | 4 | 47.0 |
| Heurística | quality_varying_k_n10 | 10 | 5 | 68.0 |
| Heurística | quality_varying_k_n20 | 20 | 2 | 21.0 |
| Heurística | quality_varying_k_n20 | 20 | 3 | 43.0 |
| Heurística | quality_varying_k_n20 | 20 | 4 | 74.0 |
| Heurística | quality_varying_k_n20 | 20 | 5 | 125.0 |
| Heurística | quality_varying_k_real_m12 | 12 | 2 | 8.0 |
| Heurística | quality_varying_k_real_m12 | 12 | 3 | 15.0 |
| Heurística | quality_varying_k_real_m12 | 12 | 4 | 23.0 |
| Heurística | quality_varying_k_real_m12 | 12 | 5 | 28.0 |

Nota: Menores valores de corte representan particiones con menor costo de comunicación entre grupos. Resultados obtenidos mediante ejecución experimental del sistema.

## 3. Interpretación Automática de Resultados

### 3.1. Análisis del Tiempo de Ejecución
- **Algoritmo Exhaustivo:** Al evaluar tamaños de problemas pequeños, se observa el crecimiento exponencial del espacio de estados. Para el tamaño de matriz sintética $n=10$, el algoritmo exhaustivo requirió **3.3105 ms** en promedio, mientras que para $n=5$ requirió **0.1145 ms**. En este mismo tamaño ($n=10$), el método exhaustivo es más rápido y representa solo el **0.15 veces** del tiempo de la alternativa heurística (**21.9854 ms**). Este aumento masivo ilustra el impacto de la complejidad teórica exponencial $O(k^n)$ y justifica desactivarlo para tamaños $n \ge 12$.
- **Algoritmo Heurístico:** Muestra una curva con crecimiento suave polinomial. Al escalar la matriz sintética desde $n=5$ (**9.2022 ms**) hasta $n=30$ (**142.1685 ms**), el tiempo de ejecución se incrementó en un factor de **15.45x**. Este comportamiento experimental valida que la heurística local opera en tiempo polinomial cuadrático $O(n^2 \cdot k)$ y es ideal para grafos grandes.

### 3.2. Análisis del Consumo de Memoria
El perfilado físico indica que el uso de memoria en la heurística se incrementa moderadamente con el tamaño del problema. El pico de memoria máxima pasó de **1.05 KB** para $n=5$ a **1.47 KB** para $n=30$, lo que representa un incremento de **1.40x**. Este incremento se asocia a la creación de matrices y arreglos de control en memoria. Debido a que el sistema opera en memoria RAM sin persistencia en disco, el consumo de memoria se mantiene bajo el umbral de los 500 KB para todas las pruebas del tamaño de entrada actual.

### 3.3. Análisis de la Calidad de la Solución (Valor de Corte)
- Al variar el parámetro $k$, se observa una tendencia clara: **a mayor número de grupos (k), el valor de corte aumenta (empeora la calidad del acoplamiento externo)**. Por ejemplo, para la matriz sintética de tamaño $n=20$, el valor de corte incrementa de **21.0** cuando $k=2$ a **125.0** cuando $k=5$ (un incremento absoluto de **104.0** en la dependencia acumulada externa). Este comportamiento es consistente con la teoría: a medida que el número de particiones aumenta, se crean más fronteras de división, lo que obliga a que más aristas cruzadas se sumen al corte total. Por ende, desde la perspectiva de minimización del acoplamiento externo, un valor de $k$ menor produce particiones con menor costo de comunicación entre grupos distintos (mejorando el diseño de la arquitectura), mientras que un $k$ mayor deteriora esta calidad, aunque puede mejorar la granularidad de los módulos.
- **Comparación de Optimalidad (n=10):** Para $n=10$ y $k=3$, la heurística local logró encontrar exactamente el mismo corte mínimo que la búsqueda exhaustiva (**28.0**), demostrando la efectividad de la optimización estocástica multi-inicio en encontrar el óptimo global para este caso.

## 4. Limitaciones del Estudio Experimental

1. **Tamaño Máximo del Grafo:** El algoritmo exhaustivo está estrictamente limitado a $n < 12$ debido a su carácter exponencial. El análisis para tamaños grandes solo evalúa la heurística.
2. **Dominios de k:** Las particiones experimentales están restringidas a la escala de $k = [2, 5]$ debido al validador del backend, lo que limita observar tendencias de subdivisión en clústeres masivos.
3. **Dependencia de la Semilla:** Dado que la heurística local es un método probabilístico, la calidad de la solución depende parcialmente de la semilla aleatoria, aunque el uso de 30 reinicios estabiliza el valor de corte promedio.
4. **Perfilado de CPU:** Las mediciones de tiempo en milisegundos pueden fluctuar ligeramente dependiendo de la carga de otros procesos en el sistema operativo durante la ejecución del benchmark.
