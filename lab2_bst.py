"""Lab 2 — BST: catálogo de produtos Menores à esquerda, maiores à direita.
"""
import pandas as pd


class No:
    def __init__(self, codigo, produto, preco, estoque):
        self.codigo = codigo
        self.produto = produto
        self.preco = preco
        self.estoque = estoque
        self.esq = None
        self.dir = None


class BST:
    def __init__(self):
        self.raiz = None

    # inserção 
    def inserir(self, codigo, produto, preco, estoque):
        self.raiz = self._inserir(self.raiz, codigo, produto, preco, estoque)

    def _inserir(self, no, codigo, produto, preco, estoque):
        if no is None:
            return No(codigo, produto, preco, estoque)
        if codigo < no.codigo:
            no.esq = self._inserir(no.esq, codigo, produto, preco, estoque)
        elif codigo > no.codigo:
            no.dir = self._inserir(no.dir, codigo, produto, preco, estoque)
        return no                  

    #  busca 
    def buscar(self, codigo):
        atual = self.raiz
        while atual is not None:
            if codigo == atual.codigo:
                return atual
            atual = atual.esq if codigo < atual.codigo else atual.dir
        return None

    # percurso em ordem 
    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is not None:
            self._em_ordem(no.esq, resultado)    
            resultado.append(no)                 
            self._em_ordem(no.dir, resultado)     

    # remoção 
    def remover(self, codigo):
        self.raiz = self._remover(self.raiz, codigo)

    def _remover(self, no, codigo):
        if no is None:
            return None
        if codigo < no.codigo:
            no.esq = self._remover(no.esq, codigo)
        elif codigo > no.codigo:
            no.dir = self._remover(no.dir, codigo)
        else:
            #o pai passa a apontar para o filho
            if no.esq is None:
                return no.dir
            if no.dir is None:
                return no.esq
            # copia o sucessor
            sucessor = no.dir
            while sucessor.esq is not None:
                sucessor = sucessor.esq
            no.codigo, no.produto = sucessor.codigo, sucessor.produto
            no.preco, no.estoque = sucessor.preco, sucessor.estoque
            no.dir = self._remover(no.dir, sucessor.codigo)
        return no

    #altura 
    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, no):
        if no is None:
            return 0
        return 1 + max(self._altura(no.esq), self._altura(no.dir))

    # visualização 
    def imprimir(self):
        self._imprimir(self.raiz, "", "raiz: ")

    def _imprimir(self, no, recuo, rotulo):
        if no is None:
            return
        print(f"{recuo}{rotulo}{no.codigo} ({no.produto})")
        self._imprimir(no.esq, recuo + "    ", "esq: ")
        self._imprimir(no.dir, recuo + "    ", "dir: ")


def verificar(arvore, titulo):
    print(f"\n--- {titulo} ---")
    arvore.imprimir()
    codigos = [no.codigo for no in arvore.em_ordem()]
    ordenado = True
    for i in range(len(codigos) - 1):
        if codigos[i] > codigos[i + 1]:
            ordenado = False
    print(f"Em ordem: {codigos} | ordenado? {ordenado} | altura: {arvore.altura()}")


def main():
    df = pd.read_csv("produtos.csv", encoding="utf-8-sig")
    arvore = BST()
    for _, r in df.iterrows():
        arvore.inserir(int(r["codigo"]), r["produto"], float(r["preco"]), int(r["estoque"]))
    print(f"{len(df)} produtos inseridos (ordem do arquivo: {list(df['codigo'])})")

    # Busca
    print("\nBuscas:")
    for codigo in [60, 10, 55]:
        no = arvore.buscar(codigo)
        if no:
            print(f"   buscar({codigo}) -> {no.produto} | R$ {no.preco:.2f} | estoque {no.estoque}")
        else:
            print(f"   buscar({codigo}) -> não encontrado")

    #em ordem
    print("\nPercurso em ordem:")
    for no in arvore.em_ordem():
        print(f"   {no.codigo:<4}{no.produto:<12}R$ {no.preco:>8.2f}   estoque {no.estoque}")

    verificar(arvore, "Árvore original")

    # Remoções
    arvore.remover(40)
    verificar(arvore, "Após remover 40 (Webcam) — nó FOLHA")
    arvore.remover(20)
    verificar(arvore, "Após remover 20 (Teclado) — nó com UM filho (10)")
    arvore.remover(50)
    verificar(arvore, "Após remover 50 (Notebook) — nó com DOIS filhos (raiz; sucessor = 60)")

    print(f"\nAltura final da árvore: {arvore.altura()}")


if __name__ == "__main__":
    main()
