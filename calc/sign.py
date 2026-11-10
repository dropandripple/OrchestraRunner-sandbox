"""Sign function for the calc package."""

from calc.errors import CalcError


def sign(x):
    """Return 1, -1, or 0 for a positive, negative, or zero number."""
    if not isinstance(x, (int, float)):
        raise CalcError("sign argument must be a number")
    return (x > 0) - (x < 0)
