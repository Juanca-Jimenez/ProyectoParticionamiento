import time
from backend.algorithms.exhaustive import exhaustive_partition
from backend.algorithms.heuristic import heuristic_partition
from backend.core.metrics import calculate_cut, get_cut_edges

class PartitionEngine:
    def __init__(self, matrix, k):
        self.matrix = matrix
        self.k = k
        self.n = len(matrix)

    def run(self):
        start_time = time.time()
        
        if self.n < 12:
            assignment, best_cut = exhaustive_partition(self.matrix, self.k)
            optimal = True
            algorithm_used = "exhaustive (óptimo garantizado)"
        else:
            assignment, best_cut = heuristic_partition(self.matrix, self.k)
            optimal = False
            algorithm_used = "heuristic (búsqueda local)"

        # Crear nombres genéricos para los componentes
        component_names = [f"Componente_{i}" for i in range(self.n)]
        
        # Obtener aristas cortadas con el formato correcto
        edges = get_cut_edges(self.matrix, assignment, component_names)
        
        # Construir particiones como diccionario (no como lista de listas)
        partitions = {}
        for i, group in enumerate(assignment):
            if group not in partitions:
                partitions[group] = []
            partitions[group].append(component_names[i])
        
        # Ordenar grupos
        partitions = dict(sorted(partitions.items()))
        
        elapsed = time.time() - start_time

        return {
            "status": "success",
            "k": self.k,
            "n": self.n,
            "optimal": optimal,
            "algorithm_used": algorithm_used,
            "partitions": partitions,
            "cut_value": best_cut,
            "cut_edges": edges,
            "execution_time_ms": round(elapsed * 1000, 2)
        }