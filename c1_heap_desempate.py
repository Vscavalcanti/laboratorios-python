"""C1 — desempate (chamados.csv)"""
import heapq
import pandas as pd


def mostrar(titulo, heap):
    heap = list(heap)               
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
    # prioridade os empates seguem a ordem de chegada
    heap_original = []
    for chegada, c in enumerate(chamados):
        heapq.heappush(heap_original, (c["prioridade"], chegada, c))

    # empate resolvido pelo menor tempo
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

    print("=" * 60)
    print("TESTE: mesmos chamados chegando em ordem INVERSA")
    print("=" * 60)
    antes, depois = montar_heaps(chamados[::-1])
    mostrar("ANTES (empate pela chegada) -> a ordem muda:", antes)
    mostrar("DEPOIS (empate pelo menor tempo) -> a ordem se mantém:", depois)


if __name__ == "__main__":
    main()