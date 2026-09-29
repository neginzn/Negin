"""YouTube search autocomplete: what people actually type. Use to pick titles and tags.
Usage: python3 tools/yt_autocomplete.py "aileen wuornos" "aileen wuornos last"
"""
import json, sys, urllib.parse, urllib.request
for q in sys.argv[1:]:
    url = "https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=" + urllib.parse.quote(q)
    print(f"== {q}")
    print(" | ".join(json.load(urllib.request.urlopen(url, timeout=15))[1]))
