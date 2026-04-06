<p align="center">
  <img src="img/pyncbt-logo.png" width="50%" alt="pyncbt logo">
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
4. Compute the controller parameters

---

## When to use pyncbt?

- Rapid controller prototyping from experimental data
- Teaching data-driven control concepts
- Reproducible research and benchmarking
- Virtual or physical laboratory setups

# Installation and requirements

## Requirements

- Python ≥ 3.9
- NumPy
- SciPy
- Matplotlib (optional, for visualization)

## Install via pip

```console
pip install pyncbt
```
