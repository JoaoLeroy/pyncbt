# NCbT overview

Non-iterative Correlation-based Tuning (NCbT) is a **direct data-driven control method** that computes fixed-structure controller parameters using a single batch of input–output data.

---

## Core idea

Instead of explicitly identifying the plant model, NCbT:

- Approximates the model-reference objective
- Uses a correlation-based criterion
- Employs instrumental variables to handle noise
- Solves a single least-squares problem

---

## Advantages

- No plant identification step
- No iterative optimization
- Works with open-loop data
- Transparent bias–variance trade-offs

---

## Mathematical summary

NCbT minimizes a correlation criterion that approximates the model-reference cost:

\[
J_{\mathrm{MR}} = \left\| M - \frac{KG}{1+KG} \right\|_2^2
\]

via an implementable approximation using weighting filters and instruments.

Refer to the original paper by Van Heusden et al. (2011) for theoretical details.