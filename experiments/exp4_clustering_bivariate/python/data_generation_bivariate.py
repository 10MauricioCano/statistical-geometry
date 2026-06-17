# ============================================================
# File: python/data_generation_bivariate.py
# Experiment: exp4_clustering_bivariate
# Description: Data generation pipeline for bivariate Gaussians (Zhang Ch.7)
# Reference: Zhang (2017) Ch.7, Sec.8.3
# ============================================================

import numpy as np


def generate_dataset_bivariate(
    mu_list: list[float],
    sigma_list: list[list[float]],
    t: int = 100,
    n: int = 30,
    rng: np.random.Generator | None = None,
) -> dict[str, np.ndarray]:
    """Generate one Monte Carlo dataset: K*t estimated (mu_hat, s1_hat, s2_hat) triples.

    Each cluster k has diagonal covariance diag(sigma1_k^2, sigma2_k^2) and
    the same mu_k for both dimensions. Zhang (2017) Ch.7 / Sec.8.3.
    """
    if rng is None:
        rng = np.random.default_rng()
    k = len(mu_list)
    assert len(sigma_list) == k
    assert all(len(s) == 2 and s[0] > 0 and s[1] > 0 for s in sigma_list)
    assert t > 1 and n > 1

    mu_hat_arr    = np.empty(k * t)
    sigma1_hat_arr = np.empty(k * t)
    sigma2_hat_arr = np.empty(k * t)
    cluster_arr   = np.empty(k * t, dtype=int)

    idx = 0
    for j in range(k):
        mu = mu_list[j]
        s1, s2 = sigma_list[j][0], sigma_list[j][1]
        for _ in range(t):
            dim1 = rng.normal(mu, s1, size=n)
            dim2 = rng.normal(mu, s2, size=n)
            mu_hat_arr[idx]     = (np.mean(dim1) + np.mean(dim2)) / 2
            sigma1_hat_arr[idx] = np.std(dim1, ddof=1)
            sigma2_hat_arr[idx] = np.std(dim2, ddof=1)
            cluster_arr[idx]    = j + 1          # 1-indexed to match R
            idx += 1

    return {
        "mu_hat":     mu_hat_arr,
        "sigma1_hat": sigma1_hat_arr,
        "sigma2_hat": sigma2_hat_arr,
        "cluster":    cluster_arr,
    }
