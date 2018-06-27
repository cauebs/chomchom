from chomchom import ContextFreeGrammar, NonTerminal


def test_n_sets():
    g = ContextFreeGrammar.from_string('''
        S -> F G H
        F -> G | a
        G -> d G | H | b
        H -> c
    ''')

    S, F, G, H = (NonTerminal(x) for x in 'SFGH')

    expected = {
        S: {S},
        F: {F, G, H},
        G: {G, H},
        H: {H},
    }

    assert g.simple_production_sets() == expected
