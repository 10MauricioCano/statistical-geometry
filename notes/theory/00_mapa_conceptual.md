# Mapa conceptual del proyecto

## La pregunta unificadora

> ¿Cómo comparar distribuciones de probabilidad de manera inteligente?

Los tres documentos responden esto desde ángulos distintos:

- **Costa et al. (2015)**: usando la geometría natural del espacio de parámetros
- **Zhang (2017)**: y cuando usas esa geometría, el ML mejora
- **Fraiman et al. (2023)**: y si las distribuciones son elípticas, basta con
  pocas proyecciones para compararlas

---

## Conceptos clave y su orden de introducción

1. Distribuciones de probabilidad como puntos en un espacio de parámetros
2. La distancia euclidiana no es apropiada → necesitamos otra métrica
3. Matriz de información de Fisher → métrica riemanniana
4. Conexión con geometría hiperbólica → semiplano de Poincaré
5. Variedad estadística = espacio de parámetros + métrica de Fisher
6. Geodésicas = caminos más cortos entre distribuciones
7. Divergencia de Kullback-Leibler y su relación con Fisher
8. Centroides en variedades (promedio de distribuciones)
9. Clustering en variedades: k-means y jerárquico con métrica estadística
10. Distribuciones elípticas como generalización de gaussianas
11. Teorema de Cramér-Wold clásico → versión para elípticas
12. Aplicaciones: tests estadísticos y clasificación por proyecciones

---

## Terminología esencial

| Término | Definición breve |
|---------|-----------------|
| Variedad estadística | Espacio de parámetros de una familia de distribuciones, equipado con la métrica de Fisher |
| Métrica de Fisher | Forma cuadrática definida por la matriz de información de Fisher; generaliza la distancia entre distribuciones |
| Geodésica | Curva de longitud mínima entre dos puntos en una variedad; análogo de "línea recta" en geometría curva |
| Semiplano de Poincaré | Modelo de geometría hiperbólica; es exactamente el espacio de gaussianas univariadas con métrica de Fisher (escalado por √2) |
| Distancia Fisher-Rao | La distancia asociada a la métrica de Fisher; mide disimilaridad entre distribuciones de manera estadísticamente correcta |
| Divergencia KL | Medida asimétrica de disimilaridad; aproxima la distancia de Fisher para distribuciones cercanas |
| Distancia de Hellinger | Distancia estadística para distribuciones discretas; usada en clustering de Poisson |
| Distribución elíptica | Familia de distribuciones cuya función característica tiene forma $e^{i\mu\cdot\xi}\psi(\xi^\top\Sigma\xi)$; incluye gaussianas, Cauchy, Student |
| Teorema de Cramér-Wold | Una distribución multivariada queda determinada por sus proyecciones unidimensionales; versión para elípticas: basta con $(d^2+d)/2$ proyecciones |
| sm-uniqueness set | Conjunto de vectores que determina de forma única una matriz simétrica; mínimo de $(d^2+d)/2$ elementos |

---

## Conexiones entre documentos

```
Costa et al. (2015)
  └─ Define: métrica Fisher, semiplano, geodésicas, distancia cerrada
       │
       ▼
Zhang (2017)
  └─ Usa: distancias de Costa et al. para clustering
  └─ Extiende: a distribuciones discretas (Hellinger)
  └─ Propone: clasificación en variedades (sin implementar)
       │
       ▼
Fraiman et al. (2023)
  └─ Generaliza: de gaussianas a distribuciones elípticas
  └─ Reduce: el problema multivariado a proyecciones 1D
  └─ Aplica: a tests estadísticos y clasificación binaria
```
