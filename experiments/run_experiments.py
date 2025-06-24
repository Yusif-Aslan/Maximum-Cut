"""CLI script to run experiment sweeps."""

from __future__ import annotations

import argparse

from pathlib import Path

import yaml
import pandas as pd


from src import (
    generate_random_graph,
    maxcut_bruteforce,
    maxcut_solver,
    maxcut_goemans_williamson,
    maxcut_qaoa,
)


defaults = {
    "gw_trials": 5,
    "qaoa_depths": [1],
    "qaoa_steps": [50],
}


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg.setdefault("algorithms", {}).setdefault("gw_trials", [defaults["gw_trials"]])
    cfg.setdefault("algorithms", {}).setdefault("qaoa_depths", defaults["qaoa_depths"])
    cfg.setdefault("algorithms", {}).setdefault("qaoa_steps", defaults["qaoa_steps"])
    return cfg


def run(config_path: str) -> None:
    cfg = load_config(config_path)
    results = []
    for spec in cfg.get("graphs", []):
        g = generate_random_graph(spec["n"], spec.get("p", 0.5), tuple(spec.get("weight_range", [1, 10])))
        label = f"n{spec['n']}_p{spec.get('p',0.5)}"
        cut, val = maxcut_bruteforce(g)
        results.append({"alg": "bruteforce", "graph": label, "value": val})
        cut, val = maxcut_solver(g)
        results.append({"alg": "solver", "graph": label, "value": val})
        cut, val = maxcut_goemans_williamson(g, trials=cfg["algorithms"].get("gw_trials", 5))
        results.append({"alg": "gw", "graph": label, "value": val})
        for p in cfg["algorithms"].get("qaoa_depths", [1]):
            cut, val = maxcut_qaoa(g, p=p, steps=cfg["algorithms"].get("qaoa_steps", [50])[0])
            results.append({"alg": f"qaoa_p{p}", "graph": label, "value": val})
    df = pd.DataFrame(results)
    Path("results").mkdir(exist_ok=True)
    out_path = Path("results") / "results.json"
    df.to_json(out_path, orient="records", lines=True)
    print(f"Saved results to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run experiments")
    parser.add_argument("--config", type=str, default="experiments/config.yaml", help="YAML configuration file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.config)
