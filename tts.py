import random
import edge_tts
import json

async def get_voice():
    voices = [voice for voice in await edge_tts.list_voices() if "en-" in voice["Locale"]]
    return random.choice(voices)["Name"]

async def generate(text,name,voice):
    communicate = edge_tts.Communicate(text, voice=voice)
    with open(f"output/{name}.mp3","wb") as fp:
        async for i in communicate.stream(): # Use stream instead of run
            if i.__len__() > 2:
                continue
            if i['data'] is not None:
                fp.write(i["data"]) # Write the bytes to the file