from .gui import MainWindow


from typing import List

from .grammar import ContextFreeGrammar, ParseError
from pprint import pformat


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
                f'Gramática G{len(self.grammars)-1} criada com sucesso.')
        except (ParseError):
            self.main_window.append_output('Gramática inválida.')

    def to_proper(self, index: int):
        g = self.grammars[index]

        # 1. Transformar em &-livre
        g1, ne = g.to_epsilon_free()
        self.__append_grammar(g1)
        self.main_window.append_output(f'Ne: {pformat(ne)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} &-Livre criada.')

        # 2. Remover ciclos (Produções simples)

        # 3. Remover Símbolos inúteis
        g2, nf = g1.remove_infertile()
        self.__append_grammar(g2)
        self.main_window.append_output(f'NF: {pformat(nf)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} sem símbolos inférteis criada.')

        g3, vi = g2.remove_unreachable()
        self.__append_grammar(g3)
        self.main_window.append_output(f'vi: {pformat(vi)}\n')
        self.main_window.append_output(
            f'Gramática intermediária G{len(self.grammars)-1} sem símbolos inalcançáveis criada.')

    def list_grammar_info(self, index: int):
        g = self.grammars[index]

        g_info = f"Informações sobre G{index}:\n"

        # L(G) é vazia, infinitia ou finita
        g_info += f"L(G{index}) é "
        if g.is_empty():
            g_info += "vazia."
        elif g.is_infinite():
            g_info += "infinita."
        else:
            g_info += "finita."
        g_info += '\n\n'

        # FIRST(A)
        g_info += "Conjuntos FIRST:\n"
        g_info += pformat(g.first)
        g_info += '\n\n'

        # FOLLOW(A)
        g_info += "Conjuntos FOLLOW:\n"
        g_info += pformat(g.follow)
        g_info += '\n\n'

        # FIRST-NT(A)
        g_info += "Conjuntos FIRST-NT:\n"
        g_info += pformat(g.first_nt)
        g_info += '\n\n'

        # Está fatorada
        if g.is_factored():
            g_info += "G está fatorada\n"
        else:
            g_info += "G não está fatorada\n"
        g_info += '\n'

        self.main_window.append_output(g_info)
