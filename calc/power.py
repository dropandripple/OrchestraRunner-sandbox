"""Exponentiation for the calc package."""

from calc.errors import CalcError  # noqa: F401  (raised once implemented)


def power(base, exponent):
    """Return ``base ** exponent``.

    ``exponent`` must be an ``int`` with ``exponent >= 0``; otherwise
    ``calc.errors.CalcError`` is raised. On valid input the result is
    ``base ** exponent``.
    """
    raise NotImplementedError
