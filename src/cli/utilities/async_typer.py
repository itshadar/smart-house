import asyncio
import inspect
from functools import partial, wraps

from typer import Typer
from typing import Any, Callable, TypeVar

T = TypeVar("T")


# Reference: https://github.com/tiangolo/typer/issues/88
class AsyncTyper(Typer):
    @staticmethod
    def maybe_run_async(decorator: Callable[..., T], f: Callable[..., Any]) -> T:
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            def runner(*args: Any, **kwargs: Any) -> Any:
                return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

            return decorator(runner)
        else:
            return decorator(f)

    def callback(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        decorator = super().callback(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)

    def command(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        decorator = super().command(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)
