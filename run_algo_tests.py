from backend.algorithms.exhaustive import exhaustive_partition
from backend.algorithms.heuristic import heuristic_partition
from backend.core.metrics import calculate_cut

matrix = [
    [0,1,2,0],
    [1,0,1,3],
    [2,1,0,1],
    [0,3,1,0]
]
for k in [2,3,4]:
    print('\n=== k=',k,'===')
    a,c = exhaustive_partition(matrix,k)
    print('exhaustive assignment:', a, 'valid:', a is not None and len(a)==len(matrix) and len(set(a))==k)
    print('cut:', c if a is not None else 'inf')
    b,d = heuristic_partition(matrix,k, restarts=10, max_no_improve=10)
    print('heuristic assignment:', b, 'valid:', b is not None and len(b)==len(matrix) and len(set(b))==k)
    print('cut:', d)
