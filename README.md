<p align="center">
  <img src="docs/img/pyncbt-logo.png" width="50%" height="50%" alt="pyncbt logo">
</p>

<h1 align="center">pyncbt · Non-iterative Correlation-based Tuning (NCbT) in Python</h1>
<p align="center">
  <a href="https://pypi.org/project/pyncbt/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pyncbt.svg"></a>
  <a href="https://pypi.org/project/pyncbt/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/pyncbt.svg"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://github.com/JoaoLeroy/pyncbt/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/JoaoLeroy/pyncbt/ci.yml?branch=main"></a>
  <a href="https://codecov.io/gh/JoaoLeroy/pyncbt"><img alt="coverage" src="https://img.shields.io/codecov/c/gh/JoaoLeroy/pyncbt"></a>
  <a href="https://pypi.org/project/pyncbt/"><img alt="Downloads" src="https://img.shields.io/pypi/dm/pyncbt"></a>
</p>

**pyncbt** é uma biblioteca Python **open-source** para projeto de controladores por **NCbT** (Non‑iterative Correlation‑based Tuning) diretamente a partir de dados SISO LTI no tempo discreto.

- **Fluxo simples**: filtro de ponderação `W` → instrumentos → MQ estável → parâmetros `ρ`.
- **Exemplos reproduzíveis**: dados `.npy`, script de benchmark e notebook no Colab.
- **Foco em reprodutibilidade**: seeds, versões e métricas reportadas.

> Documentação: **https://joaoleroy.github.io/pyncbt/**  
> PyPI: **https://pypi.org/project/pyncbt/**

---

## Instalação

```console
pip install pyncbt
```

