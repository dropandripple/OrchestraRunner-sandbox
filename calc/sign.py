"""Sign function for the calc package."""

from numbers import Real

from calc.errors import CalcError


def sign(x):
    """Return 1, -1 or 0 by the sign of ``x``; CalcError if not a real number."""
    if not isinstance(x, Real):
        raise CalcError("sign argument must be a number")
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
