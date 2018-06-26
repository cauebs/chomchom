from chomchom import ContextFreeGrammar, NonTerminal, Terminal, Epsilon, EoS


def test_first_01():
    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    d = Terminal('d')
    epsilon = Epsilon('&')

    string = '''S -> A B C
                A -> a A | &
                B -> b B | A C d
                C -> c C | &'''

    g = ContextFreeGrammar.from_string(string)

    g.calculate_first()

    expected_first = {
        NonTerminal('S'): set([a, b, c, d]),
        NonTerminal('A'): set([a, epsilon]),
        NonTerminal('B'): set([a, b, c, d]),
        NonTerminal('C'): set([c, epsilon])
    }

    assert g.first == expected_first


def test_first_02():
    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    d = Terminal('d')
    e = Terminal('e')
    epsilon = Epsilon('&')

    string = '''S -> A C | C e B | B a
                A -> a A | B C
                C -> c C | &
                B -> b B | A B | &'''

    g = ContextFreeGrammar.from_string(string)

    g.calculate_first()

    expected_first = {
        NonTerminal('S'): set([a, b, c, e, epsilon]),
        NonTerminal('A'): set([a, b, c, epsilon]),
        NonTerminal('C'): set([c, epsilon]),
        NonTerminal('B'): set([a, b, c, epsilon]),
    }

    assert g.first == expected_first


def test_first_of_string():
    string = '''S -> A B C
                A -> a A | &
                B -> b B | A C d
                C -> c C | &'''

    g = ContextFreeGrammar.from_string(string)

    g.calculate_first()

    expected = set({Terminal('c'), Terminal('d')})

    got = g.first_of_string([NonTerminal('C'), Terminal('d')])

    assert got == expected


def test_follow_01():
    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    d = Terminal('d')
    eos = EoS('$')

    string = '''S -> A B C
                A -> a A | &
                B -> b B | A C d
                C -> c C | &'''

    g = ContextFreeGrammar.from_string(string)

    g.calculate_follow()

    expected_follow = {
        NonTerminal('S'): set([eos]),
        NonTerminal('A'): set([a, b, c, d]),
        NonTerminal('B'): set([c, eos]),
        NonTerminal('C'): set([d, eos])
    }

    assert g.follow == expected_follow


def test_follow_02():
    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    d = Terminal('d')
    e = Terminal('e')
    eos = EoS('$')

    string = '''S -> A C | C e B | B a
                A -> a A | B C
                C -> c C | &
                B -> b B | A B | &'''

    g = ContextFreeGrammar.from_string(string)

    g.calculate_follow()

    expected_follow = {
        NonTerminal('S'): set([eos]),
        NonTerminal('A'): set([a, b, c, eos]),
        NonTerminal('C'): set([a, b, c, e, eos]),
        NonTerminal('B'): set([a, b, c, eos]),
    }

    assert g.follow == expected_follow
