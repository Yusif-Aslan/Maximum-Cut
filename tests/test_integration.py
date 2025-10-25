from experiments.run_experiments import run


def test_run_small_experiment(tmp_path):
    # create minimal config
    config = tmp_path / "config.yaml"
    config.write_text(
        """
        graphs:
          - n: 3
            p: 0.5
            weight_range: [1, 2]
        algorithms:
          gw_trials: 1
          qaoa_depths: [1]
          qaoa_steps: [1]
        """
    )
    run(str(config))
