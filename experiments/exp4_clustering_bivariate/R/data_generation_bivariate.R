# ============================================================
# File: R/data_generation_bivariate.R
# Experiment: exp4_clustering_bivariate
# Description: Data generation pipeline for bivariate Gaussians (Zhang Ch.7)
# Reference: Zhang (2017) Ch.7, Sec.8.3
# ============================================================

generate_dataset_bivariate <- function(mu_list, sigma_list, t = 100L, n = 30L) {
  # Each cluster k has params (mu_k, c(sigma1_k, sigma2_k)).
  # Covariance is diagonal: Sigma_k = diag(sigma1_k^2, sigma2_k^2), same mu for both dims.
  # Draws t samples of size n, estimates (mu_hat, sigma1_hat, sigma2_hat) per sample.
  # Returns labeled K*t-row data frame. Zhang (2017) Ch.7 / Sec.8.3.
  k <- length(mu_list)
  stopifnot(
    length(sigma_list) == k,
    all(sapply(sigma_list, length) == 2),
    all(sapply(sigma_list, function(s) all(s > 0))),
    t > 1L, n > 1L
  )

  rows <- vector("list", k * t)
  idx  <- 1L
  for (j in seq_len(k)) {
    mu <- mu_list[[j]]
    s1 <- sigma_list[[j]][1]
    s2 <- sigma_list[[j]][2]
    for (i in seq_len(t)) {
      dim1 <- rnorm(n, mean = mu, sd = s1)
      dim2 <- rnorm(n, mean = mu, sd = s2)
      rows[[idx]] <- data.frame(
        mu_hat     = (mean(dim1) + mean(dim2)) / 2,
        sigma1_hat = sd(dim1),
        sigma2_hat = sd(dim2),
        cluster    = j
      )
      idx <- idx + 1L
    }
  }
  do.call(rbind, rows)
}
