"""Menu Laboratórios 3 a 7 (com os desafios C5 a C10 dentro deles)
e Desafios C1 a C4. (caso de erro normalmente ta sendo aqui, não nos labs)
"""
import os
import runpy

# Garante que os arquivos sejam procurados na pasta deste menu NAO MUDAR
PASTA = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA)

LABS = {
    "3": ("Trie — autocomplete (+ desafio C5)", "lab3_trie", ["palavras.csv"]),
    "4": ("BST x AVL — balanceamento (+ desafio C6)", "lab4_bst_avl", ["dados_ordenados.csv", "dados_aleatorios.csv"]),
    "5": ("Splay — acessos frequentes (+ desafio C7)", "lab5_splay", ["acessos.csv", "produtos.csv"]),
    "6": ("TreeSort — ordenando vendas (+ desafio C8)", "lab6_treesort", ["vendas.csv"]),
    "7": ("Árvore de decisão — Gini (+ desafios C9 e C10)", "lab7_arvore_decisao", ["funcionarios.csv"]),
}

DESAFIOS = {
    "C1": ("Heap com desempate", "c1_heap_desempate", ["chamados.csv"]),
    "C2": ("Top 3 chamados urgentes", "c2_top3_urgentes", ["chamados.csv"]),
    "C3": ("Busca de faixa na BST", "c3_busca_faixa_bst", ["produtos.csv"]),
    "C4": ("BST com preço como chave", "c4_bst_preco", ["produtos.csv"]),
}

OPCOES = {**LABS, **DESAFIOS}


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def executar(codigo, limpar=True):
    if limpar:
        limpar_tela()
    titulo, modulo, arquivos = OPCOES[codigo]
    nome = f"DESAFIO {codigo}" if codigo.startswith("C") else f"LABORATÓRIO {codigo}"
    print("=" * 60)
    print(f"{nome} — {titulo}")
    print("=" * 60)

    faltando = [a for a in arquivos if not os.path.exists(a)]
    if faltando:
        print(f"Arquivo(s) não encontrado(s) nesta pasta: {', '.join(faltando)}")
        print(f"Pasta atual: {PASTA}")
        return
    try:
        runpy.run_path(modulo + ".py", run_name="__main__")
    except FileNotFoundError:
        print(f"Não encontrei o arquivo {modulo}.py nesta pasta")
    except Exception as e:
        print(f"Erro ao executar {codigo}: {e}")
    print()


def main():
    while True:
        limpar_tela()
        print("=============== MENU ===============")
        print("LABORATÓRIOS")
        for codigo, (titulo, _, _) in LABS.items():
            print(f"   {codigo:>3} - {titulo}")
        print("\nDESAFIOS")
        for codigo, (titulo, _, _) in DESAFIOS.items():
            print(f"   {codigo:>3} - {titulo}")
        print("\n     L - Executar todos os laboratórios")
        print("     D - Executar todos os desafios")
        print("     0 - Sair")
        opcao = input("\nEscolha uma opção: ").strip().upper()

        if opcao == "0":
            print("Saindo...")
            break
        elif opcao == "L":
            limpar_tela()
            for codigo in LABS:
                executar(codigo, limpar=False)
        elif opcao == "D":
            limpar_tela()
            for codigo in DESAFIOS:
                executar(codigo, limpar=False)
        elif opcao in OPCOES:
            executar(opcao)
        else:
            print("Opção inválida.")
        input("Pressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
