"""Tiny synthetic calculator for the OrchestraRunner landing sandbox."""

from calc.gcd import gcd
from calc.modulo import modulo
from calc.power import power


def add(a, b):
    return a + b


def divide(a, b):
    # Division by zero is deliberately left unhandled (a seeded finding).
    return a / b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b
