"""Solver-based exact algorithm for Maximum Cut using cvxpy."""

from __future__ import annotations

from typing import Tuple, List

import cvxpy as cp
import networkx as nx
import numpy as np


def maxcut_solver(g: nx.Graph) -> Tuple[List[int], float]:
    """Solve the max-cut problem using an integer program."""
    n = g.number_of_nodes()
    x = cp.Variable(n, boolean=True)
    W = nx.to_numpy_array(g, weight="weight")
    objective = cp.sum(cp.multiply(W, cp.abs(cp.reshape(x, (n, 1)) - x))) / 2
    problem = cp.Problem(cp.Maximize(objective))
    problem.solve()
    cut = [i for i, val in enumerate(x.value) if val > 0.5]
    return cut, problem.value
