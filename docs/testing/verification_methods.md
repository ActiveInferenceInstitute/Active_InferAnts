# Verification Methods

How to verify that Active Inference implementations are correct.

## Mathematical Properties to Verify

### 1. Posterior Normalization
```python
posterior = update_beliefs(A, obs, prior)
assert abs(posterior.sum() - 1.0) < 1e-10
```

### 2. Likelihood Normalization
```python
for col in range(A.shape[1]):
    assert abs(A[:, col].sum() - 1.0) < 1e-10
```

### 3. Transition Normalization
```python
for action in range(B.shape[2]):
    for col in range(B.shape[1]):
        assert abs(B[:, col, action].sum() - 1.0) < 1e-10
```

### 4. Free Energy Non-Negativity
```python
F = compute_free_energy(posterior, A, obs, prior)
assert F >= 0
```

### 5. Functor Laws
```python
from poly_functor import ListFunctor
f = ListFunctor()
data = [1, 2, 3]

# Identity law
assert f.hmap(lambda x: x, data) == data

# Composition law
g = lambda x: x * 2
h = lambda x: x + 1
assert f.hmap(lambda x: g(h(x)), data) == f.hmap(g, f.hmap(h, data))
```
