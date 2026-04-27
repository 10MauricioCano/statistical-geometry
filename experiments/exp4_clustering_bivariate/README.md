# Exp 4 — Clustering bivariado k=3

## Objetivo

Extender el clustering al caso bivariado: gaussianas con espacio de
parámetros tridimensional $(\mu, \sigma_1, \sigma_2)$.

## Configuración (Zhang, 2017, Sección 8.3)

- k = 3 clusters, espacio 3D
- Parámetros: $(\mu, \sigma_1, \sigma_2) = (1,1,2), (1.5, 1.5, 2.5), (2, 2, 3)$
- n = 30, t = 100, 100 réplicas

## Notas técnicas

La distancia Fisher-Rao bivariada (ecuación 8.2 de Zhang) es una suma
de dos distancias hiperbólicas univariadas. Requiere la implementación
de exp1 como dependencia.

## Archivos

- `R/clustering_bivariate.R`
- `python/clustering_bivariate.py`
- `results/`
