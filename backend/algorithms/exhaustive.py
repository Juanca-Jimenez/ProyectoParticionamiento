from backend.core.metrics import calculate_cut


def exhaustive_partition(matrix, k):
    n = len(matrix)
    best_cut = float("inf")
    best_assignment = None
    assignment = [0] * n

    def search(index):
        nonlocal best_cut, best_assignment
        if index == n:
            cut = calculate_cut(matrix, assignment)
            if cut < best_cut:
                best_cut = cut
                best_assignment = assignment.copy()
            return
        for group in range(k):
            assignment[index] = group
            search(index + 1)

    search(0)
    if best_assignment is None:
        best_assignment = assignment.copy()
    return best_assignment, best_cut
