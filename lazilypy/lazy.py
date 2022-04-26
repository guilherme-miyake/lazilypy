from logging import Logger
from pprint import pprint
from typing import (
    Generic,
    TypeVar,
    Callable,
    Any,
    Union,
    Tuple,
    Type,
    Optional,
    NewType,
)

from lazilypy import location_info
from lazilypy.defaults import supported_python_operators, proxy_operator, MethodResponse
from lazilypy.logs import logger

_T = TypeVar("_T")

try:

    class MetaNewType(NewType):  # type: ignore[valid-type,misc]
        pass

except TypeError:

    class MetaNewType(object):  # type: ignore[no-redef]
        pass


class Lazy(MetaNewType, Generic[_T]):
    _lazy_ref_instance_: Optional[_T] = None
    _lazy_default_keywords_ = ["__class__", "__supertype__"]
    _lazy_reserved_keywords_: Tuple[str, str] = ("", "")

    def __init__(
        self,
        lazy_cls: Type[_T],
        *args,
        lazy_builder: Callable[[Any], _T] = None,
        lazy_partial: bool = True,
        lazy_logger: Logger = logger,
        **kwargs,
    ):
        # create a copy of default keywords
        self._lazy_default_keywords_ = self._lazy_default_keywords_.copy()
        # Store own class in other reference
        self._lazy_cls_ = self.__class__
        # access to class property from now own should start instance (e.g: class checks)
        self._lazy_default_keywords_.pop(0)
        self._lazy_logger_ = lazy_logger
        # store non-instance class reference
        self._lazy_ref_cls_ = lazy_cls
        self.__supertype__ = lazy_cls
        # defaults builder to cls __init__
        self._lazy_builder_ = lazy_builder if lazy_builder is not None else lazy_cls
        self._lazy_args_ = args
        self._lazy_kwargs_ = kwargs
        # Lazy operates as partial by default, lazy_instance(*args,**kwargs) calls will start instance immediately
        self._lazy_default_keywords_ += ["__call__"] if lazy_partial else ""
        self._lazy_logger_.debug(
            f"{self._lazy_repr_()} Created    with {self._lazy_ref_cls_}"
        )
        self._lazy_logger_.debug(f"{self._lazy_repr_()}           {location_info()}")

    def _lazy_build_(self, *args, **kwargs):
        self._lazy_logger_.info(
            f"{self._lazy_repr_()} Starting   with args:{args}, kwargs:{kwargs}"
        )
        self._lazy_logger_.debug(f"{self._lazy_repr_()}           {location_info()}")
        self._lazy_ref_instance_ = self._lazy_builder_(*args, **kwargs)
        self._lazy_logger_.debug(f"{self._lazy_repr_()} Started   ")

    def _lazy_repr_(self):
        return f"<{self._lazy_cls_.__name__}({self._lazy_ref_cls_.__name__}) object at {hex(id(self))}>"

    def __repr__(self):
        if self._lazy_ref_instance_ is None:
            return self._lazy_repr_()
        return self._lazy_ref_instance_.__repr__()

    def __str__(self):
        if self._lazy_ref_instance_ is None:
            return self._lazy_repr_()
        return self._lazy_ref_instance_.__str__()

    def __format__(self, format_spec):
        if self._lazy_ref_instance_ is None:
            return self.__format__(format_spec)
        return self._lazy_ref_instance_.__format__(format_spec)

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

    def __getattribute__(self, item):
        logger.log(1, f"getattribute: {item}")
        if item.startswith("_lazy_") or item in self._lazy_reserved_keywords_:
            return super(Lazy, self).__getattribute__(item)
        if self._lazy_ref_instance_ is None and item in self._lazy_default_keywords_:
            return super(Lazy, self).__getattribute__(item)
        return self._lazy_instance_getter_.__getattribute__(item)

    def __setattr__(self, key: str, value):
        logger.log(2, f"setattr: {key}")
        if key.startswith("_lazy_") or key in self._lazy_reserved_keywords_:
            return super(Lazy, self).__setattr__(key, value)
        if self._lazy_ref_instance_ is None and key in self._lazy_default_keywords_:
            return super(Lazy, self).__setattr__(key, value)
        return self._lazy_instance_getter_.__setattr__(key, value)


for operator in supported_python_operators:
    setattr(Lazy, operator, proxy_operator(operator))


class LazyFactory(Generic[_T]):
    def __init__(
        self,
        lazy_cls: _T,
        *args,
        lazy_builder: Callable[[Any], _T] = None,
        lazy_logger: Logger = logger,
        **kwargs,
    ):
        self._lazy_ref_cls_ = lazy_cls
        self._lazy_builder_ = lazy_builder if lazy_builder is not None else lazy_cls
        self._lazy_args_ = args
        self._lazy_kwargs_ = kwargs
        self._lazy_logger_ = lazy_logger
        self._lazy_logger_.debug(f"{self} Created    with {self._lazy_ref_cls_}")
        self._lazy_logger_.debug(f"{self}           {location_info()}")

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
            "lazy_logger": self._lazy_logger_,
        }
        return Lazy(*use_args, **use_kwargs)


class LazyContext(Lazy, Generic[_T]):
    _lazy_reserved_keywords_ = ("__enter__", "__exit__")

    def _lazy_build_(self, *args, **kwargs) -> None:
        self._lazy_logger_.info(
            f"{self._lazy_repr_()} Starting   with args:{args}, kwargs:{kwargs}"
        )
        self._lazy_logger_.debug(f"          {location_info()}")
        self._lazy_ref_instance_ = self._lazy_builder_(*args, **kwargs).__enter__()  # type: ignore[operator]
        self._lazy_logger_.debug(f"{self._lazy_repr_()} Started   ")

    def __enter__(self) -> Union[Lazy, _T]:
        if self._lazy_ref_instance_ is None:
            return self
        return self._lazy_instance_getter_

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._lazy_ref_instance_ is not None:
            self._lazy_logger_.info(f"{self._lazy_repr_()} Exiting   ")
            self._lazy_logger_.debug(
                f"{self._lazy_repr_()}           {location_info()}"
            )
            return self._lazy_instance_getter_.__exit__(exc_type, exc_val, exc_tb)


def make_lazy(function: Union[Callable[[Any], _T], Any]):
    def wrapped(*args, **kwargs) -> Union[Lazy, _T]:
        use_kwargs = kwargs
        use_kwargs.update(
            dict(
                lazy_cls=function.__annotations__.get("return", MethodResponse),
                lazy_builder=function,
            )
        )
        return Lazy(
            *args,
            **kwargs,
        )

    return wrapped
