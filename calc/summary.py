"""Combined statistics for finite numeric iterables."""

from calc.stats import _as_numeric_list, mean, median, variance


def summary(values):
    """Return mean, median and population variance from one input snapshot."""
    data = _as_numeric_list(values)
    return {"mean": mean(data), "median": median(data), "variance": variance(data)}
