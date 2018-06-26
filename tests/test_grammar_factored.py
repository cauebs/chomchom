from chomchom import ContextFreeGrammar, NonTerminal, Terminal, Epsilon


def test_is_factored_01():
    g = ContextFreeGrammar.from_string('''
            S -> a S | a B | d S
            B -> b B | b
        ''')

    assert g.is_factored() == False


def test_is_factored_02():
    g = ContextFreeGrammar.from_string('''
            S  -> a S1 | d S
            S1 -> S | B
            B  -> b B1
            B1 -> B | &
        ''')

    assert g.is_factored() == True


def test_is_factored_03():
    g = ContextFreeGrammar.from_string('''
            S -> A B | B C
            A -> a A | &
            B -> b B | d
            C -> c C | c
        ''')

    assert g.is_factored() == False


def test_is_factored_04():
    g = ContextFreeGrammar.from_string('''
            S -> a A B | B C1
            A -> a A | &
            B -> b B | d
            C -> c C1
            C1 -> C | &
        ''')

    assert g.is_factored() == True
