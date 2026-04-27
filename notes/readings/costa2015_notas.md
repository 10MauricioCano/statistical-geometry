# Notas de lectura — Costa, Santos, Strapasson (2015)

**Título**: Fisher information distance: A geometrical reading  
**Revista**: Discrete Applied Mathematics, 197, 59–69  
**Referencia**: `references/costa2015_fisher_distance.pdf`

---

## Idea central

Cada gaussiana univariada $(\mu, \sigma)$ es un punto en el semiplano superior.
La distancia "correcta" entre dos gaussianas no es la euclidiana sino la que
surge de la matriz de información de Fisher, que resulta ser hiperbólica.

## Fórmulas clave

**Métrica de Fisher** (univariada):
$$ds^2_F = \frac{d\mu^2 + 2d\sigma^2}{\sigma^2}$$

**Relación con semiplano de Poincaré**:
$$d_F((\mu_1,\sigma_1),(\mu_2,\sigma_2)) = \sqrt{2}\, d_H\!\left(\tfrac{\mu_1}{\sqrt{2}},\sigma_1\right),\left(\tfrac{\mu_2}{\sqrt{2}},\sigma_2\right)$$

**Distancia cerrada** (caso general, ec. 9):
$$d_F = \sqrt{2}\ln\!\left(\frac{\mathcal{F} + (\mu_1-\mu_2)^2 + 2(\sigma_1^2+\sigma_2^2)}{4\sigma_1\sigma_2}\right)$$

**Caso misma media** (ec. 10):
$$d_F((\mu,\sigma_1),(\mu,\sigma_2)) = \sqrt{2}|\ln(\sigma_2/\sigma_1)|$$

## Geometría

- La curvatura del semiplano de Fisher es constante $= -\frac{1}{2}$
- Las geodésicas son semirrectas verticales y semi-elipses con excentricidad $1/\sqrt{2}$
- Un "círculo de Fisher" es una elipse euclidiana con centro desplazado hacia abajo

## Extensión multivariada

- **Gaussianas redondas** ($\Sigma = \sigma^2 I$): semiplano $(p+1)$-dimensional, distancia cerrada (ec. 18)
- **Gaussianas diagonales**: métrica producto, distancia = suma de distancias univariadas (ec. 20)
- **Caso general**: no hay forma cerrada; se usan métodos numéricos o la KL como aproximación

## Conexión con KL

La divergencia KL simetrizada se aproxima a la distancia de Fisher para
distribuciones cercanas:
$$d_{KL}(P,Q) \approx d_F(P,Q) \quad \text{cuando } d_F \to 0$$

## Preguntas abiertas / para explorar

- [ ] ¿Por qué la curvatura es exactamente $-1/2$ y no otra constante?
- [ ] ¿Qué pasa con gaussianas correlacionadas (covarianza no diagonal)?
- [ ] Verificar numéricamente la relación KL ↔ Fisher en el semiplano
