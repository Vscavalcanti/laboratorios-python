"""C7 — Splay e localidade temporal (acessos.csv)"""
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
    if raiz is None or raiz.chave == chave:
        return raiz
    if chave < raiz.chave:
        if raiz.esq is None:
            return raiz
        if chave < raiz.esq.chave:                       
            raiz.esq.esq = splay(raiz.esq.esq, chave)
            raiz = rot_direita(raiz)
        elif chave > raiz.esq.chave:                   
            raiz.esq.dir = splay(raiz.esq.dir, chave)
            if raiz.esq.dir:
                raiz.esq = rot_esquerda(raiz.esq)
        return rot_direita(raiz) if raiz.esq else raiz   
    else:
        if raiz.dir is None:
            return raiz
        if chave > raiz.dir.chave:
            raiz.dir.dir = splay(raiz.dir.dir, chave)
            raiz = rot_esquerda(raiz)
        elif chave < raiz.dir.chave:
            raiz.dir.esq = splay(raiz.dir.esq, chave)
            if raiz.dir.esq:
                raiz.dir = rot_direita(raiz.dir)
        return rot_esquerda(raiz) if raiz.dir else raiz


def inserir(raiz, chave):
    if raiz is None:
        return No(chave)
    raiz = splay(raiz, chave)
    if raiz.chave == chave:
        return raiz
    novo = No(chave)
    if chave < raiz.chave:
        novo.dir, novo.esq, raiz.esq = raiz, raiz.esq, None
    else:
        novo.esq, novo.dir, raiz.dir = raiz, raiz.dir, None
    return novo


def comparacoes(raiz, chave):
    no, comps = raiz, 0
    while no:
        comps += 1
        if chave == no.chave:
            break
        no = no.esq if chave < no.chave else no.dir
    return comps


def simular(titulo, produtos, sequencia):
    raiz = None
    for p in produtos:                     
        raiz = inserir(raiz, p)

    print(titulo)
    print("   Acesso | Produto    | Comparações | Raiz após splay")
    total_comps, trocas_de_raiz = 0, 0
    for i, p in enumerate(sequencia, start=1):
        comps = comparacoes(raiz, p)
        raiz_antes = raiz.chave
        raiz = splay(raiz, p)
        if raiz.chave != raiz_antes:
            trocas_de_raiz += 1
        total_comps += comps
        print(f"   {i:>6} | {p:<10} | {comps:>11} | {raiz.chave}")
    print(f"   -> Total de comparações: {total_comps} | "
          f"média: {total_comps / len(sequencia):.2f} | trocas de raiz: {trocas_de_raiz}\n")
    return total_comps, trocas_de_raiz


def main():
    produtos = list(pd.read_csv("produtos.csv", encoding="utf-8-sig")["produto"])
    original = list(pd.read_csv("acessos.csv", encoding="utf-8-sig")["produto"])

    #mesmo produto repetido em sequência, repete na ordem da 1ª aparição
    contagem = {}
    for p in original:
        contagem[p] = contagem.get(p, 0) + 1
    blocos = []
    for p, qtd in contagem.items():
        blocos.extend([p] * qtd)

    c1, t1 = simular("SEQUÊNCIA ORIGINAL (acessos intercalados)", produtos, original)
    c2, t2 = simular("SEQUÊNCIA EM BLOCOS (acessos repetidos agrupados)", produtos, blocos)

    print(f"{'':<12}{'Comparações':>13}{'Trocas de raiz':>16}")
    print(f"{'Original':<12}{c1:>13}{t1:>16}")
    print(f"{'Em blocos':<12}{c2:>13}{t2:>16}")


if __name__ == "__main__":
    main()
