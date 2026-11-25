def lcsq_recursiva(a, b, i, j, stats=None):
    """Subsecuencia comun mas larga (LCSq) mediante recursion ingenua."""
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if i == 0 or j == 0:
        return 0
    if a[i - 1] == b[j - 1]:
        return 1 + lcsq_recursiva(a, b, i - 1, j - 1, stats)
    return max(
        lcsq_recursiva(a, b, i - 1, j, stats),
        lcsq_recursiva(a, b, i, j - 1, stats),
    )


def lcsq_memo(a, b, i, j, memo=None, stats=None):
    """Subsecuencia comun mas larga (LCSq) mediante memoizacion (Top-Down)."""
    if memo is None:
        memo = {}
    if stats is not None:
        stats["llamadas"] = stats.get("llamadas", 0) + 1

    if i == 0 or j == 0:
        return 0
    if (i, j) in memo:
        if stats is not None:
            stats["aciertos_cache"] = stats.get("aciertos_cache", 0) + 1
        return memo[(i, j)]

    if a[i - 1] == b[j - 1]:
        memo[(i, j)] = 1 + lcsq_memo(a, b, i - 1, j - 1, memo, stats)
    else:
        memo[(i, j)] = max(
            lcsq_memo(a, b, i - 1, j, memo, stats),
            lcsq_memo(a, b, i, j - 1, memo, stats),
        )
    return memo[(i, j)]


def lcsq_tabulacion(a, b):
    """Subsecuencia comun mas larga (LCSq) mediante tabulacion (Bottom-Up)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def lcsq_reconstruir(a, b):
    """Devuelve (longitud, subsecuencia_encontrada)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    res = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], "".join(reversed(res))
