import os
import sys
import csv
import shutil
import numpy as np
import matplotlib
# Configurar Matplotlib para operar sin GUI (headless)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Asegurar que el directorio raíz del proyecto está en el PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

RESULTS_DIR = os.path.join(ROOT, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
TABLES_DIR = os.path.join(RESULTS_DIR, "tables")
REPORTS_DIR = os.path.join(RESULTS_DIR, "reports")

def load_data_from_csv():
    csv_path = os.path.join(TABLES_DIR, "summary_results.csv")
    if not os.path.exists(csv_path):
        # Fallback to plots directory if it exists there
        csv_path = os.path.join(PLOTS_DIR, "summary_results.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No se encontró el archivo CSV en {csv_path}. Ejecute el runner primero.")
        
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "algorithm": row["algorithm"],
                "dataset_type": row["dataset_type"],
                "n": int(row["n"]),
                "k": int(row["k"]),
                "execution_time_ms": float(row["execution_time_ms"]),
                "memory_peak_kb": float(row["memory_peak_kb"]),
                "cut_value": float(row["cut_value"])
            })
    return data

def generate_all_plots():
    data = load_data_from_csv()
    
    # Asegurar la existencia de directorios
    os.makedirs(PLOTS_DIR, exist_ok=True)
    
    # ----------------------------------------------------
    # Separar datos por experimentos
    # ----------------------------------------------------
    # 1. Benchmarks de tamaño (fijo k=3)
    synth_heur_size = []
    synth_exh_size = []
    real_heur_size = []
    real_exh_size = []
    
    # 2. Benchmarks de calidad (k variable)
    quality_n10_exh = []
    quality_n10_heur = []
    quality_n20_heur = []
    quality_real_m12_heur = []
    
    for row in data:
        algo = row["algorithm"]
        ds = row["dataset_type"]
        n = row["n"]
        k = row["k"]
        t = row["execution_time_ms"]
        m = row["memory_peak_kb"]
        c = row["cut_value"]
        
        # Experimento de tamaño (k=3)
        if k == 3 and not ds.startswith("quality_"):
            if ds == "synthetic":
                if algo == "Heurística":
                    synth_heur_size.append((n, t, m))
                elif algo == "Exhaustivo":
                    synth_exh_size.append((n, t, m))
            elif ds.startswith("real"):
                if algo == "Heurística":
                    real_heur_size.append((n, t, m))
                elif algo == "Exhaustivo":
                    real_exh_size.append((n, t, m))
                    
        # Experimento de calidad (k variable)
        elif ds == "quality_varying_k_n10":
            if algo == "Exhaustivo":
                quality_n10_exh.append((k, c))
            elif algo == "Heurística":
                quality_n10_heur.append((k, c))
        elif ds == "quality_varying_k_n20":
            quality_n20_heur.append((k, c))
        elif ds == "quality_varying_k_real_m12":
            quality_real_m12_heur.append((k, c))

    # Ordenar por el eje X respectivo para evitar trazos cruzados
    synth_heur_size.sort()
    synth_exh_size.sort()
    real_heur_size.sort()
    real_exh_size.sort()
    
    quality_n10_exh.sort()
    quality_n10_heur.sort()
    quality_n20_heur.sort()
    quality_real_m12_heur.sort()

    # ----------------------------------------------------
    # FIGURA 1: Tiempo de Ejecución vs Tamaño del Problema
    # ----------------------------------------------------
    plt.figure(figsize=(9, 7))
    
    # Graficar curvas sintéticas reales
    if synth_heur_size:
        ns, ts, _ = zip(*synth_heur_size)
        plt.plot(ns, ts, marker='o', linestyle='-', linewidth=2, color='#1f77b4', label='Heurística (Sintética)')
        
        # Calcular línea de tendencia para Heurística (ajuste cuadrático / grado 2)
        coeffs_h = np.polyfit(ns, ts, 2)
        poly_h = np.poly1d(coeffs_h)
        ns_smooth = np.linspace(min(ns), max(ns), 100)
        plt.plot(ns_smooth, poly_h(ns_smooth), linestyle=':', color='#3a9edb', alpha=0.8, 
                 label='Línea de Tendencia (Heurística)')
        
    if synth_exh_size:
        ns, ts, _ = zip(*synth_exh_size)
        plt.plot(ns, ts, marker='s', linestyle='--', linewidth=2, color='#d62728', label='Exhaustivo (Sintética)')
        
        # Calcular línea de tendencia para Exhaustivo (ajuste lineal / exponencial de 2 puntos)
        coeffs_e = np.polyfit(ns, ts, 1)
        poly_e = np.poly1d(coeffs_e)
        ns_smooth = np.linspace(min(ns), max(ns), 100)
        plt.plot(ns_smooth, poly_e(ns_smooth), linestyle=':', color='#f35b5b', alpha=0.8, 
                 label='Línea de Tendencia (Exhaustivo)')
        
    # Reales
    if real_heur_size:
        ns, ts, _ = zip(*real_heur_size)
        plt.plot(ns, ts, marker='^', linestyle='-.', linewidth=2, color='#ff7f0e', label='Heurística (CSV Real)')
    if real_exh_size:
        ns, ts, _ = zip(*real_exh_size)
        plt.plot(ns, ts, marker='v', linestyle=':', linewidth=2, color='#2ca02c', label='Exhaustivo (CSV Real)')
        
    plt.xlabel('Tamaño del problema (número de nodos)', fontsize=11)
    plt.ylabel('Tiempo de ejecución (ms)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left', frameon=True)
    
    # Formato de títulos académicos
    title_str = "Figura 1.\nTiempo de Ejecución vs Tamaño del Problema"
    plt.title(title_str, fontsize=12, fontweight='bold', pad=15)
    
    # Nota al pie académica obligatoria
    footer_str = "Nota: El tiempo corresponde al promedio de múltiples ejecuciones utilizando las mismas condiciones experimentales.\nResultados obtenidos mediante ejecución experimental del sistema."
    plt.figtext(0.1, 0.02, footer_str, wrap=True, horizontalalignment='left', fontsize=9, fontstyle='italic')
    plt.subplots_adjust(bottom=0.22)
    
    plot_path1 = os.path.join(PLOTS_DIR, "execution_time_vs_problem_size.png")
    plt.savefig(plot_path1, dpi=300)
    plt.close()
    print(f"Gráfico 1 generado en: {plot_path1}")

    # ----------------------------------------------------
    # FIGURA 2: Calidad de la Solución (Corte) vs Parámetro k
    # ----------------------------------------------------
    plt.figure(figsize=(9, 7))
    
    if quality_n10_exh:
        ks, cs = zip(*quality_n10_exh)
        plt.plot(ks, cs, marker='o', linestyle='-', linewidth=2, color='#d62728', label='Exhaustivo (n=10, Sintética)')
    if quality_n10_heur:
        ks, cs = zip(*quality_n10_heur)
        plt.plot(ks, cs, marker='s', linestyle='--', linewidth=2, color='#9467bd', label='Heurística (n=10, Sintética)')
    if quality_n20_heur:
        ks, cs = zip(*quality_n20_heur)
        plt.plot(ks, cs, marker='^', linestyle='-.', linewidth=2, color='#1f77b4', label='Heurística (n=20, Sintética)')
    if quality_real_m12_heur:
        ks, cs = zip(*quality_real_m12_heur)
        plt.plot(ks, cs, marker='D', linestyle=':', linewidth=2, color='#ff7f0e', label='Heurística (n=12, CSV Real)')
        
    plt.xlabel('Número de grupos (k)', fontsize=11)
    plt.ylabel('Valor de corte obtenido', fontsize=11)
    plt.xticks([2, 3, 4, 5])
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right', frameon=True)
    
    title_str2 = "Figura 2.\nCalidad de la Solución (Valor de Corte) vs Parámetro"
    plt.title(title_str2, fontsize=12, fontweight='bold', pad=15)
    
    # Nota al pie académica obligatoria
    footer_str2 = "Nota: Menores valores de corte representan particiones con menor costo de comunicación entre grupos.\nResultados obtenidos mediante ejecución experimental del sistema."
    plt.figtext(0.1, 0.02, footer_str2, wrap=True, horizontalalignment='left', fontsize=9, fontstyle='italic')
    plt.subplots_adjust(bottom=0.22)
    
    plot_path2 = os.path.join(PLOTS_DIR, "solution_quality_vs_parameter.png")
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Gráfico 2 generado en: {plot_path2}")

    # ----------------------------------------------------
    # FIGURA 3: Consumo de Memoria vs Tamaño del Problema (Opcional)
    # ----------------------------------------------------
    plt.figure(figsize=(9, 7))
    
    # Sintéticos
    if synth_heur_size:
        ns, _, ms = zip(*synth_heur_size)
        plt.plot(ns, ms, marker='o', linestyle='-', linewidth=2, color='#1f77b4', label='Heurística (Sintética)')
    if synth_exh_size:
        ns, _, ms = zip(*synth_exh_size)
        plt.plot(ns, ms, marker='s', linestyle='--', linewidth=2, color='#d62728', label='Exhaustivo (Sintética)')
        
    # Reales
    if real_heur_size:
        ns, _, ms = zip(*real_heur_size)
        plt.plot(ns, ms, marker='^', linestyle='-.', linewidth=2, color='#ff7f0e', label='Heurística (CSV Real)')
    if real_exh_size:
        ns, _, ms = zip(*real_exh_size)
        plt.plot(ns, ms, marker='v', linestyle=':', linewidth=2, color='#2ca02c', label='Exhaustivo (CSV Real)')
        
    plt.xlabel('Tamaño del problema (número de nodos)', fontsize=11)
    plt.ylabel('Memoria máxima (KB)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left', frameon=True)
    
    title_str3 = "Figura 3.\nConsumo de Memoria vs Tamaño del Problema"
    plt.title(title_str3, fontsize=12, fontweight='bold', pad=15)
    
    footer_str3 = "Nota: Valores de memoria pico medidos durante la ejecución física de las pruebas.\nResultados obtenidos mediante ejecución experimental del sistema."
    plt.figtext(0.1, 0.02, footer_str3, wrap=True, horizontalalignment='left', fontsize=9, fontstyle='italic')
    plt.subplots_adjust(bottom=0.22)
    
    plot_path3 = os.path.join(PLOTS_DIR, "memory_vs_problem_size.png")
    plt.savefig(plot_path3, dpi=300)
    plt.close()
    print(f"Gráfico 3 generado en: {plot_path3}")

    # ----------------------------------------------------
    # Copiar archivos restantes a la carpeta /results/plots/
    # ----------------------------------------------------
    # 1. summary_results.csv
    csv_src = os.path.join(TABLES_DIR, "summary_results.csv")
    csv_dst = os.path.join(PLOTS_DIR, "summary_results.csv")
    if os.path.exists(csv_src) and csv_src != csv_dst:
        try:
            shutil.copy2(csv_src, csv_dst)
            print(f"Archivo de resumen CSV copiado a: {csv_dst}")
        except Exception as e:
            print(f"No se pudo copiar {csv_src} a {csv_dst}: {e}")

    # 2. benchmark_report.json
    json_src = os.path.join(REPORTS_DIR, "benchmark_report.json")
    json_dst = os.path.join(PLOTS_DIR, "benchmark_report.json")
    if os.path.exists(json_src) and json_src != json_dst:
        try:
            shutil.copy2(json_src, json_dst)
            print(f"Reporte JSON copiado a: {json_dst}")
        except Exception as e:
            print(f"No se pudo copiar {json_src} a {json_dst}: {e}")

if __name__ == "__main__":
    generate_all_plots()
