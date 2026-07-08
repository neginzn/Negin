# Negin

A crypto signal engine that blends technical indicators (RSI, MACD, EMA/SMA
trend, Bollinger Bands) with real-time news sentiment from public crypto RSS
feeds, plus a backtester so you can see how the technical rules actually
performed historically instead of guessing.

It only reads public market data (Binance's public data mirror, no API key)
and public news feeds. **It does not hold API keys and does not place
trades.** Connecting it to a real exchange account is a separate, deliberate
step you'd take only after the backtest numbers convince you.

## Why a backtest, not a promised win rate

No indicator or news feed has a fixed, guaranteed win rate. The only honest
way to know how a strategy performs is to run it against real historical
data and read the numbers - trade count, win rate, return, and max
drawdown. That's what `negin backtest` does. Note it only replays the
*technical* rules: free news feeds don't provide a historical archive, so
sentiment can only be applied to the live signal, not backtested into the
past.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

Current signal for a symbol (technical + live news sentiment):

```bash
negin signal BTCUSDT
```

Backtest the technical strategy over recent history:

```bash
negin backtest BTCUSDT --limit 1000 --show-trades
```

`--interval` accepts any Binance kline interval (`1m`, `5m`, `15m`, `1h`,
`4h`, `1d`, ...). `--limit` is the number of candles (max 1000 per request).

## How the signal is built

- **Technical score** (`negin/signals/engine.py`): weighted blend of RSI,
  MACD histogram, EMA fast/slow trend, SMA-50 trend, and Bollinger Band
  position, each clamped to [-1, 1].
- **Sentiment score** (`negin/sentiment/analyzer.py`): keyword-weighted
  lexicon over recent CoinDesk/Cointelegraph/Decrypt headlines mentioning
  the coin. This is explainable, not a trained NLP model - a real upgrade
  path would be a labeled sentiment classifier.
- **Combined score**: `0.7 * technical + 0.3 * sentiment`, thresholded into
  BUY / SELL / HOLD.

All of these weights and thresholds are in `negin/signals/engine.py` and are
meant to be tuned against your own backtests, not treated as fixed truth.

## Tests

```bash
pip install pytest
PYTHONPATH=src python3 -m pytest tests/
```

## Disclaimer

This is a rule-based educational tool, not financial advice. Crypto markets
are volatile; most retail traders using leverage lose money over time.
Backtested performance does not guarantee future results. Never risk more
than you can afford to lose, and never connect a real trading API key
without understanding exactly what the code does first.
