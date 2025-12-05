import os
import sys

# Add the project root (../) to Python path so we can import src.*
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.portfolio_math import portfolio_stats


def test_portfolio_stats_basic():
    tickers = ["AAPL", "MSFT", "SPY"]
    weights = [0.3, 0.4, 0.3]
    stats = portfolio_stats(tickers, weights)

    assert set(stats["tickers"]) == set(tickers)
    assert abs(sum(stats["weights"]) - 1.0) < 1e-6
    assert stats["expected_annual_return"] > 0
    assert stats["annual_volatility"] > 0
