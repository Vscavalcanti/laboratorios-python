"""C6 — Comparação dados_ordenados.csv / dados_aleatorios.csv"""
import pandas as pd


class No:
    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None
        self.alt = 1


def altura(no):
    if no is None:
        return 0
    return 1 + max(altura(no.esq), altura(no.dir))


def contar_nos(no):
    if no is None:
        return 0
    return 1 + contar_nos(no.esq) + contar_nos(no.dir)


#BST 
def inserir_bst(no, chave):
    if no is None:
        return No(chave)
    if chave < no.chave:
        no.esq = inserir_bst(no.esq, chave)
    elif chave > no.chave:
        no.dir = inserir_bst(no.dir, chave)
    return no


#AVL 
def h(no):
    return no.alt if no else 0


def atualizar(no):
    no.alt = 1 + max(h(no.esq), h(no.dir))


def rot_direita(y):
    x = y.esq
    y.esq = x.dir
    x.dir = y
    atualizar(y); atualizar(x)
    return x


def rot_esquerda(x):
    y = x.dir
    x.dir = y.esq
    y.esq = x
    atualizar(x); atualizar(y)
    return y


def inserir_avl(no, chave):
    if no is None:
        return No(chave)
    if chave < no.chave:
        no.esq = inserir_avl(no.esq, chave)
    elif chave > no.chave:
        no.dir = inserir_avl(no.dir, chave)
    else:
        return no
    atualizar(no)
    fb = h(no.esq) - h(no.dir)
    if fb > 1 and chave < no.esq.chave:
        return rot_direita(no)
    if fb < -1 and chave > no.dir.chave:
        return rot_esquerda(no)
    if fb > 1 and chave > no.esq.chave:
        no.esq = rot_esquerda(no.esq)
        return rot_direita(no)
    if fb < -1 and chave < no.dir.chave:
        no.dir = rot_direita(no.dir)
        return rot_esquerda(no)
    return no


def main():
    linhas = []
    for arquivo in ["dados_ordenados.csv", "dados_aleatorios.csv"]:
        df = pd.read_csv(arquivo, encoding="utf-8-sig")
        codigos = [int(c) for c in df["codigo"]]       # ordem original
        raiz_bst, raiz_avl = None, None
        for c in codigos:
            raiz_bst = inserir_bst(raiz_bst, c)
            raiz_avl = inserir_avl(raiz_avl, c)
        linhas.append(("BST", arquivo, contar_nos(raiz_bst), altura(raiz_bst)))
        linhas.append(("AVL", arquivo, contar_nos(raiz_avl), altura(raiz_avl)))

    print(f"{'Estrutura':<11}{'Arquivo':<24}{'Nós':>5}{'Altura':>8}")
    print("-" * 48)
    for estrutura, arquivo, nos, alt in linhas:
        print(f"{estrutura:<11}{arquivo:<24}{nos:>5}{alt:>8}")
    print("-" * 48)
    print("Referências para n = 20: altura mínima possível = 5 (⌈log2(21)⌉), máxima = 20")


if __name__ == "__main__":
    main()
