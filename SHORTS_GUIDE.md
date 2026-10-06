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
