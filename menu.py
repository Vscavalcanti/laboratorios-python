"""Menu """
import os
import runpy

# garante que puxa os dados pelo menu
PASTA = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA)

LABS = {
    "1": ("Heap — chamados", "lab1_heap", ["chamados.csv"]),
    "2": ("BST — produtos", "lab2_bst", ["produtos.csv"]),
    "3": ("Trie — autocomplete", "lab3_trie", ["palavras.csv"]),
    "4": ("BST x AVL — balanceamento", "lab4_bst_avl", ["dados_ordenados.csv", "dados_aleatorios.csv"]),
    "5": ("Splay — acessos frequentes", "lab5_splay", ["acessos.csv", "produtos.csv"]),
    "6": ("TreeSort — ordenando vendas", "lab6_treesort", ["vendas.csv"]),
    "7": ("Árvore de decisão", "lab7_arvore_decisao", ["funcionarios.csv"]),
}

DESAFIOS = {
    "C1": ("Heap com desempate", "c1_heap_desempate", ["chamados.csv"]),
    "C2": ("Top 3 chamados urgentes", "c2_top3_urgentes", ["chamados.csv"]),
    "C3": ("Busca de faixa", "c3_busca_faixa_bst", ["produtos.csv"]),
    "C4": ("preço como chave", "c4_bst_preco", ["produtos.csv"]),
    "C5": ("ranking", "c5_trie_ranking", ["palavras.csv"]),
    "C6": ("Comparação de alturas", "c6_comparacao_alturas", ["dados_ordenados.csv", "dados_aleatorios.csv"]),
    "C7": ("Splay e localidade temporal", "c7_splay_localidade", ["acessos.csv", "produtos.csv"]),
    "C8": ("decrescente", "c8_treesort_decrescente", ["vendas.csv"]),
    "C9": ("Gini", "c9_gini_manual", ["funcionarios.csv"]),
    "C10": ("Entropia x Gini", "c10_entropia", ["funcionarios.csv"]),
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
                if codigo == "C5":     
                    print("(C5 é interativo: digite prefixos e aperte Enter vazio para continuar)")
                executar(codigo, limpar=False)
        elif opcao in OPCOES:
            executar(opcao)
        else:
            print("Opção inválida.")
        input("Pressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
