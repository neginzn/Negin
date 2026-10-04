# Negin – Astrology knowledge base

This repo is a Persian astrology reference plus calculation tools. When the user asks astrology questions (natal charts, house rulers, profections, lord of the year, solar returns, transits, firdaria, dashas, etc.):

1. Read the relevant file in `docs/astrology/` (index: `docs/astrology/README.md`) and follow its rules — they are the agreed reference (traditional rulers first, Whole Sign for profections, Dorothean triplicities, Egyptian bounds, Lilly scoring).
2. Never estimate planetary positions from memory. Compute them with `tools/astro.py` (needs `pip install pyswisseph`) and `tools/sky_events.py`.
3. For annual forecasts follow `docs/astrology/10-annual-forecast-workflow.md`.
4. Answer in Persian unless asked otherwise; confirm birth time and UTC offset (Iran: +3.5, +4.5 for DST before 2022).
