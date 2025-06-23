from collections import deque


def max_cut_branch_and_bound(graph):
    """Branch-and-bound exact solver for Max-Cut."""
    n = graph.num_vertices
    best_value = -1
    best_bits = None
    stack = deque([(0, [])])

    # Precompute edge weights for quick upper bound calculation
    total_edge_weight = sum(w for _, _, w in graph.all_edges())

    while stack:
        idx, bits = stack.pop()
        if idx == n:
            value = 0
            for u, v, w in graph.all_edges():
                if bits[u] != bits[v]:
                    value += w
            if value > best_value:
                best_value = value
                best_bits = list(bits)
            continue

        # Bound: every remaining edge can at most contribute total_edge_weight
        # This bound is very weak but keeps algorithm simple
        if best_value >= total_edge_weight:
            continue

        stack.append((idx + 1, bits + [0]))
        stack.append((idx + 1, bits + [1]))

    return best_value, best_bits
