<p align="center">
  <img src="https://raw.githubusercontent.com/JoaoLeroy/pyncbt/main/docs/img/pyncbt-logo.png" width="50%" alt="pyncbt logo">
</p>

<h1 align="center">pyncbt · Non-iterative Correlation-based Tuning (NCbT) in Python</h1>

<p align="center">
  <a href="https://pypi.org/project/pyncbt/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pyncbt.svg"></a>
  <a href="https://pypi.org/project/pyncbt/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/pyncbt.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://pypi.org/project/pyncbt/"><img alt="Downloads" src="https://img.shields.io/pypi/dm/pyncbt"></a>
</p>

**pyncbt** is an open‑source Python library that implements **Non‑iterative Correlation‑based Tuning (NCbT)** for direct fixed‑structure controller design from input‑output data. It requires no explicit plant model and no iterative optimization.

- **Simple workflow**: weighting filter `W` → instruments → stable least‑squares → parameters `ρ`.
- **Reproducible examples**: `.npy` data, benchmark scripts, and Colab notebook.
- **Open‑loop and closed‑loop support**: flexible for different experimental scenarios.
- **Flexible basis**: you define the controller structure (PID, FIR, integrator plus delays, etc.).

> Full documentation: [https://joaoleroy.github.io/pyncbt/](https://joaoleroy.github.io/pyncbt/)  
> PyPI package: [https://pypi.org/project/pyncbt/](https://pypi.org/project/pyncbt/)

---

## Installation

```console
pip install pyncbt
```

---

##  Interactive notebooks

Try the examples online without any installation:

>[https://colab.research.google.com/drive/1MlzWRP8eHVUVVPgt1IiL2hqU5SN7gq98?usp=sharing](Benchmark example (flexible transmission system))  

>[https://colab.research.google.com/drive/1zblNhjnmtO1QX1wz6xGg9ekQapmgzl7u?usp=sharing](PI controller for a non‑minimum phase system)

