from pytest import raises

from chomchom import ContextFreeGrammar, ParseError



def test_valid():
    string = ('E -> E + T | E - T | T'
              'T -> T * F | T / F | F'
              'F -> ( E ) | id'

    with raises(ParseError):
