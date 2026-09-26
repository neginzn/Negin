import certifi, sys, asyncio
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import edge_tts
lines = {
 "v1": "In 1974, this bank camera caught a nineteen-year-old heiress robbing a bank... with a rifle.",
 "v2": "Her name was Patty Hearst. Just two months earlier, the same group had kidnapped her.",
 "v3": "She said she was brainwashed. The jury didn't believe her.",
 "v4": "Decades later, she received a presidential pardon.",
 "v5": "So... was she a victim, or a criminal?",
}
async def main():
    for k,t in lines.items():
        await edge_tts.Communicate(t, "en-US-ChristopherNeural", rate="+2%", pitch="-4Hz").save(k+".mp3")
asyncio.run(main())
