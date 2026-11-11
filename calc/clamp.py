"""Clamp a value to a closed range."""

from calc.errors import CalcError


def clamp(value, low, high):
    if low > high:
        raise CalcError("low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value
