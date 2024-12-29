from functools import partial, wraps
from typing import Annotated, Any, Callable, get_type_hints

Inject = Annotated[Annotated, "Inject"]


class Dependency:
    def __init__(self, func: Callable[..., Any]) -> None:
        solved_dependencies = {
            name: dependency() for name, dependency in _infer_dependencies(func).items()
        }
        self._func = partial(func, **solved_dependencies)

    def __call__(self) -> Any:
        return self._func()


def injectable(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        dependencies = _infer_dependencies(func)
        solved_dependencies = {
            name: dependency() for name, dependency in dependencies.items()
        }
        return func(*args, **kwargs, **solved_dependencies)

    return wrapper


def _infer_dependencies(func: Callable[..., Any]) -> dict[str, Dependency]:
    dependencies = {}
    annotations = get_type_hints(func, include_extras=True)

    for name, annotation in annotations.items():
        if not hasattr(annotation, "__metadata__"):
            continue

        for metadata in annotation.__metadata__:
            if isinstance(metadata, Inject):
                dependencies[name] = metadata

    return dependencies
