from typing import List, NamedTuple, Dict, Set, DefaultDict, Iterable, KeysView

from itertools import combinations

from copy import deepcopy

from .utils import powerset

from .symbol import Symbol, Terminal, Epsilon, NonTerminal, EoS
from .symbol import symbol_from_string, ParseError

EPSILON = Epsilon('&')


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
        self.first_nt = DefaultDict[Symbol, Set[Symbol]](set)
        self.follow = DefaultDict[Symbol, Set[Symbol]](set)
        self.calculate_follow()
        self.calculate_first_nt()

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

    def __str__(self):
        return '\n'.join(
            f'{nt} -> ' + ' | '.join(
                ' '.join(
                    str(symbol)
                    for symbol in prod
                )
                for prod in productions
            )
            for nt, productions in self.production_rules.items()
        )

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
    def non_terminals(self) -> KeysView['NonTerminal']:
        return self.production_rules.keys()

    def find_nondeterminisms(self):
        for nt, prods in self.production_rules.copy().items():
            for a, b in combinations(prods, 2):
                if self.first_of_string(a) & self.first_of_string(b):
                    yield (nt, a, b)

    def is_factored(self) -> bool:
        return not any(self.find_nondeterminisms())

    def next_nonterminal_name(self, nt: NonTerminal) -> NonTerminal:
        n = 1
        while NonTerminal(f'{nt}{n}') in self.non_terminals:
            n += 1

        return NonTerminal(f'{nt}{n}')

    def derivations(self, sentence: List[Symbol]):
        for i, symbol in enumerate(sentence):
            if isinstance(symbol, NonTerminal):

                for prod in self.production_rules[symbol]:
                    derivation = [
                        *sentence[:i],
                        *[s for s in prod if s != Epsilon('&')],
                        *sentence[i+1:]
                    ]
                    yield derivation or Epsilon('&')

    def remove_direct_non_determinism(
        self,
        nt: NonTerminal,
        a: List[Symbol],
        b: List[Symbol],
    ):
        common = a[0]
        assert common == b[0]

        self.production_rules[nt].remove(a)
        self.production_rules[nt].remove(b)

        new_nt = self.next_nonterminal_name(nt)

        self.production_rules[nt].append([common, new_nt])
        self.production_rules[new_nt].append(a[1:])
        self.production_rules[new_nt].append(b[1:])

    def remove_indirect_non_determinism(
        self,
        nt: NonTerminal,
        a: List[Symbol],
        b: List[Symbol],
    ):
        ...

    def simple_production_sets(self) -> Dict[NonTerminal, Set[NonTerminal]]:
        ns = {nt: {nt} for nt in self.production_rules}

        for lhs, productions in self.production_rules.items():
            for rhs in productions:
                if len(rhs) == 1 and isinstance(rhs[0], NonTerminal):
                    for nt in ns[rhs[0]]:
                        ns[lhs].add(nt)

                        for other_nt, other_set in ns.items():
                            if lhs in other_set:
                                other_set.add(nt)

        return ns

    def without_simple_productions(self) -> 'ContextFreeGrammar':
        new_productions = []

        for lhs, other_nts in self.simple_production_sets().items():
            for other_nt in other_nts:
                for rhs in self.production_rules[other_nt]:
                    if len(rhs) > 1 or not isinstance(rhs[0], NonTerminal):
                        new_productions.append(ProductionRule(lhs, rhs))

        return ContextFreeGrammar(new_productions, self.start_symbol)

    def factor(self, max_steps):
        for _ in range(max_steps):
            if self.is_factored():
                return True

            for nt, a, b in self.find_nondeterminisms():
                if a[0] == b[0]:
                    self.remove_direct_non_determinism(nt, a, b)
                else:
                    self.remove_indirect_non_determinism(nt, a, b)

        return self.is_factored()

    def to_epsilon_free(self):
        ne: Set['NonTerminal'] = {nt for nt in self.non_terminals if [
            EPSILON] in self.production_rules[nt]}

        while True:
            new_ne = ne.copy()

            for lhs, rhs in self.production_rules.items():
                for prod in rhs:
                    if set(prod).issubset(new_ne):
                        new_ne.add(lhs)

            if ne == new_ne:
                break
            ne = new_ne

        new_productions: List['ProductionRule'] = [ProductionRule(lhs, rhs)
                                                   for lhs, prods in self.production_rules.items()
                                                   for rhs in prods
                                                   if rhs != [EPSILON]]

        for lhs, prods in self.production_rules.items():
            for rhs in prods:
                if set(rhs).intersection(set(ne)) != set():
                    idxs = [i
                            for i, x in enumerate(rhs)
                            if x in ne]
                    for subset in powerset(idxs):
                        if not subset:
                            continue
                        new_rhs = [s
                                   for i, s in enumerate(rhs)
                                   if i not in subset]
                        if not new_rhs:
                            continue
                        new_productions.append(ProductionRule(lhs, new_rhs))

        if self.start_symbol in ne:
            new_start = self.next_nonterminal_name(self.start_symbol)
            prods = [[self.start_symbol], [EPSILON]]
            new_productions += [ProductionRule(new_start, rhs)
                                for rhs in prods]

            return ContextFreeGrammar(new_productions, new_start), ne

        return ContextFreeGrammar(new_productions, self.start_symbol), ne

    def remove_unreachable(self):
        # Reachable symbols
        reachable: Set['Symbol'] = {self.start_symbol}

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

            new_productions = [
                ProductionRule(lhs, rhs)
                for lhs, prods in self.production_rules.items()
                for rhs in prods
                if lhs in reachable
            ]

        return ContextFreeGrammar(new_productions, self.start_symbol), reachable

    def remove_useless(self) -> 'ContextFreeGrammar':
        return self.remove_infertile().remove_unreachable()

    def remove_infertile(self):
        if self.is_empty():
            s = NonTerminal('S')
            return ContextFreeGrammar([ProductionRule(s, [s])], s)

        fertile = self.fertile()

        new_productions = []
        for lhs, rhs in self.production_rules.items():
            for prod in rhs:
                if set(prod).issubset(fertile | self.terminals | {EPSILON}):
                    new_productions.append(ProductionRule(lhs, prod))

        return ContextFreeGrammar(new_productions, self.start_symbol), fertile

    def fertile(self) -> Set['NonTerminal']:
        fertile: Set['NonTerminal'] = set()
        while True:
            new_fertile = fertile.copy()

            for nt, rhs in self.production_rules.items():
                for prod in rhs:
                    if set(prod).issubset(self.terminals | {EPSILON} | fertile):
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
                first = first.union(self.first[symbol] - set([EPSILON]))
                if EPSILON not in self.first[symbol]:
                    break
            elif isinstance(symbol, Terminal):
                first.add(symbol)
                break
        else:
            first.add(EPSILON)

        return first

    def calculate_first_nt(self):
        self.first_nt.clear()
        first_nt = {nt: set() for nt in self.non_terminals}

        for nt in self.non_terminals:
            for production in self.production_rules[nt]:
                first_symbol = production[0]
                if (isinstance(first_symbol, NonTerminal) or
                        isinstance(first_symbol, Epsilon)):
                    first_nt[nt].add(first_symbol)

        while True:
            new_first = first_nt.copy()

            for nt in self.non_terminals:
                for production in self.production_rules[nt]:
                    for symbol in production:
                        if isinstance(symbol, NonTerminal):
                            if EPSILON in new_first[symbol]:
                                new_first[nt] = new_first[nt].union(
                                    new_first[symbol] -
                                    {EPSILON} |
                                    {symbol})
                            else:
                                new_first[nt] = new_first[nt].union(
                                    new_first[symbol] | {symbol})
                                break
                        elif isinstance(symbol, Terminal):
                            break
                    else:
                        new_first[nt].add(EPSILON)

            if new_first == first_nt:
                break
            first_nt = new_first

        self.first_nt = first_nt

    def calculate_first(self):
        self.first.clear()
        first = {nt: set() for nt in self.non_terminals}

        for nt in self.non_terminals:
            for production in self.production_rules[nt]:
                first_symbol = production[0]
                if (isinstance(first_symbol, Terminal) or
                        isinstance(first_symbol, Epsilon)):
                    first[nt].add(first_symbol)

        while True:
            new_first = first.copy()

            for nt in self.non_terminals:
                for production in self.production_rules[nt]:
                    for symbol in production:
                        if isinstance(symbol, NonTerminal):
                            if EPSILON in new_first[symbol]:
                                new_first[nt] = new_first[nt].union(
                                    new_first[symbol] - {EPSILON})
                            else:
                                new_first[nt] |= new_first[symbol]
                                break
                        elif isinstance(symbol, Terminal):
                            new_first[nt].add(symbol)
                            break
                    else:
                        new_first[nt].add(EPSILON)

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
                        if (isinstance(symbol, NonTerminal) and
                                isinstance(next_symbol, NonTerminal)):
                            new_follow[symbol] = new_follow[symbol].union(self.first_of_string(
                                production[i+1:]) - {EPSILON})

                            # if B -> xAy is a production and & in FIRST(y)
                            #   FOLLOW(A) = FOLLOW(A) U FOLLOW(B)
                            if EPSILON in self.first_of_string(production[i+1:]):
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
