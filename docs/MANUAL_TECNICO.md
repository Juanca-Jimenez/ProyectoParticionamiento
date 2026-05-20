# MANUAL TÉCNICO

## Requisitos
- Python 3.9+
- Flask
- pytest

## Ejecución
1. Instalar dependencias: `pip install -r backend/requirements.txt`
2. Iniciar backend: `python backend/app.py`
3. Abrir `frontend/index.html` en el navegador.

## API
- `POST /api/partition`
  - Request JSON: `{ "matrix": [[...]], "k": 3 }` o `{ "csv": "...", "k": 3 }`
  - Respuesta: `partitions`, `assignment`, `cut_value`, `cut_edges`, `optimal`, `execution_time_seconds`
