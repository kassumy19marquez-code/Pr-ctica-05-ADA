def mochila_recursiva(pesos, valores, W, n, stats=None):
    """Problema de la mochila 0/1 mediante recursion ingenua."""
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if n == 0 or W == 0:
        return 0

    if pesos[n - 1] > W:
        return mochila_recursiva(pesos, valores, W, n - 1, stats)

    sin_tomar = mochila_recursiva(pesos, valores, W, n - 1, stats)
    tomando = valores[n - 1] + mochila_recursiva(
        pesos, valores, W - pesos[n - 1], n - 1, stats
    )
    return max(sin_tomar, tomando)


def mochila_memo(pesos, valores, W, n, memo=None, stats=None):
    """Problema de la mochila 0/1 mediante memoizacion (Top-Down)."""
    if memo is None:
        memo = {}
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if n == 0 or W == 0:
        return 0
    if (n, W) in memo:
        if stats is not None:
            stats["aciertos_cache"] = stats.get("aciertos_cache", 0) + 1
        return memo[(n, W)]

    if pesos[n - 1] > W:
        memo[(n, W)] = mochila_memo(pesos, valores, W, n - 1, memo, stats)
    else:
        sin_tomar = mochila_memo(pesos, valores, W, n - 1, memo, stats)
        tomando = valores[n - 1] + mochila_memo(
            pesos, valores, W - pesos[n - 1], n - 1, memo, stats
        )
        memo[(n, W)] = max(sin_tomar, tomando)

    return memo[(n, W)]


def mochila_tabulacion(pesos, valores, W):
    """Problema de la mochila 0/1 mediante tabulacion (Bottom-Up)."""
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w_i, v_i = pesos[i - 1], valores[i - 1]
        for cap in range(W + 1):
            dp[i][cap] = dp[i - 1][cap]
            if w_i <= cap:
                dp[i][cap] = max(dp[i][cap], v_i + dp[i - 1][cap - w_i])
    return dp[n][W]


def mochila_reconstruir(pesos, valores, W):
    """Devuelve (valor_maximo, lista_de_tuplas_(indice, peso, valor))."""
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w_i, v_i = pesos[i - 1], valores[i - 1]
        for cap in range(W + 1):
            dp[i][cap] = dp[i - 1][cap]
            if w_i <= cap:
                dp[i][cap] = max(dp[i][cap], v_i + dp[i - 1][cap - w_i])

    elegidos = []
    cap = W
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            elegidos.append((i - 1, pesos[i - 1], valores[i - 1]))
            cap -= pesos[i - 1]
    elegidos.reverse()
    return dp[n][W], elegidos
