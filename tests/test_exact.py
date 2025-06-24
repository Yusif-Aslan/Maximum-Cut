from src.data import generate_random_graph
from src.exact_bruteforce import maxcut_bruteforce
from src.exact_solver import maxcut_solver


def test_exact_methods_agree():
    g = generate_random_graph(4, 0.5)
    _, val1 = maxcut_bruteforce(g)
    _, val2 = maxcut_solver(g)
    assert abs(val1 - val2) < 1e-6
