"""Command-line entrypoint: live signal for a symbol, or a historical backtest.

This tool only reads public market data and public news feeds. It never
holds an API key and never places an order - wiring it into a real
exchange account is a deliberate, separate step you take only after you
trust the backtest numbers.
"""

from __future__ import annotations

import argparse

from negin.backtest.backtester import run_backtest
from negin.data.binance_client import fetch_klines
from negin.data.news_client import fetch_headlines, filter_by_symbol
from negin.indicators.technical import add_all_indicators
from negin.sentiment.analyzer import aggregate_sentiment, score_headlines
from negin.signals.engine import generate_signal


def cmd_signal(args: argparse.Namespace) -> None:
    df = add_all_indicators(fetch_klines(args.symbol, args.interval, args.limit))
    headlines = filter_by_symbol(fetch_headlines(max_age_hours=args.news_hours), args.symbol)
    scored = score_headlines(headlines)
    sentiment = aggregate_sentiment(scored)

    result = generate_signal(df.iloc[-1], sentiment)

    print(f"Symbol: {args.symbol.upper()}  Price: {df.iloc[-1]['close']:.2f}")
    print(f"Signal: {result.action}  (score={result.score:+.3f}, confidence={result.confidence:.0%})")
    print(f"  technical={result.technical_score:+.3f}  sentiment={result.sentiment_score:+.3f} "
          f"(from {len(scored)} headlines in last {args.news_hours}h)")
    print("  technical components:")
    for name, value in result.components.items():
        print(f"    {name:12s} {value:+.3f}")
    if scored:
        print("  top headlines:")
        for s in sorted(scored, key=lambda s: abs(s.score), reverse=True)[:5]:
            print(f"    [{s.score:+.1f}] ({s.headline.source}) {s.headline.title}")
    print()
    print("This is a rule-based lean, not financial advice. See the backtest "
          "command to check how this strategy performed historically before "
          "risking real funds.")


def cmd_backtest(args: argparse.Namespace) -> None:
    df = add_all_indicators(fetch_klines(args.symbol, args.interval, args.limit))
    result = run_backtest(df)
    print(f"Backtest for {args.symbol.upper()} ({args.interval}, last {args.limit} candles)")
    print(result.summary())
    print()
    print("Note: this backtests the technical rules only - free news feeds "
          "don't offer a historical archive, so sentiment can't be replayed "
          "into the past. Fees/slippage assumed at "
          f"{2*(0.001+0.0005)*100:.2f}% round-trip (Binance taker + slippage).")
    if args.show_trades:
        print()
        print("Trades:")
        for t in result.trades:
            print(f"  {t.entry_time} @ {t.entry_price:.2f} -> {t.exit_time} @ "
                  f"{t.exit_price:.2f}  ({t.return_pct:+.2f}%)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="negin", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("symbol", help="Trading pair, e.g. BTCUSDT")
    common.add_argument("--interval", default="1h", help="Candle interval (default: 1h)")
    common.add_argument("--limit", type=int, default=500, help="Number of candles (max 1000)")

    signal_parser = sub.add_parser("signal", parents=[common], help="Show the current signal")
    signal_parser.add_argument("--news-hours", type=int, default=48,
                                help="How far back to look for news (default: 48h)")
    signal_parser.set_defaults(func=cmd_signal)

    backtest_parser = sub.add_parser("backtest", parents=[common], help="Backtest the technical strategy")
    backtest_parser.add_argument("--show-trades", action="store_true")
    backtest_parser.set_defaults(func=cmd_backtest)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
