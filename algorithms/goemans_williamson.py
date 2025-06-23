import random
import math


def random_vector(dim):
    return [random.gauss(0, 1) for _ in range(dim)]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def goemans_williamson(graph, rounds=50):
    """Simplified Goemans-Williamson using random hyperplane rounding."""
    n = graph.num_vertices
    best_value = -1
    best_bits = None
    for _ in range(rounds):
        # Use random vectors to simulate SDP output
        vectors = [random_vector(n) for _ in range(n)]
        hyperplane = random_vector(n)
        bits = [1 if dot(v, hyperplane) >= 0 else 0 for v in vectors]
        value = 0
        for u, v, w in graph.all_edges():
            if bits[u] != bits[v]:
                value += w
        if value > best_value:
            best_value = value
            best_bits = bits
    return best_value, best_bits
