"""Read-only Binance market data client.

Uses Binance's public market-data mirror (data-api.binance.vision) which
serves klines/ticker endpoints without an API key. api.binance.com is
geo-restricted in some regions, so a couple of mirrors are tried in order.
"""

from __future__ import annotations

import pandas as pd
import requests

_BASE_URLS = [
    "https://data-api.binance.vision/api/v3",
    "https://api.binance.us/api/v3",
    "https://api.binance.com/api/v3",
]

_KLINE_COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "num_trades",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
    "ignore",
]

_NUMERIC_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_asset_volume",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
]


class BinanceClientError(RuntimeError):
    """Raised when no Binance mirror could serve the request."""


def _get(path: str, params: dict) -> object:
    last_error: Exception | None = None
    for base in _BASE_URLS:
        try:
            response = requests.get(f"{base}{path}", params=params, timeout=10)
            if response.status_code == 451:
                # Geo-restricted on this host; try the next mirror.
                last_error = RuntimeError(f"{base} returned 451 (restricted location)")
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            continue
    raise BinanceClientError(
        f"All Binance mirrors failed for {path}: {last_error}"
    ) from last_error


def fetch_klines(symbol: str, interval: str = "1h", limit: int = 500) -> pd.DataFrame:
    """Fetch OHLCV candles for a symbol (e.g. BTCUSDT).

    interval: one of 1m, 5m, 15m, 1h, 4h, 1d, ...
    limit: number of candles, max 1000 per Binance API.
    """
    raw = _get(
        "/klines",
        {"symbol": symbol.upper(), "interval": interval, "limit": limit},
    )
    df = pd.DataFrame(raw, columns=_KLINE_COLUMNS)
    df[_NUMERIC_COLUMNS] = df[_NUMERIC_COLUMNS].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
    return df[["open_time", "open", "high", "low", "close", "volume", "close_time"]]


def fetch_price(symbol: str) -> float:
    """Fetch the latest traded price for a symbol."""
    raw = _get("/ticker/price", {"symbol": symbol.upper()})
    return float(raw["price"])
