from typing import List, NamedTuple, Set, DefaultDict, Iterable

from itertools import combinations

from copy import deepcopy

from .symbol import Symbol, Terminal, Epsilon, NonTerminal, EoS
from .symbol import symbol_from_string, ParseError


class ProductionRule(NamedTuple):
    lhs: NonTerminal
    rhs: List[Symbol]


class ContextFreeGrammar:
    def __init__(
        self,
        production_rules: Iterable[ProductionRule],
        start_symbol: NonTerminal
    ) -> None:
        self.production_rules = (
            DefaultDict[NonTerminal, List[List[Symbol]]](list)
        )
        for lhs, rhs in production_rules:
            self.production_rules[lhs].append(rhs)

        self.start_symbol = start_symbol

        self.first = DefaultDict[Symbol, Set[Symbol]](set)
        self.follow = DefaultDict[Symbol, Set[Symbol]](set)
        self.calculate_follow()

    def copy(self) -> 'ContextFreeGrammar':
        return deepcopy(self)

    @classmethod
    def from_string(cls, string: str) -> 'ContextFreeGrammar':
        production_rules: List[ProductionRule] = []

        for i, line in enumerate(string.strip().splitlines()):
            try:
                lhs, line_rhs = line.split('->')
            except ValueError:
                raise ParseError(f'Expected a `->` on line {i+1}')

            nt = NonTerminal(lhs.strip())

            if i == 0:
                start_symbol = nt

            for prod_rhs in line_rhs.split('|'):
                production = ProductionRule(nt, [])

                for symbol in prod_rhs.strip().split():
                    production.rhs.append(symbol_from_string(symbol))

                if not production.rhs:
                    raise ParseError(
                        'Expected a sequence of symbols next to the `|`'
                        f'on line {i+1}'
                    )

                production_rules.append(production)

        return cls(production_rules, start_symbol)

    @property
    def terminals(self):
        terminals = set()
        for rhs in self.production_rules.values():
            for prod in rhs:
                for symbol in prod:
                    if isinstance(symbol, Terminal):
                        terminals.add(symbol)

        return terminals

    @property
    def non_terminals(self):
        return self.production_rules.keys()

    def list_nonfactoreds(self):
        for nt, prods in self.production_rules.items():
            for a, b in combinations(prods, 2):
                if self.first_of_string(a) & self.first_of_string(b):
                    yield (nt, a, b)

    def is_factored(self):
        if any(self.list_nonfactoreds()):
            return False
        return True

    def next_nonterminal_name(self, nonterminal):
        if nonterminal not in self.non_terminals:
            return nonterminal

        base = str(nonterminal)

        n = 1
        while NonTerminal(base + f'{n}') in self.non_terminals:
            n += 1

        return NonTerminal(base + f'{n}')

    def factor(self, n):
        i = 0
        current_grammar = self
        while i < n:
            if current_grammar.is_factored():
                return True
            i += 1

            # TODO
            # current_grammar = new_grammar

        return current_grammar.is_factored()

    def remove_unreachable(self):
        # Reachable symbols
        reachable = {self.start_symbol}

        while True:
            new_reachable = reachable.copy()

            for nt, rhs in self.production_rules.items():
                if nt in new_reachable:
                    for prod in rhs:
                        for symbol in prod:
                            new_reachable.add(symbol)

            if reachable == new_reachable:
                break
            reachable = new_reachable

        new_productions = [ProductionRule(
            lhs, rhs) for lhs, rhs in self.production_rules.items() if lhs in reachable]

        return ContextFreeGrammar(new_productions, self.start_symbol)

    def fertile(self):
        fertile = set()
        while True:
            new_fertile = fertile.copy()

            for nt, rhs in self.production_rules.items():
                for prod in rhs:
                    if set(prod).issubset(self.terminals | {Epsilon('&')} | fertile):
                        new_fertile.add(nt)

            if fertile == new_fertile:
                break
            fertile = new_fertile

        return new_fertile

    def is_empty(self):
        return self.start_symbol not in self.fertile()

    def first_of_string(self, string):
        first = set()

        for i, symbol in enumerate(string):
            if isinstance(symbol, NonTerminal):
                first = first.union(self.first[symbol] - set([Epsilon('&')]))
                if Epsilon('&') not in self.first[symbol]:
                    break
            elif isinstance(symbol, Terminal):
                first.add(symbol)
                break
        else:
            first.add(Epsilon('&'))

        return first

    def calculate_first(self):
        self.first.clear()
        first = {nt: set() for nt in self.non_terminals}

        for nt in self.non_terminals:
            for production in self.production_rules[nt]:
                first_symbol = production[0]
                if isinstance(first_symbol, Terminal) or isinstance(first_symbol, Epsilon):
                    first[nt].add(first_symbol)

        while True:
            new_first = first.copy()

            for nt in self.non_terminals:
                for production in self.production_rules[nt]:
                    for symbol in production:
                        if isinstance(symbol, NonTerminal):
                            if Epsilon('&') in new_first[symbol]:
                                new_first[nt] = new_first[nt].union(
                                    new_first[symbol] - set([Epsilon('&')]))
                            else:
                                new_first[nt] = new_first[nt].union(
                                    new_first[symbol])
                                break
                        elif isinstance(symbol, Terminal):
                            new_first[nt].add(symbol)
                            break
                    else:
                        new_first[nt].add(Epsilon('&'))

            if new_first == first:
                break
            first = new_first

        self.first = first

    def calculate_follow(self):
        self.calculate_first()

        self.follow.clear()
        follow = {nt: set() for nt in self.non_terminals}

        for nt in self.non_terminals:
            for production in self.production_rules[nt]:
                # FOLLOW(A) = {t | B -> xAty is a production}
                for i in range(0, len(production) - 1):
                    symbol = production[i]
                    next_symbol = production[i+1]

                    if (isinstance(symbol, NonTerminal) and
                            isinstance(next_symbol, Terminal)):
                        follow[symbol].add(next_symbol)

        follow[self.start_symbol].add(EoS('$'))

        while True:
            new_follow = follow.copy()
            for nt in self.non_terminals:
                for production in self.production_rules[nt]:
                    for i in range(0, len(production) - 1):
                        symbol = production[i]
                        next_symbol = production[i+1]

                        # if B -> xAy is a production
                        #   FOLLOW(A) = FOLLOW(A) U FIRST(y) - {&}
                        if (isinstance(symbol, NonTerminal) and isinstance(next_symbol, NonTerminal)):
                            new_follow[symbol] = new_follow[symbol].union(
                                self.first_of_string(production[i+1:]) - set([Epsilon('&')]))

                            # if B -> xAy is a production and & in FIRST(y)
                            #   FOLLOW(A) = FOLLOW(A) U FOLLOW(B)
                            if Epsilon('&') in self.first_of_string(production[i+1:]):
                                new_follow[symbol] = new_follow[symbol].union(
                                    new_follow[nt])

                    last_symbol = production[len(production) - 1]
                    if isinstance(last_symbol, NonTerminal):
                        new_follow[last_symbol] = new_follow[last_symbol].union(
                            new_follow[nt])

            if new_follow == follow:
                break
            follow = new_follow

        self.follow = follow
