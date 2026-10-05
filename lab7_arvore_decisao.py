"""Lab 7 — Árvore de decisão (Gini) """
import math
import pandas as pd

FEATURES = ["idade", "salario", "tempo_empresa", "cargo"]
CARGOS = {"analista": 0, "desenvolvedor": 1, "gerente": 2}


def gini_impurity(y_subset):
    n = len(y_subset)
    if n == 0:
        return 0.0
    contagem = {}
    for v in y_subset:
        contagem[v] = contagem.get(v, 0) + 1
    return 1.0 - sum((c / n) ** 2 for c in contagem.values())


def split_data(X, y, feature_index, threshold):
    X_esq, y_esq, X_dir, y_dir = [], [], [], []
    for linha, rotulo in zip(X, y):
        if linha[feature_index] <= threshold:
            X_esq.append(linha); y_esq.append(rotulo)
        else:
            X_dir.append(linha); y_dir.append(rotulo)
    return X_esq, y_esq, X_dir, y_dir


def find_best_split(X, y):
    melhor = {"gini": float("inf")}
    n = len(y)
    for f in range(len(X[0])):
        for t in set(linha[f] for linha in X):          # cada valor vira um limiar 
            X_e, y_e, X_d, y_d = split_data(X, y, f, t)
            if not y_e or not y_d:
                continue
            g = (len(y_e) / n) * gini_impurity(y_e) + (len(y_d) / n) * gini_impurity(y_d)
            if g < melhor["gini"]:
                melhor = {"feature": f, "threshold": t, "gini": g,
                          "esq": (X_e, y_e), "dir": (X_d, y_d)}
    return melhor if "feature" in melhor else None


def classe_majoritaria(y):
    return 1 if sum(y) > len(y) / 2 else 0


def build_tree(X, y, depth=0, max_depth=4):
    if depth >= max_depth or gini_impurity(y) == 0 or len(y) < 2:
        return {"folha": True, "classe": classe_majoritaria(y), "n": len(y)}
    split = find_best_split(X, y)
    if split is None or split["gini"] >= gini_impurity(y):
        return {"folha": True, "classe": classe_majoritaria(y), "n": len(y)}
    return {
        "folha": False, "feature": split["feature"], "threshold": split["threshold"],
        "gini": split["gini"], "n": len(y),
        "esq": build_tree(*split["esq"], depth + 1, max_depth),
        "dir": build_tree(*split["dir"], depth + 1, max_depth),
    }


def predict_one(no, x):
    while not no["folha"]:
        no = no["esq"] if x[no["feature"]] <= no["threshold"] else no["dir"]
    return no["classe"]


def predict(arvore, X):
    return [predict_one(arvore, x) for x in X]


def imprimir(no, prefixo=""):
    if no["folha"]:
        print(f"{prefixo}-> saiu = {no['classe']}  (n={no['n']})")
        return
    nome = FEATURES[no["feature"]]
    print(f"{prefixo}[{nome} <= {no['threshold']}]  gini_pond={no['gini']:.3f}  n={no['n']}")
    imprimir(no["esq"], prefixo + "   sim ")
    imprimir(no["dir"], prefixo + "   não ")


def para_binario(v):
    s = str(v).strip().lower()
    return 1 if s in ("1", "sim", "s", "yes", "true", "verdadeiro") else 0


