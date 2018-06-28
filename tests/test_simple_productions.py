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


def test_remove_simple_productions():
    g = ContextFreeGrammar.from_string('''
        S -> F G H
        F -> G | a
        G -> d G | H | b
        H -> c
    ''')

    expected = ContextFreeGrammar.from_string('''
        S -> F G H
        F -> a | d G | b | c
        G -> d G | b | c
        H -> c
    ''')

    new_grammar = g.without_simple_productions()
    new_productions = sorted(
        (lhs, sorted(rhs))
        for lhs, rhs in new_grammar.production_rules.items()
    )

    expected_productions = sorted(
        (lhs, sorted(rhs))
        for lhs, rhs in expected.production_rules.items()
    )

    assert new_productions == expected_productions
