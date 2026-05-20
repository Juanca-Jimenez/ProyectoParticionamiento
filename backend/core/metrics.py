def calculate_cut(matrix, assignment):
    n = len(matrix)
    cut = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if assignment[i] != assignment[j]:
                cut += matrix[i][j]
    return cut


def cut_edges(matrix, assignment):
    edges = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if assignment[i] != assignment[j] and matrix[i][j] != 0:
                edges.append({
                    "source": i,
                    "target": j,
                    "weight": matrix[i][j]
                })
    return edges


def get_cut_edges(matrix, assignment, component_names):
    """Versión para el frontend con from/to y nombres de componentes"""
    edges = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if assignment[i] != assignment[j] and matrix[i][j] != 0:
                edges.append({
                    "from": component_names[i],
                    "to": component_names[j],
                    "weight": matrix[i][j]
                })
    return edges