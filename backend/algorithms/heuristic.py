import random
from backend.core.metrics import calculate_cut


def heuristic_partition(matrix, k, restarts=30, max_no_improve=20):
    """
    Algoritmo heurístico de particionamiento.

    Objetivo:
    Encontrar una partición de exactamente k grupos
    que minimice el valor de corte.

    Estrategia:
    1. Generar una solución inicial aleatoria.
    2. Mejorarla mediante búsqueda local.
    3. Repetir varias veces (reinicios).
    4. Conservar la mejor solución encontrada.
    """

    
    n = len(matrix)  # Número total de componentes del sistema
    best_assignment = None  # Mejor solución encontrada entre todos los reinicios
    best_cut = float("inf")  # Mejor valor de corte encontrado

    def local_search(assignment):
        """
        Mejora una solución inicial moviendo componentes
        entre grupos si el corte disminuye.
        """

        # Calcular costo inicial
        current_cut = calculate_cut(matrix, assignment)

        # Contador de iteraciones consecutivas sin mejora
        no_improve = 0
        # Contar cuántos componentes hay en cada grupo
        counts = [0] * k
        for g in assignment:
            counts[g] += 1

       # Continuar mientras todavía aparezcan mejoras
        while no_improve < max_no_improve:
            improved = False

            # Analizar componente por componente
            for i in range(n):

                # Grupo actual del componente
                current_group = assignment[i]
                # Inicialmente asumimos que no se moverá
                best_move = current_group
                 # Mejor reducción encontrada
                best_delta = 0


                # Probar mover el componente
                # a todos los grupos posibles
                for target_group in range(k):

                      # Ignorar mover al mismo grupo
                    if target_group == current_group:
                        continue
                     # No permitir dejar grupos vacíos
                    if counts[current_group] <= 1:
                        continue

                      # Cambio estimado en el corte 
                    delta = 0

                        # Analizar impacto del movimiento
                    for j in range(n):
                    # Ignorar comparación consigo mismo
                        if i == j:
                            continue

                        # Si j pertenece al grupo actual:
                        # mover i rompería esa conexión
                        if assignment[j] == current_group:
                            delta += matrix[i][j]
                        # Si j pertenece al grupo destino:
                        # mover i fortalecería agrupamiento
                        elif assignment[j] == target_group:
                            delta -= matrix[i][j]
                    
                    # Guardar el mejor movimiento
                    if delta < best_delta:
                        best_delta = delta
                        best_move = target_group

                  # Aplicar movimiento si mejora
                if best_move != current_group:

                    # Actualizar tamaños de grupos
                    counts[current_group] -= 1
                    counts[best_move] += 1
                    # Mover componente
                    assignment[i] = best_move
                    # Actualizar corte sin recalcular completo
                    current_cut += best_delta
                    improved = True

             # Reiniciar contador si hubo mejora        
            if improved:
                no_improve = 0
            # Acercarse al criterio de parada
            else:
                no_improve += 1
        return assignment, current_cut

    def repair_assignment(assignment):
        """
        Corrige soluciones inválidas.

        Garantiza que existan exactamente k grupos.
        """

# Grupos presentes actualmente
        present = set(assignment)
        missing = [g for g in range(k) if g not in present]

        # Si ya está válida
        if not missing:
            return assignment

        # Contar tamaños de grupos
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
            # Respaldo:
            # tomar componente del grupo más grande
                largest = max(range(k), key=lambda x: counts[x])

            # Buscar nodo que menos empeore
                for i in range(n):
                    if assignment[i] == largest:
                        best_node = i
                        break
            # perform move
            counts[assignment[best_node]] -= 1
            assignment[best_node] = m
            counts[m] += 1

        return assignment

    # ==========================
    # REINICIOS ALEATORIOS
    # ==========================
    for _ in range(restarts):
        # Crear solución inicial
        assignment = [random.randrange(k) for _ in range(n)]
        # Forzar presencia de todos los grupos
        if n >= k:
            for i in range(k):
                assignment[i] = i

# Mejorar solución inicial
        assignment, current_cut = local_search(assignment)

        # Reparar si quedó inválida
        if len(set(assignment)) != k:
            assignment = repair_assignment(assignment)
            current_cut = calculate_cut(matrix, assignment)

        if len(set(assignment)) == k and current_cut < best_cut:
            best_cut = current_cut
            best_assignment = assignment.copy()

    # ==========================
    # RESPALDO FINAL
    # ==========================

    if best_assignment is None:
        # try deterministic valid fallback: first k nodes in distinct groups
        if n >= k:
            best_assignment = [i if i < k else 0 for i in range(n)]
        else:
            best_assignment = [0] * n
        best_cut = calculate_cut(matrix, best_assignment)

    return best_assignment, best_cut
