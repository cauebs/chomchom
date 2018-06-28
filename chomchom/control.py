from .gui import MainWindow

from pprint import pformat

from typing import List

from .grammar import ContextFreeGrammar, ParseError
from .utils import format_dict


class Control:
    def __init__(self):
        self.main_window = MainWindow(self)
        self.grammars: List[ContextFreeGrammar] = []

        self.main_window.show()

    def __append_grammar(self, grammar):
        self.grammars.append(grammar)
        self.main_window.update_combo_boxes(len(self.grammars))

    def create_grammar_from_string(self, string):
        try:
            g = ContextFreeGrammar.from_string(string)
            self.grammars.append(g)
            self.main_window.update_combo_boxes(len(self.grammars))
            self.main_window.append_output(
                f'Gramática G{len(self.grammars)-1} criada com sucesso.\n')
        except (ParseError):
            self.main_window.append_output('Gramática inválida.\n')

    def to_proper(self, index: int):
        g = self.grammars[index]

        # 1. Transformar em &-livre
        g1, ne = g.to_epsilon_free()
        self.__append_grammar(g1)
        self.main_window.append_output(f'Ne: {pformat(ne)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} &-Livre criada.')

        # 2. Remover ciclos (Produções simples)
        ns = g1.simple_production_sets()
        g2 = g1.without_simple_productions()
        self.__append_grammar(g1)
        self.main_window.append_output(f'Ne: {pformat(ns)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} &-Livre criada.')

        # 3. Remover Símbolos inúteis
        g3, nf = g2.remove_infertile()
        self.__append_grammar(g2)
        self.main_window.append_output(f'NF: {pformat(nf)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} sem símbolos inférteis criada.')

        g4, vi = g3.remove_unreachable()
        self.__append_grammar(g3)
        self.main_window.append_output(f'vi: {pformat(vi)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} sem símbolos inalcançáveis criada.')

    def factored_in(self, index: int, steps: int):
        g = self.grammars[index].copy()

        if g.factor(steps):
            return "Sim"
        return "Não"

    def list_grammar_info(self, index: int):
        g = self.grammars[index]

        g_info = f"Informações sobre G{index}:\n"

        # L(G) é vazia, infinitia ou finita
        g_info += f"L(G{index}) é "
        if g.is_empty():
            g_info += "vazia."
        else:
            g_info += "infinita."
        # elif g.is_infinite():
        #     g_info += "infinita."
        # else:
        #     g_info += "finita."
        g_info += '\n\n'

        # FIRST(A)
        g_info += "Conjuntos FIRST:\n"
        g_info += format_dict(g.first, 'FIRST')
        g_info += '\n\n'

        # FOLLOW(A)
        g_info += "Conjuntos FOLLOW:\n"
        g_info += format_dict(g.follow, 'FOLLOW')
        g_info += '\n\n'

        # FIRST-NT(A)
        g_info += "Conjuntos FIRST-NT:\n"
        g_info += format_dict(g.first_nt, 'FIRST-NT')
        g_info += '\n\n'

        # Está fatorada
        if g.is_factored():
            g_info += f"G{index} está fatorada\n"
        else:
            g_info += f"G{index} não está fatorada\n"
        g_info += '\n'

        self.main_window.append_output(g_info)
