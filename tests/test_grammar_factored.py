from chomchom import ContextFreeGrammar


def test_is_factored():
    g = ContextFreeGrammar.from_string('''
            S -> a S | a B | d S
            B -> b B | b
        ''')
    assert not g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S  -> a S1 | d S
            S1 -> S | B
            B  -> b B1
            B1 -> B | &
        ''')
    assert g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S -> A B | B C
            A -> a A | &
            B -> b B | d
            C -> c C | c
        ''')
    assert not g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S -> a A B | B C1
            A -> a A | &
            B -> b B | d
            C -> c C1
            C1 -> C | &
        ''')
    assert g.is_factored()


def test_factor():
    g = ContextFreeGrammar.from_string('''
            S -> a S | a B | d S
            B -> b B | b
        ''')
    assert not g.is_factored()
    g.factor(10)
    assert g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S  -> a S1 | d S
            S1 -> S | B
            B  -> b B1
            B1 -> B | &
        ''')
    assert g.is_factored()
    g.factor(10)
    assert g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S -> A B | B C
            A -> a A | &
            B -> b B | d
            C -> c C | c
        ''')
    assert not g.is_factored()
    g.factor(10)
    assert g.is_factored()

    g = ContextFreeGrammar.from_string('''
            S -> a A B | B C1
            A -> a A | &
            B -> b B | d
            C -> c C1
            C1 -> C | &
        ''')
    assert g.is_factored()
    g.factor(10)
    assert g.is_factored()
