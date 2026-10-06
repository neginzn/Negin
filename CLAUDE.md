# Negin — Animated Shorts Footage Project

Negin designs animated characters. Claude generates 5–10s footage clips of those
characters from Negin's prompts; Negin edits the clips together.
Talk to Negin in Persian (Farsi).

## Golden rules (character consistency)
1. Every character lives in `characters/<name>.md` (character bible) and has a
   Higgsfield **Reference Element** whose ID is recorded there. Never generate a
   character without its element placeholder `<<<element_id>>>` in the prompt.
2. Always prepend the project **Style Block** (`characters/_style.md`) to every prompt.
3. Never change a character's fixed traits (colors, outfit, proportions) unless
   Negin explicitly asks — then update the bible file first.
4. One clear action per clip. Split multi-action prompts into separate clips.
5. Default output: vertical 9:16 (1080x1920), 5–10s.
   - Free mode (default): `tools/animate.py` — cut-out/puppet animation of Negin's
     own artwork with ffmpeg. 100% consistent, no credits. Store character PNGs in
     `characters/img/` (transparent background; separate body parts = better motion).
   - AI mode (needs Higgsfield credits): Seedance 2.0 with the character's element.
6. Log every generated clip in `footage/LOG.md` (date, character(s), prompt, job id, link).

Audience: kids → follow the "Made for Kids" section of `SHORTS_GUIDE.md`
(COPPA labelling, YouTube quality principles, kid-friendly pacing).
