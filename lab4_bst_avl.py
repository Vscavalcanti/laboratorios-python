"""Lab 4 — BST x AVL:impacto do balanceamento
"""
from collections import deque
import pandas as pd


def ler_codigos(arquivo):
    df = pd.read_csv(arquivo, encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    col = "codigo" if "codigo" in df.columns else df.columns[0]
    return [int(v) for v in df[col]]   # exatamente na ordem


# ---------------- BST ----------------
class NoBST:
    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None


class BST:
    """Inserção iterativa: com dados ordenados a árvore vira uma 'lista' e a
    recursão estouraria o limite do Python."""
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = NoBST(chave)
            return
        atual = self.raiz
        while True:
            if chave < atual.chave:
                if atual.esq is None:
                    atual.esq = NoBST(chave); return
                atual = atual.esq
            elif chave > atual.chave:
                if atual.dir is None:
                    atual.dir = NoBST(chave); return
                atual = atual.dir
            else:
                return  # chave duplicada é ignorada

    def altura(self):
        """Conta níveis com BFS (sem recursão)."""
        if self.raiz is None:
            return 0
        nivel, fila = 0, deque([self.raiz])
        while fila:
            nivel += 1
            for _ in range(len(fila)):
                no = fila.popleft()
                if no.esq: fila.append(no.esq)
                if no.dir: fila.append(no.dir)
        return nivel

    def buscar(self, chave):
        """Retorna (encontrou, nº de comparações com nós visitados)."""
        atual, comps = self.raiz, 0
        while atual:
            comps += 1
            if chave == atual.chave:
                return True, comps
            atual = atual.esq if chave < atual.chave else atual.dir
        return False, comps


# ---------------- AVL ----------------
class NoAVL:
    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None
        self.alt = 1


def h(no):
    return no.alt if no else 0


def atualizar(no):
    no.alt = 1 + max(h(no.esq), h(no.dir))


def fator(no):
    return h(no.esq) - h(no.dir)


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


class AVL:
    def __init__(self):
        self.raiz = None
        self.rotacoes = 0

    def inserir(self, chave):
        self.raiz = self._inserir(self.raiz, chave)

    def _inserir(self, no, chave):
        if no is None:
            return NoAVL(chave)
        if chave < no.chave:
            no.esq = self._inserir(no.esq, chave)
        elif chave > no.chave:
            no.dir = self._inserir(no.dir, chave)
        else:
            return no
        atualizar(no)
        fb = fator(no)
        if fb > 1 and chave < no.esq.chave:          # # zig-zig (esq-esq)
            self.rotacoes += 1
            return rot_direita(no)
        if fb < -1 and chave > no.dir.chave:         # zig-zig (dir-dir)
            self.rotacoes += 1
            return rot_esquerda(no)
        if fb > 1 and chave > no.esq.chave:          # zig-zag (esq-dir)
            self.rotacoes += 2
            no.esq = rot_esquerda(no.esq)
            return rot_direita(no)
        if fb < -1 and chave < no.dir.chave:         # zig-zag (dir-esq)
            self.rotacoes += 2
            no.dir = rot_direita(no.dir)
            return rot_esquerda(no)
        return no

    def altura(self):
        return h(self.raiz)

    def buscar(self, chave):
        atual, comps = self.raiz, 0
        while atual:
            comps += 1
            if chave == atual.chave:
                return True, comps
            atual = atual.esq if chave < atual.chave else atual.dir
        return False, comps


def main():
    print(f"{'Cenário':<18}{'n':>6}{'Alt. BST':>10}{'Alt. AVL':>10}"
          f"{'Comp. BST':>11}{'Comp. AVL':>11}{'Rot. AVL':>10}")
    for arquivo in ["dados_ordenados.csv", "dados_aleatorios.csv"]:
        codigos = ler_codigos(arquivo)
        bst, avl = BST(), AVL()
        for c in codigos:
            bst.inserir(c)
            avl.inserir(c)

        maior = codigos[0]                  # maior sem usar max()/sort
        for c in codigos:
            if c > maior:
                maior = c

        _, comp_bst = bst.buscar(maior)
        _, comp_avl = avl.buscar(maior)
        nome = arquivo.replace("dados_", "").replace(".csv", "")
        print(f"{nome:<18}{len(codigos):>6}{bst.altura():>10}{avl.altura():>10}"
              f"{comp_bst:>11}{comp_avl:>11}{avl.rotacoes:>10}")
    print(f"\nMaior código buscado: {maior}")


if __name__ == "__main__":
    main()
