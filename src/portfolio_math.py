import numpy as np

# Simple fake "expected annual returns" and volatilities
# These aren't real market numbers, just reasonable-ish for the project.
EXPECTED_RETURNS = {
    "AAPL": 0.12,
    "MSFT": 0.10,
    "SPY": 0.08,
    "TSLA": 0.18,
}

VOLATILITIES = {
    "AAPL": 0.22,
    "MSFT": 0.20,
    "SPY": 0.15,
    "TSLA": 0.35,
}

RISK_FREE_RATE = 0.02  # 2% risk-free, for Sharpe ratio


def _build_cov_matrix(tickers):
    """
    Build a simple covariance matrix for the given tickers.
    We'll assume a baseline correlation of 0.3 between all assets,
    and 1.0 with themselves.
    """
    n = len(tickers)
    vols = np.array([VOLATILITIES[t] for t in tickers])
    # correlation matrix: 1 on diagonal, 0.3 off-diagonal
    corr = np.full((n, n), 0.3)
    np.fill_diagonal(corr, 1.0)
    cov = corr * np.outer(vols, vols)
    return cov


def portfolio_stats(tickers, weights):
    """
    Given a list of tickers and weights (same length, sum ~ 1),
    return expected annual return, volatility, and Sharpe ratio.
    """
    if len(tickers) == 0:
        raise ValueError("tickers list cannot be empty")
    if len(tickers) != len(weights):
        raise ValueError("tickers and weights must have same length")

    for t in tickers:
        if t not in EXPECTED_RETURNS:
            raise ValueError(f"Unknown ticker: {t}")

    w = np.array(weights, dtype=float)
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")

    # Normalize weights to sum to 1 if they are close
    total = w.sum()
    if not np.isclose(total, 1.0):
        w = w / total

    mu = np.array([EXPECTED_RETURNS[t] for t in tickers])
    cov = _build_cov_matrix(tickers)

    expected_return = float(w @ mu)
    variance = float(w @ cov @ w)
    volatility = float(np.sqrt(variance))
    if volatility == 0:
        sharpe = 0.0
    else:
        sharpe = (expected_return - RISK_FREE_RATE) / volatility

    return {
        "tickers": tickers,
        "weights": w.tolist(),
        "expected_annual_return": expected_return,
        "annual_volatility": volatility,
        "sharpe_ratio": sharpe,
    }

def optimize_portfolio(tickers, mode="min_variance"):
    """
    Compute optimized weights:
    - mode="min_variance": find weights with the lowest portfolio volatility
    - mode="max_sharpe": find weights maximizing Sharpe ratio

    Uses a simple grid search for transparency and numerical stability.
    """
    for t in tickers:
        if t not in EXPECTED_RETURNS:
            raise ValueError(f"Unknown ticker: {t}")

    n = len(tickers)
    if n == 0:
        raise ValueError("Must provide at least 1 ticker.")

    # Build covariance and mean return vectors
    cov = _build_cov_matrix(tickers)
    mu = np.array([EXPECTED_RETURNS[t] for t in tickers])

    best_w = None
    best_value = None

    # Grid search: weights in increments of 0.05
    steps = np.arange(0, 1.01, 0.05)
    grid = np.array(np.meshgrid(*([steps] * n))).T.reshape(-1, n)

    for w in grid:
        if abs(w.sum() - 1.0) > 1e-6:
            continue  # require weights sum to 1

        w = w.astype(float)
        expected_return = float(w @ mu)
        variance = float(w @ cov @ w)
        volatility = np.sqrt(variance)

        if mode == "min_variance":
            value = volatility  # minimize
        elif mode == "max_sharpe":
            if volatility == 0:
                continue
            value = -((expected_return - RISK_FREE_RATE) / volatility)  # maximize Sharpe
        else:
            raise ValueError("mode must be 'min_variance' or 'max_sharpe'")

        if best_value is None or value < best_value:
            best_value = value
            best_w = w

    # Compute stats for the optimal portfolio
    stats = portfolio_stats(tickers, best_w.tolist())
    stats["mode"] = mode
    return stats
