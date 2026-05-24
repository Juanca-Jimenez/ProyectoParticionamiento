import os
import sys
import csv
import time
import tracemalloc
import random

# Asegurar que el directorio raíz del proyecto está en el PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.algorithms.exhaustive import exhaustive_partition
from backend.algorithms.heuristic import heuristic_partition
from backend.core.metrics import calculate_cut

# Directorios de salida
RESULTS_DIR = os.path.join(ROOT, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
TABLES_DIR = os.path.join(RESULTS_DIR, "tables")
REPORTS_DIR = os.path.join(RESULTS_DIR, "reports")

def ensure_directories():
    for d in [PLOTS_DIR, TABLES_DIR, REPORTS_DIR]:
        os.makedirs(d, exist_ok=True)
    print("Directorios de resultados asegurados.")

def generate_symmetric_matrix(n, density=0.5, max_weight=10, seed=42):
    """Genera una matriz de adyacencia simétrica de dependencias con diagonal cero
    usando una semilla fija para garantizar la reproducibilidad.
    """
    random.seed(seed)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                w = float(random.randint(1, max_weight))
                matrix[i][j] = w
                matrix[j][i] = w
            else:
                matrix[i][j] = 0.0
                matrix[j][i] = 0.0
    return matrix

def load_real_matrix(file_name):
    """Carga una de las matrices reales guardadas en la carpeta de datasets del backend."""
    file_path = os.path.join(ROOT, "backend", "datasets", file_name)
    matrix = []
    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                matrix.append([float(cell.strip()) for cell in row])
    return matrix

def measure_execution(matrix, k, algorithm, num_runs=5):
    """Ejecuta el algoritmo indicado sobre la matriz dada, midiendo el tiempo promedio 
    de varias iteraciones en milisegundos y el consumo pico de memoria en KB.
    """
    n = len(matrix)
    
    # 1. Medir consumo de memoria (hacemos un primer run aislado para medir memoria limpia)
    tracemalloc.start()
    if algorithm == "Exhaustivo":
        assignment, cut_val = exhaustive_partition(matrix, k)
    else:
        assignment, cut_val = heuristic_partition(matrix, k)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    memory_peak_kb = round(peak / 1024.0, 3)

    # 2. Medir tiempo de ejecución promedio
    run_times = []
    for _ in range(num_runs):
        start_time = time.perf_counter()
        if algorithm == "Exhaustivo":
            exhaustive_partition(matrix, k)
        else:
            heuristic_partition(matrix, k)
        elapsed = time.perf_counter() - start_time
        run_times.append(elapsed * 1000.0) # a milisegundos
        
    avg_time_ms = round(sum(run_times) / len(run_times), 4)
    
    return avg_time_ms, memory_peak_kb, cut_val

def run_all_benchmarks():
    print("Iniciando suite de experimentos...")
    ensure_directories()
    
    results = []
    
    # --- EXPERIMENTO 1: SYNTHETIC BENCHMARK ---
    print("\n--- Corriendo Experimentos con Matrices Sintéticas ---")
    sizes = [5, 10, 15, 20, 25, 30]
    fixed_k = 3
    
    for n in sizes:
        print(f"Evaluando tamaño n={n} (Sintética)...")
        matrix = generate_symmetric_matrix(n, density=0.5, max_weight=10, seed=42)
        
        # Exhaustivo (solo si n < 12)
        if n < 12:
            try:
                t_ms, mem_kb, cut = measure_execution(matrix, fixed_k, "Exhaustivo")
                results.append({
                    "algorithm": "Exhaustivo",
                    "dataset_type": "synthetic",
                    "n": n,
                    "k": fixed_k,
                    "execution_time_ms": t_ms,
                    "memory_peak_kb": mem_kb,
                    "cut_value": cut
                })
                print(f"  [Exhaustivo] Tiempo: {t_ms} ms, Memoria: {mem_kb} KB, Corte: {cut}")
            except Exception as e:
                print(f"  Error en Exhaustivo n={n}: {e}")
                
        # Heurístico (en todos los tamaños)
        try:
            t_ms, mem_kb, cut = measure_execution(matrix, fixed_k, "Heurística")
            results.append({
                "algorithm": "Heurística",
                "dataset_type": "synthetic",
                "n": n,
                "k": fixed_k,
                "execution_time_ms": t_ms,
                "memory_peak_kb": mem_kb,
                "cut_value": cut
            })
            print(f"  [Heurística] Tiempo: {t_ms} ms, Memoria: {mem_kb} KB, Corte: {cut}")
        except Exception as e:
            print(f"  Error en Heurística n={n}: {e}")

    # --- EXPERIMENTO 2: REAL DATASET BENCHMARK ---
    print("\n--- Corriendo Experimentos con Datasets Reales ---")
    real_files = [
        ("small_4x4.csv", 4),
        ("medium_12x12.csv", 12),
        ("large_30x30.csv", 30)
    ]
    
    for filename, n in real_files:
        print(f"Evaluando archivo real {filename} (n={n})...")
        matrix = load_real_matrix(filename)
        
        # Exhaustivo (solo si n < 12, es decir, solo el de 4x4)
        if n < 12:
            t_ms, mem_kb, cut = measure_execution(matrix, fixed_k, "Exhaustivo")
            results.append({
                "algorithm": "Exhaustivo",
                "dataset_type": f"real ({filename})",
                "n": n,
                "k": fixed_k,
                "execution_time_ms": t_ms,
                "memory_peak_kb": mem_kb,
                "cut_value": cut
            })
            print(f"  [Exhaustivo] Tiempo: {t_ms} ms, Memoria: {mem_kb} KB, Corte: {cut}")
            
        # Heurístico (en todos)
        t_ms, mem_kb, cut = measure_execution(matrix, fixed_k, "Heurística")
        results.append({
            "algorithm": "Heurística",
            "dataset_type": f"real ({filename})",
            "n": n,
            "k": fixed_k,
            "execution_time_ms": t_ms,
            "memory_peak_kb": mem_kb,
            "cut_value": cut
        })
        print(f"  [Heurística] Tiempo: {t_ms} ms, Memoria: {mem_kb} KB, Corte: {cut}")

    # --- EXPERIMENTO 3: CALIDAD DE LA SOLUCIÓN VS PARAMETRO K ---
    print("\n--- Corriendo Experimentos de Calidad vs Parámetro k ---")
    
    # 3.1. Variación de k para n=10 Sintética (Exhaustivo y Heurístico para comparar)
    matrix_n10 = generate_symmetric_matrix(10, density=0.6, max_weight=10, seed=100)
    for k_val in [2, 3, 4, 5]:
        print(f"n=10 Sintética, k={k_val}...")
        # Exhaustivo
        t_ms, mem_kb, cut = measure_execution(matrix_n10, k_val, "Exhaustivo")
        results.append({
            "algorithm": "Exhaustivo",
            "dataset_type": "quality_varying_k_n10",
            "n": 10,
            "k": k_val,
            "execution_time_ms": t_ms,
            "memory_peak_kb": mem_kb,
            "cut_value": cut
        })
        # Heurística
        t_ms, mem_kb, cut = measure_execution(matrix_n10, k_val, "Heurística")
        results.append({
            "algorithm": "Heurística",
            "dataset_type": "quality_varying_k_n10",
            "n": 10,
            "k": k_val,
            "execution_time_ms": t_ms,
            "memory_peak_kb": mem_kb,
            "cut_value": cut
        })

    # 3.2. Variación de k para n=20 Sintética (Solo Heurístico, ya que n >= 12)
    matrix_n20 = generate_symmetric_matrix(20, density=0.5, max_weight=10, seed=200)
    for k_val in [2, 3, 4, 5]:
        print(f"n=20 Sintética, k={k_val}...")
        t_ms, mem_kb, cut = measure_execution(matrix_n20, k_val, "Heurística")
        results.append({
            "algorithm": "Heurística",
            "dataset_type": "quality_varying_k_n20",
            "n": 20,
            "k": k_val,
            "execution_time_ms": t_ms,
            "memory_peak_kb": mem_kb,
            "cut_value": cut
        })

    # 3.3. Variación de k para medium_12x12.csv (Solo Heurístico, ya que n >= 12)
    matrix_m12 = load_real_matrix("medium_12x12.csv")
    for k_val in [2, 3, 4, 5]:
        print(f"medium_12x12.csv Real, k={k_val}...")
        t_ms, mem_kb, cut = measure_execution(matrix_m12, k_val, "Heurística")
        results.append({
            "algorithm": "Heurística",
            "dataset_type": "quality_varying_k_real_m12",
            "n": 12,
            "k": k_val,
            "execution_time_ms": t_ms,
            "memory_peak_kb": mem_kb,
            "cut_value": cut
        })

    # Guardar en CSV
    csv_file_path = os.path.join(TABLES_DIR, "summary_results.csv")
    csv_plots_path = os.path.join(PLOTS_DIR, "summary_results.csv")
    
    for path in [csv_file_path, csv_plots_path]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "algorithm", "dataset_type", "n", "k", "execution_time_ms", "memory_peak_kb", "cut_value"
            ])
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nDatos consolidados exportados exitosamente a {csv_file_path} y {csv_plots_path}")

    # --- INVOCAR SUBMÓDULOS DE GRAFICACIÓN Y REPORTE ---
    try:
        from backend.analysis.benchmark_visualizer import generate_all_plots
        print("\nGenerando gráficas de tendencias...")
        generate_all_plots()
    except Exception as e:
        print(f"Error al generar gráficos: {e}")
        import traceback
        traceback.print_exc()

    try:
        from backend.analysis.benchmark_report import generate_reports
        print("\nGenerando reportes analíticos...")
        generate_reports()
    except Exception as e:
        print(f"Error al generar reportes: {e}")
        import traceback
        traceback.print_exc()

    print("\nSuite de experimentos finalizada con éxito.")

if __name__ == "__main__":
    run_all_benchmarks()
