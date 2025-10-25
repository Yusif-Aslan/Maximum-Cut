

from __future__ import annotations

import argparse
import random
from typing import Tuple

import networkx as nx


def generate_random_graph(n: int, p: float, weight_range: Tuple[int, int] = (1, 10)) -> nx.Graph:
    """Generate an Erdos-Renyi random weighted graph."""
    g = nx.erdos_renyi_graph(n, p)
    low, high = weight_range
    for u, v in g.edges():
        g.edges[u, v]["weight"] = random.randint(low, high)
    return g


def load_edge_list(path: str) -> nx.Graph:
    """Load a weighted graph from an edge list file."""
    g = nx.read_weighted_edgelist(path, nodetype=int)
    return g


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Graph data utilities")
    parser.add_argument("--generate", action="store_true", help="Generate a random graph")
    parser.add_argument("--n", type=int, default=4, help="Number of nodes")
    parser.add_argument("--p", type=float, default=0.5, help="Edge probability")
    parser.add_argument("--type", type=str, default="random", help="Graph type")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.generate:
        graph = generate_random_graph(args.n, args.p)
        print(f"Generated graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
