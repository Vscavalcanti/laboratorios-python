"""C3 — Busca na BST (produtos.csv)"""
import pandas as pd


class No:
    def __init__(self, chave, registro):
        self.chave = chave
        self.registro = registro
        self.esq = None
        self.dir = None


def inserir(no, chave, registro):
    if no is None:
        return No(chave, registro)
    if chave < no.chave:
        no.esq = inserir(no.esq, chave, registro)
    elif chave > no.chave:
        no.dir = inserir(no.dir, chave, registro)
    return no


visitados = []


def busca_faixa(no, minimo, maximo, resultado):
    if no is None:
        return
    visitados.append(no.chave)
    if minimo < no.chave:                 
        busca_faixa(no.esq, minimo, maximo, resultado)
    if minimo <= no.chave <= maximo:     
        resultado.append(no.registro)
    if no.chave < maximo:                 
        busca_faixa(no.dir, minimo, maximo, resultado)


def main():
    df = pd.read_csv("produtos.csv", encoding="utf-8-sig")
    raiz = None
    for r in df.to_dict("records"):
        raiz = inserir(raiz, r["codigo"], r)

    resultado = []
    busca_faixa(raiz, 30, 70, resultado)

    print("Produtos com código entre 30 e 70:")
    for r in resultado:
        print(f"   {r['codigo']:<5}{r['produto']:<12}R$ {r['preco']}")
    print(f"\nNós visitados: {len(visitados)} de {len(df)} -> {visitados}")
    print("Os nós fora da faixa que não aparecem acima foram podados (nem visitados).")


if __name__ == "__main__":
    main()
