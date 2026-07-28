# ============================================================
# File: python/data_generation.py
# Experiment: exp3_clustering_univariate_k3
# Description: Data generation pipeline (Zhang Ch.7)
# Reference: Zhang (2017) Ch.7
# ============================================================

import numpy as np


def generate_dataset(
    mu_list: list[float],
    sigma_list: list[float],
    t: int = 100,
    n: int = 30,
    rng: np.random.Generator | None = None,
) -> dict[str, np.ndarray]:
    """Generate one Monte Carlo dataset: K*t estimated (mu_hat, sigma_hat) pairs.

    For each cluster k, draws t samples of size n from N(mu_k, sigma_k^2),
    estimates (mean, std) per sample, returns a dict of arrays.
    Zhang (2017) Ch.7
    """
    if rng is None:
        rng = np.random.default_rng()
    k = len(mu_list)
    assert len(sigma_list) == k
    assert all(s > 0 for s in sigma_list)
    assert t > 1 and n > 1

    mu_hat_arr    = np.empty(k * t)
    sigma_hat_arr = np.empty(k * t)
    cluster_arr   = np.empty(k * t, dtype=int)

    idx = 0
    for j in range(k):
        for _ in range(t):
            samp                = rng.normal(mu_list[j], sigma_list[j], size=n)
            mu_hat_arr[idx]     = np.mean(samp)
            sigma_hat_arr[idx]  = np.std(samp, ddof=1)
            cluster_arr[idx]    = j + 1          # 1-indexed to match R
            idx += 1

    return {"mu_hat": mu_hat_arr, "sigma_hat": sigma_hat_arr, "cluster": cluster_arr}
