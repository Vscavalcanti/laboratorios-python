"""C2 — Top 3 urgentes (chamados.csv)"""
import heapq
import pandas as pd


def main():
    df = pd.read_csv("chamados.csv", encoding="utf-8-sig")

    fila = []
    for chegada, c in enumerate(df.to_dict("records")):
        heapq.heappush(fila, (c["prioridade"], c["tempo_estimado"], chegada, c))

    print(f"Tamanho da fila original antes: {len(fila)}")

    copia = fila.copy()          
    print("\nTrês próximos chamados a serem atendidos:")
    for i in range(3):
        prioridade, tempo, _, c = heapq.heappop(copia)
        print(f"   {i + 1}º  #{c['id']} | prioridade {prioridade} | {tempo} min | "
              f"{c['cliente']} - {c['problema']}")

    print(f"\nTamanho da fila original depois: {len(fila)}  (nada foi removido)")
    print(f"Topo da fila original continua sendo: #{fila[0][3]['id']}")


if __name__ == "__main__":
    main()
