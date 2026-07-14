# Shopify Product Video Ads

Generate vertical (9:16) product ad videos for Instagram Reels, TikTok, and
Facebook/Meta ads directly from Shopify product images.

## Requirements

- `ffmpeg` (`sudo apt-get install ffmpeg`)
- Python 3 (standard library only)

## Usage

```bash
python3 scripts/make_ad.py ads/steam-brush.json
```

The MP4 is written next to the config file. Image references can be local
paths or `https://` URLs (e.g. Shopify CDN links) — URLs are downloaded and
cached in `.image_cache/` beside the config.

## Making an ad for another product

1. Copy `ads/steam-brush.json` to a new file.
2. Replace the `scenes` image URLs with the product's image URLs
   (from the Shopify admin, or the product page).
3. Write a short headline for each scene (1–2 lines; the first scene works
   best as a hook/problem, the rest as benefits).
4. Update the `endcard` title, price, and brand.
5. Run the script.

## Config reference

| Key | Meaning | Default |
| --- | --- | --- |
| `width` / `height` | Output resolution | 1080 × 1920 |
| `fps` | Frame rate | 30 |
| `scene_duration` | Seconds each image is shown | 3.2 |
| `crossfade` | Fade duration between scenes | 0.5 |
| `scenes[].image` | Local path or URL | — |
| `scenes[].headline` | Caption lines (list of strings) | none |
| `scenes[].fontsize` | Caption size | 72 |
| `endcard.bg` / `fg` / `accent` | End-card colors (hex) | cream / dark / orange |
| `endcard.title` / `price` / `cta` / `brand` | End-card text | — |

Scenes alternate zoom-in / zoom-out (Ken Burns) automatically. The output
has a silent stereo audio track so ad platforms accept it; add music in the
platform's editor or with ffmpeg afterwards.
