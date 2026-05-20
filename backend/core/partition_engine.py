import time
import tracemalloc
from backend.algorithms.exhaustive import exhaustive_partition
from backend.algorithms.heuristic import heuristic_partition
from backend.core.metrics import get_cut_edges

class PartitionEngine:
    def __init__(self, matrix, k):
        self.matrix = matrix
        self.k = k
        self.n = len(matrix)

    def run(self):
        tracemalloc.start()
        start_time = time.time()
        
        if self.n < 12:
            assignment, best_cut = exhaustive_partition(self.matrix, self.k)
            optimal = True
            algorithm_used = "Exhaustivo"
        else:
            assignment, best_cut = heuristic_partition(self.matrix, self.k)
            optimal = False
            algorithm_used = "Heurística"

        # Validate assignment strictly: exactly n entries, groups in 0..k-1, exactly k distinct groups
        valid_assignment = (
            assignment is not None
            and len(assignment) == self.n
            and all(isinstance(group, int) and 0 <= group < self.k for group in assignment)
            and len(set(assignment)) == self.k
        )

        elapsed = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if not valid_assignment:
            return {
                "status": "error",
                "message": "El algoritmo devolvió una asignación inválida (no cumple k particiones no vacías).",
                "k": self.k,
                "n": self.n,
                "valid_assignment": False,
                "execution_time_ms": round(elapsed * 1000, 2),
                "memory_peak_kb": round(peak / 1024, 2),
            }

        component_names = [f"Componente_{i}" for i in range(self.n)]
        edges = get_cut_edges(self.matrix, assignment, component_names)
        for edge in edges:
            edge["reason"] = (
                f"Se corta porque {edge['from']} y {edge['to']} están en grupos distintos y su dependencia pesa {edge['weight']}."
            )

        partitions = {group: [] for group in range(self.k)}
        for i, group in enumerate(assignment):
            partitions[group].append(component_names[i])

        component_reasons = []
        for i, group in enumerate(assignment):
            same_weight = sum(
                self.matrix[i][j] for j in range(self.n) if j != i and assignment[j] == group
            )
            cross_weight = sum(
                self.matrix[i][j] for j in range(self.n) if assignment[j] != group
            )
            reason = (
                "porque tiene más dependencias dentro de su grupo que hacia otros grupos"
                if same_weight >= cross_weight
                else "porque sus conexiones externas pesan menos que las conexiones internas en su grupo"
            )
            component_reasons.append({
                "component": component_names[i],
                "group": group,
                "same_group_weight": same_weight,
                "cross_group_weight": cross_weight,
                "reason": reason,
            })

        explanation = {
            "solution_selection": (
                "Se eligió la solución con el menor valor de corte entre todas las asignaciones válidas "
                "que cumplen exactamente k particiones no vacías."
            ),
            "classification": (
                "Óptima" if optimal else "Aproximada"
            ),
            "algorithm_reason": (
                "Se empleó el algoritmo Exhaustivo porque el tamaño de matriz es pequeño y puede encontrar la mejor solución exacta."
                if optimal
                else "Se empleó el algoritmo Heurístico porque la matriz es más grande y buscamos una solución válida de buena calidad."
            ),
            "cut_reason": (
                "Las aristas se cortan cuando los componentes correspondientes quedan en particiones distintas; su peso se suma al valor de corte."
            ),
            "group_reason": (
                "Los componentes se separan en grupos distintos para minimizar el total de dependencias cruzadas entre particiones, "
                "manteniendo exactamente k grupos no vacíos."
            ),
            "component_reasons": component_reasons,
        }

        return {
            "status": "success",
            "k": self.k,
            "n": self.n,
            "optimal": optimal,
            "algorithm_used": algorithm_used,
            "partitions": partitions,
            "cut_value": best_cut,
            "cut_edges": edges,
            "explanation": explanation,
            "execution_time_ms": round(elapsed * 1000, 2),
            "memory_peak_kb": round(peak / 1024, 2),
            "valid_assignment": True,
            "assignment_count": len(assignment)
        }
