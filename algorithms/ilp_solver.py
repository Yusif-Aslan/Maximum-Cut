try:
    import pulp
except Exception:
    pulp = None

try:
    from . import brute_force
except ImportError:  # allow running as a script
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import brute_force


def max_cut_ilp(graph):
    """Solve Max-Cut via MILP using pulp if available."""
    if pulp is None:
        # Fallback to brute force if pulp is missing
        return brute_force.max_cut_brute_force(graph)

    prob = pulp.LpProblem("max_cut", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(graph.num_vertices)]

    y_vars = {}
    for u, v, w in graph.all_edges():
        y = pulp.LpVariable(f"y_{u}_{v}", cat="Binary")
        prob += y >= x[u] - x[v]
        prob += y >= x[v] - x[u]
        prob += y <= x[u] + x[v]
        prob += y <= 2 - x[u] - x[v]
        y_vars[(u, v)] = (y, w)

    prob += pulp.lpSum(w * y for (y, w) in y_vars.values())
    prob.solve(pulp.PulpSolverDefault(msg=False))

    value = pulp.value(prob.objective)
    bits = [int(var.varValue) for var in x]
    return value, bits


if __name__ == "__main__":
    from graphs import Graph

    g = Graph(4)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 0, 1)
    val, bits = max_cut_ilp(g)
    print("Cut value:", val)
    print("Partition:", bits)
