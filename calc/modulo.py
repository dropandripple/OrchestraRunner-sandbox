"""Modulo operation for the calc package."""

from calc.errors import CalcError


def modulo(a, b):
    """Return ``a % b``.

    Raises:
        CalcError: if ``b == 0``.
    """
    if b == 0:
        raise CalcError("modulo by zero")
    return a % b
