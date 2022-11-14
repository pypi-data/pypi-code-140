from typing import (
    Any,
    Callable,
    Optional,
    Type,
    TypeVar,
    Union,
    get_origin,
    get_type_hints,
    overload,
)

import functools
import inspect

from app_properties.config_handler import get_config

_T = TypeVar("_T")


@overload
def properties(
    cls: None = None,
    *,
    filename: str = ...,
    ignore_case: bool = ...,
    override_default: bool = ...,
    root: str = ...,
    type_cast: bool = ...,
) -> Callable[[Type[_T]], Type[_T]]:
    ...


@overload
def properties(
    cls: Type[_T],
    *,
    filename: str = ...,
    ignore_case: bool = ...,
    override_default: bool = ...,
    root: str = ...,
    type_cast: bool = ...,
) -> Type[_T]:
    ...


def properties(
    cls: Optional[Type[_T]] = None,
    *,
    filename: str = "application.yml",
    ignore_case: bool = True,
    override_default: bool = False,
    root: str = "",
    type_cast: bool = False,
) -> Union[Callable[[Type[_T]], Type[_T]], Type[_T]]:
    @functools.wraps(cls)  # type: ignore
    def wrapper(obj: Type[_T]) -> Type[_T]:
        annotated_class_vars = get_type_hints(obj)
        default_class_vars = _get_default_class_var(obj)
        config = get_config(filename, ignore_case, root)
        for class_var, type_ in annotated_class_vars.items():
            if not override_default and class_var in default_class_vars:
                continue
            value = config.get(class_var.lower() if ignore_case else class_var)
            if type_cast:
                value = _cast_types(type_, value)
            setattr(obj, class_var, value)
        return obj

    if cls is None:
        return wrapper
    return wrapper(cls)


def _cast_types(type_: type, value: Any) -> Any:
    type_ = origin if (origin := get_origin(type_)) else type_
    if isinstance(type_, type):
        return type_(value) if value else type_()
    return value


def _get_default_class_var(obj: type) -> dict:
    return {
        k: v
        for k, v in inspect.getmembers(obj)
        if not (
            k.startswith("__")
            or callable(v)
            or isinstance(v, (property, classmethod))
        )
    }
