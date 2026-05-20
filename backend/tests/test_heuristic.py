from backend.algorithms.heuristic import heuristic_partition


def test_heuristic_partition_returns_assignment():
    matrix = [[0, 1, 1, 0], [1, 0, 2, 1], [1, 2, 0, 1], [0, 1, 1, 0]]
    assignment, cut = heuristic_partition(matrix, 2, restarts=5, max_no_improve=5)
    assert isinstance(assignment, list)
    assert len(assignment) == 4
    assert cut >= 0
