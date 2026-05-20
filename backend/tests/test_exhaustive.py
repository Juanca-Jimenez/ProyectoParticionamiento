from backend.algorithms.exhaustive import exhaustive_partition


def test_exhaustive_partition_small():
    matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    assignment, cut, optimal = exhaustive_partition(matrix, 2)
    assert optimal is True
    assert cut == 3
    assert isinstance(assignment, list)
    assert len(assignment) == 3
