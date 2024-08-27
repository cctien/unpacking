from collections.abc import Callable, Mapping, Sequence
from typing import Any

from plum import dispatch


@dispatch
def apply_packed(fnct: Callable, squn: Sequence) -> Any:
    return fnct(*squn)


@dispatch
def apply_packed(fnct: Callable, tbl_assc: Mapping) -> Any:
    return fnct(**tbl_assc)


def packed(fnct: Callable) -> Callable:
    def fnct_packed(to_be_unpacked: Sequence | Mapping) -> Any:
        return apply_packed(fnct, to_be_unpacked)

    return fnct_packed


if __name__ == "__main__":

    data_args = [1, 2]
    data_kwargs = {"x": 1, "y": 2}

    def f(x: int, y: int) -> int:
        added = x + y
        print(f"{x} added to {y} produces {added}")
        return added

    assert f(*data_args) == 3
    assert f(**data_kwargs) == 3

    assert packed(f)(data_args) == 3
    assert packed(f)(data_kwargs) == 3

    assert apply_packed(f, data_args) == 3
    assert apply_packed(f, data_kwargs) == 3

    #####

    def packed_args(f: Callable) -> Callable:
        def new_f(arg: Sequence):
            return f(*arg)

        return new_f

    def packed_kwargs(f: Callable) -> Callable:
        def new_f(kwargs: Mapping):
            return f(**kwargs)

        return new_f

    def pssb_packed(f: Callable) -> Callable:
        def new_f(*args, **kwargs):
            if len(args) == 1 and len(kwargs) == 0:
                return apply_packed(f, args[0])

            return f(*args, **kwargs)

        return new_f

    assert pssb_packed(f)(*data_args) == 3
    assert pssb_packed(f)(data_args) == 3
    assert pssb_packed(f)(**data_kwargs) == 3
    assert pssb_packed(f)(data_kwargs) == 3

    @dispatch
    def apply_packed(f: Callable, *args, **kwargs) -> Any:
        return f(*args, **kwargs)

    assert apply_packed(f, *data_args) == 3
    assert apply_packed(f, **data_kwargs) == 3
