# Detective mascot (Stranger Files)

Fixed poses live in `assets/mascot/` (cut out from `source_sheet.png`, generated once from the channel artwork). Never regenerate — reuse these PNGs so the character stays identical.

| pose | file | notes |
|---|---|---|
| neutral | `neutral.png` | holds magnifying glass, talks |
| point_right | `point_right.png` | fingertip → `target`; `flip: true` points left |
| point_up_left | `point_up_left.png` | points up-left; `flip: true` = up-right |
| think | `think.png` | hand on chin (mouth hidden, blinks only) |
| surprised | `surprised.png` | mouth already open (blinks only) |

Face coordinates (eyes, mouth line, fingertip) are in `assets/mascot/meta.json`.

## Render

```
python tools/mascot/mascot.py tools/mascot/examples/point_and_narrate.json
```

- Mouth opens/closes from the `voice` file loudness (5 mouth shapes), random blinks every 2–5 s, idle bob, pop/slide/rise entrances with bounce.
- `out` ending in `.mp4` = composited on the clip; `.mov` = transparent ProRes 4444 to drop on any timeline.
- Corner narrator: `"anchor": [300, 1230]` (feet below the frame so only the upper body shows), `"enter": "rise"`.
- Needs Pillow + numpy and ffmpeg.

`cutout.py sheet.png outdir` re-splits a white-background pose sheet if new poses are ever added.
