from backend.core.metrics import calculate_cut


def exhaustive_partition(matrix, k):
    """Backtracking exhaustive search with pruning that only accepts valid partitions.

    Returns (assignment, cut) where assignment uses exactly k non-empty groups
    and groups are in range(0, k). If no valid partition exists, returns (None, inf).
    """
    n = len(matrix)
    best_cut = float("inf")
    best_assignment = None
    assignment = [-1] * n

    used = [False] * k

    # symmetry: assign first node to group 0 to reduce equivalent permutations
    assignment[0] = 0
    used[0] = True

    def search(idx, current_cut, used_count):
        nonlocal best_cut, best_assignment
        # prune if cannot reach k non-empty groups
        remaining = n - idx
        if used_count + remaining < k:
            return
        # branch-and-bound: if current cut already >= best_cut, prune
        if current_cut >= best_cut:
            return

        if idx == n:
            # only accept solutions with exactly k used groups
            if used_count == k:
                if current_cut < best_cut:
                    best_cut = current_cut
                    best_assignment = assignment.copy()
            return

        for g in range(k):
            prev_used = used[g]
            assignment[idx] = g
            if not prev_used:
                used[g] = True
                used_count += 1

            # incremental cut: pairs (j, idx) for j < idx
            added = 0.0
            for j in range(idx):
                if assignment[j] != g:
                    added += matrix[j][idx]

            search(idx + 1, current_cut + added, used_count)

            # backtrack
            if not prev_used:
                used[g] = False
                used_count -= 1
            assignment[idx] = -1

    # start search from index 1 because index 0 already set
    search(1, 0.0, 1)

    if best_assignment is None:
        return None, float("inf")
    return best_assignment, best_cut
