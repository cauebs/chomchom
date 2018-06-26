from pytest import raises

from chomchom import ContextFreeGrammar, ParseError


def test_valid():
    ContextFreeGrammar.from_string(
        'E -> E + T | E - T | T\n'
        'T -> T * F | T / F | F\n'
        'F -> ( E ) | id'
    )

    ContextFreeGrammar.from_string(
        'E -> T E1\n'
        'E1 -> + T E1 | &\n'
        'T -> F T1\n'
        'T1 -> * F T1 | &\n'
        'F -> ( E ) | id'
    )


def test_valid_with_whitespace():
    ContextFreeGrammar.from_string('''
        E -> E + T | E - T | T
        T -> T * F | T / F | F
        F -> ( E ) | id
    ''')

    ContextFreeGrammar.from_string('''
        E -> T E1
        E1 -> + T E1 | &
        T -> F T1
        T1 -> * F T1 | &
        F -> ( E ) | id
    ''')


def test_invalid_spacing():
    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E -> E+T | E-T | T\n'
            'T -> T*F | T/F | F\n'
            'F -> (E) | id'
        )

    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E -> T E1'
            'E1 -> T E1 | &'
            'T -> F T1'
            'T1 -> * FT1 | &'
            'F -> ( E ) | id'
        )


def test_invalid_syntax():
    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E + T | E - T | T\n'
            'T -> T * F | T / F | F\n'
            'F -> ( E ) | id'
        )

    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E -> T E1\n'
            'E1 ->'
            'T -> F T1\n'
            'T1 -> * F T1 | &\n'
            'F -> ( E ) | id'
        )

    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E -> E + T | E - T | T\n'
            'T -> T * F | T / F |\n'
            'F -> ( E ) | id'
        )

    with raises(ParseError):
        ContextFreeGrammar.from_string(
            'E -> T E1\n'
            'E1 -> + T E1 | &\n'
            'T -> F T1\n'
            'T1 -> | &\n'
            'F -> ( E ) | id'
        )
