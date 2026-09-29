"""Exponentiation for the calc package."""

from calc.errors import CalcError


def power(base, exponent):
    """Return ``base ** exponent``.

    ``exponent`` must be an ``int`` with ``exponent >= 0``; otherwise
    ``calc.errors.CalcError`` is raised. On valid input the result is
    ``base ** exponent``.
    """
    if not isinstance(exponent, int) or exponent < 0:
        raise CalcError("exponent must be a non-negative int")
    return base ** exponent
