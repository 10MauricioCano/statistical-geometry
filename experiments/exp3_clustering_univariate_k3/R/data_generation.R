# ============================================================
# File: R/data_generation.R
# Experiment: exp3_clustering_univariate_k3
# Description: Data generation pipeline (Zhang Ch.7)
# Reference: Zhang (2017) Ch.7
# ============================================================

generate_dataset <- function(mu_list, sigma_list, t = 100L, n = 30L) {
  # For each cluster k, draws t samples of size n from N(mu_k, sigma_k^2),
  # estimates (mu_hat, sigma_hat) per sample, returns labeled K*t-row data frame.
  k <- length(mu_list)
  stopifnot(
    length(sigma_list) == k,
    all(unlist(sigma_list) > 0),
    t > 1L, n > 1L
  )

  rows <- vector("list", k * t)
  idx  <- 1L
  for (j in seq_len(k)) {
    for (i in seq_len(t)) {
      samp        <- rnorm(n, mean = mu_list[[j]], sd = sigma_list[[j]])
      rows[[idx]] <- data.frame(
        mu_hat    = mean(samp),
        sigma_hat = sd(samp),
        cluster   = j
      )
      idx <- idx + 1L
    }
  }
  do.call(rbind, rows)
}
