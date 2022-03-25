"""This module defines ACM types and checks types at runtime. """

# define type aliases that approximate Maple types
nonnegint = int
posint = int


def require_int(name: str, value: int) -> bool:
    if type(value) is not int:
        raise TypeError(f'type of {name} is not an int: {value}')
    return True


def require_nonnegint(name: str, value: nonnegint) -> bool:
    require_int(name, value)
    if value < 0:
        raise ValueError(f'value of {name} is not a nonnegative integer: {value}')
    return True


def require_posint(name: str, value: posint) -> bool:
    require_nonnegint(name, value)
    if value == 0:
        raise ValueError(f'value of {name} is not a positive integer: {value}')
    return True
