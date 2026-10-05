"""C8 — TreeSort decrescente (vendas.csv)"""
import pandas as pd


class No:
    def __init__(self, valor, registro):
        self.valor = valor
        self.registro = registro
        self.esq = None
        self.dir = None


def inserir(no, valor, registro):
    if no is None:
        return No(valor, registro)
    if valor < no.valor:
        no.esq = inserir(no.esq, valor, registro)
    else:
        no.dir = inserir(no.dir, valor, registro)
    return no


def em_ordem_reversa(no, resultado):
    if no is not None:
        em_ordem_reversa(no.dir, resultado)     # primeiro maior
        resultado.append(no.registro)
        em_ordem_reversa(no.esq, resultado)     # depois menor


def main():
    df = pd.read_csv("vendas.csv", encoding="utf-8-sig")
    raiz = None
    for r in df.to_dict("records"):
        raiz = inserir(raiz, r["valor"], r)

    resultado = []
    em_ordem_reversa(raiz, resultado)
    pd.DataFrame(resultado, columns=df.columns).to_csv("vendas_ordenadas_desc.csv", index=False)

    print("vendas_ordenadas_desc.csv gerado (maior -> menor):\n")
    print(pd.DataFrame(resultado).to_string(index=False))

    ok = True
    for i in range(len(resultado) - 1):
        if resultado[i]["valor"] < resultado[i + 1]["valor"]:
            ok = False
    print(f"\nValidação: ordem decrescente? {ok}")


if __name__ == "__main__":
    main()
