"""Genera grafico.png: número de análisis frente a número de SP."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ambiguedad import contar, oracion

ns = list(range(0, 13))
cuentas = [contar(oracion(n)) for n in ns]

fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
ax.plot(ns, cuentas, marker="o", color="#2a6f97", linewidth=2)
ax.set_yscale("log")
ax.set_xlabel("Sintagmas preposicionales tras «vi al hombre»")
ax.set_ylabel("Análisis sintácticos posibles (escala log)")
ax.set_title("La ambigüedad crece según los números de Catalan")
ax.set_xticks(ns)
ax.grid(True, which="major", alpha=0.3)
for n, c in zip(ns, cuentas):
    if n in (1, 2, 4, 8, 12):
        ax.annotate(f"{c:,}".replace(",", "."), (n, c),
                    textcoords="offset points", xytext=(-8, 8), fontsize=9)
ax.annotate("«vi al hombre con el telescopio»", (1, 2),
            textcoords="offset points", xytext=(15, -18), fontsize=8, color="#555")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("grafico.png")
print("grafico.png generado")
