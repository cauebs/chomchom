from pprint import pprint
from chomchom import ContextFreeGrammar

g1 = ContextFreeGrammar.from_string('''
        S  -> a S1 | d S
        S1 -> S | B
        B  -> b B1
        B1 -> B | &
     ''')

g2 = ContextFreeGrammar.from_string('''
        S -> A B | B C
        A -> a A | &
        B -> b B | d
        C -> c C | c
     ''')

g3 = ContextFreeGrammar.from_string('''
        S -> a S | B C | B D
        A -> c C | A B
        B -> b B | &
        C -> a A | B C
        D -> d D d | c
     ''')

# Empty grammar
g4 = ContextFreeGrammar.from_string('''
        S -> a S
     ''')

g5 = ContextFreeGrammar.from_string('''
        S -> a S a | d D d
        A -> a B | C c | a
        B -> d D | b B | b
        C -> A a | d D | c
        D -> b b B | d
     ''')

# Has useless symbols
g6 = ContextFreeGrammar.from_string('''
        S -> a F G | b F d | S a
        A -> a A | &
        B -> c G | a C G
        C -> c B a | c a | &
        D -> d C c | &
        F -> b F d | a C | A b | G A
        G -> B c | B C a
     ''')

# Has epsilon productions
g7 = ContextFreeGrammar.from_string('''
        S -> A B
        A -> a A | &
        B -> b B | &
     ''')

# Has epsilon productions
g8 = ContextFreeGrammar.from_string('''
        S -> c S c | B A
        A -> a A | A B C | &
        B -> b B | C A | &
        C -> c C c | A S
     ''')

# Has epsilon productions
g9 = ContextFreeGrammar.from_string('''
        S -> A z A
        A -> a | &
     ''')

g10 = ContextFreeGrammar.from_string('''
        S -> A b | A B c
        B -> b B | A d | &
        A -> a A | &
     ''')

g11 = ContextFreeGrammar.from_string('''
        S -> A B C
        A -> a A | &
        B -> b B | A C d
        C -> c C | &
      ''')
