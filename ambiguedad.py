"""
Ambigüedad estructural y números de Catalan.

Una gramática independiente del contexto mínima (en forma normal de Chomsky)
para oraciones del tipo "vi al hombre con el telescopio en el parque ...".
Un parser CKY cuenta cuántos árboles distintos tiene cada oración y lo
compara con los números de Catalan.
"""
from collections import defaultdict
from math import comb

# Gramática (forma normal de Chomsky). Sujeto nulo: la oración es un SV.
#   SV  -> V SN  | SV SP      (el SP modifica al verbo)
#   SN  -> Det N | SN SP      (el SP modifica al nombre)
#   SP  -> P SN
REGLAS = [
    ("SV", "V", "SN"), ("SV", "SV", "SP"),
    ("SN", "Det", "N"), ("SN", "SN", "SP"),
    ("SP", "P", "SN"),
]
LEXICO = {
    "vi": "V",
    "al": "Det", "el": "Det", "la": "Det",
    "hombre": "N", "telescopio": "N", "parque": "N", "bufanda": "N",
    "tienda": "N", "esquina": "N", "ciudad": "N", "plaza": "N",
    "fuente": "N", "noche": "N", "lluvia": "N", "calle": "N",
    "con": "P", "en": "P", "de": "P", "junto_a": "P", "bajo": "P",
}
SPS = [
    "con el telescopio", "en el parque", "con la bufanda", "de la tienda",
    "en la esquina", "de la ciudad", "junto_a la plaza", "con la fuente",
    "en la noche", "bajo la lluvia", "de la calle", "en el parque",
]


def oracion(n):
    """'vi al hombre' seguido de n sintagmas preposicionales."""
    return ("vi al hombre " + " ".join(SPS[:n])).split()


def cky(palabras):
    """Tabla CKY con, para cada tramo y categoría, la lista de árboles."""
    n = len(palabras)
    tabla = defaultdict(lambda: defaultdict(list))
    for i, w in enumerate(palabras):
        tabla[i, i + 1][LEXICO[w]].append(w.replace("_", " "))
    for largo in range(2, n + 1):
        for i in range(n - largo + 1):
            j = i + largo
            for k in range(i + 1, j):
                for madre, izq, der in REGLAS:
                    for a in tabla[i, k][izq]:
                        for b in tabla[k, j][der]:
                            tabla[i, j][madre].append((madre, a, b))
    return tabla[0, n]["SV"]


def contar(palabras):
    """Igual que cky() pero solo cuenta árboles (sirve para n grandes)."""
    n = len(palabras)
    t = defaultdict(lambda: defaultdict(int))
    for i, w in enumerate(palabras):
        t[i, i + 1][LEXICO[w]] = 1
    for largo in range(2, n + 1):
        for i in range(n - largo + 1):
            j = i + largo
            for k in range(i + 1, j):
                for madre, izq, der in REGLAS:
                    t[i, j][madre] += t[i, k][izq] * t[k, j][der]
    return t[0, n]["SV"]


def catalan(n):
    return comb(2 * n, n) // (n + 1)


def corchetes(arbol):
    """Árbol -> corchetes etiquetados: [SV [V vi] [SN ...]]"""
    if isinstance(arbol, str):
        return arbol
    madre, a, b = arbol
    def hoja(x, cat):
        return x if not isinstance(x, str) else f"[{cat} {x}]"
    partes = []
    for hijo in (a, b):
        if isinstance(hijo, str):
            partes.append(hijo)
        else:
            partes.append(corchetes(hijo))
    return f"[{madre} " + " ".join(partes) + "]"


if __name__ == "__main__":
    print("n SP | análisis | Catalan(n+1)")
    for n in range(0, 13):
        c = contar(oracion(n))
        assert c == catalan(n + 1), (n, c)
        print(f"{n:4d} | {c:8d} | {catalan(n + 1):8d}")

    print("\nLos 5 análisis de:", " ".join(oracion(2)))
    for i, arbol in enumerate(cky(oracion(2)), 1):
        print(f"  {i}. {corchetes(arbol)}")
