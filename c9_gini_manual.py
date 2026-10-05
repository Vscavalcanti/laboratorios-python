"""C9 — pergunta 'salario <= 3500?' (funcionarios.csv)"""
import pandas as pd


def gini_impurity(y):
    n = len(y)
    if n == 0:
        return 0.0
    contagem = {}
    for v in y:
        contagem[v] = contagem.get(v, 0) + 1
    return 1.0 - sum((c / n) ** 2 for c in contagem.values())


def descrever(nome, y):
    n = len(y)
    saiu = sum(y)
    ficou = n - saiu
    g = gini_impurity(y)
    print(f"{nome}: n = {n} | saiu = {saiu} | ficou = {ficou}")
    print(f"   Gini = 1 - ({saiu}/{n})² - ({ficou}/{n})² = {g:.4f}")
    return g


def main():
    df = pd.read_csv("funcionarios.csv", encoding="utf-8-sig")
    limiar = 3500

    y_total = list(df["saiu"])
    y_esq = [s for sal, s in zip(df["salario"], df["saiu"]) if sal <= limiar]
    y_dir = [s for sal, s in zip(df["salario"], df["saiu"]) if sal > limiar]

    print(f"Pergunta: salario <= {limiar}?\n")
    g_antes = descrever("Antes da divisão", y_total)
    g_esq = descrever(f"Ramo SIM (salario <= {limiar})", y_esq)
    g_dir = descrever(f"Ramo NÃO (salario > {limiar})", y_dir)

    n = len(y_total)
    ponderado = len(y_esq) / n * g_esq + len(y_dir) / n * g_dir
    print(f"\nGini ponderado = ({len(y_esq)}/{n})·{g_esq:.4f} + ({len(y_dir)}/{n})·{g_dir:.4f} "
          f"= {ponderado:.4f}")
    print(f"Redução de impureza = {g_antes:.4f} - {ponderado:.4f} = {g_antes - ponderado:.4f}")


if __name__ == "__main__":
    main()
