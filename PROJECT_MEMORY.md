# PROJECT MEMORY — read this first in every new session

Last updated: 15 Nov 2026. Written so a brand-new Claude session can continue the work without the old chat.

## The user
- Negin. Always reply in **Persian (Farsi)**; scripts, prompts, on-screen text and metadata for the channels are in **English**.
- Works only from an **iPhone and iPad** (no computer so far). Just moved to Romania; has very little time.
- Wants Claude to do as much of the production as possible: she sends a script, Claude builds the video.
- Gets frustrated by long explanations. Keep answers short, practical, copy-paste ready.

## The two channels
### 1) Stranger Files (true crime, English, faceless)
- ~52 subs, 2.6K views / 181 watch hours in 28 days (early Nov 2026). **This is the channel that works; prioritize it.**
- Notes: `channels/stranger-files.md`, `channels/stranger-files-videos.md`. Detective mascot: `assets/mascot/`, `tools/mascot/`.
- Tools from earlier work: `tools/assemble_longform_*.py`, `tools/captions_*`, `tools/sfx_synth.py`, `tools/jay_taylor/`.

### 2) Ray (@Ray_stick) — stickman 30-day survival stories, English
- New channel (3 subs). One long video live: "Can You Survive 30 Days of an Alien Invasion?" (10:43). One Short built (`assets/shorts/reel_alien_invasion_v4.mp4`).
- Characters (never change): **Ray** = grey cap + navy hoodie, calm; **Jax** = black beanie, black tracksuit, silver chain, cheeky; **Daniel** (ep4) = orange maintenance jumpsuit; aliens = tall, green, big glossy black eyes; ships = gunmetal-grey saucers. References in `assets/survival-characters/` (incl. `alien_ref_*.png`).
- Style sheet and channel principle: `research/persian-zombie/style-sheet-ray.md`. **Core principle:** the viewer must feel they are inside a dangerous situation making decisions, while learning real, useful facts without noticing. Second-person narration ("you").
- Episode 3 (alien invasion) files: `research/persian-zombie/ep03-*`, clips in `assets/ep03/`.
- **Episode 4 (in progress): "30 Days Trapped Inside an Alien Spaceship"**
  - Script (current): `research/persian-zombie/ep04-alien-spaceship-30-days-en-v2.md`; Persian: `...-fa.md`; her original: `...-en-FINAL.md`.
  - Image prompts by chapter (85 scenes + references): `research/persian-zombie/ep04-prompts-flow.md`.
  - She generates images herself in **Google Flow (Nano Banana)**; has made: bright advanced lab, realistic NASA-style suits, a few Day-1 scenes.
  - Ends with crash on Mars → Episode 5 = 30 days on Mars.

## How we work (learned the hard way)
- **Images:** Claude writes prompts; Negin generates in Flow. To keep a location identical, use Flow **Edit** on the existing image ("Keep the laboratory exactly the same… Only change…"). For a new angle, describe what IS in frame (negatives like "not visible" fail). Never ask the image model for text; Claude adds all on-screen text as motion graphics.
- **No text in AI images, no flags/logos.** Realistic fabric spacesuits, not shiny armor. Laser cage must be empty (no booth).
- **Voice:** she uses **ElevenLabs** (her own voice choice). Open-source TTS (Piper, Kokoro) was rejected as bad. Claude trims long silences/breaths and aligns captions with Whisper (`faster-whisper` works in the sandbox).
- **Editing by Claude:** ffmpeg + Python (PIL/numpy). Example pipeline: `tools/reel/build_alien_reel.py` (captions, digital HUD, glitch transition, alien scan overlay, synthesized SFX). Avoid noise/hum layers in sound design (she heard them as radio static).
- **HUD:** modern digital HUD top-left (not the old notebook style) for Ray: DAY x/30 · PEOPLE · FOOD · WATER · OXYGEN.
- **Reference videos she likes** (analysed with Higgsfield `video_analysis_create`, since YouTube blocks the sandbox): Nobody Gets In (train), Beanie Survives (30th floor), Mr. Doomsday (mall). Learn structure only; never copy characters, stories or graphics.
- **YouTube downloads from the sandbox are bot-blocked;** do not try to bypass. Higgsfield video analysis works for YouTube links.
- **Footage for Stranger Files must be legal:** public court/police records, Creative Commons, free stock, Claude-made graphics. Never reuse other creators' YouTube footage.
- **Never:** buy views/subs, sub4sub, misleading clickbait, copyright reuploads. Never log into her accounts or accept passwords in chat (she once pasted a Google password; she was told to change it).
- Titles: always 10+ options and pick one (see `CLAUDE.md` and `youtube/YOUTUBE_GUIDE.md`).

