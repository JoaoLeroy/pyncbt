# Tutorial: Open-loop NCbT

This tutorial shows how to use `NCbT_open` to estimate controller parameters from open-loop data.

## Load data

```python
import numpy as np

u = np.load("u_t.npy")
y = np.load("y_t.npy")
t = np.load("time.npy")
Ts = 0.05
```

## Choose reference model and controller structure

```python
# Reference model M(q)
omega_bar = 10
alpha = np.exp(-Ts * omega_bar)
num_M = np.array([0, 0, 0, (1 - alpha)**2])
den_M = np.array([1, -2*alpha, alpha**2])

# Controller basis 
beta = [
    ([1], [1, -1]),
    ([0, 1], [1, -1]),
    ([0, 0, 1], [1, -1]),
    ([0, 0, 0, 1], [1, -1]),
    ([0, 0, 0, 0, 1], [1, -1]),
    ([0, 0, 0, 0, 0, 1], [1, -1])
]
l = 20
```

## Estimate parameters

```python
from pyncbt import NCbT_open

estimator = NCbT_open(u, y, num_M, den_M, Ts, t, l, beta)
rho = estimator.run()
print(rho)
```

The result is the vector of controller parameters.