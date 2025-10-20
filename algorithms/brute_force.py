from itertools import product


def max_cut_brute_force(graph):
    """Return best cut value by checking all partitions."""
    n = graph.num_vertices
    best_value = -1
    best_partition = None
    for bits in product([0, 1], repeat=n):
        value = 0
        for u, v, w in graph.all_edges():
            if bits[u] != bits[v]:
                value += w
        if value > best_value:
            best_value = value
            best_partition = bits
    return best_value, best_partition
