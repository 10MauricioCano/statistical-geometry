# ============================================================
# File: python/distances.py
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4-5; Costa et al. (2015)
# ============================================================

import numpy as np


def fisher_rao_univariate(mu1: float, sigma1: float, mu2: float, sigma2: float) -> float:
    """Fisher-Rao geodesic distance between N(mu1, sigma1^2) and N(mu2, sigma2^2).

    Zhang (2017) eq. 4.11; Costa et al. (2015) eq. 9
    """
    assert sigma1 > 0 and sigma2 > 0, "sigma must be positive"
    d_mu = mu1 - mu2
    F = np.sqrt(
        (d_mu**2 + 2 * (sigma1 - sigma2)**2) *
        (d_mu**2 + 2 * (sigma1 + sigma2)**2)
    )
    return float(
        np.sqrt(2) * np.log((F + d_mu**2 + 2 * (sigma1**2 + sigma2**2)) / (4 * sigma1 * sigma2))
    )


def fisher_rao_bivariate(
    mu1: float, sigma1: np.ndarray,
    mu2: float, sigma2: np.ndarray,
) -> float:
    """Fisher-Rao distance for bivariate Gaussians with diagonal covariance.

    theta_k = (mu_k, [sigma_k1, sigma_k2]); mu_k is a scalar (same for both dims).
    Numerically stable form: log((A+B)^2 / (4*s1*s2)),
    derived from A^2 - B^2 = 4*sigma1[i]*sigma2[i], avoiding cancellation when A≈B.
    Zhang (2017) eq. 4.12 / 8.2
    """
    sigma1 = np.asarray(sigma1, dtype=float)
    sigma2 = np.asarray(sigma2, dtype=float)
    assert sigma1.shape == (2,) and sigma2.shape == (2,), "sigma must be length-2 arrays"
    assert np.all(sigma1 > 0) and np.all(sigma2 > 0), "sigma must be positive"

    delta_mu = (mu1 - mu2) / np.sqrt(2)
    terms = np.zeros(2)
    for i in range(2):
        A_i = np.sqrt(delta_mu**2 + (sigma1[i] + sigma2[i])**2)
        B_i = np.sqrt(delta_mu**2 + (sigma1[i] - sigma2[i])**2)
        terms[i] = np.log((A_i + B_i)**2 / (4 * sigma1[i] * sigma2[i]))
    return float(np.sqrt(2 * np.sum(terms**2)))


def hellinger_discrete(p: np.ndarray, q: np.ndarray) -> float:
    """Hellinger distance between two discrete probability distributions.

    Zhang (2017) eq. 5.1
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    assert len(p) == len(q), "p and q must have the same length"
    assert np.all(p >= 0) and np.all(q >= 0), "probabilities must be non-negative"
    p = p / p.sum()
    q = q / q.sum()
    return float(np.sqrt(0.5 * np.sum((np.sqrt(p) - np.sqrt(q))**2)))
