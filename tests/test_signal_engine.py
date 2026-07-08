import pandas as pd

from negin.signals.engine import combine, generate_signal, technical_score


def _row(**overrides):
    base = dict(
        close=100.0, rsi_14=50.0, macd_hist=0.0, ema_fast=100.0, ema_slow=100.0,
        bb_upper=105.0, bb_lower=95.0, bb_mid=100.0, sma_50=100.0,
    )
    base.update(overrides)
    return pd.Series(base)


def test_neutral_row_scores_near_zero():
    score, _ = technical_score(_row())
    assert abs(score) < 0.05


def test_bullish_setup_scores_positive():
    row = _row(rsi_14=25, macd_hist=5, ema_fast=105, ema_slow=100, close=95, bb_mid=100, sma_50=90)
    score, _ = technical_score(row)
    assert score > 0


def test_bearish_setup_scores_negative():
    row = _row(rsi_14=75, macd_hist=-5, ema_fast=95, ema_slow=100, close=105, bb_mid=100, sma_50=110)
    score, _ = technical_score(row)
    assert score < 0


def test_combine_buy_action_at_high_score():
    result = combine(technical=0.5, sentiment=0.5)
    assert result.action == "BUY"
    assert result.confidence > 0


def test_combine_sell_action_at_low_score():
    result = combine(technical=-0.5, sentiment=-0.5)
    assert result.action == "SELL"


def test_combine_hold_action_near_zero():
    result = combine(technical=0.01, sentiment=-0.01)
    assert result.action == "HOLD"


def test_generate_signal_populates_components():
    result = generate_signal(_row(), sentiment=0.0)
    assert set(result.components) == {"rsi", "macd", "ema_trend", "bollinger", "sma_trend"}
