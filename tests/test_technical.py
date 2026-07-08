import numpy as np
import pandas as pd

from negin.indicators.technical import add_all_indicators, ema, rsi, sma


def _price_series(values):
    return pd.Series(values, dtype=float)


def test_sma_matches_manual_average():
    s = _price_series([1, 2, 3, 4, 5])
    result = sma(s, 3)
    assert np.isnan(result.iloc[1])
    assert result.iloc[2] == 2.0
    assert result.iloc[4] == 4.0


def test_ema_reacts_faster_than_sma_immediately_after_a_jump():
    s = _price_series([10] * 20 + [20] * 5)
    e = ema(s, 5)
    m = sma(s, 5)
    # Right at the jump, EMA (which weights the newest point highly) has
    # already moved further from the old baseline than the plain average.
    jump_index = 20
    assert e.iloc[jump_index] > m.iloc[jump_index]


def test_rsi_is_100_for_strictly_increasing_series():
    s = _price_series(list(range(1, 30)))
    result = rsi(s, 14)
    assert result.iloc[-1] > 90


def test_rsi_is_near_0_for_strictly_decreasing_series():
    s = _price_series(list(range(30, 1, -1)))
    result = rsi(s, 14)
    assert result.iloc[-1] < 10


def test_add_all_indicators_appends_expected_columns():
    df = pd.DataFrame({"close": np.linspace(100, 120, 60)})
    out = add_all_indicators(df)
    for col in ["ema_fast", "ema_slow", "sma_50", "rsi_14", "macd", "bb_upper", "bb_lower"]:
        assert col in out.columns
    assert len(out) == len(df)
