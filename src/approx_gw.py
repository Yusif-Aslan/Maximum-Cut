"""Goemans-Williamson approximation algorithm."""

from __future__ import annotations

from typing import Tuple, List

import numpy as np
import networkx as nx


def _cut_value(g: nx.Graph, subset: List[int]) -> float:
    value = 0.0
    S = set(subset)
    for u, v, w in g.edges(data="weight", default=1):
        if (u in S) != (v in S):
            value += w
    return value


def maxcut_goemans_williamson(g: nx.Graph, trials: int = 10) -> Tuple[List[int], float]:
    """Simplified GW rounding with random hyperplanes."""
    best_cut = []
    best_value = float("-inf")
    n = g.number_of_nodes()
    for _ in range(trials):
        rnd_vec = np.random.randn(n)
        subset = [i for i, v in enumerate(rnd_vec) if v > 0]
        val = _cut_value(g, subset)
        if val > best_value:
            best_value = val
            best_cut = subset
    return best_cut, best_value
