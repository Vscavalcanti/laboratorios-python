"""Lab 3 autocomplete"""
import pandas as pd


def achar_coluna(df, candidatos):
    for c in candidatos:
        if c in df.columns:
            return c
    raise KeyError(f"Nenhuma das colunas {candidatos} encontrada em {list(df.columns)}")


class TrieNode:
    def __init__(self):
        self.filhos = {}             
        self.fim_de_palavra = False   
        self.buscas = 0               


class Trie:
    def __init__(self):
        self.raiz = TrieNode()

    def insert(self, palavra, buscas=0):
        no = self.raiz
        for ch in palavra:
            if ch not in no.filhos:
                no.filhos[ch] = TrieNode()
            no = no.filhos[ch]
        no.fim_de_palavra = True
        no.buscas += buscas

    def _no_do_prefixo(self, prefixo):
        no = self.raiz
        for ch in prefixo:
            if ch not in no.filhos:
                return None
            no = no.filhos[ch]
        return no

    def search(self, palavra):
        """Palavra completa: existir E terminar em fim_de_palavra."""
        no = self._no_do_prefixo(palavra)
        return no is not None and no.fim_de_palavra

    def starts_with(self, prefixo):
        """ basta o caminho existir, não precisa terminar em fim_de_palavra."""
        no = self._no_do_prefixo(prefixo)
        resultados = []
        if no is not None:
            self._coletar(no, prefixo, resultados)
        return resultados

    def _coletar(self, no, atual, resultados):
        if no.fim_de_palavra:
            resultados.append((atual, no.buscas))
        for ch, filho in no.filhos.items():
            self._coletar(filho, atual + ch, resultados)

    def sugerir(self, prefixo, limite=5):
        """Desafio C5"""
        encontrados = self.starts_with(prefixo)
        encontrados = sorted(encontrados, key=lambda t: t[1], reverse=True)
        return encontrados[:limite]


def main():
    df = pd.read_csv("palavras.csv", encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    col_termo = achar_coluna(df, ["palavra", "termo", "palavras", "termos"])
    col_buscas = achar_coluna(df, ["buscas"])

    trie = Trie()
    for termo, buscas in zip(df[col_termo], df[col_buscas]):
        trie.insert(str(termo).strip().lower(), int(buscas))
    print(f"Termos inseridos na Trie: {len(df)}\n")

    for prefixo in ["mo", "me", "note", "te"]:
        sugestoes = trie.starts_with(prefixo)  # filtragem ordena só as sugestões encontradas, da mais buscada e menos buscada
        sugestoes = sorted(sugestoes, key=lambda t: t[1], reverse=True)
        print(f"Prefixo '{prefixo}': {len(sugestoes)} sugestão(ões)")
        for termo, buscas in sugestoes:
            print(f"   {termo:<15} {buscas:>6} buscas")
        print()

    print("Palavra completa x prefixo:")
    for t in ["note", "notebook", "mo"]:
        print(f"   search('{t}') = {trie.search(t)!s:<5} | "
              f"starts_with('{t}') -> {len(trie.starts_with(t))} termo(s)")

    desafio_c5(trie)


def desafio_c5(trie):
    print("\n" + "=" * 50)
    print("DESAFIO C5 — Trie com ranking (máx. 5 sugestões)")
    print("=" * 50)
    print("Digite um prefixo (Enter vazio para sair)")
    while True:
        prefixo = input("\nPrefixo: ").strip().lower()
        if prefixo == "":
            break
        sugestoes = trie.sugerir(prefixo, limite=5)
        if not sugestoes:
            print("   Nenhuma sugestão encontrada.")
            continue
        total = len(trie.starts_with(prefixo))
        print(f"   {len(sugestoes)} de {total} termo(s) encontrado(s):")
        for i, (termo, buscas) in enumerate(sugestoes, start=1):
            print(f"   {i}. {termo:<18}{buscas:>5} buscas")


if __name__ == "__main__":
    main()
