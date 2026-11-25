INF = float("inf")


def cambio_recursivo(monedas, monto, stats=None):
    """Minimo numero de monedas mediante recursion ingenua."""
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if monto == 0:
        return 0
    if monto < 0:
        return INF

    mejor = INF
    for c in monedas:
        res = cambio_recursivo(monedas, monto - c, stats)
        if res != INF:
            mejor = min(mejor, 1 + res)
    return mejor


def cambio_memo(monedas, monto, memo=None, stats=None):
    """Minimo numero de monedas mediante memoizacion (Top-Down)."""
    if memo is None:
        memo = {}
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if monto == 0:
        return 0
    if monto < 0:
        return INF
    if monto in memo:
        if stats is not None:
            stats["aciertos_cache"] = stats.get("aciertos_cache", 0) + 1
        return memo[monto]

    mejor = INF
    for c in monedas:
        res = cambio_memo(monedas, monto - c, memo, stats)
        if res != INF:
            mejor = min(mejor, 1 + res)

    memo[monto] = mejor
    return mejor


def cambio_tabulacion(monedas, monto):
    """Minimo numero de monedas mediante tabulacion (Bottom-Up). Retorna -1 si es imposible."""
    dp = [INF] * (monto + 1)
    dp[0] = 0
    for m in range(1, monto + 1):
        for c in monedas:
            if c <= m and dp[m - c] != INF:
                dp[m] = min(dp[m], 1 + dp[m - c])
    return -1 if dp[monto] == INF else dp[monto]


def cambio_reconstruir(monedas, monto):
    """Devuelve (min_monedas_o_-1, lista_monedas_usadas)."""
    dp = [INF] * (monto + 1)
    padre = [-1] * (monto + 1)
    dp[0] = 0
    for m in range(1, monto + 1):
        for c in monedas:
            if c <= m and dp[m - c] + 1 < dp[m]:
                dp[m] = dp[m - c] + 1
                padre[m] = c
    if dp[monto] == INF:
        return -1, []
    usadas = []
    actual = monto
    while actual > 0:
        usadas.append(padre[actual])
        actual -= padre[actual]
    return dp[monto], usadas
