# pydi
Dependency injection solution for python.

## Usage
### Step 1: Install pydi

```bash
poetry add pydi
```

or
    
```bash
pip install pydi
```

### Step 2: start using it
- Import decorator and variables
```python
from pydi import Dependency, Inject, injectable
```

- Use it for flat dependencies
```python
def foo() -> str:
    return "foo"

def bar() -> str:
    return "bar"

@injectable
def function(
    _foo: Inject[str, Dependency(foo)], _bar: Inject[str, Dependency(bar)]
):
    return _foo + _bar

assert function() == "foobar"
```

- Use it for nested dependencies
```python
def foo() -> str:
    return "foo"

@injectable
def bar(_foo: Inject[str, Dependency(foo)]) -> str:
    return _foo + "bar"

@injectable
def function(_bar: Inject[str, Dependency(bar)]):
    return "foobar" + _bar

assert function() == "foobarfoobar"
```

- Use it with other params, but make sure to make dependencies the last arguments
```python
def foo() -> str:
    return "foo"

@injectable
def bar(_foo: Inject[str, Dependency(foo)]) -> str:
    return _foo + "bar"

@injectable
def function(x: str, y: str, _bar: Inject[str, Dependency(bar)]):
    return x + _bar + y

assert function("foo", "bar") == "foofoobarbar"
```
