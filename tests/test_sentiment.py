from datetime import datetime, timezone

from negin.data.news_client import Headline
from negin.sentiment.analyzer import aggregate_sentiment, score_headlines, score_text


def test_score_text_positive_terms():
    score, matched = score_text("Bitcoin ETF approval sparks bullish rally to all-time high")
    assert score > 0
    assert "bullish" in matched


def test_score_text_negative_terms():
    score, matched = score_text("Exchange hack leads to bankruptcy and lawsuit")
    assert score < 0
    assert "hack" in matched


def test_score_text_neutral_has_no_matches():
    score, matched = score_text("Here's what happened in crypto today")
    assert score == 0
    assert matched == []


def _headline(title: str) -> Headline:
    return Headline(title=title, summary="", link="", source="test", published=datetime.now(timezone.utc))


def test_aggregate_sentiment_empty_is_neutral():
    assert aggregate_sentiment([]) == 0.0


def test_aggregate_sentiment_mixes_headlines():
    headlines = [_headline("Bitcoin rallies on ETF approval"), _headline("Exchange hacked, funds stolen")]
    scored = score_headlines(headlines)
    result = aggregate_sentiment(scored)
    assert -1.0 <= result <= 1.0
