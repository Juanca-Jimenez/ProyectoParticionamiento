def validate_matrix(matrix, k):
    if not isinstance(matrix, list) or not matrix:
        return False, "La matriz debe ser una lista no vacía."
    n = len(matrix)
    if not all(isinstance(row, list) and len(row) == n for row in matrix):
        return False, "La matriz debe ser cuadrada."
    if n < 2:
        return False, "La matriz debe tener al menos 2 componentes."
    if not isinstance(k, int):
        try:
            k = int(k)
        except Exception:
            return False, "El número de particiones k debe ser un entero."
    if k < 2 or k > 5:
        return False, "k debe estar entre 2 y 5."

    for i in range(n):
        for j in range(n):
            value = matrix[i][j]
            if not isinstance(value, (int, float)):
                return False, "Todos los valores de la matriz deben ser numéricos."
            if value < 0:
                return False, "Los valores de la matriz deben ser no negativos."
            if i == j and value != 0:
                return False, "La diagonal de la matriz debe ser 0."
            if matrix[i][j] != matrix[j][i]:
                return False, "La matriz debe ser simétrica."
    return True, "Matriz válida."
