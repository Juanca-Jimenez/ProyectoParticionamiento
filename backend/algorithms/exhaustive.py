from backend.core.metrics import calculate_cut


def exhaustive_partition(matrix, k):
    """
    Algoritmo de búsqueda exhaustiva con poda (Backtracking + Branch and Bound).

    Objetivo:
    Encontrar la k-partición con el menor valor de corte posible.

    Restricciones:
    - Deben existir exactamente k grupos.
    - Ningún grupo puede quedar vacío.

    Retorna:
    (mejor_asignacion, mejor_corte)
    """
    n = len(matrix)
    best_cut = float("inf")
    best_assignment = None
    assignment = [-1] * n

    used = [False] * k


    # ==========================
    # REDUCCIÓN DE SIMETRÍA
    # ==========================
    # Se fija el primer componente al grupo 0.
    # Esto elimina particiones equivalentes producidas
    # únicamente por renombrar grupos.
    assignment[0] = 0
    used[0] = True


    """
        Función recursiva que construye la partición.
        Parámetros:
        idx → componente que se está asignando
        current_cut → corte acumulado hasta ahora
        used_count → cantidad de grupos usados
        """
    def search(idx, current_cut, used_count):

        
        nonlocal best_cut, best_assignment

        # ==========================
        # PODA DE VIABILIDAD
        # ==========================
        # Si ya no quedan suficientes componentes
        # para llenar todos los grupos obligatorios,
        # esta rama nunca será válida.
        remaining = n - idx



        # ==========================
        # BRANCH AND BOUND
        # ==========================
        # Si el corte parcial ya supera el mejor conocido,
        # continuar sería inútil.
        if used_count + remaining < k:
            return
        # branch-and-bound: if current cut already >= best_cut, prune
        if current_cut >= best_cut:
            return

        # ==========================
        # CASO BASE
        # ==========================
        # Todos los componentes fueron procesados.

        if idx == n:
            # Solo aceptar soluciones con exactamente k grupos
            if used_count == k:
                 # Actualizar solución óptima
                if current_cut < best_cut:
                    best_cut = current_cut
                    
                    # Se copia para conservar el estado actual
                    best_assignment = assignment.copy()
            return
        
        # ==========================
        # GENERACIÓN DE RAMAS
        # ==========================
        # Intentar colocar el componente actual
        # en cada grupo posible.
        for g in range(k):
            prev_used = used[g]
             # Asignación tentativa
            assignment[idx] = g
            if not prev_used:
                used[g] = True
                used_count += 1

            # ==========================
            # CÁLCULO INCREMENTAL DEL CORTE
            # ==========================
            # Solo evaluar conexiones del nuevo componente
            # con componentes ya asignados.
            added = 0.0
            for j in range(idx):
                # Si terminan en grupos distintos,
                # esa dependencia contribuye al corte.
                if assignment[j] != g:
                    added += matrix[j][idx]

            search(idx + 1, current_cut + added, used_count)

            # ==========================
            # BACKTRACKING
            # ==========================
            # Restaurar el estado previo para
            # probar otra alternativa.
            if not prev_used:
                used[g] = False
                used_count -= 1
            assignment[idx] = -1

  # Comenzar desde el segundo componente
    # porque el primero ya quedó fijo
    search(1, 0.0, 1)

   # Si ninguna partición fue válida
    if best_assignment is None:
        return None, float("inf")
    return best_assignment, best_cut
