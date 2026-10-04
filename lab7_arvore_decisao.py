"""Lab 7 — Árvore de decisão"""
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
        for t in set(linha[f] for linha in X):          # cada valor vira um limiar candidato
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
    _, y_e, _, y_d = raiz["esq"][0], raiz["esq"][1], raiz["dir"][0], raiz["dir"][1]
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


if __name__ == "__main__":
    main()
