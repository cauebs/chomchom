from typing import List, NamedTuple, Set, DefaultDict
from typing import Iterable, Optional

from .symbol import Symbol, NonTerminal, symbol_from_string


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

    @classmethod
    def from_string(cls, string: str) -> 'ContextFreeGrammar':
        production_rules: List[ProductionRule] = []

        for i, line in enumerate(string.strip().splitlines()):
            lhs, line_rhs = line.split('->')

            nt = NonTerminal(lhs.strip())

            if i == 0:
                start_symbol = nt

            for prod_rhs in line_rhs.split('|'):
                production = ProductionRule(nt, [])

                for symbol in prod_rhs.strip().split():
                    production.rhs.append(symbol_from_string(symbol))

                production_rules.append(production)

        return cls(production_rules, start_symbol)

    def calculate_first(self, symbol):
        self.first.clear()
        # for lhs, rhs in self.production_rules:
