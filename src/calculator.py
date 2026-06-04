def somma(a, b):
    return a + b


def sottrai(a, b):
    return a - b


def moltiplica(a, b):
    return a * b


def dividi(a, b):
    if b == 0:
        raise ValueError("Non puoi dividere per zero")
    return a / b


def potenza(a, b):
    return a**b + 7
