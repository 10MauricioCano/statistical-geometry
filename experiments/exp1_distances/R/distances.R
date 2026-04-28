# ============================================================
# File: R/distances.R
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4-5; Costa et al. (2015)
# ============================================================


fisher_rao_univariate <- function(mu1, sigma1, mu2, sigma2) {
  # Fisher-Rao geodesic distance between N(mu1, sigma1^2) and N(mu2, sigma2^2).
  # Zhang (2017) eq. 4.11; Costa et al. (2015) eq. 9
  stopifnot(sigma1 > 0, sigma2 > 0)
  d_mu  <- mu1 - mu2
  F_val <- sqrt((d_mu^2 + 2 * (sigma1 - sigma2)^2) *
                (d_mu^2 + 2 * (sigma1 + sigma2)^2))
  sqrt(2) * log((F_val + d_mu^2 + 2 * (sigma1^2 + sigma2^2)) / (4 * sigma1 * sigma2))
}


fisher_rao_bivariate <- function(mu1, sigma1, mu2, sigma2) {
  # Fisher-Rao distance for bivariate Gaussians with diagonal covariance.
  # theta_k = (mu_k, c(sigma_k1, sigma_k2)); mu_k is a scalar (same for both dims).
  # Zhang (2017) eq. 4.12 / 8.2
  #
  # Numerically stable form: log((A+B)^2 / (4*s1*s2))
  # derived from A^2 - B^2 = 4*sigma1[i]*sigma2[i], avoiding cancellation when A≈B.
  stopifnot(length(sigma1) == 2, length(sigma2) == 2,
            all(sigma1 > 0), all(sigma2 > 0))
  delta_mu <- (mu1 - mu2) / sqrt(2)
  terms <- sapply(1:2, function(i) {
    A_i <- sqrt(delta_mu^2 + (sigma1[i] + sigma2[i])^2)
    B_i <- sqrt(delta_mu^2 + (sigma1[i] - sigma2[i])^2)
    log((A_i + B_i)^2 / (4 * sigma1[i] * sigma2[i]))
  })
  sqrt(2 * sum(terms^2))
}


hellinger_discrete <- function(p, q) {
  # Hellinger distance between two discrete probability distributions.
  # Zhang (2017) eq. 5.1
  stopifnot(length(p) == length(q), all(p >= 0), all(q >= 0))
  p <- p / sum(p)
  q <- q / sum(q)
  sqrt(0.5 * sum((sqrt(p) - sqrt(q))^2))
}
