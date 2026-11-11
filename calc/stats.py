"""Basic statistics for finite numeric iterables."""

from collections.abc import Mapping
import math
import statistics

from calc.errors import CalcError


def _as_numeric_list(values) -> list:
    """Return an independent, validated snapshot of the input."""
    if isinstance(values, (str, bytes, bytearray, memoryview, Mapping)):
        raise CalcError("values must be a numeric iterable")
    try:
        it = iter(values)
    except TypeError as exc:
        raise CalcError("values must be a numeric iterable") from exc

    snapshot = []
    for value in it:
        if not isinstance(value, (int, float)) or (
            isinstance(value, float) and not math.isfinite(value)
        ):
            raise CalcError("values must contain only finite int or float numbers")
        snapshot.append(int(value) if isinstance(value, bool) else value)
    if not snapshot:
        raise CalcError("values must not be empty")
    return snapshot


def _finite_result(result):
    if isinstance(result, float) and not math.isfinite(result):
        raise CalcError("statistics result out of range")
    return result


def mean(values):
    """Return the arithmetic mean of the values."""
    snapshot = _as_numeric_list(values)
    try:
        result = statistics.mean(snapshot)
    except (OverflowError, statistics.StatisticsError) as exc:
        raise CalcError("statistics result out of range") from exc
    return _finite_result(result)


def median(values):
    """Return the middle value, averaging the middle pair for even lengths."""
    ordered = sorted(_as_numeric_list(values))
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    try:
        result = statistics.mean(ordered[middle - 1:middle + 1])
    except (OverflowError, statistics.StatisticsError) as exc:
        raise CalcError("statistics result out of range") from exc
    return _finite_result(result)


def variance(values):
    """Return the population variance of the values."""
    snapshot = _as_numeric_list(values)
    try:
        result = statistics.pvariance(snapshot)
    except (OverflowError, statistics.StatisticsError) as exc:
        raise CalcError("statistics result out of range") from exc
    return _finite_result(result)
