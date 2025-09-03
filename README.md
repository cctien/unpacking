# unpacking

![PyPI](https://img.shields.io/pypi/v/unpacking)
![License](https://img.shields.io/github/license/cctien/unpacking)

Unpacking, spreading, or splatting positional arguments and keyword arguments in Python.

It provides tools of functionals as classes which gives versions of the original function which use unpacking expressions ([Python reference](https://docs.python.org/3/reference/expressions.html#calls), [PEP 448](https://peps.python.org/pep-0448/)) for the functional call underneath.

## Installation

```bash
pip install -U unpacking
```

## Usage

### Basic Example

```python
from unpacking import starred, doublestarred, unpacking

def add(x, y):
    return x + y

args = [1, 2]
kwargs = {"x": 1, "y": 2}

print(add(*args))                   # 3
print(starred(add)(args))           # 3

print(add(**kwargs))                # 3
print(doublestarred(add)(kwargs))   # 3

# `unpacking` dispatches to the unapcking expression suitable to the type of the input argument
print(unpacking(add)(args))         # 3
print(unpacking(add)(kwargs))       # 3
```

### Handling Excess Arguments

```python
from unpacking import starredpart, doublestarredpart, unpackingpart

def add(x, y):
    return x + y

args_excess = [1, 2, 3]
kwargs_excess = {"x": 1, "y": 2, "z": 3}

print(starredpart(add)(args_excess))         # 3
print(unpackingpart(add)(args_excess))       # 3

print(doublestarredpart(add)(kwargs_excess)) # 3
print(unpackingpart(add)(kwargs_excess))     # 3
```

### Multiprocessing Example

One important use case of `unpacking` is multiprocessing.

```python
from concurrent.futures import ProcessPoolExecutor

from unpacking import unpacking

def add(x, y):
    return x + y

args_list = [[1, 2], [3, 4]]
kwargs_list = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]

with ProcessPoolExecutor(2) as executor:
    print(tuple(executor.map(unpacking(add), args_list)))    # (3, 7)
    print(tuple(executor.map(unpacking(add), kwargs_list)))  # (3, 7)
```

## API Reference

- `starred(fnct)`: Call function with positional arguments from iterable.
- `doublestarred(fnct)`: Call function with keyword arguments from mapping.
- `unpacking(fnct)`: Call function with either positional or keyword arguments.
- `starredpart(fnct)`: Call function with only as many positional arguments as needed.
- `doublestarredpart(fnct)`: Call function with only needed keyword arguments.
- `unpackingpart(fnct)`: Call function with either positional or keyword arguments, only as many as needed.
