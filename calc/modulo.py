"""Modulo operation for the calc package."""

from calc.errors import CalcError  # noqa: F401  (part of the documented contract)


def modulo(a, b):
    """Return ``a % b``.

    Raises:
        CalcError: if ``b == 0``.
    """
    raise NotImplementedError
