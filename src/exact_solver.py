
from __future__ import annotations

from typing import Tuple, List

import networkx as nx
import gurobipy as gp
from gurobipy import GRB


def maxcut_solver(g: nx.Graph) -> Tuple[List[int], float]:

    m = gp.Model("maxcut")


    x = {i: m.addVar(vtype=GRB.BINARY, name=f"x_{i}") for i in g.nodes()}


    y = {}
    for i, j, data in g.edges(data=True):
        w = data.get("weight", 1.0)
        y[i, j] = m.addVar(vtype=GRB.BINARY, name=f"y_{i}_{j}")

        m.addConstr(y[i, j] >= x[i] - x[j], name=f"c1_{i}_{j}")
        m.addConstr(y[i, j] >= x[j] - x[i], name=f"c2_{i}_{j}")
        # and y ≤ x_i + x_j, y ≤ 2 - x_i - x_j
        m.addConstr(y[i, j] <= x[i] + x[j], name=f"c3_{i}_{j}")
        m.addConstr(y[i, j] <= 2 - x[i] - x[j], name=f"c4_{i}_{j}")


    obj = gp.quicksum(data.get("weight", 1.0) * y[i, j] for i, j, data in g.edges(data=True))
    m.setObjective(obj, GRB.MAXIMIZE)


    m.Params.OutputFlag = 0


    m.optimize()


    cut = [i for i in g.nodes() if x[i].X > 0.5]
    value = m.ObjVal

    return cut, value
