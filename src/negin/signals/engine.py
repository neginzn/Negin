"""Combine technical indicators and news sentiment into a single trade signal.

This produces a directional lean with an explanation, not a guarantee. Every
component score is clamped to [-1, 1]; final_score is a weighted blend and
should be read as "how many of our signals agree, and how strongly" rather
than a probability of profit.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

DEFAULT_TECHNICAL_WEIGHT = 0.7
DEFAULT_SENTIMENT_WEIGHT = 0.3

BUY_THRESHOLD = 0.15
SELL_THRESHOLD = -0.15


@dataclass
class SignalResult:
    action: str  # "BUY" | "SELL" | "HOLD"
    score: float  # combined score in [-1, 1]
    confidence: float  # abs(score), in [0, 1]
    technical_score: float
    sentiment_score: float
    components: dict[str, float] = field(default_factory=dict)


def _clip(x: float) -> float:
    return float(max(-1.0, min(1.0, x)))


def technical_score(row: pd.Series) -> tuple[float, dict[str, float]]:
    """Score the latest indicator row. Expects columns from add_all_indicators."""
    components: dict[str, float] = {}

    rsi = row.get("rsi_14", 50.0)
    components["rsi"] = _clip((50.0 - rsi) / 50.0)

    macd_hist = row.get("macd_hist", 0.0)
    close = row.get("close", 1.0) or 1.0
    components["macd"] = _clip(np.tanh(macd_hist / (0.005 * close)))

    ema_fast = row.get("ema_fast", close)
    ema_slow = row.get("ema_slow", close)
    components["ema_trend"] = _clip(np.tanh((ema_fast - ema_slow) / close * 20))

    bb_upper = row.get("bb_upper", close)
    bb_lower = row.get("bb_lower", close)
    bb_mid = row.get("bb_mid", close)
    band_width = (bb_upper - bb_lower) or 1.0
    components["bollinger"] = _clip((bb_mid - close) / (band_width / 2))

    sma_50 = row.get("sma_50", close)
    components["sma_trend"] = _clip(np.tanh((close - sma_50) / close * 20))

    weights = {
        "rsi": 0.2,
        "macd": 0.3,
        "ema_trend": 0.25,
        "bollinger": 0.15,
        "sma_trend": 0.1,
    }
    score = sum(components[k] * w for k, w in weights.items())
    return _clip(score), components


def combine(
    technical: float,
    sentiment: float,
    technical_weight: float = DEFAULT_TECHNICAL_WEIGHT,
    sentiment_weight: float = DEFAULT_SENTIMENT_WEIGHT,
) -> SignalResult:
    combined = _clip(technical * technical_weight + sentiment * sentiment_weight)
    if combined >= BUY_THRESHOLD:
        action = "BUY"
    elif combined <= SELL_THRESHOLD:
        action = "SELL"
    else:
        action = "HOLD"
    return SignalResult(
        action=action,
        score=combined,
        confidence=abs(combined),
        technical_score=technical,
        sentiment_score=sentiment,
    )


def generate_signal(
    indicator_row: pd.Series,
    sentiment: float,
    technical_weight: float = DEFAULT_TECHNICAL_WEIGHT,
    sentiment_weight: float = DEFAULT_SENTIMENT_WEIGHT,
) -> SignalResult:
    tech_score, components = technical_score(indicator_row)
    result = combine(tech_score, sentiment, technical_weight, sentiment_weight)
    result.components = components
    return result
