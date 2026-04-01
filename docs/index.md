<p align="center">
  <img src="docs/img/pyncbt-logo.png" alt="pyncbt logo" width="50%">
</p>

# pyncbt

**pyncbt** is an open-source Python library for **Non-iterative Correlation-based Tuning (NCbT)**, a data-driven controller design method for discrete-time SISO LTI systems.

The library enables direct computation of fixed-structure controllers from input–output data, without explicit plant identification or iterative optimization.

---

## Key features

- Non-iterative data-driven controller tuning
- Support for open-loop and closed-loop datasets
- Instrumental-variable-based noise rejection
- Reproducible examples and benchmarks
- Designed for research, teaching, and experimental setups

---

## Typical workflow

1. Collect input–output data (simulation or experiment)
2. Choose a reference model and controller structure
3. Estimate weighting filter and instruments
4. Compute controller parameters via least squares

---

## When to use pyncbt?

- Rapid controller prototyping from experimental data
- Teaching data-driven control concepts
- Reproducible research and benchmarking
- Virtual or physical laboratory setups
