# Sistema de Particionamiento de Dependencias

Descripción breve
------------------
Este repositorio implementa un sistema para particionar un conjunto de componentes, minimizando la suma de las dependencias que quedan entre componentes de distintas particiones (valor de corte o "cut"). Está pensado para analizar dependencias entre módulos/componentes y sugerir particiones que reduzcan el acoplamiento cruzado.

Contenido del repositorio
-------------------------
- `backend/`: servidor (Flask), implementación de algoritmos (exhaustivo y heurístico), validadores, utilidades y pruebas automáticas.
- `frontend/`: UI estática para enviar matrices y visualizar particiones.
- `docs/`: documentación técnica y resultados experimentales.
- `results/` y `backend/datasets/`: datos de ejemplo y resultados de las ejecuciones.

Problema matemático (modelo)
----------------------------
Dados n componentes y una matriz simétrica de pesos W ∈ R^{n×n} donde W[i][j] ≥ 0 representa la dependencia/peso entre i y j (W[i][i]=0), el objetivo es encontrar una asignación

$$f:\{0,\dots,n-1\} \to \{0,\dots,k-1\}$$

tal que cada grupo en el rango \{0,...,k-1\} sea no vacío y se minimice el valor de corte:

$$\mathrm{cut}(W,f)=\sum_{0\le i<j<n} W[i][j]\cdot [f(i) \ne f(j)],$$

donde $[\cdot]$ es la función indicadora (1 si la condición es verdadera, 0 en otro caso).

Restricciones importantes:
- Exactamente `k` particiones no vacías (cada etiqueta de 0 a k-1 debe aparecer al menos una vez).
- `k` debe satisfacer $1\le k \le n$.

Algoritmos incluidos
--------------------
- Exhaustivo (exacto): backtracking con poda y búsqueda completa; garantiza solución óptima para matrices pequeñas (por ejemplo n<12 por coste exponencial). Implementado en `backend/algorithms/exhaustive.py`.
- Heurístico (aproximado): búsqueda local con reinicios y estrategias de reparación para mantener exactamente `k` grupos no vacíos. Implementado en `backend/algorithms/heuristic.py`.

Instalación
------------
1. Crear un entorno virtual (recomendado):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate     # Windows (PowerShell)
```

2. Instalar dependencias del backend:

```bash
pip install -r backend/requirements.txt
```

Ejecución
---------
- Iniciar el backend (desde la carpeta `sistema-particionamiento`):

```bash
python -m backend.app
```

- Abrir la interfaz estática: abrir `frontend/index.html` en el navegador o servirla localmente:

```bash
cd frontend
python -m http.server 8000
# y abrir http://localhost:8000
```

API
---
Endpoint principal:

`POST http://localhost:5000/api/partition`

Request JSON (ejemplo):

```json
{
   "matrix": [[0,1,2],[1,0,1],[2,1,0]],
   "k": 2
}
```

Response (campos relevantes):
- `partitions`: mapeo grupo -> lista de componentes (nombres).  
- `assignment`: lista de enteros (grupo por componente).  
- `cut_value`: valor del corte calculado.  
- `cut_edges`: lista de aristas cortadas (pares con peso).  
- `optimal`: booleano si la solución es óptima (algoritmo exhaustivo) o aproximada.

Notas sobre errores comunes
-------------------------
- Si recibes: "El algoritmo devolvió una asignación inválida (no cumple k particiones no vacías)." comprueba que `k` cumple `1 <= k <= n` (n = número de filas/columnas de la matriz). El motor ahora valida `k` antes de ejecutar y devolverá un mensaje claro si `k>n` o `k<=0`.
- Asegúrate de enviar una matriz cuadrada simétrica con ceros en la diagonal.

Estructura de implementación (breve)
-----------------------------------
- `backend/core/partition_engine.py`: orquestador que decide usar algoritmo exhaustivo o heurístico según `n` y valida resultados.  
- `backend/algorithms/exhaustive.py`: búsqueda exhaustiva con poda y simetría (fija el primer nodo en grupo 0).  
- `backend/algorithms/heuristic.py`: búsqueda local con reinicios y reparación para garantizar `k` grupos no vacíos.  
- `backend/core/metrics.py`: funciones auxiliares para calcular `cut` y listar `cut_edges`.

Pruebas
-------
Ejecutar tests unitarios en `backend/tests`:

```bash
cd backend
pytest -q
```

Datos de ejemplo
---------------
En `backend/datasets/` hay matrices de ejemplo (`small_4x4.csv`, `medium_12x12.csv`, `large_30x30.csv`) que puedes cargar desde la UI o via script para experimentar.


