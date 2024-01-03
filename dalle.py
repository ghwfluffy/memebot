import base64
import subprocess
import openai

PROMPT=[
    "Theme: Rick and morty",
    "Add a person that is in focus and facing towards the perspective",
]

with open("secrets/openai.txt", "r") as file:
    openai.api_key = file.read().strip()

original = ""
with open("memes/distracted_boyfriend/DistractedBoyfriendSquare4-1.png", "rb") as file:
    original = file.read()

response = openai.Image.create_edit(
#response = openai.Image.create_variation(
    image=original,
    prompt="\n".join(PROMPT),
    n=1,
    size="1024x1024",
    response_format="b64_json",
)

data = response["data"][0]["b64_json"]
print(data)

with open("/tmp/image.png", "wb") as file:
    file.write(base64.b64decode(data.encode('utf-8')))
    file.close()
subprocess.run(["eog", "/tmp/image.png"])

exit(0)


PROMPT = [
    "Build the distracted boyfriend meme which has these 3 components:",
    "1. Girl in foreground facing perspective is the distraction",
    "2. Boyfriend further in background is walking away from perspective but head is turned back facing first girl",
    "3. Girlfriend is furthest in background walking away from perspective. She is holding hands with boyfriend. She is looking back at boyfriend in disgust.",
    "Use this theme to build the meme:",
    "the new season of rick and morty sucks",
]

response = openai.Image.create(
    prompt="\n".join(PROMPT),
    n=1,
    size="1024x1024",
    response_format="b64_json",
)

data = response["data"][0]["b64_json"]
print(data)

with open("/tmp/image.png", "wb") as file:
    file.write(base64.b64decode(data.encode('utf-8')))
    file.close()
subprocess.run(["eog", "/tmp/image.png"])

#url = response["data"][0]["url"]
#print(url)
#subprocess.run(["eog", url])
