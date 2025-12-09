# Stock Portfolio Risk Service

A containerized Flask API that computes portfolio risk metrics (expected return, volatility, Sharpe ratio) and performs basic portfolio optimization (minimum variance and maximum Sharpe). The project demonstrates course concepts including API design, numerical computing, containerization, testing, and cloud deployment.

---

# 1) Executive Summary

## Problem
New investors often pick stocks without understanding their portfolio’s risk, expected return, or risk-adjusted performance. Tools that compute such metrics are usually paid or overly complex.

## Solution
The **Stock Portfolio Risk Service** provides a clean, reproducible REST API that calculates portfolio analytics and generates optimized portfolios. It runs deterministically inside Docker, requires no API keys or external data sources, and is deployed live on Render for demonstration.

---

# 2) System Overview

## Course Concepts Used
This project integrates several course concepts:
- Flask-based API design  
- Data pipelines & numerical models  
- Docker containerization  
- Testing & validation with PyTest  
- Cloud deployment (Render)  
- Code modularization with `src/` structure  

## Architecture

### Components
| File | Purpose |
|------|---------|
| `src/app.py` | Flask routes for portfolio stats & optimization |
| `src/portfolio_math.py` | Expected returns, covariance model, stats, optimizer |
| `Dockerfile` | Container definition |
| `tests/` | Smoke tests |
| `requirements.txt` | Project dependencies |

### Data / Models / Services
The service uses hardcoded expected returns & volatilities for reproducibility:

| Ticker | Expected Return | Volatility |
|--------|------------------|------------|
| AAPL | 12% | 22% |
| MSFT | 10% | 20% |
| SPY | 8%  | 15% |
| TSLA | 18% | 35% |

- Correlation assumed = **0.3** between all assets  
- Covariance matrix constructed in `portfolio_math.py`  
- Optimizer uses a transparent grid search  

---

# 3) How to Run (Local)

### Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/app.py
```
### Health check
```
curl http://localhost:8080/health
```
### Portfolio stats:
```bash
curl -X POST http://localhost:8080/portfolio/stats \
  -H "Content-Type: application/json" \
  -d '{"tickers":["AAPL","MSFT","SPY"],"weights":[0.3,0.4,0.3]}'
```
---
# 4) How to Run (Docker)

### Build
``
bash
```
docker build -t portfolio-api:latest .
```
### Run
`
bash 
```
docker run --rm -p 8080:8080 portfolio-api:latest
```
### Health Check
``` bash
curl http://localhost:8080/health
```
---
### 5) Cloud Deployment (Render)

Live Service
```
https://stock-portfolio-risk-service.onrender.com
```
Health Endpoint
```
https://stock-portfolio-risk-service.onrender.com/health
```
---
### 6) Design Decisions

## Why this concept?
Portfolio analytics is a perfect demonstration of:
- API → data pipeline → numerical output
- containerization for reproducibility
- real computational logic without external data

## Alternatives Considered
- Live market-data APIs → rejected (API keys, nondeterministic results)
- SciPy/CVXOPT optimization → rejected (unnecessary complexity)

## Tradeoffs
- Hardcoded returns improve reproducibility but reduce realism
- Grid search is simple but not as efficient as convex solvers
- Fixed correlation = stable but not market-calibrated
  
## Security / Privacy
- No secrets, no user data stored
- Only JSON accepted
- Purely stateless service
  
## Operational Considerations
- Docker ensures one-command reproducibility
- Log output routed to stdout for debugging on Render
- Could easily scale horizontally if deployed with multiple containers

---
### 7) Results & Evaluation
## Example Output
For [AAPL, MSFT, SPY] with weights [0.3, 0.4, 0.3]:
```
{
  "tickers": ["AAPL","MSFT","SPY"],
  "weights": [0.3,0.4,0.3],
  "expected_annual_return": 0.10,
  "annual_volatility": 0.141,
  "sharpe_ratio": 0.567
}
```
## Optimization Examples
Minimum Variance:
bash
```
POST /portfolio/optimize/min_variance
```
Maximum Sharpe:
bash
```
POST /portfolio/optimize/max_sharpe
```
### Testing / Validation

Smoke tests (`tests/test_portfolio_math.py`) validated that:
- weights sum to 1
- expected return & volatility are positive
- stats dictionary is correctly produced

---
### 8) What’s Next
Potential improvements:
- Pull real historical data for dynamic covariance calculation
- Add constrained optimization (max allocation, long-only constraint)
- Add monitoring (Prometheus metrics, request logs)
- Build simple frontend visualizer
- Add CI pipeline for automated testing

---
### 9) Links
## GitHub Repository:
https://github.com/Thomasgao1/stock-portfolio-risk-service

## Cloud Deployment (Render):
https://stock-portfolio-risk-service.onrender.com

## Health Check:
https://stock-portfolio-risk-service.onrender.com/health





