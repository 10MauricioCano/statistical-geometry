# Exp 1 — Cálculo y verificación de distancias estadísticas

## Objetivo

Implementar y verificar las tres distancias estadísticas que se usan
a lo largo del proyecto, antes de aplicarlas a clustering o clasificación.

## Distancias a implementar

### 1. Fisher-Rao univariada (Costa et al., 2015, eq. 9)

Entre dos gaussianas $P = (\mu_1, \sigma_1)$ y $Q = (\mu_2, \sigma_2)$:

$$
d_F(P, Q) = \sqrt{2} \ln \left(
  \frac{\mathcal{F}(P,Q) + (\mu_1 - \mu_2)^2 + 2(\sigma_1^2 + \sigma_2^2)}{4\sigma_1\sigma_2}
\right)
$$

donde $\mathcal{F}(P,Q) = \sqrt{[(\mu_1-\mu_2)^2 + 2(\sigma_1-\sigma_2)^2][(\mu_1-\mu_2)^2 + 2(\sigma_1+\sigma_2)^2]}$

Caso especial (misma media): $d_F = \sqrt{2} |\ln(\sigma_2/\sigma_1)|$

### 2. Fisher-Rao bivariada (Zhang, 2017, eq. 8.2)

Para gaussianas bivariadas independientes $(\mu, \sigma_1, \sigma_2)$:

$$
d_F(\theta_1, \theta_2) = \sqrt{2 \sum_{i=1}^{2} \left( \ln \frac{\| (\frac{\mu_{1}}{\sqrt{2}}, \sigma_{1i}) - (\frac{\mu_{2}}{\sqrt{2}}, -\sigma_{2i}) \| + \| (\frac{\mu_{1}}{\sqrt{2}}, \sigma_{1i}) - (\frac{\mu_{2}}{\sqrt{2}}, \sigma_{2i}) \|}{\| (\frac{\mu_{1}}{\sqrt{2}}, \sigma_{1i}) - (\frac{\mu_{2}}{\sqrt{2}}, -\sigma_{2i}) \| - \| (\frac{\mu_{1}}{\sqrt{2}}, \sigma_{1i}) - (\frac{\mu_{2}}{\sqrt{2}}, \sigma_{2i}) \|} \right)^2}
$$

### 3. Hellinger para distribuciones discretas (Zhang, 2017, eq. 5.1)

Entre dos vectores de probabilidad $p = (p_0, ..., p_k)$ y $q = (q_0, ..., q_k)$:

$$
d_H(p, q) = \sqrt{\frac{1}{2} \sum_{j=0}^{k} (\sqrt{p_j} - \sqrt{q_j})^2}
$$

## Pruebas de sanidad esperadas

| Par de distribuciones | Comportamiento esperado |
|----------------------|------------------------|
| $P = Q$ | $d = 0$ |
| $P = (0, 1)$ vs $Q = (0, 2)$ | $d_F = \sqrt{2} \ln 2 \approx 0.98$ |
| Distribuciones muy separadas | $d \gg 0$ |
| Simetría: $d(P,Q) = d(Q,P)$ | Siempre |
| Cercanía al horizonte $\sigma \to 0$ | $d \to \infty$ |

## Archivos

- `R/distances.R` — funciones de distancia en R
- `python/distances.py` — funciones de distancia en Python
- `notebooks/` — exploración visual comparando las tres distancias
- `results/` — tablas de verificación

## Referencias

- Costa et al. (2015), ecuaciones (8)–(11)
- Zhang (2017), capítulos 4–5
