import random
from backend.core.metrics import calculate_cut


def heuristic_partition(matrix, k, restarts=30, max_no_improve=20):
    n = len(matrix)
    best_assignment = None
    best_cut = float("inf")

    def local_search(assignment):
        current_cut = calculate_cut(matrix, assignment)
        no_improve = 0
        while no_improve < max_no_improve:
            improved = False
            for i in range(n):
                current_group = assignment[i]
                best_move = current_group
                best_delta = 0
                for target_group in range(k):
                    if target_group == current_group:
                        continue
                    delta = 0
                    for j in range(n):
                        if i == j:
                            continue
                        if assignment[j] == current_group:
                            delta += matrix[i][j]
                        elif assignment[j] == target_group:
                            delta -= matrix[i][j]
                    if delta < best_delta:
                        best_delta = delta
                        best_move = target_group
                if best_move != current_group:
                    assignment[i] = best_move
                    current_cut += best_delta
                    improved = True
            if improved:
                no_improve = 0
            else:
                no_improve += 1
        return assignment, current_cut

    for _ in range(restarts):
        assignment = [random.randrange(k) for _ in range(n)]
        assignment, current_cut = local_search(assignment)
        if current_cut < best_cut:
            best_cut = current_cut
            best_assignment = assignment.copy()
    if best_assignment is None:
        best_assignment = [0] * n
        best_cut = calculate_cut(matrix, best_assignment)
    return best_assignment, best_cut
