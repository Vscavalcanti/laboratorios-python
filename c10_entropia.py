"""C10 — Entropia manual (funcionarios.csv)"""
import math
import pandas as pd

FEATURES = ["idade", "salario", "tempo_empresa", "cargo"]
CARGOS = {"Analista": 0, "Desenvolvedor": 1, "Gerente": 2}


def gini_impurity(y):
    n = len(y)
    if n == 0:
        return 0.0
    contagem = {}
    for v in y:
        contagem[v] = contagem.get(v, 0) + 1
    return 1.0 - sum((c / n) ** 2 for c in contagem.values())


def entropy(y):
    """Entropia = -Σ p·log2(p). 0 = nó puro; 1 = metade/metade (2 classes)."""
    n = len(y)
    if n == 0:
        return 0.0
    contagem = {}
    for v in y:
        contagem[v] = contagem.get(v, 0) + 1
    total = 0.0
    for c in contagem.values():
        p = c / n
        total -= p * math.log2(p)
    return total


def split_data(X, y, feature_index, threshold):
    y_esq, y_dir = [], []
    for linha, rotulo in zip(X, y):
        if linha[feature_index] <= threshold:
            y_esq.append(rotulo)
        else:
            y_dir.append(rotulo)
    return y_esq, y_dir


def ponderado(funcao, y_esq, y_dir):
    n = len(y_esq) + len(y_dir)
    return len(y_esq) / n * funcao(y_esq) + len(y_dir) / n * funcao(y_dir)


def main():
    df = pd.read_csv("funcionarios.csv", encoding="utf-8-sig")
    df["cargo"] = df["cargo"].map(CARGOS)
    X = df[FEATURES].values.tolist()
    y = list(df["saiu"])

    print(f"Nó original: Gini = {gini_impurity(y):.4f} | Entropia = {entropy(y):.4f}\n")

    divisoes = [("salario", 3500), ("salario", 4100), ("idade", 30),
                ("tempo_empresa", 3), ("cargo", 0)]

    print(f"{'Pergunta':<22}{'Sim':>5}{'Não':>5}{'Gini pond.':>12}{'Entropia pond.':>16}")
    resultados = []
    for nome, t in divisoes:
        y_esq, y_dir = split_data(X, y, FEATURES.index(nome), t)
        g = ponderado(gini_impurity, y_esq, y_dir)
        e = ponderado(entropy, y_esq, y_dir)
        resultados.append((f"{nome} <= {t}", g, e))
        print(f"{nome + ' <= ' + str(t):<22}{len(y_esq):>5}{len(y_dir):>5}{g:>12.4f}{e:>16.4f}")

    melhor_gini = resultados[0]
    melhor_entropia = resultados[0]
    for r in resultados:
        if r[1] < melhor_gini[1]:
            melhor_gini = r
        if r[2] < melhor_entropia[2]:
            melhor_entropia = r
    print(f"\nEscolhida por Gini:     {melhor_gini[0]}")
    print(f"Escolhida por Entropia: {melhor_entropia[0]}")

    # Ranking de cada critério (do melhor para o pior)
    print("\nRanking por Gini:     " + " > ".join(r[0] for r in sorted(resultados, key=lambda r: r[1])))
    print("Ranking por Entropia: " + " > ".join(r[0] for r in sorted(resultados, key=lambda r: r[2])))


if __name__ == "__main__":
    main()
