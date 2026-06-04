import pytest
from src.calculator import somma, sottrai, moltiplica, dividi, potenza


def test_somma():
    assert somma(2, 3) == 5


def test_sottrai():
    assert sottrai(10, 4) == 6


def test_moltiplica():
    assert moltiplica(3, 4) == 12


def test_dividi():
    assert dividi(10, 2) == 5


def test_dividi_per_zero():
    with pytest.raises(ValueError):
        dividi(10, 0)


def test_potenza():
    assert potenza(2, 3) == 8


# Test
