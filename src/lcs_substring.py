def lcs_substr_recursiva(a, b, i, j, actual=0, stats=None):
    """Subcadena comun mas larga (LCS contigua) mediante recursion ingenua."""
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if i == 0 or j == 0:
        return actual

    if a[i - 1] == b[j - 1]:
        extender = lcs_substr_recursiva(a, b, i - 1, j - 1, actual + 1, stats)
        return max(
            extender,
            lcs_substr_recursiva(a, b, i - 1, j, 0, stats),
            lcs_substr_recursiva(a, b, i, j - 1, 0, stats),
        )
    return max(
        actual,
        lcs_substr_recursiva(a, b, i - 1, j, 0, stats),
        lcs_substr_recursiva(a, b, i, j - 1, 0, stats),
    )


def lcs_substr_memo(a, b, memo=None, stats=None):
    """Subcadena comun mas larga (LCS contigua) mediante memoizacion (Top-Down)."""
    if memo is None:
        memo = {}

    def sufijo(x, y):
        if stats is not None:
            stats["llamadas"] = stats.get("llamadas", 0) + 1
        if x == 0 or y == 0:
            return 0
        if (x, y) in memo:
            if stats is not None:
                stats["aciertos_cache"] = stats.get("aciertos_cache", 0) + 1
            return memo[(x, y)]
        if a[x - 1] == b[y - 1]:
            memo[(x, y)] = 1 + sufijo(x - 1, y - 1)
        else:
            memo[(x, y)] = 0
        return memo[(x, y)]

    mejor = 0
    for x in range(1, len(a) + 1):
        for y in range(1, len(b) + 1):
            mejor = max(mejor, sufijo(x, y))
    return mejor


def lcs_substr_tabulacion(a, b):
    """Subcadena comun mas larga (LCS contigua) mediante tabulacion (Bottom-Up)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    mejor = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                mejor = max(mejor, dp[i][j])
            else:
                dp[i][j] = 0
    return mejor


def lcs_substr_reconstruir(a, b):
    """Devuelve (longitud, subcadena_encontrada)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    mejor = 0
    fin_i = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                if dp[i][j] > mejor:
                    mejor = dp[i][j]
                    fin_i = i
    return mejor, a[fin_i - mejor : fin_i]
