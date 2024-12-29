from src.pydi.main import Dependency, Inject, injectable


def test_flat_dependencies():
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


def test_nested_dependencies():
    def foo() -> str:
        return "foo"

    @injectable
    def bar(_foo: Inject[str, Dependency(foo)]) -> str:
        return _foo + "bar"

    @injectable
    def function(_bar: Inject[str, Dependency(bar)]):
        return "foobar" + _bar

    assert function() == "foobarfoobar"


def test_nested_dependency_with_positional_params():
    def foo() -> str:
        return "foo"

    @injectable
    def bar(_foo: Inject[str, Dependency(foo)]) -> str:
        return _foo + "bar"

    @injectable
    def function(x: str, y: str, _bar: Inject[str, Dependency(bar)]):
        return x + _bar + y

    assert function("foo", "bar") == "foofoobarbar"
