# ============================================================
# File: R/clustering_bivariate.R
# Experiment: exp4_clustering_bivariate
# Description: K-Means and hierarchical clustering with bivariate Fisher-Rao / Euclidean
# Reference: Zhang (2017) Ch.8, Sec.8.3; Selim & Ismail (1984)
# ============================================================
# Requires: fisher_rao_bivariate() and generate_dataset_bivariate() already sourced.

# --- Vectorized bivariate Fisher-Rao (inlined for performance) ---------------

fr_bivariate_all_pairs <- function(mu, s1, s2) {
  # Pairwise Fisher-Rao distances for n bivariate Gaussian parameter triples.
  # Inlines Zhang (2017) eq. 4.12/8.2 for vectorized computation over all pairs.
  n     <- length(mu)
  mat   <- matrix(0.0, n, n)
  upper <- which(upper.tri(mat), arr.ind = TRUE)

  mu_i <- mu[upper[, 1L]]; s1_i <- s1[upper[, 1L]]; s2_i <- s2[upper[, 1L]]
  mu_j <- mu[upper[, 2L]]; s1_j <- s1[upper[, 2L]]; s2_j <- s2[upper[, 2L]]

  dm <- (mu_i - mu_j) / sqrt(2)

  A1 <- sqrt(dm^2 + (s1_i + s1_j)^2); B1 <- sqrt(dm^2 + (s1_i - s1_j)^2)
  t1 <- log((A1 + B1)^2 / (4 * s1_i * s1_j))

  A2 <- sqrt(dm^2 + (s2_i + s2_j)^2); B2 <- sqrt(dm^2 + (s2_i - s2_j)^2)
  t2 <- log((A2 + B2)^2 / (4 * s2_i * s2_j))

  mat[upper] <- sqrt(2 * (t1^2 + t2^2))
  mat + t(mat)
}

fr_bivariate_to_center <- function(mu, s1, s2, mu_c, s1_c, s2_c) {
  # Distances from all n points to one center (mu_c, s1_c, s2_c). Zhang eq. 4.12/8.2.
  dm <- (mu - mu_c) / sqrt(2)

  A1 <- sqrt(dm^2 + (s1 + s1_c)^2); B1 <- sqrt(dm^2 + (s1 - s1_c)^2)
  t1 <- log((A1 + B1)^2 / (4 * s1 * s1_c))

  A2 <- sqrt(dm^2 + (s2 + s2_c)^2); B2 <- sqrt(dm^2 + (s2 - s2_c)^2)
  t2 <- log((A2 + B2)^2 / (4 * s2 * s2_c))

  sqrt(2 * (t1^2 + t2^2))
}

euclidean_dist_matrix_3d <- function(params) {
  as.matrix(dist(params[, c("mu_hat", "sigma1_hat", "sigma2_hat")], method = "euclidean"))
}

# --- K-Means with bivariate Fisher-Rao ---------------------------------------

kmeans_fr_bivariate <- function(params, k, max_iter = 100L, n_init = 10L) {
  # Assignment uses bivariate Fisher-Rao distance; centroid update uses arithmetic mean.
  # Best of n_init random restarts (lowest within-cluster sum of squared distances).
  n  <- nrow(params)
  mu <- params$mu_hat
  s1 <- params$sigma1_hat
  s2 <- params$sigma2_hat

  best_labels  <- NULL
  best_inertia <- Inf

  for (init in seq_len(n_init)) {
    idx <- sample.int(n, k)
    cmu <- mu[idx]; cs1 <- s1[idx]; cs2 <- s2[idx]
    labels <- integer(n)
    dists  <- matrix(NA_real_, n, k)

    for (iter in seq_len(max_iter)) {
      for (cl in seq_len(k)) {
        dists[, cl] <- fr_bivariate_to_center(mu, s1, s2, cmu[cl], cs1[cl], cs2[cl])
      }
      new_labels <- max.col(-dists, ties.method = "first")

      if (identical(new_labels, labels)) {
        labels <- new_labels
        break
      }
      labels <- new_labels

      for (cl in seq_len(k)) {
        mask <- labels == cl
        if (any(mask)) {
          cmu[cl] <- mean(mu[mask])
          cs1[cl] <- mean(s1[mask])
          cs2[cl] <- mean(s2[mask])
        }
      }
    }

    inertia <- sum(dists[cbind(seq_len(n), labels)]^2L)
    if (inertia < best_inertia) {
      best_inertia <- inertia
      best_labels  <- labels
    }
  }

  best_labels
}

# --- Hierarchical clustering -------------------------------------------------

hclust_custom <- function(dist_matrix, k, method = "complete") {
  hc <- hclust(as.dist(dist_matrix), method = method)
  cutree(hc, k = k)
}

# --- Accuracy with optimal label matching (k=3: all 3! permutations) ---------

match_accuracy_k3 <- function(true_labels, pred_labels) {
  best <- 0
  for (p1 in 1:3) {
    for (p2 in setdiff(1:3, p1)) {
      p3      <- setdiff(1:3, c(p1, p2))
      mapping <- c(p1, p2, p3)
      acc     <- mean(mapping[pred_labels] == true_labels)
      if (acc > best) best <- acc
    }
  }
  best
}

# --- Monte Carlo replication driver ------------------------------------------

run_replications <- function(mu_list, sigma_list, k = 3L, t = 100L, n = 30L,
                              n_rep = 100L, hclust_method = "complete") {
  results <- vector("list", n_rep)

  for (r in seq_len(n_rep)) {
    dat         <- generate_dataset_bivariate(mu_list, sigma_list, t = t, n = n)
    true_labels <- dat$cluster

    fr_dist <- fr_bivariate_all_pairs(dat$mu_hat, dat$sigma1_hat, dat$sigma2_hat)
    eu_dist <- euclidean_dist_matrix_3d(dat)

    km_fr <- kmeans_fr_bivariate(dat, k = k)
    km_eu <- kmeans(dat[, c("mu_hat", "sigma1_hat", "sigma2_hat")], centers = k,
                    nstart = 10L)$cluster
    hc_fr <- hclust_custom(fr_dist, k = k, method = hclust_method)
    hc_eu <- hclust_custom(eu_dist, k = k, method = hclust_method)

    results[[r]] <- data.frame(
      replication = r,
      km_fr       = match_accuracy_k3(true_labels, km_fr),
      km_eu       = match_accuracy_k3(true_labels, km_eu),
      hc_fr       = match_accuracy_k3(true_labels, hc_fr),
      hc_eu       = match_accuracy_k3(true_labels, hc_eu)
    )
  }

  do.call(rbind, results)
}
