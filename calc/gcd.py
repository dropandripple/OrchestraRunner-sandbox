"""Greatest common divisor for the calc package."""

from calc.errors import CalcError


def gcd(a, b):
    """Return the greatest common divisor of ``a`` and ``b``.

    Both ``a`` and ``b`` must be ``int``; otherwise ``calc.errors.CalcError``
    is raised. If ``a == 0 and b == 0`` a ``CalcError`` is also raised, since
    the gcd of 0 and 0 is undefined. Otherwise the non-negative greatest
    common divisor of ``a`` and ``b`` is returned, computed with the
    Euclidean algorithm.
    """
    raise NotImplementedError
