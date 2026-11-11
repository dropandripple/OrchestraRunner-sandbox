"""Areas of simple shapes with finite, non-negative dimensions."""

import math

from calc.errors import CalcError


def _validate_dimension(value):
    if (
        not isinstance(value, (int, float))
        or (isinstance(value, float) and not math.isfinite(value))
        or value < 0
    ):
        raise CalcError("dimensions must be finite, non-negative int or float numbers")
    return int(value) if isinstance(value, bool) else value


def _finite_result(result):
    if isinstance(result, float) and not math.isfinite(result):
        raise CalcError("area result out of range")
    return result


def circle_area(r):
    """Return the area of a circle with radius r as a float."""
    r = _validate_dimension(r)
    try:
        result = math.pi * r * r
    except OverflowError as exc:
        raise CalcError("area result out of range") from exc
    return _finite_result(result)


def rectangle_area(w, h):
    """Return the area of a rectangle, preserving exact integer products."""
    w = _validate_dimension(w)
    h = _validate_dimension(h)
    try:
        result = w * h
    except OverflowError as exc:
        raise CalcError("area result out of range") from exc
    return _finite_result(result)


def triangle_area(base, height):
    """Return the area of a triangle as a float."""
    base = _validate_dimension(base)
    height = _validate_dimension(height)
    try:
        result = float(base) * float(height) / 2
    except OverflowError as exc:
        raise CalcError("area result out of range") from exc
    return _finite_result(result)


def total_area(shapes):
    """Return the sum of areas from a list of (kind, args) pairs."""
    if not isinstance(shapes, list):
        raise CalcError("shapes must be a list")
    operations = {
        "circle": (circle_area, 1),
        "rectangle": (rectangle_area, 2),
        "triangle": (triangle_area, 2),
    }
    total = 0
    for entry in shapes:
        try:
            kind, args = entry
        except (TypeError, ValueError) as exc:
            raise CalcError("shapes must contain (kind, args) pairs") from exc
        try:
            operation, count = operations[kind]
        except (KeyError, TypeError) as exc:
            raise CalcError("unknown shape kind") from exc
        try:
            arg_count = len(args)
        except TypeError as exc:
            raise CalcError("shape args must have the expected length") from exc
        if arg_count != count:
            raise CalcError("wrong number of shape arguments")
        try:
            dimensions = tuple(args)
        except TypeError as exc:
            raise CalcError("shape args must be iterable") from exc
        if len(dimensions) != count:
            raise CalcError("wrong number of shape arguments")
        area = operation(*dimensions)
        try:
            total = _finite_result(total + area)
        except OverflowError as exc:
            raise CalcError("area result out of range") from exc
    return total
