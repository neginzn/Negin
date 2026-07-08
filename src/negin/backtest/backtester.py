"""Backtest the technical strategy over historical candles.

Important honesty note: this only backtests the *technical* half of the
signal engine. There is no historical, timestamped news archive available
from free RSS feeds (they only expose the last day or two of headlines), so
sentiment cannot be replayed into the past. The live CLI signal blends in
current sentiment; this backtest tells you how the technical rules alone
would have performed, which is still the only honest way to get a real
win-rate number instead of a guess.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from negin.signals.engine import BUY_THRESHOLD, SELL_THRESHOLD, technical_score

TAKER_FEE = 0.001  # Binance spot taker fee, one-way
SLIPPAGE = 0.0005  # assumed one-way slippage
ROUND_TRIP_COST = 2 * (TAKER_FEE + SLIPPAGE)


@dataclass
class Trade:
    entry_time: pd.Timestamp
    entry_price: float
    exit_time: pd.Timestamp
    exit_price: float
    return_pct: float


@dataclass
class BacktestResult:
    trades: list[Trade] = field(default_factory=list)
    total_return_pct: float = 0.0
    buy_hold_return_pct: float = 0.0
    win_rate_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    num_trades: int = 0

    def summary(self) -> str:
        return (
            f"Trades: {self.num_trades} | Win rate: {self.win_rate_pct:.1f}% | "
            f"Strategy return: {self.total_return_pct:+.2f}% | "
            f"Buy & hold: {self.buy_hold_return_pct:+.2f}% | "
            f"Max drawdown: {self.max_drawdown_pct:.2f}%"
        )


def run_backtest(
    df_with_indicators: pd.DataFrame,
    buy_threshold: float = BUY_THRESHOLD,
    sell_threshold: float = SELL_THRESHOLD,
) -> BacktestResult:
    """Long-only backtest: go long on BUY score, exit on SELL score.

    df_with_indicators must already have indicator columns (see
    negin.indicators.technical.add_all_indicators) and be sorted oldest-first.
    """
    df = df_with_indicators.reset_index(drop=True)
    in_position = False
    entry_price = 0.0
    entry_time = None
    equity = 1.0
    equity_curve = [equity]
    trades: list[Trade] = []

    warmup = 50  # skip rows where rolling indicators are still filling in
    for i in range(warmup, len(df)):
        row = df.iloc[i]
        score, _ = technical_score(row)
        price = row["close"]
        time = row["open_time"]

        if not in_position and score >= buy_threshold:
            in_position = True
            entry_price = price
            entry_time = time
        elif in_position and score <= sell_threshold:
            trade_return = (price - entry_price) / entry_price - ROUND_TRIP_COST
            equity *= 1 + trade_return
            trades.append(
                Trade(
                    entry_time=entry_time,
                    entry_price=entry_price,
                    exit_time=time,
                    exit_price=price,
                    return_pct=trade_return * 100,
                )
            )
            in_position = False
            equity_curve.append(equity)

    # Close any open position at the last available price so it counts.
    if in_position:
        last_row = df.iloc[-1]
        trade_return = (
            (last_row["close"] - entry_price) / entry_price - ROUND_TRIP_COST
        )
        equity *= 1 + trade_return
        trades.append(
            Trade(
                entry_time=entry_time,
                entry_price=entry_price,
                exit_time=last_row["open_time"],
                exit_price=last_row["close"],
                return_pct=trade_return * 100,
            )
        )
        equity_curve.append(equity)

    wins = [t for t in trades if t.return_pct > 0]
    win_rate = (len(wins) / len(trades) * 100) if trades else 0.0

    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        drawdown = (peak - value) / peak * 100
        max_dd = max(max_dd, drawdown)

    first_close = df.iloc[warmup]["close"]
    last_close = df.iloc[-1]["close"]
    buy_hold_return = (last_close - first_close) / first_close * 100

    return BacktestResult(
        trades=trades,
        total_return_pct=(equity - 1) * 100,
        buy_hold_return_pct=buy_hold_return,
        win_rate_pct=win_rate,
        max_drawdown_pct=max_dd,
        num_trades=len(trades),
    )