## Access / setup status
- **ElevenLabs API key:** not saved yet. In a fresh session call `request_credential` for host `api.elevenlabs.io`, header `xi-api-key`. (It failed in the old session only because that session was too long.)
- **Higgsfield MCP** is connected (free plan, ~6 credits): good for YouTube video analysis; image/audio generation costs credits, ask first.
- **No computer connected.** Remote Control needs Mac/Linux with Claude Desktop.
- **Upload** is always done by Negin (YouTube app / Studio). Related video on Shorts needed phone verification (done); "Advanced features" selfie verification was pending.


## NEW (26 Nov 2026): "What If" channel idea
- Decision: a **new separate channel** (not on Ray), generic **toy-brick** visual style (no LEGO name/minifig copy). Full rules: `channels/what-if-bricks.md`. English first, Persian version later. First video: "What if it was always winter?".
- Ray channel has almost no audience; not abandoned, but low priority.
- ElevenLabs key still NOT connected (she pasted a workspace id by mistake; the real key starts with `sk_`). Never use keys pasted in chat; they go in environment Network secrets.

## UPDATE 26 Nov 2026 (evening): decision to convert the Ray channel into the "What If" channel
- She decided to **rebrand the existing Ray channel (4 subs) into the What If brick channel** and start today. Her Windsor.ai connector is connected to this channel (YouTube account id 125801): Claude can read stats, reply to comments, update video details/privacy, add to playlists and **upload_video from a public URL (max 100 MB)**. Windsor plan = Trial (30 days history). Stranger Files is NOT connected yet (different Google account).
- Existing Ray videos: Short "Aliens Invaded..." (515 views), long video "Can You Survive 30 Days..." (16 views). Ask before changing/privating anything.
- Episode 1 script, titles, 18 brick-style image prompts, host design: `research/what-if/ep01-always-winter.md`.

## UPDATE 26 Nov 2026 (night): What If host "Bo" is final
- Reference image: `assets/what-if/bo_reference.jpg` (square-bodied brick figure: blue knitted beanie, white sunglasses, plain white tee with beige sleeves, navy trousers with white side stripe + white drawstring, white sneakers; NO text/logos). She chose exactly this look (minifigure-like, claw hands). Claude warned about trademark risk twice; decision is hers. Rules kept: never write the word LEGO anywhere (name/title/tags/description), no logos/text on clothes.
- Profile image: `assets/what-if/profile_bo_800.png`. Style line v2 (photoreal macro bricks) is in `channels/what-if-bricks.md`.
- Still pending: final channel name (suggested The What If Toybox), banner, ElevenLabs key, Bo scene images, ElevenLabs voice for ep01.

## UPDATE 27 Nov 2026: ElevenLabs key still failing
- Network secret for `api.elevenlabs.io` (header `xi-api-key`) exists on env "Claude code", but every key saved via the form (3 tries) returns 401 "Invalid API key". A key pasted in chat also failed (she should delete it).
- Next steps told to her: check the key is Active in ElevenLabs API Keys (Auto-disable if leaked may have turned it off) and the right workspace; or delete and re-add the Network secret in environment settings, then start a new session; or make the voice herself in the ElevenLabs app and send the mp3.
- Key settings she uses: Restrict Key on, Text to Speech + Voices Read = Access, Restrict by IP OFF.

## Git
- All work is on branch **`claude/youtube-viral-seo-rules-t1g9ga`** (main only has the initial commit unless merged). Commit and push there. Do not open PRs unless asked.

## Open tasks (pick up here)
1. Save ElevenLabs key, then build the first **Stranger Files** video end-to-end from a script she sends (voice → legal footage/graphics → edit → captions → title/description/tags).
2. Ray ep4: she continues generating images chapter by chapter; Claude assembles on the voice track with HUD, scan overlays, SFX, SRT.
3. More Shorts from Ray ep3 (vanishing girl, three knocks, red sneakers).
4. Suggested weekly rhythm: Stranger Files 1 video/week; Ray 1 video every 2 weeks.
