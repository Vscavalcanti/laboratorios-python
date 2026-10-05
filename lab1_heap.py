"""Lab 1 central de chamados Regra: o MENOR valor numérico representa a MAIOR prioridade."""
import heapq
import pandas as pd


def mostrar_chamado(item, prefixo=""):
    prioridade, id_chamado, cliente, problema = item
    print(f"{prefixo}#{id_chamado} | prioridade {prioridade} | {cliente:<10} | {problema}")


def montar_heap(df):
    heap = []
    for _, linha in df.iterrows():
        # Cada um guarda: prioridade, id, cliente, problema.
        item = (int(linha["prioridade"]), int(linha["id"]), linha["cliente"], linha["problema"])
        heapq.heappush(heap, item)
    return heap


def main():
    # 1) Ler o CSV e mostrar as cinco primeiras linhas
    df = pd.read_csv("chamados.csv", encoding="utf-8-sig")
    print("Cinco primeiras linhas de chamados.csv:")
    print(df.head().to_string(index=False))

    heap = montar_heap(df)
    print(f"\n{len(heap)} chamados inseridos na heap.")
    print("Vetor interno da heap (não é a ordem de atendimento):")
    for i, item in enumerate(heap):
        print(f"   [{i}] prioridade {item[0]} | #{item[1]}")

    # Ver o próximo a ser atendido SEM remover
    print("\nPróximo a ser atendido (consulta sem remover):")
    mostrar_chamado(heap[0], "   ")
    print(f"   Chamados ainda na heap: {len(heap)}")

    # Remove e exibi na ordem de atendimento
    print("\nOrdem de atendimento (heappop):")
    ordem = 1
    while heap:
        mostrar_chamado(heapq.heappop(heap), f"   {ordem}º  ")
        ordem += 1

    # Inserir manualmente um novo chama ele de prioridade 1
    heap = montar_heap(df)
    novo = (1, 109, "Empresa I", "Rede corporativa caiu")
    heapq.heappush(heap, novo)
    print("\nNovo chamado inserido manualmente:")
    mostrar_chamado(novo, "   ")
    print(f"   Posição no vetor interno da heap: índice {heap.index(novo)}")

    print("\nNova ordem de atendimento:")
    ordem = 1
    copia = heap.copy()
    while copia:
        item = heapq.heappop(copia)
        marca = "   <- NOVO" if item == novo else ""
        mostrar_chamado(item, f"   {ordem}º  ")
        if marca:
            print(f"{'':>9}^ chamado inserido manualmente")
        ordem += 1


if __name__ == "__main__":
    main()
