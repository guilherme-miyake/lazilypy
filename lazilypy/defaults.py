import platform

from lazilypy.logs import logger


class MethodResponse:
    """
    Missing return type in wrapped function
    Using defaults.MethodResponse class type
    """

    pass


forced_operators = {
    str: {
        "__radd__": lambda self, *args, **kwargs: args[0] + self._lazy_instance_getter_
    }
}


def to_instance(item):
    if "lazilypy.lazy.Lazy" in str(type(item)):
        return item._lazy_instance_getter_
    return item


def proxy_operator(_lazy_operator_):
    def method(self, *args, **kwargs):
        logger.log(5, _lazy_operator_)
        logger.log(5, type(self))
        instance_args = (to_instance(arg) for arg in args)
        instance_kwargs = {key: to_instance(kwargs[key]) for key in kwargs}
        if (
            self._lazy_ref_cls_ in forced_operators
            and _lazy_operator_ in forced_operators[self._lazy_ref_cls_]
        ):
            return forced_operators[self._lazy_ref_cls_][_lazy_operator_](
                self, *instance_args, **instance_kwargs
            )
        return self._lazy_instance_getter_.__getattribute__(_lazy_operator_)(
            *instance_args, **instance_kwargs
        )

    return method


int_operators = [
    # Addition ( a + b )
    "__add__",
    "__radd__",
    # Division ( a / b )
    "__truediv__",
    "__rtruediv__",
    # Division ( a // b )
    "__floordiv__",
    "__rfloordiv__",
    # Bitwise And ( a & b )
    "__and___",
    "__rand__",
    # Bitwise Exclusive Or ( a ^ b )
    "__xor__",
    # "__rxor__", TODO: Not Supported
    # Bitwise Inversion ( ~ a )
    "__invert__",
    # Bitwise Or ( a | b )
    "__or__",
    "__ror__",
    # Exponentiation ( a ** b )
    "__pow__",
    "__rpow__",
    # Left Shift ( a << b )
    "__lshift__",
    "__rlshift__",
    # Modulo ( a % b )
    "__mod__",
    "__rmod__",
    # Multiplication ( a * b )
    "__mul__",
    "__rmul__",
    # Negation (Arithmetic) ( - a )
    "__neg__",
    # Right Shift ( a >> b )
    "__rshift__",
    "__rrshift__",
    # Subtraction ( a - b )
    "__sub__",
    "__rsub__",
    # Ordering ( a < b )
    "__lt__",
    # Ordering ( a <= b )
    "__le__",
    # Equality ( a == b )
    "__eq__",
    # Difference ( a != b )
    "__ne__",
    # Ordering ( a >= b )
    "__ge__",
    # Ordering ( a > b )
    "__gt__",
]

compatibility_builtins = [
    # math.ceil(a)
    "__ceil__",
    # math.floor(a)
    "__floor__",
]

numeric_builtins = [
    # abs(a_
    "__abs__",
    # int(a)
    "__int__",
    # float(a)
    "__float__",
    # bin(a)
    # "__bin__", TODO: Not Supported
]

supported_python_operators = (
    int_operators
    + numeric_builtins
    + (compatibility_builtins if platform.python_version() > "3.9.0" else [""])
    + [
        # Concatenation ( seq1 + seq2 )
        "__concat__",
        # Containment Test ( obj in seq )
        "__contains__",
        # Identity ( a is b )
        # Identity ( a is not b )
        # Both are implemented with memory references
        # Indexed Assignment ( obj[k] = v )
        "__setitem__",
        # Indexed Deletion ( del obj[k] )
        "__delitem__",
        # Indexing ( obj[k] )
        "__getitem__",
        # Matrix Multiplication ( a @ b )
        "__matmul__",
        # Negation (Logical) ( not a )
        "__not__",
        # Positive ( + a )
        "__pos__",
        # Slice Assignment ( seq[i:j] = values )
        "__setitem__",
        # Slice Deletion ( del seq[i:j] )
        "__delitem__",
        # Slicing ( seq[i:j] )
        "__getitem__",
        # String Formatting ( s % obj )
        "__mod__",
        # Truth Test ( obj )
        "__truth__",
    ]
)

old_python_operators = [
    # x and
    "__and__",
    # bool(
    "__bool__",
    "__cached__",
    "__concat__",
    # in x
    "__contains__",
    # delete x[y]
    "__delitem__",
    # x %
    "__divmod__",
    "__doc__",
    # x[y]
    "__getitem__",
    "__getnewargs__",
    # x >
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
    "__rdivmod__",  #
    "__sizeof__",  #
    "__trunc__",  #
]
