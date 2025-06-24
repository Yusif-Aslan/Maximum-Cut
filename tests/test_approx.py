from src.data import generate_random_graph
from src.approx_gw import maxcut_goemans_williamson
from src.approx_qaoa import maxcut_qaoa


def test_gw_runs():
    g = generate_random_graph(4, 0.5)
    cut, val = maxcut_goemans_williamson(g, trials=1)
    assert isinstance(cut, list)
    assert isinstance(val, float)


def test_qaoa_runs():
    g = generate_random_graph(3, 0.5)
    cut, val = maxcut_qaoa(g, p=1, steps=1)
    assert isinstance(cut, list)
    assert isinstance(val, float)
