"""Lab 5 — Splay Tree acessos frequentes"""
import os
import pandas as pd


class No:
    def __init__(self, chave):
        self.chave = chave
        self.esq = None
        self.dir = None


def rot_direita(x):
    y = x.esq
    x.esq = y.dir
    y.dir = x
    return y


def rot_esquerda(x):
    y = x.dir
    x.dir = y.esq
    y.esq = x
    return y


def splay(raiz, chave):
    """Traz a chave (ou o último nó visitado) para a raiz usando zig, zig-zig e zig-zag."""
    if raiz is None or raiz.chave == chave:
        return raiz
    if chave < raiz.chave:
        if raiz.esq is None:
            return raiz
        if chave < raiz.esq.chave:                       # zig-zig (esq-esq)
            raiz.esq.esq = splay(raiz.esq.esq, chave)
            raiz = rot_direita(raiz)
        elif chave > raiz.esq.chave:                     # zig-zag (esq-dir)
            raiz.esq.dir = splay(raiz.esq.dir, chave)
            if raiz.esq.dir:
                raiz.esq = rot_esquerda(raiz.esq)
        return rot_direita(raiz) if raiz.esq else raiz   # zig final
    else:
        if raiz.dir is None:
            return raiz
        if chave > raiz.dir.chave:                       # zig-zig (dir-dir)
            raiz.dir.dir = splay(raiz.dir.dir, chave)
            raiz = rot_esquerda(raiz)
        elif chave < raiz.dir.chave:                     # zig-zag (dir-esq)
            raiz.dir.esq = splay(raiz.dir.esq, chave)
            if raiz.dir.esq:
                raiz.dir = rot_direita(raiz.dir)
        return rot_esquerda(raiz) if raiz.dir else raiz


class SplayTree:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = No(chave)
            return
        self.raiz = splay(self.raiz, chave)
        if self.raiz.chave == chave:
            return
        novo = No(chave)
        if chave < self.raiz.chave:
            novo.dir = self.raiz
            novo.esq = self.raiz.esq
            self.raiz.esq = None
        else:
            novo.esq = self.raiz
            novo.dir = self.raiz.dir
            self.raiz.dir = None
        self.raiz = novo

    def buscar(self, chave):
        self.raiz = splay(self.raiz, chave)
        return self.raiz is not None and self.raiz.chave == chave


def profundidade(raiz, chave):
    """Comparações necessárias para achar a chave ANTES do splay."""
    atual, comps = raiz, 0
    while atual:
        comps += 1
        if chave == atual.chave:
            return comps
        atual = atual.esq if chave < atual.chave else atual.dir
    return comps


def ler(arquivo):
    df = pd.read_csv(arquivo, encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    for c in ["produto", "produto_id", "id_produto", "codigo", "id"]:
        if c in df.columns:
            return [str(v).strip() for v in df[c]]
    return [str(v).strip() for v in df[df.columns[0]]]


def main():
    acessos = ler("acessos.csv")
    produtos = ler("produtos.csv") if os.path.exists("produtos.csv") else acessos

    arvore = SplayTree()
    for p in produtos:
        arvore.inserir(p)

    freq, vezes_na_raiz = {}, {}
    comps_por_produto = {}
    print("Acesso | Produto buscado | Comparações | Raiz após splay")
    for i, p in enumerate(acessos, start=1):
        comps = profundidade(arvore.raiz, p)
        comps_por_produto.setdefault(p, []).append(comps)
        achou = arvore.buscar(p)
        raiz = arvore.raiz.chave
        print(f"{i:>6} | {p:<15} | {comps:>11} | {raiz}{'' if achou else '  (não encontrado)'}")
        freq[p] = freq.get(p, 0) + 1
        vezes_na_raiz[raiz] = vezes_na_raiz.get(raiz, 0) + 1

    top_freq = sorted(freq.items(), key=lambda t: t[1], reverse=True)[:5]
    top_raiz = sorted(vezes_na_raiz.items(), key=lambda t: t[1], reverse=True)[:5]
    print("\nTop 5 mais acessados      | Top 5 que mais apareceram na raiz")
    for (p1, f1), (p2, f2) in zip(top_freq, top_raiz):
        print(f"   {p1:<10} {f1:>3} acessos  |    {p2:<10} {f2:>3} vezes")

    print("\nComparações médias por produto (antes de cada splay):")
    for p, lista in comps_por_produto.items():
        print(f"   {p:<10} {sum(lista)/len(lista):.2f}  {lista}")

    print(f"\nTotal de acessos: {len(acessos)} | Produtos distintos acessados: {len(freq)}")


if __name__ == "__main__":
    main()
