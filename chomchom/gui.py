import PyQt5.QtWidgets as qtw
from PyQt5 import uic


class MainWindow(qtw.QMainWindow):
    def __init__(self, ctrl):
        super(MainWindow, self).__init__()
        self.ctrl = ctrl
        uic.loadUi('./chomchom/forms/chomchom.ui', self)

        self.combo_grammar.currentIndexChanged.connect(self.show_grammar)

        self.btn_add_grammar.clicked.connect(self.add_grammar)
        self.btn_grammar_info.clicked.connect(self.list_infos)
        self.btn_remove_lr.clicked.connect(self.eliminate_left_recursions)
        self.btn_to_proper.clicked.connect(self.to_proper)

        self.dial_steps.valueChanged.connect(self.factored_in)

    def update_combo_boxes(self, index):
        self.combo_grammar.addItem(f'G{index-1}')

    def append_output(self, string):
        old = self.output.toPlainText()
        self.output.setPlainText(string + '\n' + old)

    def add_grammar(self):
        string = self.input.toPlainText()
        self.ctrl.create_grammar_from_string(string)
        self.combo_grammar.setCurrentIndex(len(self.ctrl.grammars))

    def list_infos(self):
        index = self.combo_grammar.currentIndex()
        if index == 0:
            self.append_output('Selecione uma gramática da lista.')
            return

        self.ctrl.list_grammar_info(index-1)

    def to_proper(self):
        index = self.combo_grammar.currentIndex()-1

        self.ctrl.to_proper(index)

    def eliminate_left_recursions(self):
        index = self.combo_grammar.currentIndex()-1

        ...

    def factored_in(self):
        index = self.combo_grammar.currentIndex()-1
        steps = self.dial_steps.value()

        answer = self.ctrl.factored_in(index, steps)

        self.factorable_result.setText(answer)

    def show_grammar(self):
        index = self.combo_grammar.currentIndex()
        if index == 0:
            self.input.setPlainText('')

            self.btn_add_grammar.setEnabled(True)

            self.btn_grammar_info.setEnabled(False)
            self.btn_remove_lr.setEnabled(False)
            self.btn_to_proper.setEnabled(False)
            self.dial_steps.setEnabled(False)
            return

        self.factored_in()

        self.btn_add_grammar.setEnabled(False)

        self.btn_grammar_info.setEnabled(True)
        self.btn_remove_lr.setEnabled(True)
        self.btn_to_proper.setEnabled(True)
        self.dial_steps.setEnabled(True)

        grammar_as_string = str(self.ctrl.grammars[index-1])
        self.input.setPlainText(grammar_as_string)
