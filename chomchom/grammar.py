from typing import List, Set, DefaultDict, NamedTuple
from typing import Iterable, Optional

from .symbol import Symbol, NonTerminalSymbol


class ProductionRule(NamedTuple):
    lhs: NonTerminalSymbol
    rhs: List[Symbol]


class ContextFreeGrammar:
    def __init__(
        self,
        production_rules: Iterable[ProductionRule],
        start_symbol=Optional[NonTerminalSymbol]
    ) -> None:
        self.production_rules = list(production_rules)

        if start_symbol is None:
            first_production = self.production_rules[0]
            start_symbol = first_production[0]

        self.start_symbol = start_symbol

        self.first = DefaultDict[Symbol, Set[Symbol]](set)
        self.follow = DefaultDict[Symbol, Set[Symbol]](set)

    @classmethod
    def from_string(cls, string: str) -> 'ContextFreeGrammar':
        production_rules: List[ProductionRule] = []

        for line in string.strip().splitlines():
            lhs, line_rhs = line.split('->')

            nt = NonTerminalSymbol(lhs.strip())

            for prod_rhs in line_rhs.split('|'):
                production = ProductionRule(nt, [])

                for symbol in prod_rhs.strip().split():
                    production.rhs.append(Symbol.from_string(symbol))

                production_rules.append(production)

        return cls(production_rules)

    # def calculate_first(self, symbol):
    #     self.first.clear()

    #     non_terminals = [lhs for lhs, rhs in self.production_rules]
    #     for symbol in non_terminals:
