from flask import Flask, request, jsonify
from portfolio_math import portfolio_stats, optimize_portfolio

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/portfolio/stats", methods=["POST"])
def portfolio_stats_endpoint():
    data = request.get_json() or {}
    tickers = data.get("tickers", [])
    weights = data.get("weights", [])

    try:
        stats = portfolio_stats(tickers, weights)
        return jsonify(stats)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/portfolio/optimize/<mode>", methods=["POST"])
def portfolio_optimize(mode):
    data = request.get_json() or {}
    tickers = data.get("tickers", [])

    try:
        result = optimize_portfolio(tickers, mode)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
