import random
from backend.core.metrics import calculate_cut


def heuristic_partition(matrix, k, restarts=30, max_no_improve=20):
    """Heuristic local search that ensures the returned assignment uses exactly k non-empty groups.

    Strategy:
    - Initialize assignments with first k nodes each in distinct groups to avoid empty groups.
    - Run local search but do not allow moves that would empty a group.
    - If after local search some groups are empty (rare), repair by moving nodes with minimal cost increase.
    """
    n = len(matrix)
    best_assignment = None
    best_cut = float("inf")

    def local_search(assignment):
        current_cut = calculate_cut(matrix, assignment)
        no_improve = 0
        # keep track of counts to prevent emptying a group
        counts = [0] * k
        for g in assignment:
            counts[g] += 1

        while no_improve < max_no_improve:
            improved = False
            for i in range(n):
                current_group = assignment[i]
                best_move = current_group
                best_delta = 0
                for target_group in range(k):
                    if target_group == current_group:
                        continue
                    # don't allow move that would empty current_group
                    if counts[current_group] <= 1:
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
                    counts[current_group] -= 1
                    counts[best_move] += 1
                    assignment[i] = best_move
                    current_cut += best_delta
                    improved = True
            if improved:
                no_improve = 0
            else:
                no_improve += 1
        return assignment, current_cut

    def repair_assignment(assignment):
        # ensure all groups present; for each missing group, move the node whose move
        # causes the smallest increase in cut
        present = set(assignment)
        missing = [g for g in range(k) if g not in present]
        if not missing:
            return assignment

        counts = [0] * k
        for g in assignment:
            counts[g] += 1

        for m in missing:
            best_node = None
            best_increase = float("inf")
            for i in range(n):
                src = assignment[i]
                # prefer not to empty src unless necessary
                if counts[src] <= 1:
                    continue
                increase = 0.0
                for j in range(n):
                    if i == j:
                        continue
                    if assignment[j] == src:
                        increase += matrix[i][j]
                    elif assignment[j] == m:
                        increase -= matrix[i][j]
                if increase < best_increase:
                    best_increase = increase
                    best_node = i
            if best_node is None:
                # fallback: pick any node from the largest group
                largest = max(range(k), key=lambda x: counts[x])
                for i in range(n):
                    if assignment[i] == largest:
                        best_node = i
                        break
            # perform move
            counts[assignment[best_node]] -= 1
            assignment[best_node] = m
            counts[m] += 1

        return assignment

    for _ in range(restarts):
        # initialize so first k nodes occupy distinct groups to avoid empty groups
        assignment = [random.randrange(k) for _ in range(n)]
        if n >= k:
            for i in range(k):
                assignment[i] = i

        assignment, current_cut = local_search(assignment)
        # repair if needed
        if len(set(assignment)) != k:
            assignment = repair_assignment(assignment)
            current_cut = calculate_cut(matrix, assignment)

        if len(set(assignment)) == k and current_cut < best_cut:
            best_cut = current_cut
            best_assignment = assignment.copy()

    if best_assignment is None:
        # try deterministic valid fallback: first k nodes in distinct groups
        if n >= k:
            best_assignment = [i if i < k else 0 for i in range(n)]
        else:
            best_assignment = [0] * n
        best_cut = calculate_cut(matrix, best_assignment)

    return best_assignment, best_cut
