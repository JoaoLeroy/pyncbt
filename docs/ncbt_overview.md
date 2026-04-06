# NCbT Overview

**Non-iterative Correlation-based Tuning (NCbT)** is a direct data-driven control method that tunes fixed‑structure controllers from a single batch of input–output data. It requires no explicit plant model and no iterative optimization.

## Problem setting

In model reference control, the goal is to make the closed‑loop system behave like a desired reference model \( M(q^{-1}) \). The ideal cost is

\[
J_{\mathrm{MR}}(\rho) = \left\| M - \frac{K(\rho)G}{1+K(\rho)G} \right\|_2^2,
\]

where \( G \) is the unknown plant and \( K(\rho) \) is a fixed‑structure controller linearly parameterized by \( \rho \). Direct minimization of \( J_{\mathrm{MR}} \) is non‑convex and requires a model of \( G \). NCbT avoids these difficulties through a correlation‑based approximation.

## Correlation approximation

NCbT exploits the approximation

\[
\frac{1}{1+K(\rho)G} \approx 1-M,
\]

which holds near the optimal solution. This leads to the **approximate error**:

\[
\varepsilon(t,\rho) = M u(t) - (1-M) K(\rho) y(t).
\]

The key idea is to choose \( \rho \) so that \( \varepsilon(t,\rho) \) becomes **uncorrelated** with external instrumental signals, ensuring asymptotic noise rejection. The resulting estimator is solved via a single least‑squares problem.

## Weighting filter \( W \)

To improve conditioning and efficiency, NCbT introduces a filter \( W \) that “whitens” the input spectrum. In the frequency domain:

\[
W(e^{-j\omega}) = \frac{1 - M(e^{-j\omega})}{\Phi_u(\omega)},
\]

where \( \Phi_u(\omega) \) is the power spectral density of \( u(t) \). In discrete time, \( W \) is implemented using spectral factorization (e.g., an AR model of \( u \)).

## Instrumental variables and least‑squares solution

Let \( u_W = W * u \) be the filtered input. Instruments are built by stacking a symmetric window of \( 2\ell+1 \) lags:

\[
\zeta_w(t) = \big[u_W(t+\ell),\, u_W(t+\ell-1),\, \dots,\, u_W(t-\ell)\big]^T.
\]

Regressors are defined as

\[
\phi(t) = \beta(q^{-1})\big[(1-M) y(t)\big],
\]

where \( \beta(q^{-1}) \) is a vector of stable basis functions that define the controller structure (e.g., integrator, delays, FIR). The independent term is \( u_M = M u \).

After truncating the signals to avoid boundary effects, the sample matrices are

\[
Q = \frac{1}{N}\sum_{t} \zeta_w(t) \phi^T(t), \qquad
Z = \frac{1}{N}\sum_{t} \zeta_w(t) u_M(t).
\]

The controller parameters are obtained by solving the least‑squares problem:

\[
\hat{\rho} = (Q^T Q)^{-1} Q^T Z.
\]

## Hyperparameter choices

- **Window length \( l \)** – controls the bias‑variance trade‑off. Typical values: 10–50. Larger \( l \) reduces variance but may increase bias and degrade conditioning.
- **Basis \( \beta \)** – must be stable and capture the expected controller dynamics.
- **Reference model \( M \)** – stable, strictly proper.

