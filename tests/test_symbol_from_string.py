from pytest import raises

from chomchom.symbol import symbol_from_string, ParseError
from chomchom.symbol import NonTerminal, Terminal, Epsilon, EoS


def test_valid_non_terminal():
    assert isinstance(symbol_from_string('F'), NonTerminal)
    assert isinstance(symbol_from_string('X123'), NonTerminal)
    assert isinstance(symbol_from_string('A4'), NonTerminal)
    assert isinstance(symbol_from_string('E8266'), NonTerminal)


def test_valid_terminal():
    assert isinstance(symbol_from_string('f'), Terminal)
    assert isinstance(symbol_from_string('x123'), Terminal)
    assert isinstance(symbol_from_string('+'), Terminal)
    assert isinstance(symbol_from_string('esp8266'), Terminal)


def test_valid_epsilon():
    assert isinstance(symbol_from_string('&'), Epsilon)


def test_valid_end_of_string():
    assert isinstance(symbol_from_string('$'), EoS)


def test_invalid_symbol():
    for s in [
        'Aa', 'BB', 'cC',
        'A&', '$B', "C'",
        ' A', 'B ', ' C ',
        ' a', 'b ', ' c ',
        ' &', '& ', ' & ',
        ' $', '$ ', ' $ ',
    ]:
        with raises(ParseError):
            symbol_from_string(s)
