"""Lab 6 — TreeSort: a ordenação vem do percurso em ordem.
"""
import time
import pandas as pd


class No:
    def __init__(self, valor, registro):
        self.valor = valor
        self.registros = [registro]   # valores iguais ficam no mesmo nó
        self.dir = None


class BST:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor, registro):
        if self.raiz is None:
            self.raiz = No(valor, registro)
            return
        atual = self.raiz
        while True:                    #evita estourar a recursão no pior caso
            if valor < atual.valor:
                if atual.esq is None:
                    atual.esq = No(valor, registro); return
                atual = atual.esq
            elif valor > atual.valor:
                if atual.dir is None:
                    atual.dir = No(valor, registro); return
                atual = atual.dir
            else:
                atual.registros.append(registro); return

    def em_ordem(self):
        """Percurso em ordem iterativo (esquerda -> nó -> direita)."""
        saida, pilha, atual = [], [], self.raiz
        while pilha or atual:
            while atual:
                pilha.append(atual)
                atual = atual.esq
            atual = pilha.pop()
            saida.extend(atual.registros)
            atual = atual.dir
        return saida

    def altura(self):
        if self.raiz is None:
            return 0
        maior, pilha = 0, [(self.raiz, 1)]
        while pilha:
            no, nivel = pilha.pop()
            if nivel > maior:
                maior = nivel
            if no.esq: pilha.append((no.esq, nivel + 1))
            if no.dir: pilha.append((no.dir, nivel + 1))
        return maior


def treesort(registros):
    arvore = BST()
    for r in registros:
        arvore.inserir(float(r["valor"]), r)
    return arvore.em_ordem(), arvore


def main():
    df = pd.read_csv("vendas.csv", encoding="utf-8-sig")
    registros = df.to_dict("records")       # registro completo

    t0 = time.perf_counter()
    ordenados, arvore = treesort(registros)
    t1 = time.perf_counter()

    pd.DataFrame(ordenados, columns=df.columns).to_csv("vendas_ordenadas.csv", index=False)
    print(f"{len(ordenados)} vendas gravadas em vendas_ordenadas.csv\n")

    print("Primeiras 5 linhas:")
    print(pd.DataFrame(ordenados[:5]).to_string(index=False))
    print("\nÚltimas 5 linhas:")
    print(pd.DataFrame(ordenados[-5:]).to_string(index=False))

    ok = all(float(ordenados[i]["valor"]) <= float(ordenados[i + 1]["valor"])
             for i in range(len(ordenados) - 1))
    print(f"\nValidação: arquivo ordenado pelo valor? {ok}")

    #reconstruir a BST com os valores JÁ em ordem crescente
    t2 = time.perf_counter()
    _, arvore_pior = treesort(ordenados)
    t3 = time.perf_counter()
    print(f"\nAltura da BST (ordem original):  {arvore.altura():>5}  | tempo {1000*(t1-t0):.3f} ms")
    print(f"Altura da BST (entrada crescente): {arvore_pior.altura():>4}  | tempo {1000*(t3-t2):.3f} ms")


if __name__ == "__main__":
    main()
