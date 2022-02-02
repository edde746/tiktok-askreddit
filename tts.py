import random
import edge_tts

async def get_voice():
    voices = [voice for voice in await edge_tts.list_voices() if "en-" in voice["Locale"]]
    return random.choice(voices)["Name"]

async def generate(text,name,voice):
    communicate = edge_tts.Communicate()
    with open(f"output/{name}.mp3","wb") as fp:
        async for i in communicate.run(text,voice=voice):
            if i[2] is not None:
                fp.write(i[2])