import time
from backend.algorithms.exhaustive import exhaustive_partition
from backend.algorithms.heuristic import heuristic_partition
from backend.core.metrics import calculate_cut, cut_edges

class PartitionEngine:
    def __init__(self, matrix, k):
        self.matrix = matrix
        self.k = k
        self.n = len(matrix)

    def run(self):
        start_time = time.time()
        if self.n < 12:
            assignment, best_cut, optimal = exhaustive_partition(self.matrix, self.k)
        else:
            assignment, best_cut = heuristic_partition(self.matrix, self.k)
            optimal = False

        edges = cut_edges(self.matrix, assignment)
        elapsed = time.time() - start_time
        partitions = [[] for _ in range(self.k)]
        for node, group in enumerate(assignment):
            partitions[group].append(node)

        return {
            "partitions": partitions,
            "assignment": assignment,
            "cut_value": best_cut,
            "cut_edges": edges,
            "optimal": optimal,
            "execution_time_seconds": round(elapsed, 6)
        }
