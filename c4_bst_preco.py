"""C4 — BST com preço como chave"""
import pandas as pd


class No:
    def __init__(self, preco, registro):
        self.preco = preco
        self.registro = registro
        self.esq = None
        self.dir = None


def inserir(no, preco, registro):
    if no is None:
        return No(preco, registro)
    if preco < no.preco:
        no.esq = inserir(no.esq, preco, registro)
    else:                                  # preços iguaispara a direita
        no.dir = inserir(no.dir, preco, registro)
    return no


def em_ordem(no, resultado):
    if no is not None:
        em_ordem(no.esq, resultado)
        resultado.append(no.registro)
        em_ordem(no.dir, resultado)


def main():
    df = pd.read_csv("produtos.csv", encoding="utf-8-sig")
    raiz = None
    for r in df.to_dict("records"):
        raiz = inserir(raiz, r["preco"], r)

    print(f"Raiz da BST por preço: {raiz.registro['produto']} (R$ {raiz.preco})\n")
    resultado = []
    em_ordem(raiz, resultado)
    print("Do mais barato ao mais caro:")
    for i, r in enumerate(resultado, start=1):
        print(f"   {i}. {r['produto']:<12}R$ {r['preco']:>6}   (código {r['codigo']})")


if __name__ == "__main__":
    main()
