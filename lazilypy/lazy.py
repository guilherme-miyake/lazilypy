from functools import wraps
from typing import Generic, TypeVar, Callable, Any, Union, Tuple

from lazilypy import get_logger, location_info

_T = TypeVar("_T")
lazy_logger = get_logger("Lazy Logger")


class Lazy(Generic[_T]):
    _lazy_ref_instance_ = None
    _lazy_default_keywords_ = ["__repr__"]
    _lazy_reserved_keywords_: Tuple[str, str] = ("", "")

    def __init__(
        self,
        lazy_cls: _T,
        *args,
        lazy_builder: Callable[[Any], _T] = None,
        lazy_partial: bool = True,
        **kwargs,
    ):
        self._lazy_dict_ = self.__dict__
        self._lazy_obj_ = self
        self._lazy_cls_ = self.__class__
        self._lazy_ref_cls_ = lazy_cls
        self._lazy_builder_ = lazy_builder if lazy_builder is not None else lazy_cls
        self._lazy_args_ = args
        self._lazy_kwargs_ = kwargs
        self._lazy_default_keywords_ += "__call__" if lazy_partial else ""
        lazy_logger.debug(f"{self._lazy_obj_} Created    with {self._lazy_ref_cls_}")
        lazy_logger.debug(f"{self._lazy_obj_}           {location_info()}")

    def _lazy_build_(self, *args, **kwargs):
        lazy_logger.info(
            f"{self._lazy_obj_} Starting   with args:{args}, kwargs:{kwargs}"
        )
        lazy_logger.debug(f"{self._lazy_obj_}           {location_info()}")
        self._lazy_ref_instance_ = self._lazy_builder_(*args, **kwargs)
        lazy_logger.debug(f"{self._lazy_obj_} Started   ")

    def __repr__(self):
        return f"<{self._lazy_cls_.__name__}({self._lazy_ref_cls_.__name__}) at {hex(id(self._lazy_obj_))}>"

    def __call__(self, *args, **kwargs):
        if self._lazy_ref_instance_ is None:
            if self._lazy_args_ and args:
                raise SyntaxError(
                    f"Positional arguments already defined: {self._lazy_args_}"
                )
            use_args_ = args if args else self._lazy_args_
            use_kwargs_ = self._lazy_kwargs_.copy()
            use_kwargs_.update(kwargs)
            self._lazy_build_(*use_args_, **use_kwargs_)
            return self._lazy_instance_getter_

    @property
    def _lazy_instance_getter_(self) -> _T:
        if self._lazy_ref_instance_ is None:
            self._lazy_build_(*self._lazy_args_, **self._lazy_kwargs_)
        if self._lazy_ref_instance_ is None:
            raise NameError(f"Lazy builder {self._lazy_builder_} returned {None}")
        return self._lazy_ref_instance_

    def __getattr__(self, item: str):
        if item.startswith("_lazy_") or item in self._lazy_reserved_keywords_:
            return self._lazy_dict_.__getitem__(item)

        if self._lazy_ref_instance_ is None and item in self._lazy_default_keywords_:
            return self._lazy_obj_.__dict__.__getitem__(item)
        print(item)
        return getattr(self._lazy_instance_getter_, item)

    def __setattr__(self, key: str, value):
        if key == "_lazy_dict_":
            return self.__dict__.__setitem__(key, value)
        if key.startswith("_lazy_") or key in self._lazy_reserved_keywords_:
            return self._lazy_dict_.__setitem__(key, value)
        if self._lazy_ref_instance_ is None and key in self._lazy_default_keywords_:
            return self._lazy_dict_.__setitem__(key, value)
        return self._lazy_instance_getter_.__setattr__(key, value)


class LazyFactory(Generic[_T]):
    def __init__(
        self,
        lazy_cls: _T,
        *args,
        lazy_builder: Callable[[Any], _T] = None,
        **kwargs,
    ):
        self._lazy_ref_cls_ = lazy_cls
        self._lazy_builder_ = lazy_builder if lazy_builder is not None else lazy_cls
        self._lazy_args_ = args
        self._lazy_kwargs_ = kwargs
        lazy_logger.debug(f"{self} Created    with {self._lazy_ref_cls_}")
        lazy_logger.debug(f"{self}           {location_info()}")

    def __call__(self, *args, **kwargs):
        if self._lazy_args_ and args:
            raise SyntaxError(
                f"Positional arguments already defined: {self._lazy_args_}"
            )
        use_args = args if args else self._lazy_args_
        use_kwargs = self._lazy_kwargs_.copy()
        use_kwargs |= kwargs
        use_kwargs |= {
            "lazy_cls": self._lazy_ref_cls_,
            "lazy_builder": self._lazy_builder_,
        }
        return Lazy(*use_args, **use_kwargs)


class LazyContext(Lazy, Generic[_T]):
    _lazy_reserved_keywords_ = ("__enter__", "__exit__")

    def _lazy_build_(self, *args, **kwargs) -> None:
        lazy_logger.info(
            f"{self._lazy_obj_} Starting   with args:{args}, kwargs:{kwargs}"
        )
        lazy_logger.debug(f"          {location_info()}")
        self._lazy_ref_instance_ = self._lazy_builder_(*args, **kwargs).__enter__()  # type: ignore[operator]
        lazy_logger.debug(f"{self._lazy_obj_} Started   ")

    def __enter__(self) -> Union[Lazy, _T]:
        if self._lazy_ref_instance_ is None:
            return self
        return self._lazy_instance_getter_

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._lazy_ref_instance_ is not None:
            lazy_logger.debug(f"{self._lazy_obj_} Exiting   ")
            lazy_logger.debug(f"          {location_info()}")
            return self._lazy_instance_getter_.__exit__(exc_type, exc_val, exc_tb)


def lazy_lambda(function: Union[Callable[[Any], _T], Any]):
    @wraps
    def wrapped(*args, **kwargs) -> Union[Lazy, _T]:
        return Lazy(
            function.__annotations__.get("return", None), function, *args, **kwargs
        )

    return wrapped
