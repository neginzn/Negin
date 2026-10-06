# Animated YouTube Shorts — Working Notes

## Hook (first 0.5–3 seconds)
- Viewers decide in ~1 second. Open on motion, a visual surprise, or the punchline
  setup — never an intro card, logo, or slow wide establishing shot.
- First clip of every video = strongest, most expressive moment of the character.

## Pacing
- Visual change every 2–4 seconds (new angle, close-up, push-in, reaction).
- Shot length = shortest time the beat needs to read. 2s for a gesture, ~7s for a
  slow realization. Holds/pauses after an impact are intentional, not empty.
- Shorter with high watch-through beats longer with drop-off (30s @ 85% > 60s @ 50%).
- Design for loops: last frame can flow back into the first.

## Production workflow
1. Lock the story → break into shots (one action per shot).
2. Lock references: character sheet / clean front view per character + style block.
3. Generate shot by shot; inspect continuity (colors, outfit, proportions).
4. Regenerate only what failed. Expect ~3 generations per usable shot.
5. Negin assembles the approved clips in an editor.

## Prompt template for a clip
```
[STYLE BLOCK]
Shot: <close-up / medium / wide>, camera: <static / slow push-in / pan>
<<<CHARACTER_ELEMENT_ID>>> <one clear action>, expression: <...>
Setting: <...>. Lighting/mood: <...>. Duration: <5-10>s, vertical 9:16.
```

Sources: joinbrands.com/blog/youtube-shorts-best-practices,
aibrify.com/blog/youtube-shorts-retention-curve-playbook,
arcloop.ai/handbook/en-US/pacing-control-ai-anime-short,
neolemon.com/blog/how-to-create-consistent-characters-in-ai-videos-complete-guide

---

# Kids YouTube (Made for Kids) — Rules & What Works

## Legal / YouTube settings (COPPA)
- Content aimed mainly at children under 13 MUST be marked "Made for Kids" at upload.
  Bright animated characters + nursery-rhyme pacing = YouTube treats it as kids content.
- Made for Kids disables: comments, personalized ads, notification bell, mini-player,
  end screens/cards. Monetization is lower (contextual ads only) — plan for it.
- Wrong labelling can get the channel penalised (FTC fines are per video).

## YouTube's quality principles (affect recommendations, YouTube Kids inclusion, monetization)
High quality = kindness & healthy habits, learning & curiosity, creativity &
imagination, life skills / problem-solving, diverse characters & world.
LOW quality (avoid!):
- Heavily promotional (products, logos, unboxing)
- Negative behaviour (dangerous pranks, bullying, lying, disrespect)
- Deceptively educational (wrong facts, misleading titles/thumbnails)
- Hard to follow / confusing — explicitly "often the result of mass production or
  autogeneration" → every AI-assisted video needs a clear story and clean audio
- Sensational, bizarre, keyword-stuffed titles
- Familiar characters in strange or risky situations

## What works for kids (different from adult Shorts!)
- **Familiarity wins**: same characters, same world, same style, a recurring
  intro/catchphrase/song. Reuse increases watch time → our consistency rules matter.
- **Simple loop per episode**: familiar opening → small problem/idea →
  playful action → gentle, complete ending.
- **Pacing by age**: under 3 → slow, simple, high-contrast, repetitive.
  3–5 → songs, sing-along, act-along movements. 5+ → small stories, problem-solving.
- **Songs & repetition** carry engagement and learning (colors, numbers, feelings,
  routines like brushing teeth, sharing, bedtime).
- No sudden scary tone changes, flashing, or loud jump scares.
- The hook is still needed, but gentler: a character waving/popping in and saying
  hello or a funny little surprise — not a shock.

Sources: support.google.com/youtube/answer/10774223 (YouTube best practices for kids),
vidiq.com/blog/post/is-your-youtube-content-made-for-children-ftc-coppa,
gyre.pro/blog/how-to-monetize-a-youtube-kids-channel,
whizzystudios.com/post/optimizing-3d-animated-videos-for-kids-on-youtube-best-practices-for-content-creators,
carlaeng.substack.com/p/make-ai-videos-kids-guide

---

# Budget notes (Higgsfield prices checked 2026-10-06)
| Model / settings (9:16) | Credits |
|---|---|
| Seedance 2.0 fast, 480p, no audio, 4s | 4 |
| Seedance 2.0 fast, 480p, no audio, 5s | 5 |
| Seedance 2.0 fast, 720p, no audio, 10s | 25 |
| Seedance 2.0 std, 720p, with audio, 5s | 22.5 |
| Wan 2.7 / Kling 3.0 std no sound, 5s | 7.5 |
| Seedance 2.5 draft 480p, 5s | 15 |
Rules: cheapest = Seedance 2.0 fast 480p, no audio (~1 credit/sec, ~4.5x cheaper than
default std+audio). Add music/voice in the editor. Always use a start image so fewer
generations fail. Reuse clips across episodes. Free daily alternative: Dreamina/CapCut
(Seedance, no watermark).
