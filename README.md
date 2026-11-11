# OrchestraRunner-sandbox

This is a synthetic OrchestraRunner sandbox. It contains no real code, no
private code and no credentials. It exists only to prove, against a real
protected branch, that OrchestraRunner can land exactly an approved commit
and that a different or unverified commit cannot land.

The `calc` package is deliberately tiny. `divide` leaves division by zero
unhandled on purpose.
Change whose required check is skipped (probe N4).
Change for probe N6 (reviews required).

## Additional operations

The operations below are re-exported from the top-level `calc`
package. Each raises `calc.errors.CalcError` on invalid input:

- `power(base, exponent)` returns `base ** exponent`. Raises `CalcError` if
  `exponent` is not an `int` or is negative.
- `modulo(a, b)` returns `a % b`. Raises `CalcError` if `b == 0`.
- `gcd(a, b)` returns the non-negative greatest common divisor. Raises
  `CalcError` if either argument is not an `int`, or if both are `0`. Bool
  inputs are accepted as the ints 0 and 1.
- `mean(values)` returns the arithmetic mean. Any finite iterable is accepted,
  except str/bytes/bytearray/memoryview/mappings. Elements must be finite int/float
  numbers; bools count as 0/1. Raises `CalcError` for empty, non-numeric,
  non-finite or out-of-range input. These input rules apply to all four statistics.
- `median(values)` returns the middle value in sorted order; for even-length
  input, it returns the mean of the two middle values.
- `variance(values)` returns the population variance (divide by n); a singleton
  gives 0.
- `summary(values)` returns a fresh dict with exactly the keys `mean`, `median`
  and `variance`, consuming the input once and applying the same input rules.
- `circle_area(r)` returns the circle area, pi times the radius squared, as a float.
  Geometry dimensions must be finite, non-negative int or float numbers, including
  zero; bools count as 0/1.
- `rectangle_area(w, h)` returns width times height, preserving exact int products.
- `triangle_area(base, height)` returns base times height divided by 2 as a float.
- `total_area(shapes)` sums a list of `(kind, args)` pairs: `circle` takes 1 argument,
  `rectangle` takes 2 arguments, and `triangle` takes 2 arguments.
  `total_area([])` returns 0. For example,
  `total_area([('circle', (1,)), ('rectangle', (2, 3)), ('triangle', (3, 4))])`
  returns approximately 15.14159. Invalid dimensions, malformed entries, unknown
  kinds, wrong argument counts, non-list inputs and overflow raise `CalcError`.
