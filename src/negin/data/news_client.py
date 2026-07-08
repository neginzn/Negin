"""Fetch recent crypto headlines from public RSS feeds (no API key required)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import feedparser

_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "Decrypt": "https://decrypt.co/feed",
}

# Maps a trading symbol / coin name to keywords used to filter relevant headlines.
COIN_KEYWORDS = {
    "BTC": ["bitcoin", "btc"],
    "ETH": ["ethereum", "eth", "ether"],
    "SOL": ["solana", "sol"],
    "BNB": ["binance coin", "bnb"],
    "XRP": ["ripple", "xrp"],
    "DOGE": ["dogecoin", "doge"],
    "ADA": ["cardano", "ada"],
}


@dataclass
class Headline:
    title: str
    summary: str
    link: str
    source: str
    published: datetime | None


def _parse_published(entry) -> datetime | None:
    for field in ("published_parsed", "updated_parsed"):
        value = getattr(entry, field, None)
        if value:
            return datetime(*value[:6], tzinfo=timezone.utc)
    return None


def fetch_headlines(max_age_hours: int = 48, limit_per_feed: int = 30) -> list[Headline]:
    """Fetch recent headlines across all configured feeds, newest first."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    headlines: list[Headline] = []
    for source, url in _FEEDS.items():
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:limit_per_feed]:
            published = _parse_published(entry)
            if published is not None and published < cutoff:
                continue
            headlines.append(
                Headline(
                    title=entry.get("title", ""),
                    summary=entry.get("summary", ""),
                    link=entry.get("link", ""),
                    source=source,
                    published=published,
                )
            )
    headlines.sort(key=lambda h: h.published or cutoff, reverse=True)
    return headlines


def filter_by_symbol(headlines: list[Headline], symbol: str) -> list[Headline]:
    """Keep only headlines mentioning the coin behind a trading symbol like BTCUSDT."""
    base = symbol.upper().replace("USDT", "").replace("USD", "").replace("BUSD", "")
    keywords = COIN_KEYWORDS.get(base, [base.lower()])
    relevant = []
    for h in headlines:
        text = f"{h.title} {h.summary}".lower()
        if any(kw in text for kw in keywords):
            relevant.append(h)
    return relevant
