"""Greatest common divisor for the calc package."""

from calc.errors import CalcError


def gcd(a, b):
    """Return the greatest common divisor of ``a`` and ``b``.

    Both ``a`` and ``b`` must be ``int``; otherwise ``calc.errors.CalcError``
    is raised. If ``a == 0 and b == 0`` a ``CalcError`` is also raised, since
    the gcd of 0 and 0 is undefined. Otherwise the non-negative greatest
    common divisor of ``a`` and ``b`` is returned, computed with the
    Euclidean algorithm. Bool inputs are accepted as the ints 0 and 1.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise CalcError("gcd arguments must be int")
    if a == 0 and b == 0:
        raise CalcError("gcd(0, 0) is undefined")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
