from backend.core.metrics import calculate_cut, cut_edges


def test_calculate_cut():
    matrix = [[0, 2, 0], [2, 0, 3], [0, 3, 0]]
    assignment = [0, 1, 1]
    assert calculate_cut(matrix, assignment) == 2


def test_cut_edges():
    matrix = [[0, 4, 0], [4, 0, 1], [0, 1, 0]]
    assignment = [0, 1, 1]
    edges = cut_edges(matrix, assignment)
    assert edges == [{"source": 0, "target": 1, "weight": 4}]
