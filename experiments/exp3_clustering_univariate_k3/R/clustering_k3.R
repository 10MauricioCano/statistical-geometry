# ============================================================
# File: R/clustering_k3.R
# Experiment: exp3_clustering_univariate_k3
# Description: K-Means and hierarchical clustering with Fisher-Rao / Euclidean
# Reference: Zhang (2017) Ch.8; Selim & Ismail (1984)
# ============================================================
# Requires: fisher_rao_univariate() and generate_dataset() already sourced.

# --- Distance matrices -------------------------------------------------------

fisher_rao_dist_matrix <- function(params) {
  n     <- nrow(params)
  mat   <- matrix(0.0, n, n)
  upper <- which(upper.tri(mat), arr.ind = TRUE)
  d <- mapply(
    fisher_rao_univariate,
    params$mu_hat[upper[, 1L]], params$sigma_hat[upper[, 1L]],
    params$mu_hat[upper[, 2L]], params$sigma_hat[upper[, 2L]]
  )
  mat[upper] <- d
  mat + t(mat)
}

euclidean_dist_matrix <- function(params) {
  as.matrix(dist(params[, c("mu_hat", "sigma_hat")], method = "euclidean"))
}

# --- K-Means with Fisher-Rao distance ----------------------------------------

kmeans_fr <- function(params, k, max_iter = 100L, n_init = 10L) {
  # Assignment uses Fisher-Rao distance; centroid update uses arithmetic mean
  # of (mu_hat, sigma_hat) — Fréchet mean approximation for well-separated clusters.
  # Best of n_init random restarts (lowest within-cluster sum of squared distances).
  n            <- nrow(params)
  best_labels  <- NULL
  best_inertia <- Inf

  for (init in seq_len(n_init)) {
    centers <- params[sample.int(n, k), c("mu_hat", "sigma_hat"), drop = FALSE]
    rownames(centers) <- NULL
    labels  <- integer(n)
    dists   <- matrix(NA_real_, n, k)

    for (iter in seq_len(max_iter)) {
      for (cl in seq_len(k)) {
        dists[, cl] <- mapply(
          fisher_rao_univariate,
          params$mu_hat, params$sigma_hat,
          centers$mu_hat[cl], centers$sigma_hat[cl]
        )
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
          centers$mu_hat[cl]    <- mean(params$mu_hat[mask])
          centers$sigma_hat[cl] <- mean(params$sigma_hat[mask])
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
  # Tries all 6 permutations of cluster labels {1,2,3} and returns best accuracy.
  best <- 0
  for (p1 in 1:3) {
    for (p2 in setdiff(1:3, p1)) {
      p3      <- setdiff(1:3, c(p1, p2))
      mapping <- c(p1, p2, p3)          # mapping[pred_label] → remapped label
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
    dat         <- generate_dataset(mu_list, sigma_list, t = t, n = n)
    true_labels <- dat$cluster

    fr_dist <- fisher_rao_dist_matrix(dat)
    eu_dist <- euclidean_dist_matrix(dat)

    km_fr <- kmeans_fr(dat, k = k)
    km_eu <- kmeans(dat[, c("mu_hat", "sigma_hat")], centers = k,
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
