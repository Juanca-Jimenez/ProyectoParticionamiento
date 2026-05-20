# DOCUMENTACIÓN FORMAL

## Propósito
Sistema de particionamiento óptimo de matrices de dependencias para minimizar la suma de dependencias entre grupos distintos.

## Arquitectura
- backend: servidor Flask con API REST en `/api/partition`
- frontend: página estática para ingreso de matrices y visualización de resultados

## Módulos
- `backend/core/validator.py`: valida la matriz de entrada
- `backend/core/partition_engine.py`: orquesta la selección de algoritmo
- `backend/core/metrics.py`: calcula la función de corte y las aristas cortadas
- `backend/algorithms/exhaustive.py`: búsqueda exhaustiva para n < 12
- `backend/algorithms/heuristic.py`: búsqueda local con reinicios para n >= 12
