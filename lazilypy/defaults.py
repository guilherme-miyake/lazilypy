from lazilypy.logging import logger


class MethodResponse:
    """
    Missing return type in wrapped function
    Using defaults.MethodResponse class type
    """

    pass


def proxy_operator(_lazy_operator_):
    def method(self, *args, **kwargs):
        logger.debug(_lazy_operator_)
        return self._lazy_instance_getter_.__getattribute__(_lazy_operator_)(
            *args, **kwargs
        )

    return method


supported_python_operators = [
    "__abs__",
    "__add__",
    "__and__",
    "__bool__",
    "__cached__",
    "__ceil__",
    "__concat__",
    "__contains__",
    "__delitem__",
    "__divmod__",
    "__doc__",
    "__eq__",
    "__float__",
    "__floor__",
    "__floordiv__",
    "__ge__",
    "__getitem__",
    "__getnewargs__",
    "__gt__",
    "__iadd__",
    "__iand__",
    "__iconcat__",
    "__ifloordiv__",
    "__ilshift__",
    "__imatmul__",
    "__imod__",
    "__imul__",
    "__index__",
    "__int__",
    "__inv__",
    "__invert__",
    "__ior__",
    "__ipow__",
    "__irshift__",
    "__isub__",
    "__itruediv__",
    "__ixor__",
    "__le__",
    "__lshift__",
    "__lt__",
    "__matmul__",
    "__mod__",
    "__mul__",
    "__ne__",
    "__neg__",
    "__not__",
    "__or__",
    "__pos__",
    "__pow__",
    "__radd__",
    "__rand__",
    "__rdivmod__",
    "__rfloordiv__",
    "__rlshift__",
    "__rmod__",
    "__rmul__",
    "__ror__",
    "__round__",
    "__rpow__",
    "__rrshift__",
    "__rshift__",
    "__rsub__",
    "__rtruediv__",
    "__rxor__",
    "__setitem__",
    "__sizeof__",
    "__sub__",
    "__truediv__",
    "__trunc__",
    "__xor__",
    "_abs",
]
