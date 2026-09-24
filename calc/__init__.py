"""Tiny synthetic calculator for the OrchestraRunner landing sandbox."""


def add(a, b):
    return a + b


def divide(a, b):
    # Division by zero is deliberately left unhandled (a seeded finding).
    return a / b
