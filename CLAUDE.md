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
5. Default output: vertical 9:16, 5–10s, model Seedance 2.0 (element-compatible).
6. Log every generated clip in `footage/LOG.md` (date, character(s), prompt, job id, link).

See `SHORTS_GUIDE.md` for what makes animated YouTube Shorts work.
