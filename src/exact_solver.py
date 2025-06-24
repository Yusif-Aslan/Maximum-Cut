"""Solver-based exact algorithm for Maximum Cut using Gurobi."""
from __future__ import annotations

from typing import Tuple, List

import networkx as nx
import gurobipy as gp
from gurobipy import GRB


def maxcut_solver(g: nx.Graph) -> Tuple[List[int], float]:
    """
    Solve the max-cut problem by formulating it as a mixed-integer
    linear program in Gurobi.

    Returns:
        cut: List of node indices on one side of the cut.
        value: Total weight of the cut.
    """
    # Create model
    m = gp.Model("maxcut")

    # Binary decision variables x_i ∈ {0,1}, one per node
    x = {i: m.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in g.nodes()}

    # For each edge (i,j), binary y_{ij}=1 if i and j are separated
    y = {}
    for i, j, data in g.edges(data=True):
        w = data.get("weight", 1.0)
        y[i, j] = m.addVar(vtype=GRB.BINARY, name=f"y_{i}_{j}")
        # McCormick constraints: y ≥ x_i - x_j, y ≥ x_j - x_i
        m.addConstr(y[i, j] >= x[i] - x[j], name=f"c1_{i}_{j}")
        m.addConstr(y[i, j] >= x[j] - x[i], name=f"c2_{i}_{j}")
        # and y ≤ x_i + x_j, y ≤ 2 - x_i - x_j
        m.addConstr(y[i, j] <= x[i] + x[j], name=f"c3_{i}_{j}")
        m.addConstr(y[i, j] <= 2 - x[i] - x[j], name=f"c4_{i}_{j}")

    # Set objective: maximize sum_{(i,j)} w_{ij} * y_{ij}
    obj = gp.quicksum(data.get("weight", 1.0) * y[i, j] for i, j, data in g.edges(data=True))
    m.setObjective(obj, GRB.MAXIMIZE)

    # Silence Gurobi output if you want:
    m.Params.OutputFlag = 0

    # Optimize
    m.optimize()

    # Extract solution
    cut = [i for i in g.nodes() if x[i].X > 0.5]
    value = m.ObjVal

    return cut, value
