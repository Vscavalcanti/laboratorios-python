"""C1 — Heap com desempate (chamados.csv)
Chamados de mesma prioridade são desempatados pelo MENOR tempo_estimado.
Como o heapq é uma Min-Heap, o menor valor sai primeiro: prioridade 1 = mais urgente.
"""
import heapq
import pandas as pd


def mostrar(titulo, heap):
    heap = list(heap)                 # cópia: não destrói a fila recebida
    print(titulo)
    print(f"   {'Ordem':<6}{'ID':<6}{'Prior.':<8}{'Tempo':<7}Problema")
    ordem = 1
    while heap:
        item = heapq.heappop(heap)
        c = item[-1]                  # o registro completo é o último elemento da tupla
        print(f"   {ordem:<6}{c['id']:<6}{c['prioridade']:<8}{c['tempo_estimado']:<7}{c['problema']}")
        ordem += 1
    print()


def montar_heaps(chamados):
    # Antes: só a prioridade; empates seguem a ordem de chegada no arquivo
    heap_original = []
    for chegada, c in enumerate(chamados):
        heapq.heappush(heap_original, (c["prioridade"], chegada, c))

    # Depois: (prioridade, tempo_estimado) -> empate resolvido pelo menor tempo
    heap_desempate = []
    for chegada, c in enumerate(chamados):
        heapq.heappush(heap_desempate, (c["prioridade"], c["tempo_estimado"], chegada, c))

    return heap_original, heap_desempate


def main():
    df = pd.read_csv("chamados.csv", encoding="utf-8-sig")
    chamados = df.to_dict("records")

    antes, depois = montar_heaps(chamados)
    mostrar("Atendimento ANTES (só prioridade, empate pela ordem de chegada):", antes)
    mostrar("Atendimento DEPOIS (prioridade + menor tempo_estimado):", depois)

    # No arquivo, os empates já chegam com o menor tempo primeiro, então as duas
    # ordens coincidem. Para provar que a regra funciona, invertemos a chegada:
    print("=" * 60)
    print("TESTE: mesmos chamados chegando em ordem INVERSA")
    print("=" * 60)
    antes, depois = montar_heaps(chamados[::-1])
    mostrar("ANTES (empate pela chegada) -> a ordem muda:", antes)
    mostrar("DEPOIS (empate pelo menor tempo) -> a ordem se mantém:", depois)


if __name__ == "__main__":
    main()
