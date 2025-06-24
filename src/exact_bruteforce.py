
from __future__ import annotations

import itertools
from typing import Tuple, List

import networkx as nx


def maxcut_bruteforce(g: nx.Graph) -> Tuple[List[int], float]:
    best_cut = []
    best_value = float('-inf')
    nodes = list(g.nodes())
    for bits in itertools.product([0, 1], repeat=len(nodes)):
        cut = [nodes[i] for i, b in enumerate(bits) if b == 1]
        value = 0.0
        for u, v, w in g.edges(data="weight", default=1):
            if (u in cut) != (v in cut):
                value += w
        if value > best_value:
            best_value = value
            best_cut = cut
    return best_cut, best_value
