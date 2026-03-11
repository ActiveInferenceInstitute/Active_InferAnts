# Category Theory in Active Inference

Compositional mathematical structures for analysis and measurement.

## PolyFunctor (`3_MEASURE/poly_functor.py`)

Generic `PolyFunctor[A, B]` base class implementing polynomial functors via `hmap`:

| Functor | Data Structure | `hmap` Behavior |
|---------|----------------|-----------------|
| `Tuple2Functor` | 2-tuple | Apply to both elements |
| `Tuple3Functor` | 3-tuple | Apply to all three elements |
| `ListFunctor` | List | Map over each element |
| `MaybeFunctor` | Optional (None/value) | Apply if value exists |
| `EitherFunctor` | Left/Right tagged union | Apply only to Right |
| `TreeFunctor` | Binary tree | Recursive application |

### Functor Laws

All implementations must satisfy:
1. **Identity**: `hmap(id, x) == x`
2. **Composition**: `hmap(f ∘ g, x) == hmap(f, hmap(g, x))`

## CategoryTheoryAnalyzer (`3_MEASURE/categorization.py`)

Graph-based categorization using NetworkX:

| Feature | Description |
|---------|-------------|
| Objects | Nodes in the category graph |
| Morphisms | Directed edges with composition tracking |
| Functors | Mappings between category graphs |
| Composition | Morphism composition with associativity |

## Application

Category theory provides the compositional structure for combining measurement results across different analysis dimensions. `PolyFunctor.hmap` enables polymorphic transformations across heterogeneous data.
