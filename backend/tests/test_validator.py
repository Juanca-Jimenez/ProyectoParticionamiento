import pytest
from backend.core.validator import validate_matrix


def test_validate_matrix_valid():
    matrix = [[0, 1], [1, 0]]
    valid, message = validate_matrix(matrix, 2)
    assert valid is True
    assert "válida" in message.lower()


def test_validate_matrix_invalid_symmetry():
    matrix = [[0, 1], [0, 0]]
    valid, message = validate_matrix(matrix, 2)
    assert not valid
    assert "simétrica" in message.lower()


def test_validate_matrix_invalid_diagonal():
    matrix = [[1, 0], [0, 0]]
    valid, message = validate_matrix(matrix, 2)
    assert not valid
    assert "diagonal" in message.lower()
