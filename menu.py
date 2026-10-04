"""Menu"""
import os
import importlib

#procura os csv e chama os laboratórios
PASTA = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA)

LABS = {
    "3": ("Trie — autocomplete", "lab3_trie", ["palavras.csv"]),
    "4": ("BST x AVL — balanceamento", "lab4_bst_avl", ["dados_ordenados.csv", "dados_aleatorios.csv"]),
    "5": ("Splay — acessos frequentes", "lab5_splay", ["acessos.csv", "produtos.csv"]),
    "6": ("TreeSort — ordenando vendas", "lab6_treesort", ["vendas.csv"]),
    "7": ("Árvore de decisão — Gini", "lab7_arvore_decisao", ["funcionarios.csv"]),
}


def executar(numero):
    titulo, modulo, arquivos = LABS[numero]
    print("\n" + "=" * 60)
    print(f"LABORATÓRIO {numero} — {titulo}")
    print("=" * 60)

    faltando = [a for a in arquivos if not os.path.exists(a)]
    if faltando:
        print(f"Arquivo não encontrado na pasta: {', '.join(faltando)}")
        print(f"Pasta atual: {PASTA}")
        return
    try:
        lab = importlib.import_module(modulo)
        lab.main()
    except ModuleNotFoundError as e:
        print(f"Não encontrado: {e.name}")
    except Exception as e:
        print(f"Erro ao executar o laboratório {numero}: {e}")


def main():
    while True:
        print("\n========== MENU DE LABORATÓRIOS ==========")
        for numero, (titulo, _, _) in LABS.items():
            print(f"  {numero} - {titulo}")
        print("  T - Executar todos")
        print("  0 - Sair")
        opcao = input("Escolha uma opção: ").strip().upper()

        if opcao == "0":
            print("Saindo...")
            break
        elif opcao == "T":
            for numero in LABS:
                executar(numero)
        elif opcao in LABS:
            executar(opcao)
        else:
            print("Opção inválida.")
            continue
        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
