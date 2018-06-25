

## Funcionalidades
1. Verificar se L(G) é vazia, finita ou infinita
    - Vazia: Inicial não é fértil
    - Finita: A partir de um não terminal, não é possível voltar a ele
1. GLC -> GLC Própria
    1. Transformar em &-livre
    2. Remover ciclos (Produções simples)
    3. Remover Símbolos inúteis
        1. Encontrar Não-Terminais férteis
        2. Eliminar símbolos inalcançáveis
2. FIRST(A)
3. FOLLOW(A)
4. FIRST-NT(A)
5. Verificar se GLC está fatorada
    1. Verificar se GLC é fatorável em **n** passos
6. Verificar se GLC possui ou não recursão à esquerda
    1. Identificar os tipos das recursões(direta/indireta)
    2. Eliminar recursões