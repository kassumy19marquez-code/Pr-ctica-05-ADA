import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cambio import INF, cambio_memo, cambio_reconstruir, cambio_recursivo, cambio_tabulacion
from lcs_substring import (
    lcs_substr_memo,
    lcs_substr_reconstruir,
    lcs_substr_recursiva,
    lcs_substr_tabulacion,
)
from lcsq import lcsq_memo, lcsq_reconstruir, lcsq_recursiva, lcsq_tabulacion
from mochila import mochila_memo, mochila_reconstruir, mochila_recursiva, mochila_tabulacion


def medir(fn, *args, **kwargs):
    t0 = time.perf_counter()
    res = fn(*args, **kwargs)
    dt_ms = (time.perf_counter() - t0) * 1000
    return res, dt_ms


def correr_mochila():
    print("\n=== PROBLEMA DE LA MOCHILA (0/1) ===")
    rng = random.Random(42)
    casos = [
        ("Clasico", [10, 20, 30], [60, 100, 120], 50, True),
        ("Capacidad chica", [5, 8, 12], [10, 15, 25], 4, True),
        (
            "Mediano (n=22)",
            [rng.randint(1, 20) for _ in range(22)],
            [rng.randint(10, 100) for _ in range(22)],
            65,
            True,
        ),
        (
            "Grande solo DP (n=60, W=300)",
            [rng.randint(1, 25) for _ in range(60)],
            [rng.randint(10, 150) for _ in range(60)],
            300,
            False,
        ),
    ]

    for nombre, pesos, valores, W, correr_rec in casos:
        n = len(pesos)
        r_tab, t_tab = medir(mochila_tabulacion, pesos, valores, W)
        _, elegidos = mochila_reconstruir(pesos, valores, W)

        stats_m = {}
        r_mem, t_mem = medir(mochila_memo, pesos, valores, W, n, None, stats_m)

        if correr_rec:
            stats_r = {}
            r_rec, t_rec = medir(mochila_recursiva, pesos, valores, W, n, stats_r)
            assert r_rec == r_mem == r_tab, f"Discrepancia en {nombre}"
            rec_str = f"{t_rec:.3f} ms (llamadas={stats_r['llamadas']})"
        else:
            assert r_mem == r_tab, f"Discrepancia en {nombre}"
            rec_str = "omitida por costo O(2^n)"

        print(
            f"[{nombre}] val={r_tab} elegidos={elegidos} | Rec: {rec_str} | "
            f"Memo: {t_mem:.3f} ms (llamadas={stats_m['llamadas']}) | "
            f"Tab: {t_tab:.3f} ms"
        )


def correr_cambio():
    print("\n=== PROBLEMA DEL CAMBIO (MIN. MONEDAS) ===")
    casos = [
        ("Contraejemplo voraz", [1, 3, 4], 6, True),
        ("Inalcanzable", [5, 10], 7, True),
        ("Monto moderado", [1, 2, 5, 10], 27, True),
        ("Monto grande solo DP", [1, 3, 5, 10, 25], 450, False),
    ]

    for nombre, monedas, monto, correr_rec in casos:
        r_tab, t_tab = medir(cambio_tabulacion, monedas, monto)
        _, usadas = cambio_reconstruir(monedas, monto)
        val_tab = INF if r_tab == -1 else r_tab

        stats_m = {}
        r_mem, t_mem = medir(cambio_memo, monedas, monto, None, stats_m)

        if correr_rec:
            stats_r = {}
            r_rec, t_rec = medir(cambio_recursivo, monedas, monto, stats_r)
            assert r_rec == r_mem == val_tab, f"Discrepancia en {nombre}"
            rec_str = f"{t_rec:.3f} ms (llamadas={stats_r['llamadas']})"
        else:
            assert r_mem == val_tab, f"Discrepancia en {nombre}"
            rec_str = "omitida por explosion combinatoria"

        print(
            f"[{nombre}] min_monedas={r_tab} usadas={usadas} | Rec: {rec_str} | "
            f"Memo: {t_mem:.3f} ms (llamadas={stats_m['llamadas']}) | "
            f"Tab: {t_tab:.3f} ms"
        )


def correr_cadenas():
    print("\n=== LCSq Y SUBCADENA COMUN MAS LARGA (LCS) ===")
    pares = [
        ("Ejemplo clasico", "ABCBDAB", "BDCABA", True),
        ("Subsecuencia vs Subcadena", "AGGTAB", "GXTXAYB", True),
        ("Sin coincidencia contigua", "abcdef", "xyzw", True),
        (
            "Cadenas largas solo DP",
            "X" * 40 + "ABCDE12345" + "Y" * 40,
            "Z" * 35 + "ABCDE12345" + "W" * 45,
            False,
        ),
    ]

    for nombre, a, b, correr_rec in pares:
        m, n = len(a), len(b)
        q_tab, tq_tab = medir(lcsq_tabulacion, a, b)
        _, seq_q = lcsq_reconstruir(a, b)
        qm_stats = {}
        q_mem, tq_mem = medir(lcsq_memo, a, b, m, n, None, qm_stats)

        s_tab, ts_tab = medir(lcs_substr_tabulacion, a, b)
        _, sub_s = lcs_substr_reconstruir(a, b)
        sm_stats = {}
        s_mem, ts_mem = medir(lcs_substr_memo, a, b, None, sm_stats)

        assert q_mem == q_tab and s_mem == s_tab

        if correr_rec:
            qr_stats = {}
            q_rec, tq_rec = medir(lcsq_recursiva, a, b, m, n, qr_stats)
            sr_stats = {}
            s_rec, ts_rec = medir(lcs_substr_recursiva, a, b, m, n, 0, sr_stats)
            assert q_rec == q_tab and s_rec == s_tab
            q_rec_txt = f"{tq_rec:.2f} ms (ll={qr_stats['llamadas']})"
            s_rec_txt = f"{ts_rec:.2f} ms (ll={sr_stats['llamadas']})"
        else:
            q_rec_txt = "omitida"
            s_rec_txt = "omitida"

        print(
            f"[{nombre}] LCSq={q_tab} ('{seq_q}') [Rec:{q_rec_txt}, Memo:{tq_mem:.2f}ms, Tab:{tq_tab:.2f}ms] | "
            f"LCS={s_tab} ('{sub_s}') [Rec:{s_rec_txt}, Memo:{ts_mem:.2f}ms, Tab:{ts_tab:.2f}ms]"
        )


if __name__ == "__main__":
    correr_mochila()
    correr_cambio()
    correr_cadenas()
