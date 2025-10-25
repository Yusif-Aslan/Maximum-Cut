import networkx as nx
from src.data import generate_random_graph


def test_generate_random_graph():
    g = generate_random_graph(4, 0.5)
    assert isinstance(g, nx.Graph)
    assert g.number_of_nodes() == 4
