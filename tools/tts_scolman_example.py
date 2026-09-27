import certifi, asyncio
certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
import edge_tts
L = {
 "v1": "This man is looking at the person who killed his son. And the killer... is smiling.",
 "v2": "Joshua Scolman was already in prison, for a drunk driving crash that killed three people. Then, in 2022, he stabbed a fellow inmate — twenty-five-year-old Timothy Nabors Junior — to death. Because of the color of his skin.",
 "v3": "When Scolman was given the chance to speak... this is what he said.",
 "v4": "The judge sentenced him to life in prison. With no chance of release.",
 "v5": "What would you have said to him?",
}
async def main():
    for k, t in L.items():
        await edge_tts.Communicate(t, "en-US-AndrewMultilingualNeural", rate="-4%").save(k + ".mp3")
asyncio.run(main())
