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

`power`, `modulo` and `gcd` are re-exported from the top-level `calc`
package. Each raises `calc.errors.CalcError` on invalid input:

- `power(base, exponent)` returns `base ** exponent`. Raises `CalcError` if
  `exponent` is not an `int` or is negative.
- `modulo(a, b)` returns `a % b`. Raises `CalcError` if `b == 0`.
- `gcd(a, b)` returns the non-negative greatest common divisor. Raises
  `CalcError` if either argument is not an `int`, or if both are `0`. Bool
  inputs are accepted as the ints 0 and 1.