def main():
    df = pd.read_csv("funcionarios.csv", encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    df["cargo"] = df["cargo"].astype(str).str.strip().str.lower().map(CARGOS)

    X = df[FEATURES].values.tolist()
    y = [para_binario(v) for v in df["saiu"]]

    print(f"Registros: {len(y)} | saíram: {sum(y)} | ficaram: {len(y) - sum(y)}")
    print(f"Gini da base inteira: {gini_impurity(y):.4f}\n")

    raiz = find_best_split(X, y)
    y_e, y_d = raiz["esq"][1], raiz["dir"][1]
    print("Melhor divisão na raiz:")
    print(f"   {FEATURES[raiz['feature']]} <= {raiz['threshold']}  (Gini ponderado = {raiz['gini']:.4f})")
    print(f"   Lado <=: {len(y_e):>3} pessoas, {100*sum(y_e)/len(y_e):5.1f}% saíram (Gini {gini_impurity(y_e):.3f})")
    print(f"   Lado  >: {len(y_d):>3} pessoas, {100*sum(y_d)/len(y_d):5.1f}% saíram (Gini {gini_impurity(y_d):.3f})\n")

    arvore = build_tree(X, y, max_depth=4)
    print("Árvore (max_depth=4):")
    imprimir(arvore)

    pred = predict(arvore, X)
    acertos = sum(1 for a, b in zip(pred, y) if a == b)
    print(f"\nAcurácia nos próprios dados: {acertos}/{len(y)} = {acertos/len(y):.2%}")

    desafio_c9(X, y)
    desafio_c10(X, y)


def entropy(y_subset):
    """Desafio C10: Entropia = -Σ p·log2(p)."""
    n = len(y_subset)
    if n == 0:
        return 0.0
    contagem = {}
    for v in y_subset:
        contagem[v] = contagem.get(v, 0) + 1
    total = 0.0
    for c in contagem.values():
        p = c / n
        total -= p * math.log2(p)
    return total


def ponderado(funcao, y_esq, y_dir):
    n = len(y_esq) + len(y_dir)
    return len(y_esq) / n * funcao(y_esq) + len(y_dir) / n * funcao(y_dir)


def desafio_c9(X, y):
    print("\n" + "=" * 50)
    print("DESAFIO C9 — Gini manual: salario <= 3500?")
    print("=" * 50)
    _, y_esq, _, y_dir = split_data(X, y, FEATURES.index("salario"), 3500)
    for nome, ys in [("Antes da divisão", y), ("Ramo SIM (<= 3500)", y_esq), ("Ramo NÃO (> 3500)", y_dir)]:
        n, saiu = len(ys), sum(ys)
        print(f"{nome}: n = {n} | saiu = {saiu} | ficou = {n - saiu}")
        print(f"   Gini = 1 - ({saiu}/{n})² - ({n - saiu}/{n})² = {gini_impurity(ys):.4f}")
    g = ponderado(gini_impurity, y_esq, y_dir)
    print(f"\nGini ponderado = ({len(y_esq)}/{len(y)})·{gini_impurity(y_esq):.4f} + "
          f"({len(y_dir)}/{len(y)})·{gini_impurity(y_dir):.4f} = {g:.4f}")
    print(f"Redução de impureza = {gini_impurity(y):.4f} - {g:.4f} = {gini_impurity(y) - g:.4f}")


def desafio_c10(X, y):
    print("\n" + "=" * 50)
    print("DESAFIO C10 — Entropia x Gini")
    print("=" * 50)
    print(f"Nó original: Gini = {gini_impurity(y):.4f} | Entropia = {entropy(y):.4f}\n")
    divisoes = [("salario", 3500), ("salario", 4100), ("idade", 30),
                ("tempo_empresa", 3), ("cargo", 0)]
    print(f"{'Pergunta':<22}{'Sim':>5}{'Não':>5}{'Gini pond.':>12}{'Entropia pond.':>16}")
    melhor_g, melhor_e = None, None
    for nome, t in divisoes:
        _, y_esq, _, y_dir = split_data(X, y, FEATURES.index(nome), t)
        g = ponderado(gini_impurity, y_esq, y_dir)
        e = ponderado(entropy, y_esq, y_dir)
        rotulo = f"{nome} <= {t}"
        print(f"{rotulo:<22}{len(y_esq):>5}{len(y_dir):>5}{g:>12.4f}{e:>16.4f}")
        if melhor_g is None or g < melhor_g[1]:
            melhor_g = (rotulo, g)
        if melhor_e is None or e < melhor_e[1]:
            melhor_e = (rotulo, e)
    print(f"\nEscolhida por Gini:     {melhor_g[0]}")
    print(f"Escolhida por Entropia: {melhor_e[0]}")


if __name__ == "__main__":
    main()
