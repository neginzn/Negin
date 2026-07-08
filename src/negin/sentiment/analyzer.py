"""Lightweight crypto-news sentiment scoring.

This is a keyword-weighted lexicon, not a trained NLP model. It is meant to
give a directional, explainable nudge (which headlines pushed the score up or
down) rather than a precise sentiment probability - real sentiment models
need labeled data and are a separate upgrade path.
"""

from __future__ import annotations

from dataclasses import dataclass

from negin.data.news_client import Headline

_STRONG_POSITIVE = {
    "etf approval": 3,
    "approves": 2,
    "all-time high": 3,
    "ath": 2,
    "institutional inflow": 2,
    "inflows": 1.5,
}
_POSITIVE = {
    "adoption": 1.5,
    "partnership": 1,
    "bullish": 2,
    "rally": 1.5,
    "surge": 1.5,
    "breakout": 1.5,
    "upgrade": 1,
    "integration": 1,
    "listing": 1,
    "buyback": 1.5,
    "outperform": 1,
    "record high": 2,
    "gain": 0.5,
    "soar": 1.5,
}
_STRONG_NEGATIVE = {
    "hack": 3,
    "exploit": 2.5,
    "breach": 2.5,
    "rug pull": 3,
    "insolvency": 3,
    "bankruptcy": 3,
    "fraud": 2.5,
    "scam": 2.5,
    "sec charges": 2.5,
    "sec sues": 2.5,
    "lawsuit": 1.5,
    "ban": 2,
    "crackdown": 2,
}
_NEGATIVE = {
    "bearish": 2,
    "crash": 2,
    "sell-off": 1.5,
    "selloff": 1.5,
    "outflow": 1.5,
    "outflows": 1.5,
    "delisting": 1.5,
    "liquidation": 1.5,
    "liquidations": 1.5,
    "downgrade": 1,
    "plunge": 1.5,
    "slump": 1,
    "warns": 0.5,
    "risk": 0.3,
}

_LEXICON: dict[str, float] = {
    **_STRONG_POSITIVE,
    **_POSITIVE,
    **{k: -v for k, v in _NEGATIVE.items()},
    **{k: -v for k, v in _STRONG_NEGATIVE.items()},
}

_MAX_ABS_SCORE_PER_HEADLINE = 4.0


@dataclass
class HeadlineScore:
    headline: Headline
    score: float
    matched_terms: list[str]


def score_text(text: str) -> tuple[float, list[str]]:
    lowered = text.lower()
    total = 0.0
    matched: list[str] = []
    for term, weight in _LEXICON.items():
        if term in lowered:
            total += weight
            matched.append(term)
    clamped = max(-_MAX_ABS_SCORE_PER_HEADLINE, min(_MAX_ABS_SCORE_PER_HEADLINE, total))
    return clamped, matched


def score_headlines(headlines: list[Headline]) -> list[HeadlineScore]:
    scored = []
    for h in headlines:
        score, matched = score_text(f"{h.title} {h.summary}")
        scored.append(HeadlineScore(headline=h, score=score, matched_terms=matched))
    return scored


def aggregate_sentiment(scored: list[HeadlineScore]) -> float:
    """Average per-headline score, normalized to roughly [-1, 1].

    Returns 0.0 (neutral) when there are no headlines to score.
    """
    if not scored:
        return 0.0
    avg = sum(s.score for s in scored) / len(scored)
    return max(-1.0, min(1.0, avg / _MAX_ABS_SCORE_PER_HEADLINE))
