"""C5 — ranking (palavras.csv)"""
import pandas as pd


class TrieNode:
    def __init__(self):
        self.filhos = {}
        self.fim_de_palavra = False
        self.buscas = 0


class Trie:
    def __init__(self):
        self.raiz = TrieNode()

    def insert(self, palavra, buscas):
        no = self.raiz
        for ch in palavra:
            if ch not in no.filhos:
                no.filhos[ch] = TrieNode()
            no = no.filhos[ch]
        no.fim_de_palavra = True
        no.buscas = buscas

    def starts_with(self, prefixo):
        no = self.raiz
        for ch in prefixo:
            if ch not in no.filhos:
                return []
            no = no.filhos[ch]
        resultados = []
        self._coletar(no, prefixo, resultados)
        return resultados

    def _coletar(self, no, atual, resultados):
        if no.fim_de_palavra:
            resultados.append((atual, no.buscas))
        for ch, filho in no.filhos.items():
            self._coletar(filho, atual + ch, resultados)

    def sugerir(self, prefixo, limite=5):
        """Top 'limite' sugestões do prefixo, da mais buscada para a menos buscada."""
        encontrados = self.starts_with(prefixo)
        encontrados = sorted(encontrados, key=lambda t: t[1], reverse=True)
        return encontrados[:limite]


def main():
    df = pd.read_csv("palavras.csv", encoding="utf-8-sig")
    trie = Trie()
    for termo, buscas in zip(df["termo"], df["buscas"]):
        trie.insert(str(termo).strip().lower(), int(buscas))

    print("Autocomplete (Enter vazio para sair)")
    while True:
        prefixo = input("\nDigite um prefixo: ").strip().lower()
        if prefixo == "":
            break
        sugestoes = trie.sugerir(prefixo, limite=5)
        total = len(trie.starts_with(prefixo))
        if not sugestoes:
            print("   Nenhuma sugestão encontrada.")
            continue
        print(f"   {len(sugestoes)} de {total} termo(s) encontrado(s):")
        for i, (termo, buscas) in enumerate(sugestoes, start=1):
            print(f"   {i}. {termo:<18}{buscas:>5} buscas")


if __name__ == "__main__":
    main()
