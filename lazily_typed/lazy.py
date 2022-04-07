from typing import Generic, TypeVar, Callable, Any

from lazily_typed import get_logger, location_info

_T = TypeVar('_T')
lazy_logger = get_logger("Lazy Logger")


class Lazy(Generic[_T]):
    _cls: _T
    _instance: _T
    _object_close_method: str
    _builder: Callable[[Any], _T]
    _args: tuple
    _kwargs: dict

    def __init__(
            self,
            cls: _T,
            *args,
            builder: Callable[[Any], _T] = None,
            object_close_method: str = 'close',
            **kwargs
    ):
        self._cls = cls
        self._instance: object = None
        self._object_close_method = object_close_method
        self._builder = builder if builder is not None else cls
        self._args = args
        self._kwargs = kwargs

        lazy_logger.debug(f"<{hex(id(self))}> Created   {self} with {self._cls}")
        lazy_logger.debug(f"<{hex(id(self))}> Location  {location_info()}")

    def __repr__(self):
        return f"<{self.__name__}({self._cls.__name__})>"

    @property
    def instance__(self) -> _T:
        if self._instance is None:
            self.__build(*self._args, **self._kwargs)
        return self._instance

    def __build(self, *args, **kwargs):
        lazy_logger.info(f"<{hex(id(self))}> Starting  {self} with args:{args}, kwargs:{kwargs}")
        lazy_logger.debug(f"<{hex(id(self))}>           {location_info()}")
        self._instance = self._builder(*args, **kwargs)
        lazy_logger.debug(f"<{hex(id(self))}> Started   {self}")

    def __call__(self, *args, **kwargs):
        """
        this = Lazy(MyClass)(v1,v2,v3,k1=v4) ~= MyClass(v1,v2,v3,k1=v4)
        :param args:
        :param kwargs:
        :return: object MyClass or object()
        """
        if self._instance is None:
            if self._args and args:
                raise ValueError("Positional Arguments")
            use_args = args if args else self._args
            use_kwargs = self._kwargs | kwargs
            self.__build(*use_args, **use_kwargs)
            return self.instance__
        return self.instance__.__call__(*args, **kwargs)

    def __getattr__(self, item):
        if item in self.__class__.__annotations__:
            return getattr(self, item)
        return getattr(self.instance__, item)

    def __setattr__(self, key, value):
        if key in self.__class__.__annotations__:
            return self.__dict__.__setitem__(key, value)
        return self.instance__.__setattr__(key, value)


class LazyFactory:
    _cls: _T
    _object_close_method: str
    _builder: Callable[[Any], _T]
    _args: tuple
    _kwargs: dict
    __init__ = Lazy.__init__

    def __call__(self, *args, **kwargs):
        """
        factory = LazyFactory(MyClass)
        lazy_instance = factory(v1,v2)
        other_lazy_instance = factory(v3,v4)
        :param args:
        :param kwargs:
        :return: object MyClass or object()
        """
        if self._args and args:
            raise ValueError("Positional Arguments")
        use_args = args if args else self._args
        use_kwargs = self._kwargs | kwargs
        return self.__build(*use_args, **use_kwargs)

    def __build(self, *args, **kwargs):
        return Lazy(
            cls=self._cls,
            builder=self._builder,
            object_close_method=self._object_close_method,
            *args,
            **kwargs
        )


class LazyContext(Lazy):
    """
    with LazyContext(FileHandler, open, path, 'w') as f:
        do stuff
        f.write()
    """

    @property
    def instance__(self) -> _T:
        if self._instance is None:
            self.__build(*self._args, **self._kwargs)
        return self._instance

    def __enter__(self) -> _T:
        if self._instance is None:
            return self
        return self.instance__

    def __build(self, *args, **kwargs) -> None:
        lazy_logger.info(f"<{hex(id(self))}> Starting  {self} with args:{args}, kwargs:{kwargs}")
        lazy_logger.debug(f"<{hex(id(self))}>           {location_info()}")
        self._instance = self._builder(*args, **kwargs).__enter__()
        lazy_logger.debug(f"<{hex(id(self))}> Started   {self}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._instance is not None:
            lazy_logger.debug(f"<{hex(id(self))}> Exiting   {self}")
            lazy_logger.debug(f"<{hex(id(self))}>           {location_info()}")
            if hasattr(self.instance__, '__exit__'):
                return self.instance__.__exit__(exc_type, exc_val, exc_tb)


def lazy_lambda(function: _T):
    def wrapped(*args, **kwargs):
        return Lazy(function.__annotations__.get('return', None), function, *args, **kwargs)

    f: _T = wrapped
    return f
