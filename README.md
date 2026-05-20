# Sistema de Particionamiento Óptimo de Dependencias

Este proyecto implementa un sistema full stack para particionar componentes en `k` grupos minimizando la suma de dependencias entre grupos distintos.

## Estructura
- `backend/`: servidor Flask, algoritmos, validación, pruebas y datasets.
- `frontend/`: interfaz web estática para ingreso de matriz y visualización de resultados.
- `docs/`: documentación técnica, de usuario y resultados experimentales.

## Cómo ejecutar
1. Instalar dependencias:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Iniciar el backend desde la carpeta `sistema-particionamiento`:
   ```bash
   python -m backend.app
   ```
3. Abrir `frontend/index.html` en el navegador.

## API
POST `http://localhost:5000/api/partition`

Request JSON:
```json
{
  "matrix": [[0,1,2],[1,0,1],[2,1,0]],
  "k": 2
}
```

Response JSON incluye:
- `partitions`
- `assignment`
- `cut_value`
- `cut_edges`
- `optimal`
- `execution_time_seconds`
